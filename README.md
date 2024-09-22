## Install
```bash
uv sync
```

## Credentials
From environments or [pass](https://www.passwordstore.org/) as a fallback.
Keys:
- `TG_API_ID`
- `TG_API_HASH`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`

## Export chat
```bash
uv run src/export-chat.py -n CHAT_NAME -o CHAT_EXPORT_JSON_STRINGS_PATH
```

## Process export
```bash
uv run src/process-export.py -i PATH_TO_JSON_STRINGS
```
