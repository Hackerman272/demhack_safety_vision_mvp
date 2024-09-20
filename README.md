## Install
```bash
uv sync
```

## Export chat
```bash
uv run python src/export-chat.py -n CHAT_NAME -o CHAT_EXPORT_JSON_STRINGS_PATH
```

## Process export
```bash
uv run src/process-export.py -i PATH_TO_JSON_STRINGS
```
