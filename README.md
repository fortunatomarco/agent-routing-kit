# Agent routing kit

Read when: you want the map of the kit, or you meet it for the first time.
Reader: human or maintainer.

A project-agnostic kit for work where one coordinator agent routes tasks to workers of different models and efforts. It holds the routing policy, the brief and review rules, the communication rules, and a guard plugin that restricts the coordinator in T3 Code. Each project sets its communication choices in a small overlay. Routing applies in every project: a coordinator always routes, and the project opts in by the provider instance it starts the coordinator on. The overlay's optional `Routing` section only sets parameters.

## File map

Read a file when its trigger fires. Line 3 of each rule file ("Read when:") names its trigger and line 4 ("Reader:") names its reader.

| File | Holds |
| --- | --- |
| `policy.md` | roles, closed and open tasks, the six routes, where work runs, the route line |
| `briefs-review-escalation.md` | the six-item brief, the return rule, the review chain, escalation |
| `threads-and-cache.md` | when to reuse or restart a thread, rotation |
| `dashboard.md` | the coordinator's status view |
| `delegation-t3.md` | T3 Code: role signals, the `delegate_task` targets table, worker policy, nesting, coordinator discipline |
| `t3-compat.md` | the T3 Code version the kit was checked against, how to read it, and the T3 features that overlap the kit |
| `computer-use-prompts.md` | rules for a Codex Computer Use prompt |
| `decision-boards.md` | T3 Code: the two-step decision board (build worker, wait worker), the two briefs, failure cases, what is tested; run by `tools/lavish_board.py` |
| `rationale.md`, `rationale-evidence.md` | why each route is what it is; cache and price evidence |
| `communication.md` | language and STE levels, selectors, missing information, the five level-80 rules, ASD-STE100 rules 1 to 18, scope and limits |
| `GLOSSARY.md` | plain meaning of the kit terms, with a pointer to the rule that holds the criteria |
| `overlay-template.md` | required Communication settings, optional routing parameters, the kit commit checked by a project |
| `guard/` | the coordinator guard plugin: hooks, `launch_args.py`, `README.md` (install, test, risks) |
| `tests/test_guard.py` | synthetic check of the hooks |
| `GLOBAL-DELIVERY.md` | how the kit becomes global: the pointer lines, access and sandbox, protection, the guard install, the test protocol |
| `examples/` | evidence behind the rules: the STE source check, the access probe, and the research notes on T3 Code and Firstmate |

One rule lives in one file. A file points to another file instead of copying it.

## Requirements

- `python3` on `PATH`. The guard hooks run `python3 -I`. Without it the hooks do not block anything (`guard/README.md`, Install step 1).
- T3 Code, at the version recorded in `t3-compat.md` or later.
- Claude Code and Codex, both signed in: workers run on the `claudeAgent` and `codex` provider instances.

## Adopt the kit in a project

The steps, the overlay structure and the definition of an adopted project are in `overlay-template.md`, sections "Adopt the kit in a project" and "Kit check".

## Check

From this folder: `python3 -I tests/test_guard.py`. It exits 0 when every hook case passes.
