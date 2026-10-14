#!/usr/bin/env python3
"""PreToolUse hook for Bash. Loaded only by the coordinator provider instance (--plugin-dir in launchArgs).
Allows a fixed list of read-only / git commands plus the project's configured script runners
(`.agent-routing/guard.json`, see guard_config.py), denies everything else (exit 2)."""
import json, re, shlex, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script folder off sys.path
import guard_config

try:
    payload = json.load(sys.stdin)
    cmd = payload["tool_input"]["command"]
except Exception:
    print("coordinator-bash-guard: unreadable payload, denied (fail closed)", file=sys.stderr)
    sys.exit(2)

READONLY = {"ls", "wc", "grep", "head", "tail", "pwd"}
GIT_READ = {"status", "log", "diff", "show", "rev-parse", "branch"}
BAD_GIT_ARG = re.compile(r"^(--output|--ext-diff|--textconv|-c$|-C$|--exec-path|--git-dir|--work-tree|--no-verify|--amend|--allow-empty-message|-F$|--file)")

def deny(why):
    print(f"coordinator-bash-guard: denied ({why}). Hand the task to a worker.", file=sys.stderr)
    sys.exit(2)

try:
    RUNNERS = guard_config.load_script_runners(payload.get("cwd") or ".")
except Exception:
    deny("unreadable guard config, fail closed")

if "\n" in cmd or "\r" in cmd:
    deny("newline")  # shlex would treat an unquoted newline as plain whitespace
if "`" in cmd or "$(" in cmd or "${" in cmd or "<(" in cmd or ">(" in cmd:
    deny("substitution")
try:
    lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    toks = list(lex)
except ValueError:
    deny("unparseable")

segments, cur = [], []
for t in toks:
    if set(t) <= set("&|;()<>") and t:
        if t in ("&&", "||", ";", "|"):
            segments.append(cur); cur = []
        else:
            deny(f"operator {t}")  # redirects, background, subshells
    else:
        cur.append(t)
segments.append(cur)

def ok(seg):
    if not seg: return False
    c = seg[0]
    if c == "git":
        if len(seg) < 2 or seg[1].startswith("-"): return False
        sub, rest = seg[1], seg[2:]
        if any(BAD_GIT_ARG.match(a) for a in rest): return False
        if sub in GIT_READ:
            return not (sub == "branch" and any(not a.startswith("-") for a in rest) )
        if sub == "add": return True
        if sub == "commit":
            return "-m" in rest or any(a.startswith("--message") for a in rest)
        return False
    if c in RUNNERS:
        return len(seg) >= 2 and seg[1] in RUNNERS[c]
    if c in READONLY: return True
    return False

for seg in segments:
    if not ok(seg):
        deny("not on the allowlist: " + " ".join(seg)[:80])
sys.exit(0)
