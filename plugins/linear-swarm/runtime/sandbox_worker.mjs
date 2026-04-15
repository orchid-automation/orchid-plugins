#!/usr/bin/env node

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { basename, resolve } from "node:path";
import process from "node:process";

import { claudeCode, run } from "@ai-hero/sandcastle";
import { vercel } from "@ai-hero/sandcastle/sandboxes/vercel";

const DEFAULT_MODEL = "zai/glm-5.1";
const DEFAULT_TIMEOUT_SECONDS = 900;
const SWARM_GIT_EMAIL = "linear-swarm@orchidautomation.com";
const SWARM_GIT_NAME = "orchid-linear-swarm";

function usage() {
  console.error(`Usage:
  sandbox_worker.mjs --branch <branch> --brief <brief-file> --commit-msg <message> [options]

Options:
  --repo <owner/repo>          Validate the current repo slug against origin
  --repo-url <url>             Validate the current repo remote URL
  --model <slug>               Claude-compatible model slug (default: ${DEFAULT_MODEL})
  --linear-issue <ISSUE-ID>    Post progress comments to Linear if LINEAR_API_KEY is available
  --ticket-id <ISSUE-ID>       Optional ticket id for log naming
  --timeout <seconds>          Sandbox timeout in seconds (default: ${DEFAULT_TIMEOUT_SECONDS})
  --sandbox <name>             Accepted for compatibility; ignored
  --help                       Show this help
`);
}

function fail(message, code = 1) {
  console.error(`Error: ${message}`);
  process.exit(code);
}

function envValue(...names) {
  for (const name of names) {
    const direct = process.env[name];
    if (direct) {
      return direct;
    }

    const pluginOption = process.env[`CLAUDE_PLUGIN_OPTION_${name}`];
    if (pluginOption) {
      return pluginOption;
    }
  }

  return "";
}

function execCommand(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: options.cwd,
    env: options.env ?? process.env,
    encoding: "utf8",
    stdio: options.capture === false ? "inherit" : ["ignore", "pipe", "pipe"],
  });

  if (result.error) {
    throw result.error;
  }

  if (options.check !== false && result.status !== 0) {
    const stderr = (result.stderr || "").trim();
    const stdout = (result.stdout || "").trim();
    const details = stderr || stdout || `exit ${result.status}`;
    throw new Error(`${command} ${args.join(" ")} failed: ${details}`);
  }

  return result;
}

function execGit(args, options = {}) {
  return execCommand("git", args, options);
}

function parseArgs(argv) {
  const parsed = {
    repo: "",
    repoUrl: "",
    branch: "",
    briefPath: "",
    commitMessage: "",
    model: DEFAULT_MODEL,
    linearIssue: "",
    ticketId: "",
    timeoutSeconds: DEFAULT_TIMEOUT_SECONDS,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === "--help") {
      usage();
      process.exit(0);
    }

    const next = argv[index + 1];
    const takeValue = () => {
      if (!next || next.startsWith("--")) {
        fail(`${arg} requires a value`);
      }
      index += 1;
      return next;
    };

    switch (arg) {
      case "--repo":
        parsed.repo = takeValue();
        break;
      case "--repo-url":
        parsed.repoUrl = takeValue();
        break;
      case "--branch":
        parsed.branch = takeValue();
        break;
      case "--brief":
        parsed.briefPath = takeValue();
        break;
      case "--commit-msg":
        parsed.commitMessage = takeValue();
        break;
      case "--model":
        parsed.model = takeValue();
        break;
      case "--linear-issue":
        parsed.linearIssue = takeValue();
        break;
      case "--ticket-id":
        parsed.ticketId = takeValue();
        break;
      case "--timeout": {
        const value = Number.parseInt(takeValue(), 10);
        if (!Number.isFinite(value) || value <= 0) {
          fail("--timeout must be a positive integer");
        }
        parsed.timeoutSeconds = value;
        break;
      }
      case "--sandbox":
        takeValue();
        break;
      default:
        fail(`Unknown argument: ${arg}`);
    }
  }

  if (!parsed.branch) {
    fail("--branch is required");
  }
  if (!parsed.briefPath) {
    fail("--brief is required");
  }
  if (!parsed.commitMessage) {
    fail("--commit-msg is required");
  }

  return parsed;
}

function normalizeRepoSlug(input) {
  if (!input) {
    return "";
  }

  return input
    .trim()
    .replace(/^https?:\/\/github\.com\//, "")
    .replace(/^git@github\.com:/, "")
    .replace(/\.git$/, "")
    .replace(/^\/+/, "");
}

function repoSlugFromRemote(remoteUrl) {
  const normalized = normalizeRepoSlug(remoteUrl);
  return normalized.includes("/") ? normalized : "";
}

function getGitRepoRoot() {
  return execGit(["rev-parse", "--show-toplevel"]).stdout.trim();
}

function ensureGitExclude(repoRoot, pattern) {
  const gitDir = execGit(["rev-parse", "--git-dir"], { cwd: repoRoot }).stdout.trim();
  const excludePath = resolve(repoRoot, gitDir, "info", "exclude");
  if (!existsSync(excludePath)) {
    return;
  }

  const current = readFileSync(excludePath, "utf8");
  const line = `${pattern}\n`;
  if (!current.includes(line)) {
    writeFileSync(excludePath, `${current}${current.endsWith("\n") ? "" : "\n"}${line}`, "utf8");
  }
}

function isWorkingTreeClean(repoRoot) {
  const status = execGit(["status", "--porcelain"], { cwd: repoRoot }).stdout.trim();
  return status.length === 0;
}

function getPluginDataDir() {
  const explicit = process.env.CLAUDE_PLUGIN_DATA;
  if (explicit) {
    return explicit;
  }

  const xdg = process.env.XDG_CACHE_HOME;
  if (xdg) {
    return resolve(xdg, "claude-code", "linear-swarm");
  }

  const home = process.env.HOME;
  if (home) {
    return resolve(home, ".cache", "claude-code", "linear-swarm");
  }

  return resolve(process.cwd(), ".linear-swarm-cache");
}

function sanitizeForPath(input) {
  return input.replace(/[^A-Za-z0-9._-]+/g, "-");
}

function readLinkedVercelProject(repoRoot) {
  const linkedPath = resolve(repoRoot, ".vercel", "project.json");
  if (!existsSync(linkedPath)) {
    return {};
  }

  try {
    const payload = JSON.parse(readFileSync(linkedPath, "utf8"));
    return {
      teamId: payload.orgId || "",
      projectId: payload.projectId || "",
    };
  } catch (error) {
    throw new Error(`Failed to parse ${linkedPath}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function readVercelCliToken() {
  const candidates = [
    resolve(process.env.HOME || "", ".vercel", "auth.json"),
    resolve(process.env.HOME || "", "Library", "Application Support", "com.vercel.cli", "auth.json"),
  ];

  for (const candidate of candidates) {
    if (!existsSync(candidate)) {
      continue;
    }

    try {
      const payload = JSON.parse(readFileSync(candidate, "utf8"));
      if (payload?.token) {
        return payload.token;
      }
    } catch {
      // Ignore malformed CLI auth files and continue.
    }
  }

  return "";
}

function resolveSandboxAuth(repoRoot) {
  const linked = readLinkedVercelProject(repoRoot);
  const oidcToken = envValue("VERCEL_OIDC_TOKEN");
  const token = envValue("VERCEL_TOKEN", "VERCEL_ACCESS_TOKEN") || readVercelCliToken();
  const teamId = envValue("VERCEL_TEAM_ID") || linked.teamId || "";
  const projectId = envValue("VERCEL_PROJECT_ID") || linked.projectId || "";

  return {
    oidcToken,
    token,
    teamId,
    projectId,
  };
}

function shortSha(sha) {
  return sha.slice(0, 12);
}

async function postLinearComment(linearKey, issueId, body) {
  if (!linearKey || !issueId) {
    return;
  }

  const resolvedIssueId = await resolveLinearIssueId(linearKey, issueId);

  const response = await fetch("https://api.linear.app/graphql", {
    method: "POST",
    headers: {
      Authorization: linearKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: `
        mutation CommentCreate($issueId: String!, $body: String!) {
          commentCreate(input: { issueId: $issueId, body: $body }) {
            success
          }
        }
      `,
      variables: {
        issueId: resolvedIssueId,
        body,
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`Linear comment failed with ${response.status}`);
  }
}

async function resolveLinearIssueId(linearKey, issueId) {
  if (/^[0-9a-f]{8}-[0-9a-f-]{27}$/i.test(issueId)) {
    return issueId;
  }

  const response = await fetch("https://api.linear.app/graphql", {
    method: "POST",
    headers: {
      Authorization: linearKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: `
        query IssueSearch($query: String!) {
          issueSearch(query: $query, first: 1) {
            nodes {
              id
              identifier
            }
          }
        }
      `,
      variables: {
        query: issueId,
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`Linear lookup failed with ${response.status}`);
  }

  const payload = await response.json();
  const node = payload?.data?.issueSearch?.nodes?.[0];
  if (node?.identifier === issueId && node?.id) {
    return node.id;
  }

  return issueId;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const repoRoot = getGitRepoRoot();
  ensureGitExclude(repoRoot, ".sandcastle/");

  if (!isWorkingTreeClean(repoRoot)) {
    fail("sandbox-worker requires a clean git working tree before fan-out. Commit or stash local changes first.");
  }

  const originUrl = execGit(["remote", "get-url", "origin"], { cwd: repoRoot }).stdout.trim();
  const originSlug = repoSlugFromRemote(originUrl);

  const requestedRepo = normalizeRepoSlug(args.repo || args.repoUrl);
  if (requestedRepo && originSlug && requestedRepo !== originSlug) {
    fail(`--repo ${requestedRepo} does not match origin ${originSlug}`);
  }

  const brief = readFileSync(resolve(args.briefPath), "utf8");
  const baseSha = execGit(["rev-parse", "HEAD"], { cwd: repoRoot }).stdout.trim();
  const linearKey = envValue("LINEAR_API_KEY");
  const gatewayKey = envValue("VERCEL_AI_GATEWAY_KEY");

  if (!gatewayKey) {
    fail("VERCEL_AI_GATEWAY_KEY is required for sandbox workers");
  }

  const auth = resolveSandboxAuth(repoRoot);
  if (!auth.oidcToken && !auth.token) {
    fail("Vercel Sandbox auth is missing. Set VERCEL_OIDC_TOKEN or VERCEL_TOKEN.");
  }

  if (!auth.oidcToken && (!auth.teamId || !auth.projectId)) {
    fail("Vercel Sandbox token auth also needs VERCEL_TEAM_ID and VERCEL_PROJECT_ID, or a linked .vercel/project.json.");
  }

  if (auth.oidcToken && !process.env.VERCEL_OIDC_TOKEN) {
    process.env.VERCEL_OIDC_TOKEN = auth.oidcToken;
  }
  if (auth.token && !process.env.VERCEL_TOKEN) {
    process.env.VERCEL_TOKEN = auth.token;
  }
  if (auth.teamId && !process.env.VERCEL_TEAM_ID) {
    process.env.VERCEL_TEAM_ID = auth.teamId;
  }
  if (auth.projectId && !process.env.VERCEL_PROJECT_ID) {
    process.env.VERCEL_PROJECT_ID = auth.projectId;
  }

  const pluginDataDir = getPluginDataDir();
  const repoKey = sanitizeForPath(originSlug || basename(repoRoot));
  const logDir = resolve(pluginDataDir, "logs", repoKey);
  mkdirSync(logDir, { recursive: true });
  const logPath = resolve(logDir, `${sanitizeForPath(args.ticketId || args.branch)}.log`);

  try {
    await postLinearComment(
      linearKey,
      args.linearIssue,
      `[worker] Sandbox worker started on \`${args.branch}\` with model \`${args.model}\``,
    );
  } catch {
    // Non-fatal. Linear is an audit trail, not a hard dependency.
  }

  let result;
  try {
    result = await run({
      agent: claudeCode(args.model, {
        env: {
          ANTHROPIC_BASE_URL: "https://ai-gateway.vercel.sh",
          ANTHROPIC_AUTH_TOKEN: gatewayKey,
          ANTHROPIC_API_KEY: "",
        },
      }),
      sandbox: vercel({
        runtime: "node22",
        timeout: args.timeoutSeconds * 1000,
        resources: { vcpus: 4 },
        ...(auth.token
          ? {
              token: auth.token,
              teamId: auth.teamId,
              projectId: auth.projectId,
            }
          : {}),
      }),
      prompt: brief,
      logging: {
        type: "file",
        path: logPath,
      },
      branchStrategy: {
        type: "branch",
        branch: args.branch,
      },
      hooks: {
        onSandboxReady: [
          {
            command: "command -v git >/dev/null 2>&1 || (echo 'git is required inside the Vercel Sandbox runtime' >&2; exit 1)",
          },
          {
            command: "command -v claude >/dev/null 2>&1 || (npm install -g @anthropic-ai/claude-code >/tmp/linear-swarm-claude-install.log 2>&1 || (cat /tmp/linear-swarm-claude-install.log >&2; exit 1))",
          },
          {
            command: `git config --global user.email ${SWARM_GIT_EMAIL} && git config --global user.name ${SWARM_GIT_NAME}`,
          },
        ],
      },
      maxIterations: 1,
      idleTimeoutSeconds: args.timeoutSeconds,
      name: args.ticketId || args.branch,
      throwOnDuplicateWorktree: false,
    });
  } catch (error) {
    try {
      await postLinearComment(
        linearKey,
        args.linearIssue,
        `✗ Sandbox worker failed on \`${args.branch}\`: ${error instanceof Error ? error.message : String(error)}`,
      );
    } catch {
      // Non-fatal.
    }
    throw error;
  }

  let preservedWorktreePath = result.preservedWorktreePath || "";
  if (preservedWorktreePath) {
    const statusBeforeCommit = execGit(["status", "--porcelain"], { cwd: preservedWorktreePath }).stdout.trim();
    if (statusBeforeCommit) {
      execGit(["add", "-A"], { cwd: preservedWorktreePath });
      execGit(
        [
          "-c",
          `user.email=${SWARM_GIT_EMAIL}`,
          "-c",
          `user.name=${SWARM_GIT_NAME}`,
          "commit",
          "-m",
          args.commitMessage,
        ],
        { cwd: preservedWorktreePath },
      );
    }
  }

  const finalSha = execGit(["rev-parse", args.branch], { cwd: repoRoot }).stdout.trim();
  const branchChanged = finalSha !== baseSha;

  if (!branchChanged) {
    try {
      await postLinearComment(
        linearKey,
        args.linearIssue,
        `✗ Sandbox worker produced no changes on \`${args.branch}\``,
      );
    } catch {
      // Non-fatal.
    }
    fail(`sandbox-worker completed without changing ${args.branch}`);
  }

  try {
    await postLinearComment(
      linearKey,
      args.linearIssue,
      `✓ Sandbox worker committed \`${shortSha(finalSha)}\` on \`${args.branch}\``,
    );
  } catch {
    // Non-fatal.
  }

  console.log(`FINAL COMMIT: ${finalSha}`);
  console.log(`BRANCH:       ${args.branch}`);
  console.log(`LOG FILE:     ${logPath}`);
  if (preservedWorktreePath) {
    console.log(`WORKTREE:     ${preservedWorktreePath}`);
  }
  if (result.commits.length > 0) {
    console.log(
      `SANDBOX COMMITS: ${result.commits.map((commit) => shortSha(commit.sha)).join(", ")}`,
    );
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
