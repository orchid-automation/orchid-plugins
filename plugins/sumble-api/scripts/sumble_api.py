#!/usr/bin/env python3
"""
Shared Sumble API helper for all slash commands.
Usage: python3 scripts/sumble_api.py <endpoint> '<json_payload>'

Endpoints: organizations/find, organizations/enrich, people/find, jobs/find
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = "https://api.sumble.com/v3"

# ── Auth ──────────────────────────────────────────────────────────────

def get_api_key():
    key = os.environ.get("SUMBLE_API_KEY", "").strip()
    if not key:
        print("Error: SUMBLE_API_KEY not set.")
        print('Run: export SUMBLE_API_KEY="your-key-here"')
        print("Get a key at: https://sumble.com/account/api-keys")
        sys.exit(1)
    return key

# ── Domain normalization ──────────────────────────────────────────────

def normalize_domain(raw):
    """Convert 'https://www.stripe.com/', 'stripe', 'Stripe.com' → 'stripe.com'"""
    d = raw.lower().strip()
    d = d.replace("https://", "").replace("http://", "").replace("www.", "")
    d = d.rstrip("/")
    if "." not in d:
        d = d + ".com"
    return d

# ── API call with retries ────────────────────────────────────────────

def call_api(endpoint, payload, retries=2):
    key = get_api_key()
    url = f"{BASE_URL}/{endpoint}"
    data = json.dumps(payload).encode()

    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            })
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read())

        except urllib.error.HTTPError as e:
            body = e.read().decode()
            try:
                err = json.loads(body)
                detail = err.get("detail", str(e))
            except json.JSONDecodeError:
                detail = body or str(e)

            if e.code == 402:
                print("Error: No credits remaining.")
                print("Purchase credits at: https://sumble.com/account/api-usage")
                sys.exit(1)

            if e.code == 401:
                print("Error: Invalid API key.")
                print("Check your key at: https://sumble.com/account/api-keys")
                sys.exit(1)

            if e.code in (429, 502, 503, 504) and attempt < retries:
                wait = 2 ** attempt
                time.sleep(wait)
                continue

            print(f"Error ({e.code}): {detail}")
            sys.exit(1)

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

# ── Output formatters ────────────────────────────────────────────────

def print_header(label, count, credits_used, credits_remaining):
    print(f"Found {count} {label} | Credits used: {credits_used} | Remaining: {credits_remaining}")
    print()

def print_orgs(data):
    orgs = data.get("organizations", [])
    print_header("organizations", data.get("total", len(orgs)), data.get("credits_used", 0), data.get("credits_remaining", "?"))
    for org in orgs:
        name = org.get("name", "Unknown")
        domain = org.get("domain", "")
        industry = org.get("industry", "N/A")
        emp = org.get("total_employees", "?")
        hq_parts = [org.get("headquarters_state", ""), org.get("headquarters_country", "")]
        hq = ", ".join(p for p in hq_parts if p)
        li = org.get("linkedin_organization_url", "")
        techs = ", ".join(e["term"] for e in org.get("matching_entities", []) if e.get("type") == "technologies")
        print(f"- **{name}** ({domain})")
        print(f"  Industry: {industry} | Employees: {emp} | HQ: {hq}")
        if techs:
            print(f"  Matched: {techs}")
        if li:
            print(f"  LinkedIn: {li}")
        print()
    _next_steps("organizations")

def print_enrich(data):
    org = data.get("organization", {})
    techs = data.get("technologies", [])
    print(f"# {org.get('name', 'Unknown')} ({org.get('domain', '')})")
    print_header("technologies", data.get("technologies_count", len(techs)), data.get("credits_used", 0), data.get("credits_remaining", "?"))
    for t in techs:
        print(f"- **{t['name']}** — Jobs: {t.get('jobs_count', 0)} | People: {t.get('people_count', 0)} | Teams: {t.get('teams_count', 0)} | Last post: {t.get('last_job_post', 'N/A')}")
    print()
    _next_steps("enrich")

def print_people(data):
    people = data.get("people", [])
    print_header("people", data.get("people_count", len(people)), data.get("credits_used", 0), data.get("credits_remaining", "?"))
    for p in people:
        name = p.get("name", "Unknown")
        title = p.get("job_title", "N/A")
        level = p.get("job_level", "")
        loc = p.get("location", "N/A")
        start = p.get("start_date", "N/A")
        li = p.get("linkedin_url", "")
        level_str = f" ({level})" if level else ""
        print(f"- **{name}** — {title}{level_str}")
        print(f"  Location: {loc} | Started: {start}")
        if li:
            print(f"  LinkedIn: {li}")
        print()
    _next_steps("people")

def print_jobs(data):
    jobs = data.get("jobs", [])
    print_header("jobs", data.get("total", len(jobs)), data.get("credits_used", 0), data.get("credits_remaining", "?"))
    for j in jobs:
        title = j.get("job_title", "N/A")
        org_name = j.get("organization_name", "")
        domain = j.get("organization_domain", "")
        loc = j.get("location", "N/A")
        techs = j.get("matched_technologies", "N/A")
        posted = (j.get("datetime_pulled") or "N/A")[:10]
        url = j.get("url", "")
        print(f"- **{title}** at {org_name} ({domain})")
        print(f"  Location: {loc} | Technologies: {techs} | Posted: {posted}")
        if url:
            print(f"  Details: {url}")
        print()
    _next_steps("jobs")

def _next_steps(context):
    suggestions = {
        "organizations": "Dig deeper: /sumble-enrich [domain] | Find contacts: /sumble-find-people [domain]",
        "enrich": "Find contacts: /sumble-find-people [domain] | See hiring: /sumble-find-jobs [domain]",
        "people": "Enrich company: /sumble-enrich [domain] | See hiring: /sumble-find-jobs [domain]",
        "jobs": "Enrich company: /sumble-enrich [domain] | Find contacts: /sumble-find-people [domain]",
    }
    print(f"Next steps: {suggestions.get(context, '')}")

# ── Formatters map ───────────────────────────────────────────────────

FORMATTERS = {
    "organizations/find": print_orgs,
    "organizations/enrich": print_enrich,
    "people/find": print_people,
    "jobs/find": print_jobs,
}

# ── CLI entry point ──────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 sumble_api.py <endpoint> '<json_payload>'")
        print("Endpoints: organizations/find, organizations/enrich, people/find, jobs/find")
        sys.exit(1)

    endpoint = sys.argv[1]
    try:
        payload = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON payload — {e}")
        sys.exit(1)

    # Normalize domain if present
    org = payload.get("organization")
    if isinstance(org, dict) and "domain" in org:
        org["domain"] = normalize_domain(org["domain"])

    data = call_api(endpoint, payload)
    formatter = FORMATTERS.get(endpoint)
    if formatter:
        formatter(data)
    else:
        print(json.dumps(data, indent=2))
