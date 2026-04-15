#!/usr/bin/env python3
"""Prepare a Codex-native Linear swarm plan and optionally execute shared workers."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
SHARED_ROOT = REPO_ROOT / "plugins" / "_shared" / "linear-swarm"
sys.path.insert(0, str(SHARED_ROOT / "scripts"))

from linear_api import api_key, get_issue, list_children, list_project_parents, list_projects  # type: ignore

WORKER_BRIEF_TEMPLATE = Template((SHARED_ROOT / "templates" / "worker-brief.md").read_text(encoding="utf-8"))
SANDBOX_WORKER = SHARED_ROOT / "bin" / "sandbox-worker"

TEST_COMMAND_HINT = re.compile(r"`([^`]*(?:pytest|npm test|pnpm test|pnpm lint|npm run [^`]+|pnpm [^`]+|yarn [^`]+|bun [^`]+|cargo test|go test|uv run [^`]+)[^`]*)`")
FILE_PATH_HINT = re.compile(r"(?:^|[\s`(])((?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+)")


@dataclass
class WorkItem:
    issue: dict[str, Any]
    subtasks: list[dict[str, Any]]
    parent_context: dict[str, Any] | None


def slugify(value: str, limit: int = 48) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:limit].strip("-") or "task"


def normalize_agent_provider(value: str) -> str:
    normalized = value.strip().lower()
    if normalized == "claude":
        return "claude-code"
    if normalized not in {"opencode", "claude-code"}:
        return "opencode"
    return normalized


def current_git_ref() -> tuple[str, str]:
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=REPO_ROOT, text=True).strip()
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    return branch, sha


def choose_project(team: str, query: str, key: str) -> dict[str, Any]:
    projects = list_projects(team, key, query=query, limit=50)
    if not projects:
        raise SystemExit(f'No Linear project matched "{query}" in team "{team}"')
    exact = next((project for project in projects if project.get("name", "").lower() == query.lower()), None)
    return exact or projects[0]


def collect_issue_items(issue_identifier: str, key: str) -> tuple[str, list[WorkItem]]:
    parent = get_issue(issue_identifier, key)
    children = list_children(issue_identifier, key, include_closed=False)
    if children:
        return parent.get("title", issue_identifier), [
            WorkItem(issue=child, subtasks=[], parent_context=parent) for child in children
        ]
    return parent.get("title", issue_identifier), [WorkItem(issue=parent, subtasks=[], parent_context=None)]


def collect_project_items(team: str, project_query: str, key: str) -> tuple[str, list[WorkItem]]:
    project = choose_project(team, project_query, key)
    parents = list_project_parents(project["id"], key, include_closed=False, limit=250)
    items = [
        WorkItem(issue=parent, subtasks=list_children(parent["id"], key, include_closed=False), parent_context=None)
        for parent in parents
    ]
    return project["name"], items


def issue_description(issue: dict[str, Any]) -> str:
    return (issue.get("description") or "").strip()


def extract_file_paths(*descriptions: str) -> list[str]:
    seen: set[str] = set()
    results: list[str] = []
    for description in descriptions:
        for match in FILE_PATH_HINT.findall(description or ""):
            candidate = match.strip("` ,.)(")
            if "/" not in candidate or candidate.startswith("http"):
                continue
            if candidate not in seen:
                seen.add(candidate)
                results.append(candidate)
    return [
        candidate
        for candidate in results
        if not any(other != candidate and other.startswith(f"{candidate}/") for other in results)
    ]


def extract_test_commands(*descriptions: str) -> list[str]:
    commands: list[str] = []
    seen: set[str] = set()
    for description in descriptions:
        for command in TEST_COMMAND_HINT.findall(description or ""):
            normalized = command.strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                commands.append(normalized)
    return commands


def render_subtask_list(subtasks: list[dict[str, Any]]) -> str:
    if not subtasks:
        return "- None"
    lines = []
    for subtask in subtasks:
        summary = issue_description(subtask).splitlines()[0] if issue_description(subtask) else ""
        suffix = f" — {summary}" if summary else ""
        lines.append(f"- {subtask.get('identifier', subtask.get('id', 'task'))}: {subtask.get('title', '').strip()}{suffix}")
    return "\n".join(lines)


def derive_test_spec(item: WorkItem, file_paths: list[str], commands: list[str]) -> str:
    checks: list[str] = []
    checks.append(f"- Confirm the Linear acceptance criteria for `{item.issue.get('identifier', item.issue.get('id', 'issue'))}` are satisfied.")
    if file_paths:
        checks.append("- Restrict changes to the scoped file list unless the Linear description proves another file is required.")
    else:
        checks.append("- Identify the minimal file set needed before editing; do not broaden scope without cause.")
    if commands:
        checks.extend([f"- Run `{command}`" for command in commands])
    else:
        checks.append("- No explicit automated command was provided in Linear. Use a targeted manual checklist and cite what you verified.")
    checks.append("- Review the final diff and make sure the branch is ready for Codex review.")
    return "\n".join(checks)


def render_task_description(item: WorkItem) -> str:
    parts = []
    if item.parent_context:
        parts.append(f"Parent goal: {item.parent_context.get('title', '').strip()}")
        parent_desc = issue_description(item.parent_context)
        if parent_desc:
            parts.append(parent_desc)
    desc = issue_description(item.issue)
    if desc:
        parts.append(desc)
    return "\n\n".join(part for part in parts if part).strip() or item.issue.get("title", "").strip()


def build_branch_name(issue: dict[str, Any]) -> str:
    identifier = issue.get("identifier", "task").lower()
    title = slugify(issue.get("title", "task"))
    return f"codex/{identifier}-{title}"


def build_commit_message(issue: dict[str, Any]) -> str:
    identifier = issue.get("identifier", "TASK")
    return f"feat: implement {identifier.lower()}"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def prepare_run_directory(base: Path | None) -> Path:
    if base:
        base.mkdir(parents=True, exist_ok=True)
        return base
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    run_dir = Path("/tmp/linear-swarm-codex") / stamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def prepare_item_assets(project_name: str, item: WorkItem, run_dir: Path, worker: str, model: str, agent_provider: str, hitl: str) -> dict[str, Any]:
    issue = item.issue
    identifier = issue.get("identifier", issue.get("id", "task"))
    file_paths = extract_file_paths(
        issue_description(issue),
        *(issue_description(subtask) for subtask in item.subtasks),
        issue_description(item.parent_context or {}),
    )
    test_commands = extract_test_commands(
        issue_description(issue),
        *(issue_description(subtask) for subtask in item.subtasks),
        issue_description(item.parent_context or {}),
    )
    test_spec = derive_test_spec(item, file_paths, test_commands)

    branch = build_branch_name(issue)
    commit_message = build_commit_message(issue)
    title = f"{commit_message} ({identifier})"

    test_path = run_dir / "tests" / f"{identifier}.md"
    brief_path = run_dir / "briefs" / f"{identifier}.md"
    pr_body_path = run_dir / "pr" / f"{identifier}.md"

    write_text(test_path, f"# Test Spec for {identifier}\n\n{test_spec}")
    write_text(
        brief_path,
        WORKER_BRIEF_TEMPLATE.substitute(
            TICKET_IDS=identifier,
            PROJECT_NAME=project_name,
            TASK_DESCRIPTION=render_task_description(item),
            SUBTASK_LIST=render_subtask_list(item.subtasks),
            FILE_LIST="\n".join(f"- {path}" for path in file_paths) if file_paths else "- Determine the minimal file list from the scoped issue before editing.",
            TEST_SPEC=test_spec,
        ),
    )
    write_text(
        pr_body_path,
        "\n".join(
            [
                f"## Summary",
                f"- Implements `{identifier}`",
                f"- Prepared by `linear-swarm-codex`",
                "",
                "## Validation",
                test_spec,
            ]
        ),
    )

    command = [
        str(SANDBOX_WORKER),
        "--branch",
        branch,
        "--brief",
        str(brief_path),
        "--commit-msg",
        commit_message,
        "--model",
        model,
        "--agent-provider",
        agent_provider,
        "--hitl",
        hitl,
        "--linear-issue",
        identifier,
        "--ticket-id",
        identifier,
    ]

    return {
        "issue": identifier,
        "title": title,
        "branch": branch,
        "commit_message": commit_message,
        "files": file_paths,
        "test_spec_file": str(test_path),
        "brief_file": str(brief_path),
        "pr_body_file": str(pr_body_path),
        "command": command if worker == "sandbox" else [],
    }


def run_workers(items: list[dict[str, Any]]) -> None:
    for item in items:
        command = item.get("command") or []
        if not command:
            continue
        subprocess.run(command, cwd=REPO_ROOT, check=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare and optionally run a Codex-native Linear swarm")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--issue", help="Parent issue or standalone issue identifier")
    target.add_argument("--team-project", nargs=2, metavar=("TEAM", "PROJECT"), help="Linear team key and project name")
    parser.add_argument("--worker", default="sandbox", choices=["sandbox"], help="Execution lane to prepare")
    parser.add_argument("--model", default="zai/glm-5.1", help="Cloud worker model slug")
    parser.add_argument(
        "--agent-provider",
        default=normalize_agent_provider(os.getenv("LINEAR_SWARM_AGENT_PROVIDER", "opencode")),
        choices=["opencode", "claude-code"],
        help="Worker agent provider",
    )
    parser.add_argument("--hitl", default="on-error", choices=["off", "on-error"], help="Worker recovery mode")
    parser.add_argument("--run-dir", type=Path, default=None, help="Optional output directory for generated artifacts")
    parser.add_argument("--execute", action="store_true", help="Launch prepared sandbox workers after writing the run directory")
    parser.add_argument("--dry-run", action="store_true", help="Generate the run plan only")
    parser.add_argument("--json", action="store_true", help="Print the resulting run manifest as JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.agent_provider = normalize_agent_provider(args.agent_provider)
    if args.execute and args.dry_run:
        raise SystemExit("--execute and --dry-run are mutually exclusive")
    key = api_key()
    base_branch, base_sha = current_git_ref()

    if args.issue:
        project_name, work_items = collect_issue_items(args.issue, key)
        target = {"type": "issue", "issue": args.issue}
    else:
        team, project_query = args.team_project
        project_name, work_items = collect_project_items(team, project_query, key)
        target = {"type": "project", "team": team, "project": project_query}

    if not work_items:
        raise SystemExit("No active work items were found for the requested target")

    run_dir = prepare_run_directory(args.run_dir)
    manifest_items = [
        prepare_item_assets(project_name, item, run_dir, args.worker, args.model, args.agent_provider, args.hitl)
        for item in work_items
    ]
    phase7_path = run_dir / "phase7.json"
    write_text(
        phase7_path,
        json.dumps(
            {
                "base": base_branch,
                "items": [
                    {
                        "issue": item["issue"],
                        "branch": item["branch"],
                        "title": item["title"],
                        "body_file": item["pr_body_file"],
                    }
                    for item in manifest_items
                ],
            },
            indent=2,
        ),
    )

    manifest = {
        "target": target,
        "project_name": project_name,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "run_dir": str(run_dir),
        "worker": args.worker,
        "model": args.model,
        "agent_provider": args.agent_provider,
        "hitl": args.hitl,
        "phase7_plan": str(phase7_path),
        "items": manifest_items,
    }
    write_text(run_dir / "manifest.json", json.dumps(manifest, indent=2))

    if args.execute and not args.dry_run:
        run_workers(manifest_items)

    if args.json:
        json.dump(manifest, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    print(f"Prepared Codex swarm run in {run_dir}")
    print(f"Base branch: {base_branch} @ {base_sha[:12]}")
    print(f"Worker lane: {args.worker} via {args.agent_provider} ({args.model})")
    print(f"Phase 7 plan: {phase7_path}")
    print("")
    for item in manifest_items:
        print(f"- {item['issue']} -> {item['branch']}")
        print(f"  brief: {item['brief_file']}")
        print(f"  tests: {item['test_spec_file']}")
        if item["command"]:
            print(f"  worker: {' '.join(item['command'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
