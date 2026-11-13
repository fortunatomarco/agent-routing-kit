# Delegating in T3 Code

Read when: your tool list carries `mcp__t3-code__` tools and you coordinate, delegate, or start a thread. `policy.md` holds the routes; this file holds how T3 Code carries them out.
Reader: coordinator.

## Signals and instance

- `mcp__t3-code__` tools mean T3 Code. Who is a worker and who is the coordinator: `policy.md`, "Role". The coordinator always routes, in every project, with or without an overlay.
- The coordinator is a dispatcher. Whatever the first message says, do these before your first action: read `policy.md`, then hand every task that is not routing, a brief, a gate or the dashboard to a worker through `delegate_task`. Name the skills and the pipeline of the request in the brief.
- The active coordinator target is `providerInstanceId: claudeAgent_claude_coordinator`, `model: claude-sonnet-5-5`, `effort: high`. It is a restricted instance (`guard/README.md`). Choosing this instance is how a project opts in to routing. Workers never run on it (see Workers).

## Targets

Delegate every worker through `delegate_task` with a complete target; the built-in Agent tool cannot set effort. Use these exact delegated targets. The Route column repeats the route names of `policy.md` and must stay equal to them.

| Route | `providerInstanceId` | `model` | options |
| --- | --- | --- | --- |
| Opus planner | `claudeAgent` | `claude-opus-5-5` | `effort: xhigh` |
| Sol closed work | `codex` | `gpt-6.1-sol` | `reasoningEffort: medium`; `serviceTier: default` (Standard service tier) |
| Sonnet implementation | `claudeAgent` | `claude-sonnet-5-5` | `effort: high` |
| Haiku verifier | `claudeAgent` | `claude-haiku-5-5` | `effort: xhigh` |
| Luna mechanical work | `codex` | `gpt-6-luna` | `reasoningEffort: max`; `serviceTier: default` (Standard service tier) |
| Computer Use | `codex` | from `~/.codex/config.toml` | `reasoningEffort` = `model_reasoning_effort`; `serviceTier` = `service_tier` |

- When `orchestrator_capabilities` does not list a target's model or option value, tell the user and hold that task.
- Load the coordinator's tool schemas with one `ToolSearch` call at the first need (delegate, status, cancel, configuration, thread read and list, pending requests), not one tool at a time. Call `orchestrator_capabilities` once per thread, and again only after a target is rejected.
- Before each `delegate_task`, write one line: route, the policy clause that applies, and why the brief is closed or open. A closed task does not go to a Claude route; the exceptions are Haiku as verifier and Haiku's short closed tasks in an environment without Codex. "I default to Sonnet" is not a reason.
- A need for rendering, screenshots, visual checks, shell or tests is not a reason to choose a Claude route. Codex workers can view images and run tools. The brief says what must be verified and tells the worker to check which tools exist before choosing one.
- Set `runtimeMode: full-access` and a complete `target` on every worker (see Workers).
- A child receives only your prompt, so write it as the complete worker brief (`briefs-review-escalation.md`). Codex also reads the project's `AGENTS.md`.
- When routing matters, confirm what the child actually ran with `t3_thread_configuration` on its `childThreadId`.

## Workers

A worker runs commands and edits files, so it never inherits the coordinator guard.

1. **Instance and mode:** a plain provider instance (`claudeAgent` or `codex`, never a guarded one), `runtimeMode: full-access`, and an explicit `target`. The delegation guard denies a missing or guarded instance (`guard/README.md`). The user does not approve prompts by hand, so the protections are automatic.
2. **Rules in every brief:** see `briefs-review-escalation.md`, "Rules in every brief".
3. **Review:** the coordinator checks every result before it accepts it (`briefs-review-escalation.md`, "Review").
4. **OS lock:** `chmod -R a-w` on a folder is the provider-independent protection. Use it for the kit and for any folder a project wants frozen (`GLOBAL-DELIVERY.md`, section 3).
5. **Isolation:** one git worktree per task that edits code (`delegate_task` with `isolation: worktree`; the child starts from the parent's local commit and does not get uncommitted edits), unless `overlay.checkout` says the project needs one shared checkout. Code work ends in one pull request per feature, and the coordinator reviews it before anything is merged (`briefs-review-escalation.md`, "Review"). The worker opens the pull request with `gh` and returns its URL, the head commit and the check state; the coordinator calls `link_pull_request` on it and merges nothing. A worker reads the checks with `gh pr checks`. `watch_pull_request` and `write_pull_request_guides` are used only when the user asks, because each wake of the coordinator costs quota. Run one code task at a time by default. Start code tasks in parallel only when the user asks, because parallel sessions draw on the same subscription quota and parallel work can exhaust the plan limits.
6. **Not adopted: the Claude native sandbox.** Reasons and sources: `rationale.md`, "Decisions not taken".

## Running and tracking tasks

- Use `mode: "async"` for long work and end your turn: T3 wakes you when the child finishes. Call `task_status` only when you need the result inside the current turn.
- Retain every returned `taskId` and check it with `task_status` before delegating matching work. A `childThreadId` is backing storage for the child, not a target for new work.
- Accept a result only when `task_status` shows `workState: result_available` and `hasPendingChildRuns: false`: a finished turn with live nested work is not a finished task.
- Probes: when the same check must run over a list (modes, files, sources) and each item has an objective result (a message, a number, yes or no), use two workers, not one per item. Send the first item alone. Once its result is accepted, send the remaining items to one worker with the same method. The worker returns the raw result of each item (the exact message or value), not a verdict. The coordinator, or a verifier that is not that worker, rechecks one item chosen at random. Interpretation, judgement and prose are not probes: each keeps its own worker and verifier.
- For each delegated review round, call `delegate_task` again. Give each round a distinct `clientRequestId`, stable across retries of that round. Include the original brief, prior findings, responses, and unresolved objections. Do not continue a review through `t3_thread_send` on `childThreadId`.

## Nesting

- A worker delegates only when its brief says so. Nesting stops at two levels: coordinator, worker, sub-worker (verified 2026-10-08: a Haiku 5.5 worker delegated to a Haiku 5.5 sub-worker and got the result back). T3 does not enforce the limit, because every sub-worker also has `delegate_task`, so each sub-worker brief ends with "You are the last level; do the task yourself."
- Precision rises with depth. The coordinator makes every routing and splitting decision and writes each sub-brief in full (six items, target, effort), ready to send. The worker sends the sub-briefs, collects the results and reports them; it neither routes nor splits an open task. A sub-brief is a closed task with an objective check.
- Nest only to fan out one closed task over a list of items (the same extraction over twelve sources). Delegate everything else from the coordinator as sibling workers.

## Coordinator discipline

The coordinator thread is a control tower and holds no work, so its context lasts the whole project.

- Its tool calls are `delegate_task`, `task_status`, `AskUserQuestion`, dashboard posts, the reads a brief or a review needs, and gate commands, within the tools in `guard/README.md`. A worker takes every other action, whatever its size, including every edit to a rule file.
- Before each tool call, ask: is this routing, a brief, a gate or the dashboard? If not, delegate it.
- Reading long tool output, or searching saved result files, is worker work: delegate it instead of reading or grepping it in the coordinator thread.
- A request that names a skill or describes a build, design or multi-step pipeline is a delegation trigger. Copy the user's pipeline and the skill names into the brief; the worker invokes the skills, the coordinator does not.
- Never tell the user that a skill cannot run, or ask the user to run it, before a worker has tried. A skill that only the user may invoke is still worker work when the user invoked it or asked for it in this session: the brief says so, gives the path of its `SKILL.md`, and the worker follows it (`briefs-review-escalation.md`).
- Run iterative work with the user one round per worker, through `delegate_task`:
  1. The worker keeps a state file in the work folder: decisions taken, file paths, next step.
  2. The worker returns as the brief's return rule says, with the open choices as options with a recommendation.
  3. The coordinator puts the choices on `AskUserQuestion`, or on a decision board when the project routes important decisions there (`decision-boards.md`: the board is built by one worker and answered through a second worker), then sends the next round as a new `delegate_task` whose brief points to the state file. A board round ends when the wait worker returns.
- Images, screenshots, page snapshots, HTML and long tool output stay with the worker. The coordinator receives paths and a text summary; the user opens the files.
- Before delegating a Computer Use task, save the full prompt in `overlay.codex-prompts`, show the user a very short brief of it, not the prompt itself, and wait for their approval on `AskUserQuestion`. The prompt follows `computer-use-prompts.md`.
- Handoff and commits: before work goes to a new chat, a worker commits the project's working branch locally. The commit holds every changed and new file that the new chat must read: rules, reports and the handoff. No push, no merge, no co-author line. Pushing and merging stay the user's decision. The handoff names each file by its full path, because a new chat starts in a worktree that holds only committed files. Before any push, a worker checks the files in `examples/` for private data, because the kit repository is public.
