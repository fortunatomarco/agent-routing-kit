"""Shared project lookup for the coordinator hooks.

The project root is the nearest ancestor of the session's cwd that holds `.agent-routing/` or `.git`
(the cwd itself when neither exists). The project's guard config is `<root>/.agent-routing/guard.json`;
the environment variable AGENT_ROUTING_GUARD_CONFIG overrides that path (the tests use it).
"""
import json
import os
from pathlib import Path

CONFIG_ENV = "AGENT_ROUTING_GUARD_CONFIG"
CONFIG_REL = Path(".agent-routing") / "guard.json"


def project_root(cwd):
    start = Path(cwd).expanduser().resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".agent-routing").is_dir() or (candidate / ".git").exists():
            return candidate
    return start


def load_script_runners(cwd):
    """Return {command: set(script paths)} from the guard config; an absent config means no runner."""
    path = os.environ.get(CONFIG_ENV)
    path = Path(path) if path else project_root(cwd) / CONFIG_REL
    if not path.is_file():
        return {}
    data = json.loads(path.read_text())
    runners = {}
    for entry in data.get("scriptRunners", []):
        command, scripts = entry["command"], entry["scripts"]
        if not isinstance(command, str) or not all(isinstance(s, str) for s in scripts):
            raise ValueError("scriptRunners entries need a string command and a list of string scripts")
        runners.setdefault(command, set()).update(scripts)
    return runners


# Provider instances that carry the coordinator guard. A worker must never run on one of them.
GUARDED_INSTANCES = ("claudeAgent_claude_coordinator",)


def load_guarded_instances(cwd):
    """Return GUARDED_INSTANCES plus the optional `guardedInstances` list of the guard config.

    The config can add instances and cannot remove a built-in one. An absent config adds none."""
    guarded = set(GUARDED_INSTANCES)
    path = os.environ.get(CONFIG_ENV)
    path = Path(path) if path else project_root(cwd) / CONFIG_REL
    if not path.is_file():
        return guarded
    extra = json.loads(path.read_text()).get("guardedInstances", [])
    if not isinstance(extra, list) or not all(isinstance(i, str) and i for i in extra):
        raise ValueError("guardedInstances must be a list of non-empty strings")
    return guarded | set(extra)
