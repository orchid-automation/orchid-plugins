#!/usr/bin/env python3
"""Post a comment to a Linear issue via the GraphQL API.

Works from anywhere — inside a Vercel Sandbox worker, from a hook script,
or from the orchestrator as a fallback when the Linear MCP isn't available.

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
import json
import os
import sys
import urllib.request
import urllib.error

LINEAR_API = "https://api.linear.app/graphql"


def post_comment(issue_id: str, body: str, api_key: str) -> bool:
    """Post a comment to a Linear issue. Returns True on success."""
    # Escape for GraphQL string
    escaped_body = body.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    query = {
        "query": f"""
            mutation {{
                commentCreate(input: {{
                    issueId: "{issue_id}"
                    body: "{escaped_body}"
                }}) {{
                    success
                    comment {{ id }}
                }}
            }}
        """
    }

    req = urllib.request.Request(
        LINEAR_API,
        data=json.dumps(query).encode("utf-8"),
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            success = result.get("data", {}).get("commentCreate", {}).get("success", False)
            if not success:
                errors = result.get("errors", [])
                if errors:
                    sys.stderr.write(f"Linear API error: {errors[0].get('message', 'unknown')}\n")
            return success
    except urllib.error.URLError as e:
        sys.stderr.write(f"Linear API unreachable: {e}\n")
        return False
    except Exception as e:
        sys.stderr.write(f"Linear comment failed: {e}\n")
        return False


def resolve_issue_id(identifier: str, api_key: str) -> str | None:
    """Resolve a human identifier (e.g., PROJ-42) to a Linear UUID."""
    query = {
        "query": f"""
            query {{
                issueSearch(query: "{identifier}", first: 1) {{
                    nodes {{ id identifier }}
                }}
            }}
        """
    }

    req = urllib.request.Request(
        LINEAR_API,
        data=json.dumps(query).encode("utf-8"),
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            nodes = result.get("data", {}).get("issueSearch", {}).get("nodes", [])
            if nodes and nodes[0].get("identifier") == identifier:
                return nodes[0]["id"]
    except Exception:
        pass
    return None


def main() -> int:
    p = argparse.ArgumentParser(description="Post a comment to a Linear issue")
    p.add_argument("--issue", required=True, help="Issue ID (UUID or identifier like PROJ-42)")
    p.add_argument("--body", required=True, help="Comment body (markdown supported)")
    p.add_argument("--key", default=os.getenv("LINEAR_API_KEY", ""), help="Linear API key")
    args = p.parse_args()

    if not args.key:
        sys.stderr.write("Error: LINEAR_API_KEY not set. Pass --key or set the env var.\n")
        return 1

    issue_id = args.issue
    # If it looks like an identifier (PROJ-42), resolve to UUID
    if "-" in issue_id and not issue_id.startswith("0"):
        resolved = resolve_issue_id(issue_id, args.key)
        if resolved:
            issue_id = resolved
        else:
            sys.stderr.write(f"Could not resolve {args.issue} to a Linear issue UUID.\n")
            return 1

    if post_comment(issue_id, args.body, args.key):
        print(f"✓ Comment posted on {args.issue}")
        return 0
    else:
        print(f"✗ Failed to post comment on {args.issue}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
