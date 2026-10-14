# Coordinator guard

Read when: you install, rebuild, test or change the restricted coordinator instance `claudeAgent_claude_coordinator` in T3 Code, or a hook denies a coordinator call. This folder is a Claude Code plugin; the kit's `delegation-t3.md` says how the coordinator behaves inside it.

## What the instance allows

- **Built-in tools, six:** `Read`, `Glob`, `Grep`, `Bash`, `AskUserQuestion`, `ToolSearch`. It has no `Write`, `Edit` or `Skill`. The `mcp__t3-code__` orchestration tools (`delegate_task`, `task_status`) stay. `launch_args.py` holds the tool list and the denied-tool list.
- **Bash allowlist,** enforced by `hooks/coordinator-bash-guard.py`; anything else is denied:
  - `git status`, `log`, `diff`, `show`, `rev-parse`, `branch` in read-only forms;
  - `git add`, and `git commit -m` without `--amend`, `--no-verify`, `-c` or `-F`;
  - the script runners and scripts that the project lists in `.agent-routing/guard.json` (below);
  - `ls`, `wc`, `grep`, `head`, `tail`, `pwd`.

  Joins with `&&`, `||`, `;` or `|` pass only when every part is on the list. Redirects, `$(...)`, backticks, newlines and background `&` are denied. Read a file with `Read`, since `cat`, `sed` and `jq` are off the list.
- **Read guard,** enforced by `hooks/coordinator-read-guard.py`: `Read`, `Grep` and `Glob` deny paths under `tool-results` and files over 64 KiB outside the project. `mcp__t3-code__t3_thread_read` allows only `view: "messages"` with explicit `limit` of 1-10 and `maxCharsPerItem` of 1-4000. On denial, hand the reading to a worker. Both hooks are needed: a thread read can create a long result before a file tool touches its saved copy.
- **Delegation guard,** enforced by `hooks/coordinator-delegate-guard.py`. It exists because a worker started without an explicit target inherits the coordinator provider instance, and so its guard: such a worker could not run commands or edit files. The hook checks three tools and denies a call whose provider instance is missing or guarded (`GUARDED_INSTANCES` in `hooks/guard_config.py`, default `claudeAgent_claude_coordinator`):
  - `delegate_task`: `target.providerInstanceId`;
  - `t3_thread_launch`: `modelSelection.instanceId`;
  - `create_threads`: `threads[].target.providerInstanceId`, every entry.

  The denial says to name an explicit non-guarded provider instance and model. The three field names come from the live T3 tool schemas (2026-10-12), not from other kit files. A `target` with only `driverKind` or only `model` counts as missing: the hook does not guess which instance a driver resolves to. The project can add instances with a `guardedInstances` list in `.agent-routing/guard.json`; the built-in entry cannot be removed.
- **Removed tools:** every `mcp__t3-code__` preview and device tool, `html_preview`, `html_render`, and every `mcp__claude_ai_Claude_Docs__` tool. `--disallowedTools` names each one in full, because the glob form `mcp__t3-code__preview_*` is untested.
- **Worker:** it runs on a plain provider instance (`claudeAgent` or `codex`) with all tools, so it loads skills, edits files and writes documents. The brief names the skill. `delegation-t3.md`, "Workers", has the worker policy.

## Project config

The project root is the nearest ancestor of the session's working folder that holds `.agent-routing/` or `.git`. The hooks read `<root>/.agent-routing/guard.json`:

```json
{"scriptRunners": [{"command": "tools/python", "scripts": ["scripts/check.py"]}], "guardedInstances": ["claudeAgent_other_guard"]}
```

`guardedInstances` is optional and adds provider instances that no delegation may target (see the delegation guard).

Each runner is a command exactly as the coordinator types it, with the scripts it may run as its first argument. An absent file means no runner. An unreadable file denies every Bash call (fail closed). The coordinator has no `Write`, so only a worker changes this file; the user reviews it like any rule file.

## Install

Audience: the session that installs or rebuilds the instance. The T3 settings file (`~/.t3/userdata/settings.json`) is the user's to open.

1. Check that `python3` is on `PATH`: the hooks run `python3 -I`. A missing `python3` makes the hook exit 127, which Claude Code treats as a non-blocking error, so `Bash` would run unguarded (expected, untested). Step 4 catches it.
2. Print the entry for this machine: `python3 -I guard/launch_args.py <absolute path of this folder> --entry`. It prints `launchArgs` with `--tools`, `--disallowedTools` and `--plugin-dir` in this order, plus `autoCompactWindow`. `--extra-deny` adds tools to the denied list.
3. Put the printed entry under `providerInstances.claudeAgent_claude_coordinator` in the T3 settings. `launchArgs` is read once, when a thread starts.
4. Start a new coordinator thread on the instance and run the test below.

Done when the test below passes in the new thread.

## Test

Run it in a new thread on the instance after every change; an existing thread cannot verify it, because plugin hooks load at thread start.

First run the synthetic check from the kit root: `python3 -I tests/test_guard.py`. It covers each matcher and the Bash allow and deny cases, but does not prove Claude Code loaded the plugin. Its parameters are in the file header.

1. **Tools:** ask the coordinator to list its tools. Pass: the six built-ins, no `Write`, `Edit` or `Skill`, and no preview, device, `html_*` or Claude Docs tool.
2. **Allowed:** ask it to run `git status` and to ask a question with `AskUserQuestion`. Pass: the status prints and the selector appears.
3. **Denied:** ask it to run `python3 -c 'print(1)'`, `curl example.com` and `echo x > /tmp/coord-test.txt`. Pass: the guard denies each, and `/tmp/coord-test.txt` does not exist.
4. **Worker:** have it delegate a trivial task with `providerInstanceId: claudeAgent`. Pass: the worker has `Write`, `Edit`, `Skill`, Claude Docs and `preview_*`.
5. **Delegation guard:** ask it to delegate a trivial task with no `target`, then with `providerInstanceId: claudeAgent_claude_coordinator`. Pass: the guard denies both with the message that names an explicit non-guarded instance.
6. **File reads:** ask for a `Read` and a `Grep` of a real file under the current session's `~/.claude/projects/<project>/<session>/tool-results/`, then a `Read` of a project rule file and `Grep`/`Glob` in the project. Pass: both saved-result reads are denied with a worker delegation message; the project reads work.
7. **Thread reads:** ask for `t3_thread_read` with `view: "activity", limit: 100` on a known thread, then `view: "messages", limit: 3, maxCharsPerItem: 2000`. Pass: activity is denied; the short messages view works. Use a worker for any long result.

## Changing the allowlist or denied tools

1. Edit the allowlist in `hooks/coordinator-bash-guard.py`, or the lists in `launch_args.py` and then the settings entry (reprint it with the Install steps).
2. Update "What the instance allows" in this file to match.
3. Start a new coordinator thread and run the Test. The change is done when all seven steps pass.

## Residual risks

- The glob form `mcp__t3-code__preview_*` in `--disallowedTools` is untested. Name each tool.
- Other `mcp__t3-code__` tools stay, among them `t3_thread_launch`, `t3_project_delete` and `schedule_task`. Their responses, and small `t3_thread_read` responses, can still contain unexpectedly long output.
- Large files inside the project are allowed so rule and dashboard reads keep working. `Grep` or `Glob` on a broad directory, `@` file references, and the allowed Bash read commands can still expose long content. The hooks cannot prevent a coordinator that chooses a worker-less path from doing other worker tasks.
- `git add` and `git commit -m` can stage and commit any file in the project.
- `grep`, `head`, `tail` and `ls` can read any path on the machine.
- The delegation guard checks the delegation tools only. It does not stop a process the coordinator creates another way (for example a shell command that starts an agent), and it does not check the model, the runtime mode or other tools that start work. A target that names an unguarded instance with a restricted tool set is also allowed: the hook cannot see tool lists.
- The guard fails closed on an unreadable payload; see Install step 1 for the missing-`python3` case.
- Plugin loading by `--plugin-dir` with this folder shared by several projects is untested here: the origin project used one folder per project. Step 4 of Install, run from a second project, verifies it.
