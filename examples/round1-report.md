# Round 1 report: agent routing kit

Read when: you review round 1 of the kit, or you decide the open choices O1 to O5. This file lives in `examples/` because it names the origin project; the acceptance grep allows such names only there.

## Result

The kit is drafted at `<kit-folder>/`. A git repository exists there; nothing is committed. Nothing is installed, and nothing outside the kit folder changed. I did not open `<home>/Documents/t3-porting`: the coordinator's finding (a 2026-10-06 migration snapshot, not a routing kit) was enough, and I have no reason to disagree.

## Heading count per source file

| Source file | Headings, levels 1 to 3 |
| --- | --- |
| `coordinator.md` | 13 |
| `routing-rationale.md` | 13 |
| `procedures.md` | 7 |
| `collaboration.md` | 7 |
| `collaboration-t3-code.md` | 5 |
| `collaboration-claude-projects.md` | 5 |
| `coordinator-guard/README.md` | 6 |
| Total | 56 |

I read "the seven source files" as the six rule files plus `coordinator-guard/README.md`, the only other Markdown file in the guard folder. Headings inside fenced code blocks are not counted. The table has 56 rows, one per heading; a script built it and stopped if a heading had no row.

## Inventory

| Source file and heading | Class | Disposition | Note |
| --- | --- | --- | --- |
| `coordinator.md`: # Coordinator rules | generic | policy.md (title only) | Title; the kit has its own. |
| `coordinator.md`: ## Active coordinator | Claude Projects-specific | overlay | One environment at a time is the origin setup. The idea that one coordinator controls rule changes became overlay text. |
| `coordinator.md`: ## Agents and routing | generic | policy.md | Routes, closed/open, route line, no-stall kept. Planner condition 2 became overlay.stakes. Wiki and thesis wording became overlay.records. Claude Projects clauses went to the overlay. |
| `coordinator.md`: ## Briefs, review and escalation | generic | briefs-review-escalation.md | Six-item brief, return rule, review chain, escalation kept. wiki_check became overlay.gate; the Claude Projects local-thread clause went to the overlay. |
| `coordinator.md`: ## Threads and cache cost | generic | threads-and-cache.md | Kept. The 300k rotation became overlay.rotation with the same default. |
| `coordinator.md`: ## Coordinator dashboard | generic | dashboard.md | Kept. '<user>' became 'the user'; 'supervisor' became 'a third party'. |
| `coordinator.md`: ## T3 Code: routing pilot | T3-specific | measurement.md | The pointer paragraph merged into measurement.md; the log path became overlay.measurement-log. |
| `coordinator.md`: ## Claude Projects: context | Claude Projects-specific | overlay | Project memory rules; names thesis knowledge. Example overlay holds it. |
| `coordinator.md`: ## Claude Projects: threads | Claude Projects-specific | overlay | Thread resolve, model and effort settings, 8,192-byte cut. |
| `coordinator.md`: ## Claude Projects: navigation | Claude Projects-specific | overlay | Links and review copies for a user whose files sit on one machine. |
| `coordinator.md`: ## T3 Code: delegating | T3-specific | delegation-t3.md | Targets table copied exactly. The closed/open duplicate was removed (policy.md holds it). Codex prompt folder became overlay.codex-prompts. |
| `coordinator.md`: ## T3 Code: coordinator discipline | T3-specific | delegation-t3.md | Kept. The closed/open paragraph moved to policy.md, 'Closed and open'. |
| `coordinator.md`: ## T3 Code: coordinator instance | T3-specific | guard/README.md | Tool list, Bash allowlist, read guard, removed tools, worker: now 'What the instance allows'. The script allowlist became guard.json. |
| `routing-rationale.md`: # Routing rationale | generic | rationale.md (title only) | Title. |
| `routing-rationale.md`: ## How to use | generic | rationale.md | Commit hashes and repo-line evidence kinds dropped. |
| `routing-rationale.md`: ## Routes | generic | rationale.md | Container heading for the six route entries. |
| `routing-rationale.md`: ### Planner: Opus 5.5 at xhigh | generic | rationale.md | Thesis wording generalized; commit hashes dropped; URLs kept. |
| `routing-rationale.md`: ### Sol: gpt-6-sol at medium, Standard service tier | generic | rationale.md | Commit hashes and line refs dropped; owner reasons kept. |
| `routing-rationale.md`: ### Sonnet 5.5 at high (coordinator, prose, integration, fallback) | generic | rationale.md | Fallback no longer a route; heading shortened. /tmp and hash references dropped. |
| `routing-rationale.md`: ### Haiku 5.5 at xhigh (verifier; short closed tasks in Claude Projects) | generic | rationale.md | Claude Projects became 'an environment without Codex'. |
| `routing-rationale.md`: ### Luna: gpt-6-luna at max, Standard service tier | generic | rationale.md | Screenshots and /tmp reports not carried; model-level quotes and URLs kept. |
| `routing-rationale.md`: ### Computer Use: Codex desktop automation | generic | rationale.md | Porting report evidence not carried; marked motivo non documentato beyond the observation. |
| `routing-rationale.md`: ## Rules shared by all routes | generic | rationale.md | Thread ids, commit hashes and /tmp paths dropped. Cache and measurement text moved to rationale-evidence.md. |
| `routing-rationale.md`: ## Prices and quota | generic | rationale-evidence.md | Price table kept with its fetch date. The first quota reading was project data and was dropped. |
| `routing-rationale.md`: ## Decisions not taken | generic | rationale.md | Kept. The tool-removal entry now says the guard replaced the prose rule. |
| `routing-rationale.md`: ## To confirm with the user | user-preference | rationale.md ('Open reasons') | Only the open items kept; answered items live in their route entries. |
| `procedures.md`: # Procedures | generic | dropped | Title. Each procedure went to its own file or to the overlay. |
| `procedures.md`: ## Explaining formulas and model changes | thesis-specific | overlay | Claude Docs and rendered-equation rule for a thesis. |
| `procedures.md`: ## Changing these rules | Claude Projects-specific | overlay | Steps 3 to 6 are the Claude Projects sync. Generic residue went to rationale.md 'How to use' and guard/README.md 'Changing the allowlist or denied tools'. |
| `procedures.md`: ## Moving between Claude Projects and T3 Code | Claude Projects-specific | overlay | Handoff file and checkout facts. The generic residue is policy.md 'Where work runs'. |
| `procedures.md`: ## T3-routed Sol, Luna and Computer Use | T3-specific | dropped | Restates the six-item brief, the common rules and the Computer Use approval; each already lives in one kit file. |
| `procedures.md`: ## Measuring the routing pilot | generic | measurement.md | Kept; the log path became a parameter. |
| `procedures.md`: ## Codex Computer Use prompts | generic | computer-use-prompts.md | Generic items kept. LSEG, Safari/Brave and the extraction loop went to the overlay. |
| `collaboration.md`: # Collaboration rules | generic | dropped | Title. |
| `collaboration.md`: ## Environment and role | generic | policy.md ('Role') | Role signals kept; adapter choice went to delegation-t3.md and the overlay. |
| `collaboration.md`: ## Where to read more | generic | dropped | Replaced by policy.md 'Before you act' and the README file map. |
| `collaboration.md`: ## Where knowledge lives | thesis-specific | overlay | Names wiki, questions and the data decision log. |
| `collaboration.md`: ## Talking with the user | user-preference | communication.md ('Every reply') | Language, selector, missing information, durable-facts rule kept; '<user>' became 'the user'. |
| `collaboration.md`: ## Writing | user-preference | communication.md; overlay | STE rules rewritten at 100%. Official-output style and formulas in a Claude Doc went to the overlay. |
| `collaboration.md`: ## Workflow | thesis-specific | overlay | Names the thesis wiki. |
| `collaboration-t3-code.md`: # Collaboration rules: T3 Code adapter | T3-specific | dropped | Title. |
| `collaboration-t3-code.md`: ## Role | T3-specific | delegation-t3.md ('Signals and instance') | Kept. |
| `collaboration-t3-code.md`: ## Setting | T3-specific | overlay | T3 project name, workspace and iPhone access are the user's setup. |
| `collaboration-t3-code.md`: ## Talking with the user | T3-specific | communication.md; overlay | AskUserQuestion went to communication.md; clickable path:line links to the overlay. |
| `collaboration-t3-code.md`: ## Documents | T3-specific | overlay | Claude Docs and artifacts. |
| `collaboration-claude-projects.md`: # Collaboration rules: Claude Projects adapter | Claude Projects-specific | dropped | Title. |
| `collaboration-claude-projects.md`: ## Role | Claude Projects-specific | overlay | hearthbot role signals. |
| `collaboration-claude-projects.md`: ## Setting | Claude Projects-specific | overlay | Local folder, Remote Control, 8,192-byte cut. |
| `collaboration-claude-projects.md`: ## Decisions | Claude Projects-specific | overlay | Decision cards. |
| `collaboration-claude-projects.md`: ## Documents | Claude Projects-specific | overlay | Claude Docs through local threads. |
| `coordinator-guard/README.md`: # Coordinator guard | T3-specific | guard/README.md (title and intro) | Kept. |
| `coordinator-guard/README.md`: ## Instance settings | T3-specific | guard/README.md ('Install'); guard/launch_args.py | The verbatim JSON entry is now printed by launch_args.py; the origin plugin path is a parameter. |
| `coordinator-guard/README.md`: ## Read guard decision | T3-specific | guard/README.md ('What the instance allows') | Kept; hook documentation link and live-check note dropped as origin evidence. |
| `coordinator-guard/README.md`: ## Rebuild on another machine | T3-specific | guard/README.md ('Install') | Kept as the install steps. |
| `coordinator-guard/README.md`: ## Test | T3-specific | guard/README.md ('Test'); tests/test_guard.py | Kept; six live steps unchanged. |
| `coordinator-guard/README.md`: ## Residual risks | T3-specific | guard/README.md ('Residual risks') | Kept; one risk added for a plugin folder shared by several projects. |

## Split rationale

The kit splits by trigger, so a session reads only the file its situation names. `policy.md` holds the rules that every delegating session needs (roles, closed and open, routes, route line). The next four files each match one situation: a brief or a review (`briefs-review-escalation.md`), a thread that idles (`threads-and-cache.md`), a status request (`dashboard.md`) and a delegation in T3 Code (`delegation-t3.md`). `computer-use-prompts.md` and `measurement.md` are procedures with their own trigger and their own end condition. `rationale.md` and `rationale-evidence.md` are read only when a route changes, so they stay out of every other path; the evidence file is separate because cache figures and prices are look-ups, not reasons. `communication.md` applies to every session that writes to a person, so it stands alone and has no routing text. The guard is a plugin with code, so it keeps its own folder and one README; its tests sit in `tests/` at the kit root because they test kit code. Project facts go to one overlay template, so a rule never needs a project copy. No rule appears in two kit files: `delegation-t3.md` holds the targets table and `policy.md` holds the route names, and the table says its Route column must equal them.

## Decisions I took (not reopening a fixed decision)

- Round files that name the origin project live in `examples/`, because acceptance check b allows project names only there.
- Guard config: the hooks read `<project root>/.agent-routing/guard.json`, because a global plugin cannot hold project scripts. The project root is the nearest ancestor of the session folder that holds `.agent-routing/` or `.git`. This replaces the fixed `parents[3]` of the origin hook.
- `guard/launch_args.py` is the single home of the tool lists; the README does not copy them. Its output, with the plugin path removed, is identical to the origin `launchArgs` (checked by script).
- `rationale.md` keeps every owner reason and URL, and drops hashes, thread ids and `/tmp` references. Where the dropped source was the only support, the text says "motivo non documentato" or "not carried".
- `communication.md` has a draft section for text in another language. It states the recommended option O1-A and is marked "pending the user's choice".
- Kit rules that are not STE (define terms, examples, lists above three items) stay in `communication.md`, marked as kit rules.

## What I could not generalize, and why

- **The hosted-chat adapter (Claude Projects).** It depends on derived copies built by a project script and on a 16,000-character field. It stays in the overlay. See O3.
- **The approved dictionary and the exact text of the 53 rules.** ASD gives the standard by request form only. I did not obtain it. Ten of the 18 rules in `communication.md` carry `non verificato`. See O4.
- **An STE rule set for Italian.** No ASD page I read addresses another language. The Italian text in the draft is my adaptation. See O1.
- **Sources I no longer have.** The audit of one coordinator thread, the porting report, the third-party resolver report and the launch-page screenshots are not in the kit. The quotes and numbers that came only from them are either kept as the owner's statements or marked.
- **Live guard behaviour.** The synthetic test passes, but a new T3 coordinator thread must prove that the plugin loads from the kit folder, and that a second project works. I may not touch the T3 settings in round 1.
- **Prices and cache terms** are dated 2026-10-09 and were not fetched again.
- **Test edits.** I did not change what the original checks expect. Two labels and paths now use parameters: the origin's wiki-script case became "Bash configured script" (it reads a runner from a test config), and the three repository-path cases use `GUARD_TEST_PROJECT` and `GUARD_TEST_RULE_FILE`. I added eight cases for the new config and the project-root lookup.

## Open choices

The coordinator puts these on a selector. Each has a recommendation.

### O1. What does 100% mean for text in Italian?

ASD-STE100 is a controlled form of English with American spelling ([A] in `communication.md`). The current rule lets the user be answered in Italian or English.

| Option | What it means | Effect on the user |
| --- | --- | --- |
| A (recommended) | STE applies to English text. Italian text follows the Italian equivalent drafted in `communication.md`: the structural rules (active voice, one idea per sentence, 20 and 25 word limits, one term per concept, and so on) in Italian, no word list. | The user keeps Italian replies. They get shorter sentences, no conditional or subjunctive where the indicative works, and the "si" form only when the agent is unknown. |
| B | Agents write all text the user reads in English only. Italian only when the user asks. | The user reads English in every reply, also when they write Italian. This is the only option that is STE in the strict sense. It overrides the current language rule. |
| C | STE applies to English text only. Italian text keeps today's plain-writing rules. | Smallest change. "100%" covers only English documents. Italian chat replies stay as they are today. |

Why A: it keeps the language rule, extends the same discipline to Italian, and says honestly that the dictionary part exists only in English. The Italian adaptation is mine and not verified by ASD, so the user should read one sample before approving it.

### O2. How does the kit reach every project?

| Option | Effect |
| --- | --- |
| A (recommended) | Four pointer lines in `~/.claude/CLAUDE.md` and one in `~/.codex/AGENTS.md` (`GLOBAL-DELIVERY.md`). Reaches Claude and Codex. About 130 tokens per session. |
| B | A Claude Code skill whose description is the pointer. Same footprint, Claude only. |
| C | Inline the policy in the global file. Breaks the small-footprint rule. |

### O3. How does a hosted chat that cannot read the kit folder get the kit text?

| Option | Effect |
| --- | --- |
| A (recommended) | The kit gives no hosted-chat support. The first adopting project keeps its derived copies in its own overlay until it stops using that chat. |
| B | The kit adds a script that prints a derived copy. More machinery, and it ties the kit to one chat product. |
| C | Drop the hosted chat for kit projects. This is the user's call about their tools. |

### O4. How do we check STE compliance?

| Option | Effect |
| --- | --- |
| A (recommended) | The user requests the free Issue 9 PDF from ASD ([E]) and stores it outside version control at `overlay.ste-dictionary`. Agents read it before they write. Cost to the user: one web form. Context cost of the PDF: not measured. |
| B | A: and a Haiku xhigh verifier checks each official document against the PDF. More cost; fits the verifier rule. |
| C | Neither. Agents apply rules 2 to 18, and write "STE rules applied, dictionary not checked". |

### O5. How much of `communication.md` does each session read?

| Option | Effect |
| --- | --- |
| A (recommended) | One file, about 2,100 tokens, read once per session. One home for the rules and their sources. |
| B | A short core (about 700 tokens) plus a sources file. Cuts the load, and splits rules from their proof. |

## Acceptance evidence

### a. Inventory

56 rows for 56 headings. Counts per file are in the table at the top of this report.

### b. Boundary grep

Command: `grep -rniE "thesis|wiki|<user>|lseg|proposal|supervisor" <kit-folder> --include=*.md --include=*.py --include=*.json`

Result: all matches are inside `examples/`. Lines per file, counted before this report file was written (this report names the same words, inside `examples/` too):

```
  1 examples/ste-source-check.md
```

Matches outside `examples/`: 0 (the re-run after writing this report gives the same result).

### c. Guard tests

Command, from the kit root: `python3 -I tests/test_guard.py`. The script prints the full command line of each case; the paths below are shortened to the hook name.

```
PASS | Read small project rule | coordinator-read-guard.py | exit 0 (expected 0)
PASS | Read tool-results | coordinator-read-guard.py | exit 2 (expected 2)
PASS | Read symlink to tool-results | coordinator-read-guard.py | exit 2 (expected 2)
PASS | Grep tool-results | coordinator-read-guard.py | exit 2 (expected 2)
PASS | Glob tool-results | coordinator-read-guard.py | exit 2 (expected 2)
PASS | Grep project | coordinator-read-guard.py | exit 0 (expected 0)
PASS | Glob project | coordinator-read-guard.py | exit 0 (expected 0)
PASS | Read large external | coordinator-read-guard.py | exit 2 (expected 2)
PASS | thread messages short | coordinator-read-guard.py | exit 0 (expected 0)
PASS | thread activity 100 | coordinator-read-guard.py | exit 2 (expected 2)
PASS | thread excessive chars | coordinator-read-guard.py | exit 2 (expected 2)
PASS | thread unbounded | coordinator-read-guard.py | exit 2 (expected 2)
PASS | thread long item | coordinator-read-guard.py | exit 2 (expected 2)
PASS | Bash git status | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash git log | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash git diff | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash git add | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash git commit | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash configured script | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash readonly | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash python -c | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash curl | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash redirect | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash substitution | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash newline | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash background | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash bad commit | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | malformed JSON | coordinator-read-guard.py | exit 2 (expected 2)
PASS | Bash malformed JSON | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash script not in config | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash runner without script | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash joined configured script | coordinator-bash-guard.py | exit 0 (expected 0)
PASS | Bash joined unlisted script | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash script with absent config | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Bash script with unreadable config | coordinator-bash-guard.py | exit 2 (expected 2)
PASS | Read large file inside project, cwd in subfolder | coordinator-read-guard.py | exit 0 (expected 0)
PASS | Read large file outside project, cwd in subfolder | coordinator-read-guard.py | exit 2 (expected 2)
37/37 passed
exit=0
```

### d. Em dash

A recursive `grep -rIn` for the em dash character over the kit (the `.git` folder excluded) finds 0 lines.

### e. The other repository

`git -C <home>/Documents/Dev/llm-wiki status --short` is identical to the list at the start (12 lines: the five modified and seven untracked paths named in the brief). I ran no `git add` or `git commit` there.

### f. Routes, side by side

| Route | `coordinator.md` "Agents and routing" | `coordinator.md` "T3 Code: delegating" | Kit `policy.md` | Kit `delegation-t3.md` |
| --- | --- | --- | --- | --- |
| Coordinator | Claude Sonnet 5.5 at high | `claudeAgent_claude_coordinator`, `claude-sonnet-5-5`, `effort: high` | Claude Sonnet 5.5 at high | `claudeAgent_claude_coordinator`, `claude-sonnet-5-5`, `effort: high` |
| Planner | Opus xhigh | `claudeAgent`, `claude-opus-5-5`, `effort: xhigh` | Opus xhigh | `claudeAgent`, `claude-opus-5-5`, `effort: xhigh` |
| Sol | Sol medium | `codex`, `gpt-6-sol`, `reasoningEffort: medium`, `serviceTier: default` | Sol medium | `codex`, `gpt-6-sol`, `reasoningEffort: medium`, `serviceTier: default` |
| Sonnet | Sonnet high | `claudeAgent`, `claude-sonnet-5-5`, `effort: high` | Sonnet high | `claudeAgent`, `claude-sonnet-5-5`, `effort: high` |
| Haiku | Haiku xhigh (Claude Haiku 5.5) | `claudeAgent`, `claude-haiku-5-5`, `effort: xhigh` | Haiku xhigh (Claude Haiku 5.5) | `claudeAgent`, `claude-haiku-5-5`, `effort: xhigh` |
| Luna | Luna max | `codex`, `gpt-6-luna`, `reasoningEffort: max`, `serviceTier: default` | Luna max | `codex`, `gpt-6-luna`, `reasoningEffort: max`, `serviceTier: default` |
| Computer Use | `~/.codex/config.toml` | `codex`, from `~/.codex/config.toml`, `model_reasoning_effort`, `service_tier` | Codex config file `~/.codex/config.toml` | `codex`, from `~/.codex/config.toml`, `model_reasoning_effort`, `service_tier` |

The seven table rows (header plus six routes) of the two files are byte-identical; I checked them with `diff`.

### g. STE rules in `communication.md`

18 rules in the table. 8 are `sourced` (rules 1 to 8, each stated on an ASD page). 10 carry the mark `non verificato` (rules 9 to 18): four of them also name a secondary URL, six have no source. The mark is spelled exactly `non verificato`. Other `non verificato` items: the dictionary content, any ASD statement on other languages. Evidence per URL: `examples/ste-source-check.md`.

## Decisions

The user decided O1 to O5 on 2026-10-12. The options above stay as asked in round 1. Round 2 applied the decisions (`examples/round2-report.md`).

| Choice | Decision | Where applied |
| --- | --- | --- |
| O1 | Option B: agents write all text the user reads in English only, and another language only when the user asks. The Italian-equivalent draft was removed. | `communication.md`, "Every reply" and "STE scope and limits" |
| O2 | Option A in a changed form, called "global kit with targeted access": the kit is global, the pointer lines are plain text with no `@` import, and access to the kit is by exact path. | `GLOBAL-DELIVERY.md`, sections 1 to 4 |
| O3 | Option A: the kit gives no support for hosted chats such as Claude Projects. A project that uses such a chat keeps its own copies. | (removed from the public copy) |
| O4 | None of A, B, C. The user gave a starting source: the Wikipedia page "Simplified Technical English". Round 2 checked the 10 `non verificato` rules against it. | `communication.md`, `examples/ste-source-check.md` |
| O5 | Option A: `communication.md` stays one file. | `communication.md` |
