# Global delivery plan

Read when: you install the kit for all projects of a machine, review that plan, or change access to the kit folder. Nothing here is applied yet. Round 3 applies it after the user approves.

## Footprint rule

Always-loaded text is a few plain-text lines that point at the kit and say when to read which file. Full text loads on trigger only, by a read of the exact file path. The kit's source home is its own folder, outside every project.

## 1. Pointer lines in the global file

On this machine `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` are the same file. Both are links, through `/nix/store/...-home-manager-files/`, to `home/AGENTS.md` in the dotfiles repository at `<home>/github/<github-user>/dotfiles` (`examples/nix-source-20261012.md`). The repository README says the files under `home/` are the real files and need no rebuild. Append this section to `home/AGENTS.md`. It does not touch the existing lines. Claude and Codex both read it.

```markdown
## Agent routing kit
- Kit folder: <kit-folder>. It sits outside your project: read its files by exact path with your read tool, and treat the kit as read-only.
- Start of every session, before your first reply: check whether `.agent-routing/overlay.md` exists in the project folder. Use your file read or file search tool, not a shell command. Do this step also for a short question.
- Communication: if the overlay exists, read it, then read `communication.md` in the kit folder, and apply the `language` and `ste-level` it sets to every reply. If it does not exist, apply no language or STE rule; when the user starts a project or asks to adopt the kit, ask for `language` (`english` or `user`) and `ste-level` (`off`, `80` or `100`), then create the overlay and record the kit commit.
- Routing, with or without an overlay: if your tool list has an orchestration tool such as `delegate_task` and no file edit tool, and the first message does not open "Act as the ... sub-agent", you are a coordinator. Read `policy.md` before your first action and route all work. The overlay's optional `Routing` section only sets parameters.
```

Rules for the block:

- **No `@` import.** The lines are plain text. Firstmate documents that a CLAUDE.md chain that reaches outside the project can trigger the dialog "Allow external CLAUDE.md file imports?" ([firstmate, harness-adapters/claude.md, lines 23-24](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/harness-adapters/references/harness/claude.md#L23-L24)). A pointer line imports nothing; the agent reads the file only when its trigger fires. Round 3 checks that no dialog appears (checklist item 12).
- **Absolute path.** The block uses the absolute path. The Read tool needs one.
- **Footprint.** The block has four bullets. Every session checks for the overlay with a file read or file search before the first reply, including for a short question. `communication.md` is read only when an overlay exists, before a user-facing reply.
- **Workers.** A worker whose brief opens "Act as the ... sub-agent" follows its brief. The required session-start overlay check still applies; if an overlay exists, the worker reads it and `communication.md` before its first reply. The brief names any other kit file it needs. Codex workers read the same block.
- **Do not commit in the dotfiles repository.** It holds uncommitted changes of the owner (`home.nix`, `home/.claude/settings.json` and others). Round 3 edits `home/AGENTS.md` only, and the owner stages and commits it.

## 2. Access and sandbox

The pointer lines send an agent to a folder outside its project. This section records what the providers allow there.

**Probe, measured 2026-10-12** from a project outside the kit. Thread runtime modes were confirmed with `t3_thread_configuration`.

| Provider | Mode | Samples | Read | Write | Request to the user |
| --- | --- | ---: | --- | --- | --- |
| Codex (gpt-6-luna) | auto-accept-edits | 2 | ok | denied both: `zsh:1: operation not permitted` (sandbox) | none |
| Codex (gpt-6-luna) | auto | 2 | ok | denied both: same error (sandbox) | none |
| Codex (gpt-6-luna) | approval-required | 1 usable | ok | ok | yes, inferred: the worker reported sandbox_mode read-only and approval_policy unless-trusted, and its write succeeded, so the user approved an escalation; the user reported approving 2 requests |
| Codex (gpt-6-luna) | full-access | 1 | ok | ok | none; mode shown as danger-full-access |
| Claude (haiku-5-5) | auto | 3 | ok | ok in all 3 | none shown in the third sample (the user was told to deny writes; no refusal came); none reported in the first two |
| Claude (haiku-5-5) | auto-accept-edits | 3 | ok | ok in all 3 | unknown: a worker cannot see an approval and the user did not record approvals per call |
| Claude (haiku-5-5) | approval-required | 2 | ok | ok in both | unknown: same reason |
| Claude (haiku-5-5) | full-access | 1 | ok | ok | none |

The Claude workers saw only the project folder and `~/.t3/userdata/attachments` as working directories. `~/.claude/settings.json` holds no permission rules. Full record: `examples/probe-results-20261012.md`.

**What it shows.**

- Both providers read the kit in every mode probed: a global kit stays readable.
- The Codex sandbox kept the kit read-only in auto-accept-edits and auto, with no help from the user.
- Codex in approval-required wrote to the kit after the user approved a request.
- Claude wrote to the kit in every mode probed. Whether a request reached the user in auto-accept-edits and approval-required is unknown; in auto none was reported. Nothing in the provider kept the kit read-only.
- In full-access mode no provider limits anything.
- The kit needs its own protection in every mode: the lock of section 3.

**What it does not show.**

- The cause of the Claude result is unexplained, so it may change with a Claude Code or T3 update.
- Other models of each provider are untested.
- A request waits in the worker's chat and can go unseen or be approved without reading; a human gate is not a protection of the kit.

T3 documents only part of this. Its Codex adapter maps the four modes to a `readOnly`, `workspaceWrite` and `dangerFullAccess` sandbox ([T3 Codex adapter, lines 664-700](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts#L664-L700)). Its permission guide says "Providers enforce permissions differently." ([permission modes, lines 21-25](https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md#L21-L25)). The T3 documentation has no inside/outside-workspace matrix per mode (`examples/research-t3-docs-20261012.md`, Q1).

## 3. Protection plan

Apply in this order. The first item protects against every provider; the second adds a layer for Claude Code.

1. **OS-level read-only lock on the kit folder.** It works whatever the provider does, because the file system refuses the write.

   Lock:

   ```bash
   chmod -R a-w ~/Documents/Dev/agent-routing-kit
   ```

   Unlock (restores owner write; run before an edit or a commit, because `.git` is locked too):

   ```bash
   chmod -R u+w ~/Documents/Dev/agent-routing-kit
   ```

   Tested on a temporary copy on 2026-10-12: an append and a new file were refused, and `python3 -I tests/test_guard.py` printed `37/37 passed` with the copy locked. Not applied to the kit itself. Limit: a process of the same user can run `chmod`, so the lock stops an accidental write and not a deliberate unlock.

2. **Claude Code deny rule for Edit and Write on the kit path.** Untested. Draft rule for the `permissions.deny` list of the Claude settings:

   ```json
   {"permissions": {"deny": ["Edit(~/Documents/Dev/agent-routing-kit/**)", "Write(~/Documents/Dev/agent-routing-kit/**)"]}}
   ```

   The path syntax of the rule, and whether an `Edit` rule also covers `Write`, are non verificato: check them in the Claude Code settings documentation in round 3. A deny rule does not cover Bash commands such as `sed -i`; the lock in item 1 does. `~/.claude/settings.json` is a link (section 1), so round 3 edits its source.

Codex needs neither item to stay read-only in the two modes probed. Add the lock anyway: item 1 is provider-independent.

## 4. Targeted access for project-level Claude instances

Add `--add-dir <kit path>` (absolute path) to `config.launchArgs` of each project-level Claude instance in `~/.t3/userdata/settings.json`. Status: **untested; T3 docs do not confirm it; firstmate uses it.**

- Firstmate: "Every Claude launch, in both modes, also passes `--add-dir` for exactly this task's Firstmate channel directories" ([docs/configuration.md, lines 866-868](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L866-L868)).
- T3: the Claude adapter parses launch arguments into SDK `extraArgs` and sets `additionalDirectories` to the working and attachment directories ([Claude adapter, lines 1059-1067](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1059-L1067)). T3 documents no `add-dir` recipe that guarantees an extra path is readable or writable in a given mode (`examples/research-t3-docs-20261012.md`, Q3).
- Whether an added directory is also writable is not stated in the sources read. The lock (section 3, item 1) stays the protection either way.

The probe read the kit without this flag in two modes, so the flag may matter only in approval-required mode. Checklist item 9 tests that.

## 5. The coordinator instance

The coordinator read guard denies `Read`, `Grep` and `Glob` on a file above 64 KiB (65,536 bytes) outside the project (`guard/hooks/coordinator-read-guard.py`, `MAX_EXTERNAL_BYTES`). The kit folder is outside every adopting project, so the limit applies to kit reads.

`wc -c` on the kit's Markdown files (2026-10-12): the largest is `rationale.md` at 25,041 bytes (24.5 KiB). It fits, with 40,495 bytes to spare. No kit file is near the limit. Re-run `wc -c *.md examples/*.md guard/README.md` after any large edit.

## 6. Guard plugin in T3 Code

The T3 settings file is global, so one instance entry serves every project. The guard reads each project's own `.agent-routing/guard.json`.

1. In each project that uses a script runner in Bash (for example a check script), create `.agent-routing/guard.json` first (`guard/README.md`, "Project config"). Without it the coordinator loses those scripts when the plugin path changes.
2. Print the entry: `python3 -I <KIT>/guard/launch_args.py <KIT>/guard --entry`, where `<KIT>` is the absolute path of the kit folder.
3. In `~/.t3/userdata/settings.json`, under `providerInstances.claudeAgent_claude_coordinator`, keep `driver`, `displayName`, `enabled` and `autoCompactWindow`, and set `config.launchArgs` to the printed value. Only `--plugin-dir` differs from the origin entry: it points at `<KIT>/guard`.
4. Start a new coordinator thread (launch args apply at thread start) and run the Test in `guard/README.md`.

Done when the seven Test steps pass in a new thread of two different projects.

## 7. A project adopts the overlay

1. Copy `overlay-template.md` to `<project>/.agent-routing/overlay.md` and fill the Communication settings. Fill the routing table only to change a default.
2. Add `.agent-routing/guard.json` if the project has a restricted coordinator.
3. In a new session of the project, verify that it uses a file read or file search tool to check for the overlay and reads the overlay and `communication.md` before its first reply. Verify that it reads `policy.md` before routing work.

A project without `.agent-routing/overlay.md` applies no language or STE rule; its coordinator still routes with the defaults.

## 8. Test protocol for round 3

Closed checklist: round 3 is done when every item has a recorded result in `examples/probe-results-<date>.md`, with the provider, mode, thread runtime mode (from `t3_thread_configuration`) and the exact error or output. Run every item from a project outside the kit. Run each read and write case twice, to address the one-sample limit.

Part A - lock off (baseline).

1. Read `communication.md` in the kit by absolute path: Codex, approval-required.
2. The same read: Codex, auto-accept-edits.
3. The same read: Codex, auto.
4. The same read: Claude, approval-required.
5. The same read: Claude, auto-accept-edits.
6. The same read: Claude, auto.
7. For each of the six cases, create the file `probe-write-test.txt` in the kit root, then delete it if it was created. Record: written, denied (with the error), or prompt shown.
8. Repeat items 1 to 7 for full access mode, for Claude and Codex, and record only (no pass condition).

Part B - protection and access.

9. Claude, approval-required, with `--add-dir <kit path>` in the instance and then without it: read `communication.md`. Record whether a prompt appears in each case.
10. Lock the kit. Repeat the write attempt for Claude in auto and in full-access, and for Codex in auto-accept-edits, auto and full-access. Pass: every case is denied. Modes that ask the user are not repeated: the OS refuses the write even if the user approves.
11. With the lock off, add the deny rule (section 3, item 2) and repeat the write attempt for Claude in the three modes. Record whether the rule alone denies the write.
12. Open a fresh session in a project with the pointer lines and an overlay. Before its first reply, pass: the session uses a file read or file search tool to check for `.agent-routing/overlay.md`, including for a short question, reads the overlay and `communication.md`, and shows no "Allow external CLAUDE.md file imports?" dialog. Also check a project without an overlay: the session uses the file tool to check, then applies no language or STE rule.
13. In the coordinator instance, read `policy.md` and `communication.md` for a project with an overlay. Pass: both reads work.
14. Restore the lock, run `python3 -I tests/test_guard.py` and `git status --short` in the kit. Pass: the test prints no failure (59/59 at plugin version 2.1.0), and the status lists only files that round 3 changed on purpose.

## 9. Risks of a global kit

- An edit in the kit folder reaches every project's next session at once. Edit on a branch or a copy, and commit before the edit is relied on. With the lock on, unlock first.
- A new rule in the kit that a project's overlay contradicts is a conflict: the overlay wins for its own parameters, and nothing else in the overlay may restate a kit rule.
- The guard plugin folder is shared by all projects that use the coordinator instance. Its behaviour for a second project is untested here (`guard/README.md`, "Residual risks").
- No provider sandbox protects the kit from a Claude worker in the modes probed (section 2). Until section 3 is applied, treat the kit as writable by any Claude worker.

## Alternatives not chosen

- A Claude Code skill with the pointer as its description: the same footprint, and it reaches Claude only, not Codex. The user chose pointer lines (O2).
- An `@` import of the kit file from the global file: risks the external-import dialog (section 1).
- The full policy inlined in `~/.claude/CLAUDE.md`: breaks the footprint rule.
