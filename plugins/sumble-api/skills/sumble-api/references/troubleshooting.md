# Troubleshooting

## "Error: SUMBLE_API_KEY not set"

The environment variable isn't available in this Claude Code session.

**Fix:**
1. Add to your shell profile: `echo 'export SUMBLE_API_KEY="your-key"' >> ~/.zshrc`
2. **Restart Claude Code** — it only reads ~/.zshrc at launch
3. Get a key at: https://sumble.com/account/api-keys

## "Error: No credits remaining" (HTTP 402)

Your Sumble account has no credits left.

**Fix:**
- Purchase credits at: https://sumble.com/account/api-usage
- Check credits before large batch operations (costs are per-result)

**Credit costs:**
| Endpoint | Cost |
|----------|------|
| organizations/find | 5 credits/org/filter term |
| organizations/enrich | 5 credits/technology found |
| people/find | 1 credit/person |
| jobs/find | 3 credits/job |

## "Error: Invalid API key" (HTTP 401)

The key exists but is rejected by Sumble.

**Fix:**
- Regenerate at: https://sumble.com/account/api-keys
- Update in ~/.zshrc and restart Claude Code

## 0 results returned

The search matched but found nothing.

**Common causes:**
- **Too narrow filters**: Remove one filter at a time to broaden (e.g., drop country, drop job_level)
- **Company not indexed**: Sumble may not have data for small or very new companies
- **Wrong filter values**: Job functions and levels must match Sumble's exact values (e.g., "Engineer" not "Engineering")
- **Date too recent**: `since` filter may exclude older but relevant data

**Fix:** Try with fewer filters, or remove the `since` date.

## "Error: Missing API key" with curl

Curl has shell interpolation issues with the Sumble Bearer token. The slash commands use python3 urllib instead, which handles the token correctly.

If you see this error, the skill is using an outdated version. Update:
```
/plugin marketplace update orchid-plugins
/plugin install sumble-api@orchid-plugins
```

## Domain not recognized

If a domain returns errors, try:
- Just the domain: `stripe.com` not `https://www.stripe.com/`
- The helper auto-normalizes, but some edge cases may slip through
- Try the company's primary domain (not a subdomain like `docs.stripe.com`)
