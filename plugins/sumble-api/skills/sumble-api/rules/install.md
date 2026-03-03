# Sumble API Setup Rule

This rule runs automatically before any Sumble API skill execution.

## Pre-flight Auth Check

Before making any Sumble API call, run:

```bash
python3 "SCRIPT_PATH" --check-auth
```

Where `SCRIPT_PATH` is resolved from:
!`find ~/.claude/plugins -path "*/sumble-api/scripts/sumble_api.py" 2>/dev/null | head -1`

## If SUMBLE_API_KEY is NOT set

Do NOT attempt the API call. Instead, tell the user:

1. **Get a key**: Sign up at https://sumble.com and generate an API key at https://sumble.com/account/api-keys
2. **Set the key**:
   ```bash
   echo 'export SUMBLE_API_KEY="your-key-here"' >> ~/.zshrc
   ```
3. **Restart Claude Code** — it only reads shell profiles at launch

Then stop. Do not proceed with the original request until the key is configured.

## If SUMBLE_API_KEY IS set

Proceed with the requested skill. Do not mention the auth check to the user.
