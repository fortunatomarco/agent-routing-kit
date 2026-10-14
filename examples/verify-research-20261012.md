# Citation verification - research-t3-docs-20261012.md and research-firstmate-20261012.md

Verifier: review sub-agent, 2026-10-12. Read-only except this file. The two reports were not edited.

## Method

- Sources fetched in this session:
  - t3code: `raw.githubusercontent.com/pingdotgg/t3code/main/<path>` for 12 files, copies in `/tmp/verify-t3-T5lObz`.
  - firstmate: `raw.githubusercontent.com/kunchenguid/firstmate/a1ecefb43086401f4a6243d6ccebf72969211c84/<path>` for 8 files, copies in `/tmp/verify-fm-RXIYhu`. The raw fetch at that commit also confirms the commit exists.
  - Bare repo and same-name repos: fetched as GitHub HTML pages.
- Each cited line range was printed and compared with the quote.
- Judged only: (a) quote present at the cited lines, (b) quote supports the sentence it is attached to.
- Formatting differences were not counted as changed words: markdown bold and link markup, table pipes, line wraps, comment prefixes, and TypeScript `as const`. Every quote was found with its words unchanged.
- No t3code quote moved: all were present at the cited lines on `main`, so no "present-lines-moved" rows.
- Rows 1-25 are t3code. Rows 26-55 are firstmate.

## Citation table

| # | Report | Q | URL | Result | Note |
|---|---|---|---|---|---|
| 1 | t3 | Q1 | https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md#L11-L16 | pass | Lines 13 and 16 hold both quotes. |
| 2 | t3 | Q1 | https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md#L14-L15 | pass | Lines 14 and 15. |
| 3 | t3 | Q1 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts#L664-L700 | pass | Lines 672, 675, 683, 691, 699. Mapping matches the sentence. |
| 4 | t3 | Q1 | https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md#L21-L25 | pass | Line 23. |
| 5 | t3 | Q2 | https://github.com/pingdotgg/t3code/blob/main/docs/internals/providers.md#L3-L6 | pass | Lines 3-5, link markup stripped. |
| 6 | t3 | Q2 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts#L664-L700 | pass | Lines 665-667 and 672-699. |
| 7 | t3 | Q2 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts#L779-L792 | pass | Lines 783, 790, 792. The "explicit" wording also needs lines 720-727, outside this range: both policies come from `runtimeModeDefaults` unless overridden. |
| 8 | t3 | Q2 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1698-L1707 | pass | Lines 1700, 1702, 1706 are quoted. Line 1704 returns "auto", which the quote list omits but the sentence needs. |
| 9 | t3 | Q2 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1721-L1752 | pass | Lines 1722, 1732, 1751. |
| 10 | t3 | Q3 | https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/providerInstance.ts#L124-L131 | pass | Lines 128 and 130. The type behind `environment` is outside the range, so "variables" is not shown. |
| 11 | t3 | Q3 | https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/settings.ts#L635-L640 | pass | Line 639, Codex settings block. |
| 12 | t3 | Q3 | https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/settings.ts#L684-L689 | pass | Line 688, inside `ClaudeSettings` (starts at line 658), so the Claude claim holds. |
| 13 | t3 | Q3 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1059-L1067 | pass | Lines 1059, 1061-1063. The label also cites 975-979; `extraArgs` (978) and `parseCliArgs` (979) are there. |
| 14 | t3 | Q3 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/provider/codexLaunchArgs.ts#L12-L15 | pass | Lines 13-14 split across two lines in source; words identical. |
| 15 | t3 | Q4 | https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/orchestrator-mcp-server.md#L210-L245 | pass | Lines 233-234, wrapped. |
| 16 | t3 | Q4 | https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/orchestrator-mcp-server.md#L240-L245 | pass | Lines 244-245, wrapped. |
| 17 | t3 | Q4 | https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/orchestrator-mcp-server.md#L460-L463 | pass | Lines 460-461, wrapped. |
| 18 | t3 | Q5 | https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-claude.md#L1-L5 | pass | Line 3. |
| 19 | t3 | Q5 | https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-claude.md#L68-L72 | pass | Lines 70-71, wrapped. |
| 20 | t3 | Q5 | https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-codex.md#L22-L26 | pass | Line 24. |
| 21 | t3 | Q5 | https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-codex.md#L34-L38 | pass | Lines 37-38 hold the quote. Line 36 ("A shared Codex home") supports "share a Codex home". |
| 22 | t3 | Q5 | https://github.com/pingdotgg/t3code/blob/main/apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts#L1052-L1057 | pass | Lines 1052-1054. Quote drops the two `as const` casts and joins lines. |
| 23 | t3 | Q6 | https://github.com/pingdotgg/t3code/blob/main/docs/internals/environment-auth.md#L103-L109 | pass | Lines 105-107, wrapped. |
| 24 | t3 | Q6 | https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md#L286-L288 | pass | Line 288. Does not say "separate from the provider sandbox"; see untied list. |
| 25 | t3 | Q6 | https://github.com/pingdotgg/t3code/blob/main/docs/internals/providers.md#L132-L138 | pass | Lines 137-138. The sentence sits in the Attachments section; the report generalises it. |
| 26 | fm | header | https://github.com/kunchenguid/firstmate | pass | Repo page returns HTTP 200. Pinned commit exists (raw files fetched at a1ecefb). |
| 27 | fm | header | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/LICENSE#L1-L3 | pass | Line 1 "MIT License"; line 3 "Copyright (c) 2026 Kun Chen". |
| 28 | fm | header | https://github.com/Coditan/firstmate | pass | Page returns 200, title "GitHub - Coditan/firstmate". Surfacing in search is not checkable. |
| 29 | fm | header | https://github.com/pandanax/firstmate | pass | Page returns 200, title "GitHub - pandanax/firstmate". Surfacing in search is not checkable. |
| 30 | fm | F1 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L18-L29 | pass | Line 20. |
| 31 | fm | F1 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1096-L1100 | pass | Line 1098. |
| 32 | fm | F1 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/AGENTS.md#L148-L153 | pass | Line 150. "Not the fleet routing policy" is inferred. |
| 33 | fm | F1 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1202-L1204 | pass | Line 1204. |
| 34 | fm | F2 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-brief.sh#L2-L4 | pass | Line 3, comment prefix dropped. |
| 35 | fm | F2 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-spawn.sh#L51-L54 | pass | Lines 52-53, wrapped with comment prefix. |
| 36 | fm | F2 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L866-L868 | pass | Line 866 lists the four directories; line 868 says the grant never covers anything wider. |
| 37 | fm | F2 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/harness-adapters/references/harness/claude.md#L23-L24 | pass | Line 23. |
| 38 | fm | F3 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/architecture.md#L280-L283 | pass | Line 282, link markup stripped. |
| 39 | fm | F3 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-spawn.sh#L2155-L2160 | pass | Lines 2157 and 2159. |
| 40 | fm | F3 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L856-L864 | pass | Lines 858, 859, 861, 864. |
| 41 | fm | F3 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/bin/fm-spawn.sh#L2162 | pass | Line 2162 holds the fragment. |
| 42 | fm | F3 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1048 | pass | Line 1048. "This" refers to the launch-env allowlist section (from line 990). |
| 43 | fm | F4 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1096-L1100 | pass | Line 1099. |
| 44 | fm | F4 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/AGENTS.md#L93-L96 | pass | Line 95. |
| 45 | fm | F4 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1113-L1129 | pass | Line 1122 holds the fragment inside a longer object. |
| 46 | fm | F4 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1206-L1209 | pass | Line 1208. The "fallback" wording is not in this range; see untied list. |
| 47 | fm | F5 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L39-L45 | pass | Line 45. |
| 48 | fm | F5 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L97-L105 | pass | Line 99. The eligibility gate is at lines 64-86, outside this range. |
| 49 | fm | F5 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L583-L587 | pass | Line 585. |
| 50 | fm | F5 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/AGENTS.md#L86-L108 | pass | Inline citation. Negative claim: "quality" does not appear in AGENTS.md, docs/configuration.md or SKILL.md (grep of the fetched copies). |
| 51 | fm | F5 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L39-L115 | pass | Inline citation. Lines 41, 67 and 112-115 support one snapshot per intake and spendPriority as the ranker. |
| 52 | fm | F6 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1048 | pass | Line 1048. Covers the env filter, not clean worktrees; see untied list. |
| 53 | fm | F6 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/harness-adapters/references/harness/claude.md#L23-L24 | pass | Line 23 holds the quote; line 24 covers the gating. |
| 54 | fm | F6 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/.agents/skills/quota-array-dispatch/SKILL.md#L29-L32 | pass | Line 30. The source says "known limitation"; the report calls it an "error". |
| 55 | fm | F6 | https://github.com/kunchenguid/firstmate/blob/a1ecefb43086401f4a6243d6ccebf72969211c84/docs/configuration.md#L1193-L1200 | pass | Line 1200. |

## Summary

Counts (55 citations):

- pass: 55 (t3: 25, firstmate: 30)
- present-lines-moved: 0
- fail: 0
- unreachable: 0

No non-pass rows, so no quotes of source text are needed here.

## Claims in the report text not tied to any citation

Absence claims ("not documented") cannot be quoted. They are listed so the coordinator can decide.

t3code report:

1. Q1: "not documented: an exhaustive inside/outside workspace matrix for file reads, writes, shell commands, and network in each mode." Absence claim, no citation.
2. Q2: "These are distinct provider mechanisms, and the T3 documentation does not state that they yield identical filesystem boundaries." Absence claim, no citation.
3. Q3: "not documented: a T3-supported provider-instance setting or `add-dir` recipe that guarantees an arbitrary extra path is readable or writable under a given mode." Absence claim, no citation.
4. Q3: "The cited code shows configuration channels, not an access grant for the proposed shared folder." Judgement. Consistent with rows 10-14, but not itself cited.
5. Q3: "T3 exposes instance environment variables." Partly tied (row 10). The type behind `environment` is outside the cited range.
6. Q4: "It does not specify a separately inherited filesystem sandbox object; the selected child provider applies its own runtime mode and policy." Absence claim. The "own runtime mode and policy" part is only indirectly supported by row 16.
7. Q5: "not documented: T3 itself loading `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or following links from either file to a shared folder." Absence claim, no citation.
8. Q5: "the cited T3 docs and code do not describe the provider's instruction-file discovery rules." Absence claim, no citation.
9. Q6: "This client scope is separate from an agent's provider sandbox." Partly tied (row 24). Row 24 says the scopes control direct client file access. The word "separate" is inferred, not stated.

firstmate report:

10. Header: "surfaced in search" for Coditan/firstmate and pandanax/firstmate. Existence is verified (rows 28-29); the search step is not checkable.
11. F1: "shared supervisor instructions live in its tracked `AGENTS.md`." The file exists at the pinned commit, but no F1 citation says it holds the supervisor instructions.
12. F2: "sends the worker a launch prompt or doorbell pointing to that record." No cited range covers a doorbell. The doorbell is documented, uncited, at `docs/configuration.md:782` and `bin/fm-brief.sh:370-374`.
13. F3: "These are firstmate's documented launch choices, not a guarantee that a worker cannot access paths outside the project." Inference, no citation. The hedge is appropriate.
14. F4: "firstmate retains the documented fallback and validation path." The fallback wording is at `AGENTS.md:106`, inside the 86-108 range cited only in F5 (row 50), not in F4.
15. F5: "Measured model-quality score: not documented in the routing sources inspected." Absence claim. Tied by silence in the cited ranges (row 50).
16. F6: "The documentation warns that clean worktrees and an environment filter do not enforce a filesystem sandbox, so same-user credentials and paths can remain reachable." Only the environment-filter half is cited (row 52). No cited range covers clean worktrees. Line 1048 names credential files, not "paths".
