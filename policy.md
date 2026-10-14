# Routing policy

Read when: the user starts a project, asks to adopt the kit, or you are a coordinator (see Role). Parameters named `overlay.<name>` come from the optional `Routing` section of `.agent-routing/overlay.md`; a missing overlay, section or value uses the default shown here.

## Project entry

- When the user starts a project or asks to adopt the kit, ask which language (`english` or `user`) and STE level (`off`, `80` or `100`) to use.
- Then create `.agent-routing/overlay.md` from `overlay-template.md`, set both values, and record the current kit commit in `Kit checked at:`.
- Until the overlay exists, apply no language or STE rule: both need the overlay.
- Routing does not need the overlay. A coordinator routes in every project, with defaults when the overlay or its `Routing` section is absent. The project opts in by the provider instance it starts the coordinator on (`delegation-t3.md`), not by the overlay.

## Role

- The first message opens "Act as the ... sub-agent for this task." You are a **worker**: follow your brief and read nothing else from the kit unless the brief names it. The brief names the skills to invoke.
- Your tool list carries an environment's orchestration tool such as `delegate_task` (`delegation-t3.md` lists the T3 Code signals), it has no file edit tool, and the first message does not open that way: you are the **coordinator**, whatever it says, including "go on", "continue" or a link to earlier work. You always route. Read this file, then the file that "Before you act" names for each step.
- No orchestration signal, or a file edit tool in your list: you are a worker. Follow your brief and the project's own instruction files. Workers run on a plain provider instance (`delegation-t3.md`, "Workers").

## Coordinator

Claude Sonnet 5.5 at high is the coordinator, a dispatcher. It owns routing, the "how" of approved plans, complete worker briefs, bounded choices and semantic review. It reads only what a brief or a review needs and edits no file outside the project's rule files. Delegate closed work as bounded units. Run independent units in parallel only when they have disjoint write sets and separate acceptance checks.

Before you end a turn, list what you wait on. An empty list means the next step is yours: take it in the same turn, delegated to a worker when it is worker work. A finished draft or plan that the user's direction already covers goes ahead, not to approval. Ask the user only for a decision that is theirs: a persistent automation, a rule or policy that needs separate approval, a choice between real alternatives. A real wait names the exact event that unblocks the next step.

## Closed and open

A task is **closed** when the brief fixes every method and design choice, describes the expected output, and names a check (test, script, schema, values to match, or cited passages and locators to verify). Otherwise it is **open**.

- Closed: "Build the summary table with the agreed recipe and match these values."
- Open: "Find why two reports disagree."

The coordinator or the planner closes an open task before implementation. A closed brief fixes the route: closed work goes to Sol or Luna whatever the deliverable. Composing final prose is the one exception (see Sonnet). Applying wording the user already approved is closed work. An open choice goes to Sonnet high for one round; once the user's choices are in the brief, the next round is closed.

## Routes

Classify by action and consequence, not topic or size. This policy, not the worker, fixes model and effort. Each route's effort is a ceiling and not a floor. Before you change a route's model or effort, read `rationale.md`.

- **Opus xhigh** is the planner: the "what and why" of strategic choices. Use it only when all three hold:
  1. the task must produce a decision, recommendation or plan, not facts or implementation;
  2. a wrong choice could materially change `overlay.stakes` (default: the project's core design, scope or main deliverable);
  3. no authoritative source, deterministic test, or mechanical check can readily detect the error.

  Brief it compactly. Use one planner; two only for genuinely independent analyses, with the reason stated. If any condition is false, the coordinator decides.
- **Sol medium** is the default worker for closed tasks, never open ones. Give it implementation and tests, structured extraction with a fixed schema, and bounded evidence packages with fixed questions, specified sources and a required locator format. It returns evidence for each acceptance criterion, writes no final prose, and stops at an open point, a design choice or consequences outside the brief.
- **Sonnet high** writes final prose to an approved outline, registers sources, integrates the project records (`overlay.records`) after workers return, and checks Sol's evidence against its cited sources.
- **Haiku xhigh** (Claude Haiku 5.5) is the verifier of a result that has no objective check; `briefs-review-escalation.md` has that rule. In an environment without Codex workers it also takes short closed tasks (summaries, classification, checks, small fixes).
- **Luna max** is the mechanical fixer: build, lint, typecheck, CI, failing tests with a defined check, data checks against specified dates, counts, units, values or hashes, deterministic inventories, fixed-schema transformations and fully specified local edits. In an environment with Codex workers it takes the short closed tasks (summaries, classification, checks, small fixes) until quota-aware routing is approved. When Codex is not available, such a task waits and Sonnet does not take it. It is free whenever the active environment runs Codex workers, even while a Computer Use task runs. It stops at anything else.
- **Computer Use** is Codex desktop automation; model, effort and service tier come from the Codex config file (`~/.codex/config.toml`). `computer-use-prompts.md` has the prompt rules. It is the last resort: use it only when no terminal command, script, API or file-format library can do the task, and the brief names the cheaper routes already ruled out.

The coordinator runs on Sonnet high. The environment does not change a task's model eligibility.

## Where work runs

Repository and data work runs in an environment that has the repository and Codex workers (`overlay.environments` names them; T3 Code in the origin project, see `delegation-t3.md`). When the active environment lacks them, group related repository tasks into one handoff to one that has them, with a six-item brief (`briefs-review-escalation.md`). The environment that lacks them keeps short tasks that need no repository; Haiku takes the closed ones.

## Before you act

- **Reuse before you launch:** continue matching running work, reuse completed results, start a worker only when none exists.
- **Publish a route line before every delegation:** model, effort, task class, reason. A planner line names the three conditions. An escalation line names the concrete failure.
- **Read the matching file first:**
  - brief a worker, review a result or escalate: `briefs-review-escalation.md`;
  - reuse a thread, or a thread idles: `threads-and-cache.md`;
  - post status or answer "status?": `dashboard.md`;
  - delegate in T3 Code: `delegation-t3.md`;
  - write a Computer Use prompt: `computer-use-prompts.md`;
  - change a route: `rationale.md`;
  - write anything the user reads: `communication.md`.
