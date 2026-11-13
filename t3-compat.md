# T3 Code compatibility record

Read when: you review or change an instruction that depends on T3 Code behavior (`delegation-t3.md`, `guard/`, `decision-boards.md`, `threads-and-cache.md`), or you update the kit for a new T3 Code version.
Reader: maintainer.

## Version checked

| Item | Value |
| --- | --- |
| Date read | 2026-10-22 |
| Running `serverVersion` | `0.1.1-nightly.20261020.3411` |
| Build commit | `d36b7da2485b` (full `d36b7da2485bc889b320a285deea181f637d760a`) |
| Latest stable seen | `v0.1.1` (2026-10-21) |
| Newest nightly seen | `v0.1.2-nightly.20261021.3499` (2026-10-21) |
| Upstream `main` read | `e07595714a467e18c750107137d2c2e50f0c3530` |

## Read the version

- `t3_environment_read` returns `serverVersion`. `orchestrator_capabilities` has no version field.
- The local build commit is `t3codeCommitHash` in the app's `package.json` (read it from the app bundle).

## Keep it current

When you change an instruction that depends on T3 Code, compare `serverVersion` with the table. If it is newer, re-read the T3 changes since the recorded version, update the table and the overlap table below, then slim the kit where a T3 feature now does the work. A session start needs no check.

## Overlap with T3 features

The verdicts are inferred from the T3 Code changes named in the table. No T3 feature fully replaces a kit element.

| Kit element | T3 feature and date | Slim? |
| --- | --- | --- |
| One worktree per task (`delegation-t3.md`, Workers item 5) | `delegate_task` with `isolation: worktree`, PR 19102, 2026-10-14; included in `v0.0.46-nightly.20261014.3093` | Yes: briefs need no hand-made checkout. Keep the policy and the `overlay.checkout` exception. |
| Delegation mechanics repeated in `delegation-t3.md` | Option inheritance and returned child options, PR 16595, 2026-10-20; included in `v0.1.1-nightly.20261020.3401` | Yes: shorten to a pointer. Keep the targets table. |
| Fresh-thread rotation for a cold Claude cache (`threads-and-cache.md`) | Claude idle compaction, PR 21682, 2026-10-20 (beta); global default and per-instance setting, PR 23037, 2026-10-21 | Maybe: test it, then change the rotation rule. PR 23037 is not confirmed in the installed build. |
| Decision board (`decision-boards.md`) | Pending requests; a child question wakes the parent, PRs 19521 and 19538, 2026-10-15 | Partly: a plain relay of one question can use the native tools. The visual board has no equivalent. |
| PR workflow | `link_pull_request`, `watch_pull_request`, `write_pull_request_guides`; added 2026-09-09, 2026-10-03 and 2026-10-11 | Not a slimming case. The kit mentions none of them: decide whether to adopt them. |
| Coordinator guard, review gate, runtime-mode protections, nesting depth cap, dashboard | Partial mechanisms only | No: keep. |
