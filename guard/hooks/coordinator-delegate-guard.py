#!/usr/bin/env python3
"""PreToolUse hook for the T3 delegation tools. Loaded only by the coordinator provider instance.
A worker started without an explicit provider instance inherits the coordinator instance and so its guard.
Denies (exit 2) a delegation whose target instance is missing or guarded (see guard_config.py)."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script folder off sys.path
import guard_config


def deny(why):
    print(f"coordinator-delegate-guard: denied ({why}). Name an explicit non-guarded provider instance "
          "and model in `target` (`modelSelection` for t3_thread_launch).", file=sys.stderr)
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

try:
    GUARDED = guard_config.load_guarded_instances(payload.get("cwd") or ".")
except Exception:
    deny("unreadable guard config, fail closed")


def check(instance, where):
    if not isinstance(instance, str) or not instance:
        deny(f"{where} has no provider instance, so the worker would inherit the coordinator guard")
    if instance in GUARDED:
        deny(f"{where} names the guarded instance {instance}")


# Field names, from the T3 tool schemas: delegate_task target.providerInstanceId;
# t3_thread_launch modelSelection.instanceId; create_threads threads[].target.providerInstanceId.
name = tool.rsplit("__", 1)[-1]
if name == "delegate_task":
    target = inputs.get("target")
    check(target.get("providerInstanceId") if isinstance(target, dict) else None, "target")
elif name == "t3_thread_launch":
    selection = inputs.get("modelSelection")
    check(selection.get("instanceId") if isinstance(selection, dict) else None, "modelSelection")
elif name == "create_threads":
    threads = inputs.get("threads")
    if not isinstance(threads, list) or not threads:
        deny("threads is not a non-empty list")
    for i, thread in enumerate(threads):
        target = thread.get("target") if isinstance(thread, dict) else None
        check(target.get("providerInstanceId") if isinstance(target, dict) else None, f"threads[{i}].target")
else:
    deny("unexpected tool")
sys.exit(0)
