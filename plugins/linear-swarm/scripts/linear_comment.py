#!/usr/bin/env python3
"""Post a comment to a Linear issue via the GraphQL API.

Works from anywhere — inside a Vercel Sandbox worker, from a hook script,
or from the orchestrator when it needs an unattended Linear comment path.

Usage:
    python3 linear_comment.py --issue PROJ-42 --body "✓ Worker completed" --key $LINEAR_API_KEY

    # Or as a Python import:
    from linear_comment import post_comment
    post_comment("issue-uuid", "✓ Done", api_key)

Requires: LINEAR_API_KEY (passed via --key or LINEAR_API_KEY env var).
Zero external dependencies — stdlib only.
"""

from __future__ import annotations

import argparse
import os
import sys

from linear_api import LinearError, api_key, graphql_request, resolve_issue


def post_comment(issue_id: str, body: str, api_key: str) -> bool:
    """Post a comment to a Linear issue. Returns True on success."""
    try:
        data = graphql_request(
            """
            mutation($issueId: String!, $body: String!) {
              commentCreate(input: { issueId: $issueId, body: $body }) {
                success
                comment { id }
              }
            }
            """,
            api_key,
            {"issueId": issue_id, "body": body},
        )
        return bool(data.get("commentCreate", {}).get("success", False))
    except LinearError as exc:
        sys.stderr.write(f"{exc}\n")
        return False


def resolve_issue_id(identifier: str, api_key: str) -> str | None:
    """Resolve a human identifier (e.g., PROJ-42) to a Linear UUID."""
    try:
        issue = resolve_issue(identifier, api_key)
        return issue.get("id")
    except LinearError:
        pass
    return None


def main() -> int:
    p = argparse.ArgumentParser(description="Post a comment to a Linear issue")
    p.add_argument("--issue", required=True, help="Issue ID (UUID or identifier like PROJ-42)")
    p.add_argument("--body", required=True, help="Comment body (markdown supported)")
    p.add_argument("--key", default=os.getenv("LINEAR_API_KEY", ""), help="Linear API key")
    args = p.parse_args()

    try:
        key = api_key(args.key)
    except LinearError as exc:
        sys.stderr.write(f"Error: {exc}. Pass --key or set the env var.\n")
        return 1

    issue_id = args.issue
    # If it looks like an identifier (PROJ-42), resolve to UUID
    if "-" in issue_id and not issue_id.startswith("0"):
        resolved = resolve_issue_id(issue_id, key)
        if resolved:
            issue_id = resolved
        else:
            sys.stderr.write(f"Could not resolve {args.issue} to a Linear issue UUID.\n")
            return 1

    if post_comment(issue_id, args.body, key):
        print(f"✓ Comment posted on {args.issue}")
        return 0
    else:
        print(f"✗ Failed to post comment on {args.issue}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
