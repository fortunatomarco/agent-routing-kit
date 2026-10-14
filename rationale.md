# Routing rationale

Read when: you change a route's model, effort, threshold or service tier, or someone asks why a route exists. It holds reasons and evidence; the rules stay in `policy.md`. Cache evidence and prices are in `rationale-evidence.md`.

The reasons below come from the kit owner's origin project, stated 2026-10-09 and 2026-10-10 unless a line says otherwise. "The owner" is the person who decides routing for the kit. Evidence from the origin project that the kit does not carry (commit hashes, session logs, local reports, screenshots) is dropped; a claim that lost its source is marked "motivo non documentato".

## How to use

1. Find the route you change. Read its constraint, evidence and "Would change if".
2. Change the route only when the new evidence meets its "Would change if", or the owner decides otherwise. Check "Decisions not taken" first: a rejected option stays rejected until its condition is met.
3. After the change, edit the route entry here: add the reason and the evidence. A reason you cannot source is written "motivo non documentato", never guessed.
4. Evidence kinds: a URL, a kit file, a measured block in `overlay.measurement-log` (measure first, cite after).

Short names: "tutorial" is https://academy.claude.com/tutorials/choosing-the-right-effort-level-in-claude-code ; "model-config" is https://code.claude.com/docs/en/model-config ; "cost page" is https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence ; "launch page" is https://openai.com/index/introducing-gpt-6-sol-and-luna/ ; "Codex models page" is https://learn.chatgpt.com/docs/models ; "effort review" is a review of every route's effort against the tutorial, model-config and cost page, made in the origin project (the file is not carried; its findings are quoted where used).

## Routes

### Planner: Opus 5.5 at xhigh

- **Constraint:** the "what and why" of choices that could change the project's core design or deliverable, where no source or test detects the error.
- **Evidence:**
  - Tutorial: "The other time to turn the effort up is when the task is something you cannot quickly check yourself". This matches condition 3.
  - model-config: `max` "may show diminishing returns and is prone to overthinking, so test before adopting it broadly". The tutorial says "Do not leave the effort on max". So the planner sits at xhigh, not max.
  - Cost: Opus 5.5 output is $20 per 1M tokens, so 100k extra thinking tokens cost $2.00. The route is rare because three conditions must hold.
  - Cost page, for coding only: "`xhigh` scored about 1.4 points higher for 2.5 times the cost of `high`". No planning benchmark exists (effort review).
- **Why three conditions, why failure never activates it:** the owner's reason: Opus is the costliest route and also the most intelligent model, so it triggers only for a task worth that cost. For failure, the owner confirmed this inference: a failure usually means a weak brief or an execution error, which Sonnet high or the coordinator fixes more cheaply than a strategic Opus review.
- **Why one planner:** motivo non documentato. Open.
- **Would change if:** a measured block shows Opus high gives the same planning decision as xhigh (test in separate sessions, as the cost page says), or the planner is used often enough that its cost shows in the measurement log.

### Sol: gpt-6-sol at medium, Standard service tier

- **Constraint:** closed tasks only: implementation and tests, fixed-schema extraction, bounded evidence packages. It writes no final prose and stops at an open point.
- **Evidence:**
  - Effort history in the origin project: high, then xhigh, then medium. The rule text of the final change states: "Effort is a ceiling, not a floor: medium for a closed task, xhigh for an open one." Sol takes closed tasks, so medium.
  - model-config, `medium` on Claude models: "fits day-to-day engineering work with a clear scope". This covers Claude models only; no fetched text covers the Codex effort scale (effort review: "unverified").
  - Prices: gpt-6-sol equals Sonnet 5.5 on list price (`rationale-evidence.md`, "Prices"). When Codex runs on a plan allowance, the OpenAI dollar figures compare models and do not bill.
  - Evidence checking: the Sonnet coordinator checks Sol's evidence against the cited sources. The owner's reason: in the owner's view OpenAI models have poor judgment and tend to over-engineer, so a check by Sonnet reduces that friction.
- **Standard service tier:** the fast tier costs 2x on the API and 2.5x of included plan usage in Codex. The owner's reason for Standard: this setup does not need speed. Speed comes from delegating micro tasks, each a small piece that closes quickly; the work is to put each task where it belongs.
- **Why Sol rather than a Claude model for closed work:** the owner's reason: the workflow leans heavily on Claude. To keep the Claude subscription from running out while the Codex subscription stays fully available, the work is split to cut Claude quota use or to raise use of OpenAI models.
- **Why Sol returns no final prose:** motivo non documentato.
- **Would change if:** pilot blocks show Sol medium failing the acceptance checks of closed tasks. Then raise one level at a time (tutorial: "adjust one level at a time"). Codex's scale is unverified, so measure before comparing it with Claude levels.

### Sonnet 5.5 at high (coordinator, prose, integration)

- **Constraint:** final prose, source registration, record integration, checking Sol's evidence, and the dispatcher role.
- **Evidence:**
  - Effort: model-config, `high`: "Work where verification matters or edge cases are likely". The coordinator's reviews are work "you cannot quickly check yourself" (tutorial).
  - Effort history: coordinator Opus medium, then Sonnet xhigh, then Sonnet high. The owner's reason for xhigh to high: cost. The owner used the briefcase benchmark and the knowledge-work benchmark as a proxy for the cost of Sonnet 5.5, and the extra intelligence was not backed by the cost increase: in long sessions the cost of Sonnet 5.5 at xhigh skyrocketed. The effort review judged the step consistent with the tutorial ("Do not leave the effort on max") and the cost page ("Below the model's ceiling, the highest effort levels pay for depth the task never uses").
  - Why Sonnet and not Opus as coordinator: the price reason, confirmed by the owner: Sonnet 5.5 costs half of Opus 5.5 on input and output (`rationale-evidence.md`, "Prices") and the coordinator thread is long. Opus stays in the lineup in case Sonnet falls short of the judgment and intelligence the task needs.
  - Dispatcher role: the owner observed that a coordinator without the role still did worker tasks. The role was tightened once; `guard/README.md` enforces it by tool restriction. Why it holds no work: its context lasts the whole project.
  - Cost of a long coordinator thread: cache reads are $0.20 per 1M, so a 200k-token context costs $0.04 per turn.
  - Keep one effort per thread: the cost page, section "What breaks the cache", says "Changing `effort` or the thinking configuration between requests invalidates the cache from that point onward". This is why `threads-and-cache.md` says a thread keeps its assigned model and effort.
- **Would change if:** a test of brief quality at `medium` and at `high` shows no loss (open question in the effort review); one route cannot split dispatch from prose without a second row. Test each level in a separate session, so the cache break does not distort the result (cost page, "Tune effort").

### Haiku 5.5 at xhigh (verifier; short closed tasks without Codex)

- **Constraint:** the verifier for a result that has no objective check, and, in an environment without Codex workers, short closed tasks (summaries, classification, checks, small fixes).
- **Evidence:**
  - Verifier at xhigh: the rule text of the origin project stated "A verdict has no machine check, so it runs at xhigh." The line was removed when two Haiku rows merged; its reason holds today.
  - Former route merge (short tasks and verifier into one route): motivo non documentato; the owner does not remember the reason.
  - 100k limit: an early rule limited Haiku to contexts under 100k tokens because "its price rises fivefold above 100k" (list price $0.10 to $0.50 per 1M input). The owner dropped the limit. The owner's reason: Haiku pricing is lower under 100k tokens, as the blog post announcing Haiku 5.5 says (not read here), but above 100k it is still cheap and still below Sonnet, so for the tasks Haiku takes it is better to dispatch Haiku than Sonnet. This matches the price fact: above 100k, Haiku input at $0.50 costs a quarter of Sonnet input at $2.
  - Cost page, "Compare models on cost per task": Haiku 5.5 answered GPQA Diamond at "about a twentieth of Claude Opus 5.5's cost per question, with 85% accuracy compared with 91% for Opus 5.5". It "suits high-volume and latency-sensitive work with checkable outputs". A verifier checks work that has no objective check, so this is a tension to keep in view.
  - Verifier gets the brief, the diff and the cited sources, never the worker's reasoning; it adds no criterion of its own. The owner confirmed the reasons: the worker's reasoning would bias the verdict, and extra criteria would grow the scope beyond the user's request.
  - Short tasks: in an environment with Codex workers they go to Luna only (owner's decision 2026-10-10, see "Rules shared by all routes"); Haiku takes them where Codex is absent.
- **Decision of 2026-10-09: no change.** The effort review proposed Haiku high: the tutorial says to adjust down for simple tasks, and over-high effort gives "identifying more tasks than you actually assigned", which the verifier rule forbids. The review has no measurement behind it. The verifier role justifies xhigh, and a single route stays simpler than two.
- **Would change if:** a pilot test runs the same verification at `high` and at `xhigh` and counts false failures that add criteria. A higher count at xhigh moves the route to high in `policy.md` and `delegation-t3.md`.

### Luna: gpt-6-luna at max, Standard service tier

- **Constraint:** mechanical work with a defined check: build, lint, typecheck, CI, failing tests, data checks, inventories, fixed-schema transformations, fully specified local edits. It stops at anything else. It is free whenever the active environment runs Codex workers, even while a Computer Use task runs.
- **Evidence:**
  - Preferred over Haiku "so the routing does not lean on Claude" (rule text of the origin project).
  - Computer Use shares the Codex setup: the Codex config file set `model = "gpt-6-luna"`, `model_reasoning_effort = "max"`, `service_tier = "default"` when read on 2026-10-09. The Computer Use page does not say which model Computer Use uses, so "Computer Use runs on the config-file model" is an assumption that no page read confirms.
  - Prices: gpt-6-luna equals Haiku 5.5 up to 100K on list price (`rationale-evidence.md`, "Prices").
  - Why max: the early rule text states `max` with no reason. The owner's account: the choice rests on a benchmark and on the Max model's performance there. The owner did not check the Codex documentation on reasoning effort. The benchmark is DeepSWE v1.1. Evidence found afterwards:
    - Official figures, from the launch page. The fetch tool got HTTP 403, so the owner read the page in a browser on 2026-10-09 and sent screenshots, which the kit does not carry. "On DeepSWE v1.1, which tests performance on complex software-engineering tasks in real codebases, GPT-6 Sol at max effort scores 68.8%". "GPT-6 Luna at max effort scores 66.6%, comparable to Claude Opus 5 and Fable 5 at medium effort. In these comparisons, Luna costs 93% less per task than Opus 5 and 96% less than Fable 5." The vendor published these figures about its own models.
    - Computer-use chart on the same page (OSWorld 2.0, offline set): "GPT-6 Luna (max) is able to exceed GPT-5.6 Sol (medium) at one tenth of its cost." The points carry no labels, so reading the best point as max rests on the page text only.
    - Codex models page: "GPT-6 Luna supports reasoning efforts up to **Max**, but not **Ultra**." Also "Start with **High** for Luna", "Most tasks don't need Max or Ultra", and "Reasoning efforts don't map exactly between model generations." Max "gives the selected model more time to reason about a single task", for when "depth matters more than speed or usage".
    - The owner's rabbit-hole intuition: higher reasoning means more thinking tokens, and so more tries by the model. The first half has a source: "Higher effort can improve results for complex tasks, but it takes longer and uses more tokens" (Codex models page, Astra section). "More tries" and "max keeps the model out of rabbit holes" have no source, so they stay the owner's untested intuition. A test: the same Computer Use task at high and at max.
    - Not mapped: the Codex effort scale against the benchmark's effort scale. The figures also come from software-engineering and computer-use tasks, not from the whitelist (lint, builds, inventories).
  - Against max: tutorial, "Do not leave the effort on max; try again at the default"; model-config, `max` is for "Hard problems you want Claude to work through without you". These cover Claude models. The Codex scale has no matching text beyond the page quoted above (effort review: "lower (principle supported; Codex effect unverified)").
- **Priority rule removed (owner's decision of 2026-10-09).**
  - Old rule: Luna was free only when no Computer Use task was active or imminent, and while one was, a Luna task went to Haiku xhigh instead. The owner's two original reasons: (1) not to disturb the Computer Use task, which the owner now doubts it does; (2) to save Codex quota when Computer Use ran on GPT-5.6 Luna at max, which cost more than GPT-6 Luna at max.
  - The owner's reason for removing it: no evidence was found that a second task interferes with Computer Use. If two Luna instances can run at once, the owner wants them to. The quota argument is weaker too, because gpt-6-luna costs about half of gpt-5.6-luna per token and one twentieth of GPT-6 Sol (`rationale-evidence.md`, "Prices").
  - Evidence: the only documented conflict is two Computer Use tasks on the same app: "Do not run two Computer Use tasks against the same app at the same time." "Competing actions can change the current window or state and make the result unreliable." "On macOS, Computer Use can work in the background while you use other apps." (https://learn.chatgpt.com/use-cases/use-your-computer-with-codex). Nothing official covers a second task that is not Computer Use. A second task also draws on the same plan allowance ("Local messages and cloud chats share your plan's usage allowance.", https://learn.chatgpt.com/docs/pricing), and no page gives a per-task credit figure.
  - Status: the reason is absence of evidence, not evidence of no interference. Inference, untested: a Luna worker edits files and runs shell commands, which should not touch the windows Computer Use controls.
  - Kept: the Computer Use route, its config-file source and its approval step. Two Computer Use tasks on the same app stay a risk, per the page above, though no rule states it.
  - Would change if (priority rule): Computer Use runs show interference when a Luna worker runs alongside, either an observed case or a concurrency A/B (the same Computer Use task 5 times alone and 5 times beside a Luna worker, comparing success, steps and duration), or the owner measures that concurrent Luna runs drain the plan allowance.
- **Decision of 2026-10-09: no change.** Luna stays at max until measured. No work block existed in the origin measurement log, so no measured cost or quality exists for any effort.
- **Would change if (max):** pilot blocks show Luna at max overthinking: work beyond the whitelist, or high plan usage for a mechanical task. Then try medium and step lower one level at a time, with the escalation to Sonnet high as the safety net.

### Computer Use: Codex desktop automation

- **Constraint:** desktop apps, driven through Codex. Model, effort and service tier come from the Codex config file.
- **Evidence:**
  - Config as the single source: the origin project found that the setting was never stated and that an omitted model takes the provider's first model, `gpt-6-astra`; the report behind that finding is not carried, so treat the behaviour as an observation, motivo non documentato beyond it. Hence the explicit target row in `delegation-t3.md`.
  - Runs only from T3 Code in the origin setup; the owner has no Codex Computer Use from Claude Projects.
  - Verified in the origin project: a Claude coordinator delegated a Computer Use task to Codex in T3 and received the result with no extra prompt.
- **Would change if:** the owner changes the Codex config file. The rule needs no edit then. If Luna moves to medium, decide separately whether the config follows.

## Rules shared by all routes

- **Closed briefs determine the route (owner's decision of 2026-10-10).** Reason: routing followed deliverable type, although the briefs fixed the outcome and acceptance check. The Claude subscription is the scarce one (see "Why Sol rather than a Claude model for closed work"). Evidence: the owner audited one coordinator thread and found closed tasks routed to Sonnet high; the coordinator admitted the misrouting. The audit numbers are not carried: motivo non documentato for the exact counts. Sol and Luna capability tests on 2026-10-10 both rendered to PNG and viewed images, with verdict FULL (local notes, not carried). A visual check does not determine the model route. **Would change if:** pilot blocks show Sol or Luna failing the acceptance checks of closed tasks.
- **No stall when nothing is awaited (owner's decision of 2026-10-10).** Reason, in the owner's words: not stalling when nothing is awaited must be a general rule of the workflow, not only a personal memory note. Evidence: in an analysis thread, after the last dependency had finished, the coordinator kept a drafted rule change pending and ended its turn waiting for an approval the owner had already implied. Nothing blocked the next step, and the owner had to ask "are we waiting for something?" before work resumed. The rule sits in `policy.md`, "Coordinator", because every delegating session reads it. **Would change if:** motivo non documentato (the owner gave no condition). Inference, not sourced: a coordinator acts on a decision that was truly the owner's, which makes the list of their decisions too narrow; or stalls recur with the rule in place.
- **Short closed tasks go to Luna (owner's decision of 2026-10-10).** Reason, in the owner's words (translated): without quota-aware model routing, for now short closed tasks are done only by Luna, until enough data exists from the test running with quota-axi. Evidence: before this decision, Luna was free whenever the Codex environment was active; independent work may run in parallel with disjoint write sets and separate acceptance checks; the owner asked why Luna should be unavailable, since the only case seen is the Codex quota running out, and two Luna workers can run at once. Clarified the same day: in an environment without Codex, the equivalent Claude model of the same level takes them, so Haiku; with the Codex quota finished, the task waits, left open until quota-aware routing exists. **Would change if:** quota-axi samples cover at least 14 days, including the Claude and Codex weekly resets, so quota-aware routing can be designed and the owner approves it; the held case (Codex quota finished) is then reopened.
- **Short returns.** Each brief fixes a report file and a final message of at most 150 words. Reasons: coordinator context grows from worker output. Cost page, "Set budgets and output caps": "Output tokens cost five times input tokens on Claude Sonnet 5, and in an agent loop every token the model writes comes back as input on every later turn". The same section measured a one-line answer at 39% fewer output tokens and 14% lower cost per run, with accuracy "within run-to-run noise". The measurement is not about subagent returns.
- **A thread keeps its model and effort.** An effort change breaks the cache (cost page, "What breaks the cache"). The cache periods and their measurement are in `rationale-evidence.md`, "Cache".
- **Rotation at 300k tokens.** `autoCompactWindow` is 300,000 tokens, set by the owner; their reason: it "keeps long sessions out of the low-quality part of a full context". The coordinator hands off at that point (moved from 100k to 300k). The owner's reason: staying out of the zone where, according to engineers the owner trusts, model quality degrades, around 300k to 400k tokens. It rests on third-party opinion; no source was read for it. A handoff beats compaction: no source was found for this as a cost-page finding; the page reports that a compaction request wrote an 81,000-token context to the cache instead of reading it, costing $0.21 against $0.04 for the same pass (cost page, measurement 18). Whether the claim "handoff beats compaction" came from another source: open.
- **Verification chain** (gate, verifier, review): the owner's reason: workers can report a passed check that did not pass, and OpenAI models over-engineer (see the Sol entry), so something independent of the worker checks the result. The verifier's xhigh has its own reason in the Haiku entry.
- **No Sonnet fallback for closed tasks when Codex is not available (owner's decision of 2026-10-10).** Reason, in the owner's words (translated): remove it; without quota-aware routing there is no use for it; keep it at most for when it exists. Evidence: the removed clause disagreed with the hold rule in `briefs-review-escalation.md` ("hold the task") and with the decision that closed work waits when Codex is exhausted (`policy.md`, Luna). The owner allows keeping the clause for when quota-aware routing exists. **Would change if:** quota-aware routing is designed and the owner approves it.

## Decisions not taken

- **Workers choose their own route.** Rule: "This policy, not the worker, fixes model and effort". The owner's reason for the reversal from "whoever starts a thread sets its model and effort": workers picked routes inconsistently and cost was not controlled. Open gap: nothing says whether a brief may lower the effort of a row for a simple task (effort review).
- **Luna from max to medium.** Not taken on 2026-10-09: the principle supports it, the Codex effect is unverified, and no measurement exists. Condition to revisit: see the Luna entry.
- **Haiku from xhigh to high.** Not taken on 2026-10-09: the verifier role justifies xhigh. Condition to revisit: see the Haiku entry.
- **Coordinator at medium for pure dispatch.** Not taken: untested, and one route cannot split dispatch from prose (effort review).
- **Automatic quota-aware routing.** Not adopted. The owner must separately approve reconsideration (measurement.md, removed 2026-10-12). Quota percentages from different providers are not interchangeable. A third-party resolver that sends the brief to an external classifier API and ranks candidates by quota did not fit (source report not carried: motivo non documentato beyond this summary).
  - The owner's reason for a fixed policy now: the quota-axi tool is installed, and the routing should already monitor quota spending; the removed pilot procedure recorded quota spending (measurement.md, removed 2026-10-12). The owner's direction: quota-aware routing later, where the choice of provider reacts to the quota available and to the days left until the quota refreshes.
  - Open direction, not a rule. The pilot data is the input for that decision. Whether quota-axi reports the days to the refresh was not checked.
- **Removing the coordinator's tools by prose alone.** Replaced by the restricted instance (`guard/README.md`). The origin research found the mechanism (a second Claude provider instance with `launchArgs` set to `--disallowedTools ...`) and the origin project later ran it end to end.
- **Persistent sub-coordinators and deeper nesting.** Not adopted: nesting stops at two levels (`delegation-t3.md`); a third-party framework's "command structure stays flat" agrees (source report not carried).

## Open reasons

Each item is a reason the origin history does not state. Reply with the reason, or "no reason"; the entry is then updated.

1. Why one planner (Planner entry). Open.
2. Why Sol returns no final prose (Sol entry). Open.
3. Why Haiku and the verifier merged into one route. Open; the owner does not remember.
4. Codex effort scale against the benchmark's effort scale (Luna entry). Open.
5. Where the 60-minute and 30-minute cache figures came from (`rationale-evidence.md`, "Cache"). Open.
6. Whether "handoff beats compaction" has a source beyond the cost page (Rotation entry). Open.
7. Should a brief be allowed to lower a row's effort for a simple task? This is a rule change, not a reason. Open.
