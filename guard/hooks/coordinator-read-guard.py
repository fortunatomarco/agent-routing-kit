#!/usr/bin/env python3
"""Keep large result extraction out of the coordinator's PreToolUse calls."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script folder off sys.path
import guard_config

# 64 KiB catches saved tool results while leaving ordinary short briefs alone.
MAX_EXTERNAL_BYTES = 64 * 1024
# Bound thread reads to a short review summary, not a full activity timeline.
MAX_THREAD_ITEMS = 10
MAX_CHARS_PER_ITEM = 4000


def deny(reason):
    print(f"coordinator-read-guard: denied ({reason}). Hand the reading to a worker.", file=sys.stderr)
    sys.exit(2)


try:
    payload = json.load(sys.stdin)
    tool = payload["tool_name"]
    inputs = payload["tool_input"]
    if (not isinstance(tool, str) or not isinstance(inputs, dict)
            or not isinstance(payload.get("cwd", "."), str)):
        raise ValueError("tool_input must be an object")
except (KeyError, ValueError, TypeError):
    deny("unreadable payload, fail closed")

if tool in {"Read", "Grep", "Glob"}:
    key = "file_path" if tool == "Read" else "path"
    raw = inputs.get(key, payload.get("cwd"))
    if not isinstance(raw, str) or not raw:
        deny("missing path")
    try:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = Path(payload.get("cwd", ".")) / path
        resolved = path.resolve()
        repo = guard_config.project_root(payload.get("cwd") or ".")
    except (OSError, ValueError, TypeError):
        deny("cannot inspect path")
    if "tool-results" in path.parts or "tool-results" in resolved.parts:
        deny("tool-results path")
    path = resolved
    pattern = inputs.get("pattern" if tool == "Glob" else "glob", "")
    if not isinstance(pattern, str):
        deny("invalid pattern")
    if "tool-results" in Path(pattern).parts:
        deny("tool-results pattern")
    try:
        if repo not in (path, *path.parents) and path.is_file() and path.stat().st_size > MAX_EXTERNAL_BYTES:
            deny("large file outside project")
    except OSError:
        deny("cannot inspect path")
elif tool in {"mcp__t3-code__t3_thread_read", "mcp__t3_code__t3_thread_read"}:
    def bounded(name, maximum):
        value = inputs.get(name)
        return type(value) is int and 0 < value <= maximum

    if (not isinstance(inputs.get("threadId"), str) or not inputs["threadId"]
            or inputs.get("view", "messages") != "messages"
            or "itemId" in inputs
            or not bounded("limit", MAX_THREAD_ITEMS)
            or not bounded("maxCharsPerItem", MAX_CHARS_PER_ITEM)
            or ("runLimit" in inputs and not bounded("runLimit", MAX_THREAD_ITEMS))):
        deny("unbounded thread read")
else:
    deny("unexpected tool")
