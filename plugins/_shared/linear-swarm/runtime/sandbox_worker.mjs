#!/usr/bin/env node

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { basename, resolve } from "node:path";
import process from "node:process";

import { claudeCode, createSandbox, opencode, run } from "@ai-hero/sandcastle";
import { vercel } from "@ai-hero/sandcastle/sandboxes/vercel";

const DEFAULT_MODEL = "zai/glm-5.1";
const DEFAULT_TIMEOUT_SECONDS = 900;
const DEFAULT_HITL_MODE = "off";
const DEFAULT_AGENT_PROVIDER = "opencode";
const SWARM_GIT_EMAIL = "linear-swarm@orchidautomation.com";
const SWARM_GIT_NAME = "orchid-linear-swarm";

function usage() {
  console.error(`Usage:
  sandbox_worker.mjs --branch <branch> --brief <brief-file> --commit-msg <message> [options]

Options:
  --repo <owner/repo>          Validate the current repo slug against origin
  --repo-url <url>             Validate the current repo remote URL
  --model <slug>               Worker model slug (default: ${DEFAULT_MODEL})
  --agent-provider <name>      Worker agent provider: opencode or claude-code (default: ${DEFAULT_AGENT_PROVIDER})
  --hitl <off|on-error>        Launch or prepare a human-in-the-loop recovery session on worker failure
  --linear-issue <ISSUE-ID>    Post progress comments to Linear if LINEAR_API_KEY is available
  --ticket-id <ISSUE-ID>       Optional ticket id for log naming
  --failure <message>          Failure text passed to direct HITL entry
  --enter-hitl                 Skip the AFK sandbox run and enter HITL directly
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
    agentProvider: normalizeAgentProvider(envValue("LINEAR_SWARM_AGENT_PROVIDER") || DEFAULT_AGENT_PROVIDER),
    linearIssue: "",
    ticketId: "",
    timeoutSeconds: DEFAULT_TIMEOUT_SECONDS,
    hitlMode: DEFAULT_HITL_MODE,
    failureMessage: "",
    enterHitl: false,
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
      case "--agent-provider": {
        const value = normalizeAgentProvider(takeValue());
        if (!["opencode", "claude-code"].includes(value)) {
          fail("--agent-provider must be one of: opencode, claude-code");
        }
        parsed.agentProvider = value;
        break;
      }
      case "--linear-issue":
        parsed.linearIssue = takeValue();
        break;
      case "--ticket-id":
        parsed.ticketId = takeValue();
        break;
      case "--hitl": {
        const value = takeValue();
        if (!["off", "on-error"].includes(value)) {
          fail("--hitl must be one of: off, on-error");
        }
        parsed.hitlMode = value;
        break;
      }
      case "--failure":
        parsed.failureMessage = takeValue();
        break;
      case "--enter-hitl":
        parsed.enterHitl = true;
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

function normalizeAgentProvider(value) {
  const normalized = value.trim().toLowerCase();
  if (normalized === "claude") {
    return "claude-code";
  }
  return normalized;
}

function buildClaudeEnv(gatewayKey) {
  return {
    ANTHROPIC_BASE_URL: "https://ai-gateway.vercel.sh",
    ANTHROPIC_AUTH_TOKEN: gatewayKey,
    ANTHROPIC_API_KEY: "",
  };
}

function buildVercelSandbox(auth, timeoutSeconds, env = {}) {
  return vercel({
    runtime: "node22",
    timeout: timeoutSeconds * 1000,
    resources: { vcpus: 4 },
    env,
    ...(auth.token
      ? {
          token: auth.token,
          teamId: auth.teamId,
          projectId: auth.projectId,
        }
      : {}),
  });
}

function sanitizeModelAlias(model) {
  const value = model.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return value || "model";
}

function buildOpenCodeConfig(model, gatewayKey) {
  const alias = sanitizeModelAlias(model);
  const configuredModel = `vercel/${alias}`;
  return {
    config: {
      $schema: "https://opencode.ai/config.json",
      provider: {
        vercel: {
          npm: "@ai-sdk/openai-compatible",
          name: "Vercel AI Gateway",
          options: {
            baseURL: "https://ai-gateway.vercel.sh/v1",
            apiKey: gatewayKey,
          },
          models: {
            [alias]: {
              name: model,
              id: model,
            },
          },
        },
      },
      model: configuredModel,
      default_agent: "build",
      agent: {
        build: {
          model: configuredModel,
        },
      },
    },
    configuredModel,
  };
}

function buildAgentRuntime(agentProvider, model, gatewayKey) {
  if (agentProvider === "claude-code") {
    return {
      agent: claudeCode(model, {
        env: buildClaudeEnv(gatewayKey),
      }),
      sandboxEnv: {},
      installCommand:
        "command -v claude >/dev/null 2>&1 || (npm install -g @anthropic-ai/claude-code >/tmp/linear-swarm-claude-install.log 2>&1 || (cat /tmp/linear-swarm-claude-install.log >&2; exit 1))",
      setupCommands: [],
    };
  }

  const { config, configuredModel } = buildOpenCodeConfig(model, gatewayKey);
  return {
    agent: opencode(configuredModel),
    sandboxEnv: {
      LINEAR_SWARM_OPENCODE_CONFIG_B64: Buffer.from(JSON.stringify(config), "utf8").toString("base64"),
    },
    installCommand:
      "command -v opencode >/dev/null 2>&1 || (npm install -g opencode-ai >/tmp/linear-swarm-opencode-install.log 2>&1 || (cat /tmp/linear-swarm-opencode-install.log >&2; exit 1))",
    setupCommands: [
      "node -e \"const fs=require('fs'); const dir=process.env.HOME + '/.config/opencode'; const raw=process.env.LINEAR_SWARM_OPENCODE_CONFIG_B64; if(!raw){throw new Error('LINEAR_SWARM_OPENCODE_CONFIG_B64 missing')} fs.mkdirSync(dir,{recursive:true}); fs.writeFileSync(dir + '/opencode.json', Buffer.from(raw,'base64').toString('utf8'));\"",
    ],
  };
}

function buildSandboxHooks(agentRuntime) {
  return {
    onSandboxReady: [
      {
        command: "command -v git >/dev/null 2>&1 || (echo 'git is required inside the Vercel Sandbox runtime' >&2; exit 1)",
      },
      {
        command: agentRuntime.installCommand,
      },
      ...agentRuntime.setupCommands.map((command) => ({ command })),
      {
        command: `git config --global user.email ${SWARM_GIT_EMAIL} && git config --global user.name ${SWARM_GIT_NAME}`,
      },
    ],
  };
}

function shellQuote(value) {
  if (value.length === 0) {
    return "''";
  }

  return `'${value.replace(/'/g, `'\\''`)}'`;
}

function canLaunchInteractiveHitl() {
  return Boolean(process.stdin.isTTY && process.stdout.isTTY && process.stderr.isTTY);
}

function gitRevParseOrFallback(repoRoot, ref, fallback) {
  try {
    return execGit(["rev-parse", ref], { cwd: repoRoot }).stdout.trim();
  } catch {
    return fallback;
  }
}

function buildHitlPrompt(args, brief, failureMessage) {
  return [
    `You are resuming Linear swarm work on branch \`${args.branch}\`.`,
    args.linearIssue ? `Linear issue: ${args.linearIssue}` : "",
    "This is a human-in-the-loop recovery session triggered because the automated sandbox run failed or produced no usable commit.",
    failureMessage ? `Failure that triggered the handoff:\n${failureMessage}` : "",
    "Original worker brief:",
    brief,
    [
      "Instructions:",
      "1. Inspect the current branch and repository state.",
      "2. Recover the task with the minimum necessary changes.",
      "3. Run the checks described in the brief.",
      `4. Commit with this message when the branch is ready: ${args.commitMessage}`,
      "5. Stop once the branch is ready for the normal review, smoke, and PR phases.",
    ].join("\n"),
  ]
    .filter(Boolean)
    .join("\n\n");
}

function buildHitlCommand(args, failureMessage = "") {
  const pieces = [
    "swarm-hitl",
    "--branch",
    shellQuote(args.branch),
    "--brief",
    shellQuote(resolve(args.briefPath)),
    "--commit-msg",
    shellQuote(args.commitMessage),
    "--model",
    shellQuote(args.model),
  ];

  if (args.repo) {
    pieces.push("--repo", shellQuote(args.repo));
  }
  if (args.repoUrl) {
    pieces.push("--repo-url", shellQuote(args.repoUrl));
  }
  if (args.linearIssue) {
    pieces.push("--linear-issue", shellQuote(args.linearIssue));
  }
  if (args.ticketId) {
    pieces.push("--ticket-id", shellQuote(args.ticketId));
  }
  if (failureMessage) {
    pieces.push("--failure", shellQuote(failureMessage));
  }

  return pieces.join(" ");
}

async function maybeEnterHitl({
  repoRoot,
  args,
  brief,
  baseSha,
  auth,
  agentRuntime,
  linearKey,
  gatewayKey,
  failureMessage,
}) {
  const startSha = gitRevParseOrFallback(repoRoot, args.branch, baseSha);

  if (!canLaunchInteractiveHitl()) {
    const command = buildHitlCommand(args, failureMessage);
    try {
      await postLinearComment(
        linearKey,
        args.linearIssue,
        `[hitl] Automated sandbox run failed on \`${args.branch}\`. Resume manually with:\n\`\`\`bash\n${command}\n\`\`\``,
      );
    } catch {
      // Non-fatal.
    }
    throw new Error(
      `sandbox-worker failed on ${args.branch}; no interactive TTY is available for HITL. Resume manually with:\n${command}`,
    );
  }

  let sandbox;
  let preservedWorkspacePath = "";
  try {
    sandbox = await createSandbox({
      branch: args.branch,
      sandbox: buildVercelSandbox(auth, args.timeoutSeconds, agentRuntime.sandboxEnv),
      hooks: buildSandboxHooks(agentRuntime),
      throwOnDuplicateWorktree: false,
    });

    try {
      await postLinearComment(
        linearKey,
        args.linearIssue,
        `[hitl] Entering interactive recovery on \`${args.branch}\``,
      );
    } catch {
      // Non-fatal.
    }

    await sandbox.interactive({
      agent: agentRuntime.agent,
      prompt: buildHitlPrompt(args, brief, failureMessage),
      name: `${args.ticketId || args.branch}-hitl`,
    });

    const statusBeforeCommit = execGit(["status", "--porcelain"], {
      cwd: sandbox.worktreePath,
    }).stdout.trim();
    if (statusBeforeCommit) {
      execGit(["add", "-A"], { cwd: sandbox.worktreePath });
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
        { cwd: sandbox.worktreePath },
      );
    }

    const finalSha = execGit(["rev-parse", args.branch], { cwd: repoRoot }).stdout.trim();
    if (finalSha === startSha) {
      throw new Error(`HITL session ended without a new commit on ${args.branch}`);
    }

    try {
      await postLinearComment(
        linearKey,
        args.linearIssue,
        `✓ HITL committed \`${shortSha(finalSha)}\` on \`${args.branch}\``,
      );
    } catch {
      // Non-fatal.
    }

    return {
      finalSha,
      preservedWorktreePath: "",
      commits: [],
      mode: "hitl",
    };
  } finally {
    if (sandbox) {
      const closeResult = await sandbox.close();
      preservedWorkspacePath = closeResult?.preservedWorkspacePath || "";
    }
  }
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
        query SearchIssues($term: String!) {
          searchIssues(term: $term, first: 10) {
            nodes {
              id
              identifier
            }
          }
        }
      `,
      variables: {
        term: issueId,
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`Linear lookup failed with ${response.status}`);
  }

  const payload = await response.json();
  const node = (payload?.data?.searchIssues?.nodes || []).find(
    (candidate) => candidate?.identifier === issueId,
  );
  if (node?.id) {
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
  const agentRuntime = buildAgentRuntime(args.agentProvider, args.model, gatewayKey);

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

  if (args.enterHitl && !gatewayKey) {
    fail("VERCEL_AI_GATEWAY_KEY is required for swarm-hitl recovery sessions");
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

  if (args.enterHitl) {
    const hitlResult = await maybeEnterHitl({
      repoRoot,
      args,
      brief,
      baseSha,
      auth,
      agentRuntime,
      linearKey,
      gatewayKey,
      failureMessage: args.failureMessage || "Manual HITL requested.",
    });
    console.log(`FINAL COMMIT: ${hitlResult.finalSha}`);
    console.log(`BRANCH:       ${args.branch}`);
    console.log(`LOG FILE:     ${logPath}`);
    console.log("MODE:         hitl");
    return;
  }

  let result;
  let finalSha = "";
  let preservedWorktreePath = "";
  let completionMode = "sandbox";
  try {
    result = await run({
      agent: agentRuntime.agent,
      sandbox: buildVercelSandbox(auth, args.timeoutSeconds, agentRuntime.sandboxEnv),
      prompt: brief,
      logging: {
        type: "file",
        path: logPath,
      },
      branchStrategy: {
        type: "branch",
        branch: args.branch,
      },
      hooks: buildSandboxHooks(agentRuntime),
      maxIterations: 1,
      idleTimeoutSeconds: args.timeoutSeconds,
      name: args.ticketId || args.branch,
      throwOnDuplicateWorktree: false,
    });
    preservedWorktreePath = result.preservedWorktreePath || "";
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

    finalSha = execGit(["rev-parse", args.branch], { cwd: repoRoot }).stdout.trim();
    if (finalSha === baseSha) {
      throw new Error(`sandbox-worker completed without changing ${args.branch}`);
    }
  } catch (error) {
    const failureMessage = error instanceof Error ? error.message : String(error);
    if (args.hitlMode === "on-error") {
      try {
        const hitlResult = await maybeEnterHitl({
          repoRoot,
          args,
          brief,
          baseSha,
          auth,
          agentRuntime,
          linearKey,
          gatewayKey,
          failureMessage,
        });
        finalSha = hitlResult.finalSha;
        preservedWorktreePath = hitlResult.preservedWorktreePath || "";
        completionMode = hitlResult.mode;
      } catch (hitlError) {
        try {
          await postLinearComment(
            linearKey,
            args.linearIssue,
            `✗ Sandbox worker failed on \`${args.branch}\`: ${failureMessage}`,
          );
        } catch {
          // Non-fatal.
        }
        throw hitlError;
      }
    } else {
      try {
        await postLinearComment(
          linearKey,
          args.linearIssue,
          `✗ Sandbox worker failed on \`${args.branch}\`: ${failureMessage}`,
        );
      } catch {
        // Non-fatal.
      }
      throw error;
    }
  }

  try {
    await postLinearComment(
      linearKey,
      args.linearIssue,
      `✓ ${completionMode === "hitl" ? "HITL recovery" : "Sandbox worker"} committed \`${shortSha(finalSha)}\` on \`${args.branch}\``,
    );
  } catch {
    // Non-fatal.
  }

  console.log(`FINAL COMMIT: ${finalSha}`);
  console.log(`BRANCH:       ${args.branch}`);
  console.log(`LOG FILE:     ${logPath}`);
  console.log(`MODE:         ${completionMode}`);
  console.log(`AGENT:        ${args.agentProvider}`);
  if (preservedWorktreePath) {
    console.log(`WORKTREE:     ${preservedWorktreePath}`);
  }
  if (result?.commits?.length > 0) {
    console.log(
      `SANDBOX COMMITS: ${result.commits.map((commit) => shortSha(commit.sha)).join(", ")}`,
    );
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
