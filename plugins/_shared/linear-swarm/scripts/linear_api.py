#!/usr/bin/env python3
"""Read and update Linear issues via GraphQL using LINEAR_API_KEY.

This module exists so linear-swarm can run unattended inside nested Claude
sessions without relying on browser-based Linear MCP OAuth.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any

LINEAR_API = "https://api.linear.app/graphql"
UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

ISSUE_FIELDS = """
id
identifier
title
description
state { id name type }
parent { id identifier title }
team {
  id
  key
  name
  states { nodes { id name type } }
}
project { id name slugId }
"""

PROJECT_FIELDS = """
id
name
slugId
state
teams { nodes { id key name } }
"""


class LinearError(RuntimeError):
    """Raised when the Linear GraphQL API rejects a request."""


def api_key(explicit: str = "") -> str:
    key = explicit or os.getenv("LINEAR_API_KEY", "")
    if not key:
        raise LinearError("LINEAR_API_KEY not set")
    return key


def graphql_request(query: str, key: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"query": query}
    if variables:
        payload["variables"] = variables

    request = urllib.request.Request(
        LINEAR_API,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": key, "Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = str(exc)
        raise LinearError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise LinearError(f"Linear API unreachable: {exc}") from exc

    errors = body.get("errors") or []
    if errors:
        message = errors[0].get("message", "unknown Linear API error")
        raise LinearError(message)
    return body.get("data") or {}


def issue_lookup_fields() -> str:
    return ISSUE_FIELDS


def resolve_issue(identifier_or_id: str, key: str) -> dict[str, Any]:
    identifier_or_id = identifier_or_id.strip()
    if UUID_RE.match(identifier_or_id):
        data = graphql_request(
            f"query($id: String!) {{ issue(id: $id) {{ {issue_lookup_fields()} }} }}",
            key,
            {"id": identifier_or_id},
        )
        issue = data.get("issue")
        if issue:
            return issue

    data = graphql_request(
        f"""
        query($term: String!) {{
          searchIssues(term: $term, first: 10) {{
            nodes {{ {issue_lookup_fields()} }}
          }}
        }}
        """,
        key,
        {"term": identifier_or_id},
    )
    nodes = data.get("searchIssues", {}).get("nodes", [])
    for node in nodes:
        if node.get("identifier", "").lower() == identifier_or_id.lower():
            return node
    if nodes:
        return nodes[0]
    raise LinearError(f"Could not resolve issue {identifier_or_id}")


def get_issue(identifier_or_id: str, key: str) -> dict[str, Any]:
    return resolve_issue(identifier_or_id, key)


def list_children(parent_identifier_or_id: str, key: str, include_closed: bool = False) -> list[dict[str, Any]]:
    parent = resolve_issue(parent_identifier_or_id, key)
    data = graphql_request(
        f"""
        query($parentId: ID!, $first: Int!) {{
          issues(filter: {{ parent: {{ id: {{ eq: $parentId }} }} }}, first: $first) {{
            nodes {{ {issue_lookup_fields()} }}
          }}
        }}
        """,
        key,
        {"parentId": parent["id"], "first": 250},
    )
    nodes = data.get("issues", {}).get("nodes", [])
    if include_closed:
        return nodes
    return [node for node in nodes if node.get("state", {}).get("type") not in {"completed", "canceled"}]


def list_projects(team_key: str, key: str, query: str = "", limit: int = 50) -> list[dict[str, Any]]:
    data = graphql_request(
        f"""
        query($teamKey: String!, $first: Int!) {{
          projects(
            filter: {{ accessibleTeams: {{ some: {{ key: {{ eq: $teamKey }} }} }} }}
            first: $first
            includeArchived: false
          ) {{
            nodes {{ {PROJECT_FIELDS} }}
          }}
        }}
        """,
        key,
        {"teamKey": team_key, "first": limit},
    )
    nodes = data.get("projects", {}).get("nodes", [])
    if not query:
        return nodes

    q = query.strip().lower()

    def rank(node: dict[str, Any]) -> tuple[int, str]:
        name = node.get("name", "").lower()
        if name == q:
            return (0, name)
        if q in name:
            return (1, name)
        return (2, name)

    filtered = [node for node in nodes if q in node.get("name", "").lower()]
    target = filtered or nodes
    return sorted(target, key=rank)


def list_project_parents(project_id: str, key: str, include_closed: bool = False, limit: int = 250) -> list[dict[str, Any]]:
    data = graphql_request(
        f"""
        query($projectId: ID!, $first: Int!) {{
          issues(
            filter: {{
              project: {{ id: {{ eq: $projectId }} }}
              parent: {{ null: true }}
            }}
            first: $first
          ) {{
            nodes {{ {issue_lookup_fields()} }}
          }}
        }}
        """,
        key,
        {"projectId": project_id, "first": limit},
    )
    nodes = data.get("issues", {}).get("nodes", [])
    if include_closed:
        return nodes
    return [node for node in nodes if node.get("state", {}).get("type") not in {"completed", "canceled"}]


def resolve_state_id(issue: dict[str, Any], target_state: str) -> str:
    states = issue.get("team", {}).get("states", {}).get("nodes", [])
    target = target_state.strip().lower()
    for state in states:
        if state.get("name", "").lower() == target:
            return state["id"]
    for state in states:
        if state.get("type", "").lower() == target:
            return state["id"]
    raise LinearError(
        f'Could not resolve state "{target_state}" for team {issue.get("team", {}).get("key", "unknown")}'
    )


def set_issue_state(identifier_or_id: str, state_name: str, key: str) -> dict[str, Any]:
    issue = resolve_issue(identifier_or_id, key)
    state_id = resolve_state_id(issue, state_name)
    data = graphql_request(
        f"""
        mutation($id: String!, $stateId: String!) {{
          issueUpdate(id: $id, input: {{ stateId: $stateId }}) {{
            success
            issue {{ {issue_lookup_fields()} }}
          }}
        }}
        """,
        key,
        {"id": issue["id"], "stateId": state_id},
    )
    payload = data.get("issueUpdate") or {}
    if not payload.get("success"):
        raise LinearError(f'Failed to set {identifier_or_id} to state "{state_name}"')
    return payload["issue"]


def dump_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query and update Linear issues via GraphQL")
    parser.add_argument("--key", default="", help="Linear API key (defaults to LINEAR_API_KEY)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_cmd = subparsers.add_parser("get", help="Get one issue by identifier or UUID")
    get_cmd.add_argument("--id", required=True, help="Issue identifier or UUID")

    children_cmd = subparsers.add_parser("children", help="List child issues of a parent issue")
    children_cmd.add_argument("--parent", required=True, help="Parent issue identifier or UUID")
    children_cmd.add_argument("--include-closed", action="store_true", help="Include completed/canceled issues")

    projects_cmd = subparsers.add_parser("projects", help="List projects for a team")
    projects_cmd.add_argument("--team", required=True, help="Linear team key")
    projects_cmd.add_argument("--query", default="", help="Optional project-name filter")
    projects_cmd.add_argument("--limit", type=int, default=100, help="Maximum projects to return")

    parents_cmd = subparsers.add_parser("project-parents", help="List top-level issues for a project")
    parents_cmd.add_argument("--project-id", required=True, help="Linear project UUID")
    parents_cmd.add_argument("--include-closed", action="store_true", help="Include completed/canceled issues")
    parents_cmd.add_argument("--limit", type=int, default=250, help="Maximum issues to return")

    state_cmd = subparsers.add_parser("set-state", help="Move an issue to a named workflow state")
    state_cmd.add_argument("--id", required=True, help="Issue identifier or UUID")
    state_cmd.add_argument("--state", required=True, help='Target state name, e.g. "In Review" or "Done"')

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        key = api_key(args.key)
        if args.command == "get":
            dump_json(get_issue(args.id, key))
            return 0
        if args.command == "children":
            dump_json(list_children(args.parent, key, include_closed=args.include_closed))
            return 0
        if args.command == "projects":
            dump_json(list_projects(args.team, key, query=args.query, limit=args.limit))
            return 0
        if args.command == "project-parents":
            dump_json(
                list_project_parents(
                    args.project_id,
                    key,
                    include_closed=args.include_closed,
                    limit=args.limit,
                )
            )
            return 0
        if args.command == "set-state":
            dump_json(set_issue_state(args.id, args.state, key))
            return 0
    except LinearError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1

    parser.error(f"Unhandled command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
