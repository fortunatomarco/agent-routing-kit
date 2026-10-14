#!/usr/bin/env python3
"""Print the launchArgs string for the restricted coordinator provider instance.

Usage: python3 -I guard/launch_args.py [PLUGIN_DIR] [--entry] [--extra-deny TOOL[,TOOL...]]
  PLUGIN_DIR   absolute path of the guard folder (default: the folder that holds this script)
  --entry      print the whole provider-instance JSON entry instead of the launchArgs string
  --extra-deny add tools to --disallowedTools, each named in full

This script is the single home of the built-in tool list and the denied-tool list.
"""
import argparse
import json
from pathlib import Path

BUILTIN_TOOLS = ["Read", "Glob", "Grep", "Bash", "AskUserQuestion", "ToolSearch"]
DENIED_TOOLS = [
    "mcp__t3-code__device_close", "mcp__t3-code__device_list", "mcp__t3-code__device_open",
    "mcp__t3-code__device_screenshot", "mcp__t3-code__html_preview", "mcp__t3-code__html_render",
    "mcp__t3-code__preview_click", "mcp__t3-code__preview_dialog", "mcp__t3-code__preview_drag",
    "mcp__t3-code__preview_evaluate", "mcp__t3-code__preview_hover", "mcp__t3-code__preview_navigate",
    "mcp__t3-code__preview_open", "mcp__t3-code__preview_press", "mcp__t3-code__preview_recording_start",
    "mcp__t3-code__preview_recording_stop", "mcp__t3-code__preview_resize", "mcp__t3-code__preview_scroll",
    "mcp__t3-code__preview_select", "mcp__t3-code__preview_set_appearance", "mcp__t3-code__preview_snapshot",
    "mcp__t3-code__preview_status", "mcp__t3-code__preview_type", "mcp__t3-code__preview_upload",
    "mcp__t3-code__preview_wait_for",
    "mcp__claude_ai_Claude_Docs__batch", "mcp__claude_ai_Claude_Docs__create",
    "mcp__claude_ai_Claude_Docs__delete", "mcp__claude_ai_Claude_Docs__export",
    "mcp__claude_ai_Claude_Docs__guide", "mcp__claude_ai_Claude_Docs__query",
    "mcp__claude_ai_Claude_Docs__read", "mcp__claude_ai_Claude_Docs__update",
]
AUTO_COMPACT_WINDOW = "300000"


def launch_args(plugin_dir, extra_deny):
    denied = DENIED_TOOLS + [t for t in extra_deny if t not in DENIED_TOOLS]
    return (f'--tools "{",".join(BUILTIN_TOOLS)}" '
            f'--disallowedTools "{",".join(denied)}" '
            f'--plugin-dir {plugin_dir}')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("plugin_dir", nargs="?", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--entry", action="store_true")
    parser.add_argument("--extra-deny", default="")
    args = parser.parse_args()
    plugin_dir = Path(args.plugin_dir).expanduser()
    if not plugin_dir.is_absolute():
        parser.error("PLUGIN_DIR must be an absolute path")
    if not (plugin_dir / ".claude-plugin" / "plugin.json").is_file():
        parser.error(f"{plugin_dir} has no .claude-plugin/plugin.json")
    extra = [t for t in args.extra_deny.split(",") if t]
    value = launch_args(plugin_dir, extra)
    if args.entry:
        print(json.dumps({
            "driver": "claudeAgent",
            "displayName": "Claude (coordinator)",
            "enabled": True,
            "config": {"autoCompactWindow": AUTO_COMPACT_WINDOW, "launchArgs": value},
        }, indent=2))
    else:
        print(value)


if __name__ == "__main__":
    main()
