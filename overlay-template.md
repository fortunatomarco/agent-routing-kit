# Project overlay template

Read when: a project starts, adopts the kit, or needs its overlay values. Copy this file to `.agent-routing/overlay.md` in the project. Without that file, apply no language or STE rule; routing still applies with its defaults. Ask the user for the language and STE level before you create it.

The overlay holds project choices and facts. It does not copy kit rules. `Kit checked at:` records the last kit commit the project checked. It does not pin the project to that commit. The shared kit path makes new kit commits available to every adopting project.

## Communication

language: <english|user>
ste-level: <off|80|100>

`english` means write user-facing text in English. `user` means write it in the language the user uses. The STE levels are defined in `communication.md`.

Optional communication parameters:

| Parameter | Used in | Default |
| --- | --- | --- |
| `overlay.glossary` | `communication.md`, level 100 | none: name the project glossary file |
| `overlay.ste-dictionary` | `communication.md`, level 100 | none: path of a local copy of ASD-STE100 Issue 9, kept out of version control |
| `overlay.ste-exceptions` | `communication.md`, level 100 | none: extra text categories outside STE, each with a reason |

## Routing parameters (optional)

Routing applies in every project (`policy.md`, "Role"). Add this section only to change a default. A missing section or value uses the default below.

| Parameter | Used in | Default |
| --- | --- | --- |
| `overlay.stakes` | `policy.md`, planner condition 2 | the project's core design, scope or main deliverable |
| `overlay.records` | `policy.md`, Sonnet route | none: name the records that Sonnet integrates after workers return (index, log, open questions, summaries) |
| `overlay.gate` | `briefs-review-escalation.md`, Gate | none: only `git status --short` and the brief's acceptance command |
| `overlay.environments` | `policy.md`, Where work runs | one environment that has the repository and Codex workers |
| `overlay.rotation` | `threads-and-cache.md` | 300k tokens |
| `overlay.codex-prompts` | `delegation-t3.md`, Computer Use approval | `codex-prompts/` in the project |
| `overlay.cu-browser` | `computer-use-prompts.md` | a browser the user does not use for their own work |
| `overlay.board-browser` | `decision-boards.md` | none: use the T3 preview only; otherwise use `open -a` with the macOS browser app name |
| `overlay.checkout` | `delegation-t3.md`, Workers | one git worktree per task; write `shared` when the project's own rules require one shared checkout |

## Project facts

Each project keeps its own facts here and points to the kit rule it configures.

- **Planner wording:** a project may restate the three planner conditions with its own example. It keeps the form: decision, wrong choice is costly, no readily available check.
- **Environment adapters:** describe how an environment-specific tool or service works in the project.
- **Project gates:** list commands in `overlay.gate`; list coordinator script runners in `.agent-routing/guard.json` (`guard/README.md`).
- **Project procedures:** keep project-specific rule-change steps, handoffs, data-extraction loops, and Computer Use facts such as the data source's name.
- **Preferences:** keep project-specific preferences here unless a global instruction file already holds them.
- **Style for official outputs:** keep extra writing rules for documents with a formal reader.

## Kit check

Kit checked at: <full kit commit hash>

Update this line when the project checks a new kit commit.

The project is adopted when `.agent-routing/overlay.md` has its Communication settings, the `Kit checked at:` line, and any routing parameters the project changes. Its instruction files have no duplicate kit rule that the environment can read from the kit. A hosted project that cannot read the kit keeps the rule copies it needs.
