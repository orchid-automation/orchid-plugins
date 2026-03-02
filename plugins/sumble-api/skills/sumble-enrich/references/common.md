# Common API Information

## TL;DR

Sumble API uses Bearer token authentication with credit-based pricing. Base URL is `https://api.sumble.com/v3/`. Rate limit is 10 requests/second. Common errors: 401 (bad token), 402 (no credits), 429 (rate limited). Monitor credits_remaining in responses.

## Base URL

All API endpoints use the base URL:
```
https://api.sumble.com/v3/
```

Example full endpoint URL:
```
https://api.sumble.com/v3/organizations/find
```

## Authentication

The Sumble API uses Bearer token authentication. Include your API key in the Authorization header of every request.

**Header format:**
```
Authorization: Bearer YOUR_API_KEY
```

**CURL example:**
```bash
curl -X POST https://api.sumble.com/v3/organizations/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filters": {"technologies": ["python"]}}'
```

**Environment variable setup:**
```bash
export SUMBLE_API_KEY="your_api_key_here"
```

**Important**:
- API keys are sensitive credentials - never commit them to version control
- Generate keys at https://sumble.com/account/api-keys
- Store keys securely in environment variables or secrets management systems
- Rotate keys periodically for security

## Credits System

API calls consume credits based on the endpoint and results returned:

| Endpoint | Cost |
|----------|------|
| `/v3/organizations/find` | 5 credits per organization, per filter term (minimum 5) |
| `/v3/organizations/enrich` | 5 credits per technology found |
| `/v3/people/find` | 1 credit per person returned |
| `/v3/jobs/find` | 3 credits per job returned |

**Important notes:**
- Technology categories: Each technology in a category counts separately (e.g., a category with 3 technologies = 3 filter terms)
- Minimum charge: organizations/find has a 5 credit minimum per organization
- Monitor usage: Every response includes `credits_used` and `credits_remaining` fields

**Response example showing credits:**
```json
{
  "id": "0199f400-4123-7eca-9082-be2c94676bfc",
  "credits_used": 25,
  "credits_remaining": 9975,
  "organizations": [...]
}
```

## Rate Limits

**Limit**: 10 requests per second (aggregated across all endpoints)
**Bursting**: Occasional bursts above the limit are allowed
**Response**: When rate limited, API returns HTTP 429

**Best practices:**
- Implement exponential backoff when you receive 429 responses
- Space out requests when making bulk API calls
- Monitor rate limit responses and adjust request frequency

## Error Responses

The API uses standard HTTP status codes:

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Check request body format and parameters |
| 401 | Unauthorized | Invalid or missing API key |
| 402 | Insufficient Credits | Purchase more credits or upgrade plan |
| 422 | Validation Error | Request parameters failed validation |
| 429 | Rate Limited | Wait and retry (see rate limits above) |
| 500 | Server Error | Contact Sumble support |

**400 Bad Request:**
- Caused by malformed JSON or invalid request structure
- Check that Content-Type header is set to application/json
- Validate JSON syntax and required fields

**401 Unauthorized:**
- API key is missing, invalid, or expired
- Verify Authorization header format: `Bearer YOUR_KEY`
- Regenerate API key if necessary

**402 Insufficient Credits:**
- Your account has run out of credits
- Check credits_remaining in recent responses
- Purchase additional credits or upgrade your plan

**422 Validation Error:**
- Request parameters don't meet validation requirements
- Common issues: invalid filter values, limit/offset out of range
- Check parameter types and allowed values in endpoint documentation

**429 Rate Limited:**
- Exceeded 10 requests per second
- Implement retry with exponential backoff
- Consider batching requests or spreading them over time

**500 Server Error:**
- Rare server-side issue
- Retry after a brief wait
- If persistent, contact support@sumble.com

## Error Recovery Guidance

**When API calls fail:**

1. **Check the status code** - Different codes require different actions
2. **For 401 errors** - Verify your API key is correct and properly formatted
3. **For 402 errors** - Check credits_remaining from your last successful call
4. **For 429 errors** - Implement exponential backoff (wait 1s, then 2s, then 4s...)
5. **For 500 errors** - Retry after 5-10 seconds; if persistent, contact support

**Monitoring credits:**
- Always parse `credits_remaining` from responses
- Set up alerts when credits drop below threshold
- Estimate costs before large batch operations using the credits table above

**Handling partial failures:**
- If a batch operation fails partway through, check which records were processed
- Use offset parameter to resume from where you left off
- Keep track of processed IDs to avoid duplicates

## SDKs and Tools

**Official SDK**: None currently available - use standard HTTP clients

**Recommended HTTP clients:**
- **CURL**: Command-line testing and scripting
- **Postman**: Interactive API testing and collection management
- **HTTPie**: User-friendly command-line alternative to curl
- **Language-specific**: requests (Python), axios (JavaScript), http (Go)

**Content-Type**: Always set to `application/json` for POST requests
