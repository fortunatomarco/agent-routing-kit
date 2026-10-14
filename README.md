# Agent routing kit

A project-agnostic kit for work where one coordinator agent routes tasks to workers of different models and efforts. It holds the routing policy, the brief and review rules, the communication rules, and a guard plugin that restricts the coordinator in T3 Code. Each project sets its communication choices in a small overlay. Routing applies in every project: a coordinator always routes, and the project opts in by the provider instance it starts the coordinator on. The overlay's optional `Routing` section only sets parameters. Everything here is a draft; nothing is installed.

## Requirements

- Host: T3 Code, which provides `delegate_task`. The kit does not target the bare Claude Code CLI.
- Coordinator: a restricted Claude provider instance with the guard plugin. The kit assumes the id `claudeAgent_claude_coordinator`; `guard/README.md` has the install steps.
- Workers: plain provider instances, Claude (`claudeAgent`) and Codex (`codex`). The Sol and Luna routes use Codex models. Without Codex workers, `policy.md` has Haiku take short closed tasks and keeps Sonnet off them; it does not say where Sol's closed work goes.
- Python 3, for the guard hooks and `tools/lavish_board.py`. The files state no minimum version.
- Model names, effort levels and the instance id are the author's setup. Adapt the targets table in `delegation-t3.md` to the models your account lists.
- `GLOBAL-DELIVERY.md` has the install order.

## File map

Read a file when its trigger fires. The first line of each file names its trigger.

| File | Holds |
| --- | --- |
| `policy.md` | roles, closed and open tasks, the six routes, where work runs, the route line |
| `briefs-review-escalation.md` | the six-item brief, the return rule, the review chain, escalation |
| `threads-and-cache.md` | when to reuse or restart a thread, rotation |
| `dashboard.md` | the coordinator's status view |
| `delegation-t3.md` | T3 Code: role signals, the `delegate_task` targets table, worker policy, nesting, coordinator discipline |
| `computer-use-prompts.md` | rules for a Codex Computer Use prompt |
| `decision-boards.md` | T3 Code: the two-step decision board (build worker, wait worker), the two briefs, failure cases, what is tested; run by `tools/lavish_board.py` |
| `rationale.md`, `rationale-evidence.md` | why each route is what it is; cache and price evidence |
| `communication.md` | language and STE levels, selectors, missing information, the five level-80 rules, ASD-STE100 rules 1 to 18, scope and limits |
| `overlay-template.md` | required Communication settings, optional routing parameters, the kit commit checked by a project |
| `guard/` | the coordinator guard plugin: hooks, `launch_args.py`, `README.md` (install, test, risks) |
| `tests/test_guard.py` | synthetic check of the hooks |
| `GLOBAL-DELIVERY.md` | how the kit becomes global: the pointer lines, access and sandbox, protection, the guard install, the round 3 test |
| `examples/` | the STE source check, the access probe, the round reports |

One rule lives in one file. A file points to another file instead of copying it.

## Adopt the kit in a project

1. Install the global pointer from `GLOBAL-DELIVERY.md`, once per machine.
2. When the user starts a project or asks to adopt the kit, ask which language and STE level to use. Then copy `overlay-template.md` to `.agent-routing/overlay.md`, set both values, and record the kit commit in `Kit checked at:`.
3. Without `.agent-routing/overlay.md`, apply no language or STE rule. Routing does not need the overlay: a coordinator (a session with `delegate_task` and no file edit tool, not opened with "Act as the ... sub-agent") reads `policy.md` and routes, with defaults when the overlay or its `Routing` section is absent.
4. For a project with a coordinator guard, add `.agent-routing/guard.json` (`guard/README.md`, "Project config").
5. Start a new session in the project. Before its first reply, use a file read or file search tool to check whether `.agent-routing/overlay.md` exists, including for a short question. If it exists, read the overlay and `communication.md` before replying; read `policy.md` before routing work.

The overlay has this structure:

```markdown
## Communication
language: <english|user>
ste-level: <off|80|100>

## Routing (optional)
...

Kit checked at: <full kit commit hash>
```

The `Routing` section is optional and holds parameters only. The language and STE level definitions are in `communication.md`.

The project is adopted when step 5 passes and its instruction files hold no duplicate kit rule that the environment can read from the kit. A hosted project that cannot read the kit keeps the rule copies it needs.

`Kit checked at:` records the last kit commit the project checked. It does not pin the project to that commit. A new kit commit is available to every adopting project through the shared kit path.

## Check

From this folder: `python3 -I tests/test_guard.py`. It exits 0 when every hook case passes.

## License

MIT. See [LICENSE](LICENSE).
