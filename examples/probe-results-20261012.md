# Probe results - 2026-10-12

Read when: you need the measured facts on whether workers read and write the kit folder from another project, or you plan the round 3 test. This file lives in `examples/` because it records one machine and one session; `GLOBAL-DELIVERY.md`, "Access and sandbox", summarizes it.

## Method

- Four worker threads were started from a project outside the kit folder, one per provider and mode.
- Each worker tried to read a kit file and to write in the kit folder.
- Thread runtime modes were confirmed with `t3_thread_configuration`: `runtimeMode` matched the requested mode for the three threads checked. The thread ids were not in the brief for this round; the fourth thread was not checked.
- The Claude workers saw only the project folder and `~/.t3/userdata/attachments` as working directories.
- `~/.claude/settings.json` holds no permission rules.

## Results

The first-round wording 'no prompt' is superseded by the table below: a worker cannot see a user approval.

| Provider | Mode | Read kit | Write kit |
| --- | --- | --- | --- |
| Codex (gpt-6-luna) | auto-accept-edits | ok | denied: `zsh:1: operation not permitted` |
| Codex (gpt-6-luna) | auto | ok | denied: same error |
| Claude (haiku-5-5) | auto-accept-edits | ok | ok, no prompt |
| Claude (haiku-5-5) | auto | ok | ok, no prompt |

## Facts

- Both providers read the kit from outside the project in both modes.
- Codex could not write the kit in either mode; the error was the same in both.
- Claude wrote the kit in both modes with no prompt.

## Limits

- One sample per case.
- Approval-required mode was not tested.
- Full access mode was not tested.
- The cause of the Claude result is unexplained. This file offers no explanation.
- One model per provider: gpt-6-luna and haiku-5-5.

## Baseline, second and third round

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

Limits:

- One to three samples per case.
- Claude workers cannot see their permission mode.
- The first-round thread modes were confirmed with `t3_thread_configuration`.
- The cause of the Claude results is unexplained.
- A user approval is invisible to a worker.

## Related evidence

- T3 maps Codex modes to a `readOnly`, `workspaceWrite` or `dangerFullAccess` sandbox and says providers enforce permissions differently: `research-t3-docs-20261012.md`, Q1 and Q2.
- Firstmate states that its environment filter "is not a sandbox" and passes `--add-dir` for Claude workers: `research-firstmate-20261012.md`, F2 and F3.
- Round 3 repeats the probe with two samples per case and adds approval-required: `GLOBAL-DELIVERY.md`, "Test protocol for round 3".
