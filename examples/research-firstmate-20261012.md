https://github.com/kunchenguid/firstmate  
Commit read: `a1ecefb43086401f4a6243d6ccebf72969211c84`  
Licence: MIT ([LICENSE, lines 1-3](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/LICENSE#L1-L3)).

Other same-name repositories surfaced in search: [Coditan/firstmate](https://github.com/Coditan/firstmate) and [pandanax/firstmate](https://github.com/pandanax/firstmate). The evidence below uses Kun Chen's repository at the commit above.

## F1. Where is routing policy and config? How do projects find it?

Routing is held by the firstmate installation/home, not separately in each project: shared supervisor instructions live in its tracked `AGENTS.md`, while optional private routing rules live in the home's gitignored `config/crew-dispatch.json`. `FM_HOME` chooses that home, and firstmate reads its rules at task intake before passing a concrete profile to the worker launcher. Project `AGENTS.md` holds project knowledge, not the fleet routing policy; secondmate homes inherit the dispatch file.

- [docs/configuration.md, lines 18-29](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L18-L29): “`FM_HOME` selects the operational home for one firstmate instance.”
- [docs/configuration.md, lines 1096-1100](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1096-L1100): “`config/crew-dispatch.json` is an optional local, gitignored file containing natural-language rules”
- [AGENTS.md, lines 148-153](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/AGENTS.md#L148-L153): “Knowledge useful to almost every contributor to one project belongs in that project's committed `AGENTS.md`”
- [docs/configuration.md, lines 1202-1204](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1202-L1204): “Secondmate homes inherit this file from the primary”

## F2. How do workers get instructions across folders or sandboxes? Do they read outside the project?

Firstmate writes each task's brief in its home, renders a launch-brief overlay, and sends the worker a launch prompt or doorbell pointing to that record. Later instructions use a task-specific steering inbox. Yes, workers read outside their worktree: for Claude, firstmate explicitly grants the brief, inbox, launch record, and shared skills directories with `--add-dir`; this is a limited path grant, not a claim that the worktree contains all worker instructions. Its Claude adapter also documents a separate external-import dialog when a global `CLAUDE.md` imports a file outside the project tree.

- [bin/fm-brief.sh, lines 2-4](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-brief.sh#L2-L4): “data/<task-id>/brief.md under the active firstmate home.”
- [bin/fm-spawn.sh, lines 51-54](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-spawn.sh#L51-L54): “private launch-brief overlay, including the exact task-owned steering inbox.”
- [docs/configuration.md, lines 866-868](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L866-L868): “Every Claude launch, in both modes, also passes `--add-dir` for exactly this task's Firstmate channel directories”
- [.agents/skills/harness-adapters/references/harness/claude.md, lines 23-24](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/harness-adapters/references/harness/claude.md#L23-L24): “a loaded CLAUDE.md chain reaches outside the project tree”

## F3. Sandbox, permissions, and runtime modes

Firstmate separates workers into clean Git worktrees, but its launcher does not use Codex's approval or filesystem sandbox: the Codex command explicitly bypasses both. Claude workers default to `--dangerously-skip-permissions`, with an optional home-level `auto` mode; in either mode, the launcher grants its task-channel directories. OpenCode's launch template allows all permissions. Its environment allowlist is explicitly not a sandbox and cannot revoke same-user file access. These are firstmate's documented launch choices, not a guarantee that a worker cannot access paths outside the project.

- [docs/architecture.md, lines 280-283](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/architecture.md#L280-L283): “treehouse pools clean worktrees”
- [bin/fm-spawn.sh, lines 2155-2160](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-spawn.sh#L2155-L2160): “`--dangerously-bypass-approvals-and-sandbox`”
- [docs/configuration.md, lines 856-864](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L856-L864): “An absent file defaults to bypass”
- [bin/fm-spawn.sh, line 2162](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-spawn.sh#L2162): “`{"permission":{"*":"allow"}`”
- [docs/configuration.md, line 1048](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1048): “This is not a sandbox”

## F4. How are model and effort routed? Prose, config, or code?

The policy is a combination: natural-language `when` conditions and concrete harness/model/effort profiles are declared in JSON, firstmate judges the best matching rule, and code validates the result and launches the selected harness. The precedence is captain override, matching rule, configured default, then static harness. An optional typed resolver can classify the written brief, but firstmate retains the documented fallback and validation path.

- [docs/configuration.md, lines 1096-1100](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1096-L1100): “Firstmate chooses the best matching rule with judgment; shell scripts do not match the natural-language rules.”
- [AGENTS.md, lines 93-96](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/AGENTS.md#L93-L96): “Routing precedence is an explicit per-task captain override, then the best-fit configured rule”
- [docs/configuration.md, lines 1113-1129](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1113-L1129): “`"harness": "<adapter>", "model": "<optional model>", "effort": "<low|medium|high|xhigh|max|ultra, optional>"`”
- [docs/configuration.md, lines 1206-1209](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1206-L1209): “resolves one concrete crewmate or scout profile from a written brief”

## F5. Cost, quota, quality, and routing feedback

At each profile-array intake, firstmate reads `quota-axi` allowance and runway data, filters candidates for eligibility, task reasoning-class fit, and likely completion runway, then ranks the survivors by `spendPriority`. Measured model-quality score: not documented in the routing sources inspected ([AGENTS.md, section 4](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/AGENTS.md#L86-L108) and [quota-array-dispatch](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L39-L115)); they require qualitative reasoning-class fit. An optional pipeline-spend ledger records cost after task teardown, but the documented route uses the current quota snapshot, not that ledger.

- [.agents/skills/quota-array-dispatch/SKILL.md, lines 39-45](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L39-L45): “`spendPriority` is THE quota-perspective ranker.”
- [.agents/skills/quota-array-dispatch/SKILL.md, lines 97-105](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L97-L105): “Keep only candidates that meet the required reasoning class for this task”
- [docs/configuration.md, lines 583-587](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L583-L587): “opts this home into recording per-task no-mistakes pipeline spend”

## F6. Documented limits, risks, and failures

The documentation warns that clean worktrees and an environment filter do not enforce a filesystem sandbox, so same-user credentials and paths can remain reachable. Claude's external-import consent can block a fresh worker when an instruction chain leaves the project tree. The narrow quota helper has a documented provider-mapping error for cross-provider candidates, and malformed dispatch config blocks spawns instead of silently falling back.

- [docs/configuration.md, line 1048](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1048): “it cannot revoke same-user access to credential files”
- [.agents/skills/harness-adapters/references/harness/claude.md, lines 23-24](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/harness-adapters/references/harness/claude.md#L23-L24): “Allow external CLAUDE.md file imports?”
- [.agents/skills/quota-array-dispatch/SKILL.md, lines 29-32](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L29-L32): “a candidate whose established provider differs from that primary family is checked against the wrong quota row.”
- [docs/configuration.md, lines 1193-1200](https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1193-L1200): “malformed configuration must be reported and corrected rather than selected around.”
