#!/usr/bin/env python3
"""Daytona sandbox worker runner for linear-swarm.

Invoked by the `linear-swarm:daytona-worker` skill. Runs headless Claude Code
inside a Daytona sandbox with a cheap model via Vercel AI Gateway, committing
the result to a branch and pushing.

Usage:
    python3 daytona_worker.py \\
        --sandbox claude-sandbox \\
        --repo-url https://github.com/owner/repo.git \\
        --branch brandon/playkit-35-fix-tests \\
        --model zai/glm-5.1 \\
        --brief-file /tmp/brief.md \\
        --vag-key $VERCEL_AI_GATEWAY_KEY \\
        --gh-token $(gh auth token)
"""

from __future__ import annotations

import argparse
import base64
import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    """Run a command on the local machine."""
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if check and result.returncode != 0:
        sys.stderr.write(f"FAILED: {' '.join(cmd)}\n{result.stderr}\n")
        sys.exit(result.returncode)
    return result


def dtx(sandbox: str, args: list[str]) -> subprocess.CompletedProcess:
    """Run a command inside the sandbox via `daytona exec`. Single command, no inner shell."""
    return run(["daytona", "exec", sandbox, "--", *args])


def dtx_py(sandbox: str, python_code: str) -> subprocess.CompletedProcess:
    """Run Python code inside the sandbox via the base64+exec pattern.

    Daytona's shell-quoting is brutal — this is the only reliable way to pass
    multi-line scripts with special characters. The single-quoted outer + escaped
    parens survive zsh's re-tokenization on the Mac side.
    """
    b64 = base64.b64encode(python_code.encode()).decode()
    # Use bash -c on the local side to control quoting explicitly
    shell_cmd = (
        f"daytona exec {sandbox} -- python3 -c "
        f"'exec\\(__import__\\(\"base64\"\\).b64decode\\(\"{b64}\"\\).decode\\(\\)\\)'"
    )
    return run(["bash", "-c", shell_cmd])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--sandbox", default="claude-sandbox")
    p.add_argument("--repo-url", required=True)
    p.add_argument("--repo-name", help="Directory name inside sandbox. Defaults to repo URL basename")
    p.add_argument("--branch", required=True)
    p.add_argument("--model", default="zai/glm-5.1")
    p.add_argument("--brief-file", required=True, help="Path to file containing the worker brief")
    p.add_argument("--vag-key", required=True, help="Vercel AI Gateway key")
    p.add_argument("--gh-token", required=True, help="GitHub token for clone + push")
    p.add_argument("--commit-msg", required=True)
    p.add_argument("--timeout", type=int, default=900)
    args = p.parse_args()

    repo_name = args.repo_name or args.repo_url.rstrip("/").split("/")[-1].removesuffix(".git")
    work_dir = f"/tmp/{repo_name}"
    brief = Path(args.brief_file).read_text()

    # 1. Wake sandbox (no-op if already running)
    run(["daytona", "start", args.sandbox], check=False)

    # 2. Clean + clone
    dtx(args.sandbox, ["rm", "-rf", work_dir])
    dtx(args.sandbox, [
        "git", "clone", "--depth", "1",
        f"https://{args.gh_token}@github.com/{args.repo_url.split('github.com/')[-1]}",
        work_dir,
    ])

    # 3. Git config + branch (single-token args, no inner shell)
    dtx(args.sandbox, ["git", "-C", work_dir, "config", "user.email", "linear-swarm@orchidautomation.com"])
    dtx(args.sandbox, ["git", "-C", work_dir, "config", "user.name", "orchid-linear-swarm"])
    dtx(args.sandbox, ["git", "-C", work_dir, "checkout", "-b", args.branch])

    # 4. Run headless Claude via VAG with the brief, using the base64+exec pattern
    runner_py = f"""
import subprocess, os
env = os.environ.copy()
env['ANTHROPIC_BASE_URL'] = 'https://ai-gateway.vercel.sh'
env['ANTHROPIC_AUTH_TOKEN'] = {args.vag_key!r}
env['ANTHROPIC_API_KEY'] = ''
env['ANTHROPIC_DEFAULT_SONNET_MODEL'] = {args.model!r}
prompt = {brief!r}
result = subprocess.run(
    ['claude', '-p', '--dangerously-skip-permissions', prompt],
    env=env, capture_output=True, text=True, timeout={args.timeout}, cwd={work_dir!r}
)
print('=== STDOUT ===')
print(result.stdout)
print('=== STDERR (last 2000) ===')
print(result.stderr[-2000:])
print('=== RC ===', result.returncode)
"""
    dtx_py(args.sandbox, runner_py)

    # 5. Commit + push via Python wrapper (avoids shell-quoting on commit message)
    commit_py = f"""
import subprocess
subprocess.run(['git', '-C', {work_dir!r}, 'add', '-A'], check=True)
r = subprocess.run(
    ['git', '-C', {work_dir!r}, 'commit', '-m', {args.commit_msg!r}],
    capture_output=True, text=True
)
print('commit:', r.stdout, r.stderr)
r2 = subprocess.run(
    ['git', '-C', {work_dir!r}, 'push', '--force', 'origin', {args.branch!r}],
    capture_output=True, text=True
)
print('push:', r2.stdout, r2.stderr)
print('push rc:', r2.returncode)
"""
    dtx_py(args.sandbox, commit_py)

    # 6. Report final commit hash
    result = dtx(args.sandbox, ["git", "-C", work_dir, "rev-parse", "HEAD"])
    print(f"FINAL COMMIT: {result.stdout.strip()}")
    print(f"BRANCH:       {args.branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
