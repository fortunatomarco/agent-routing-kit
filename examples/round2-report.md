# Round 2 report: agent routing kit

Read when: you review round 2 or start round 3. This file lives in `examples/` because it names the origin project. Date: 2026-10-12. Nothing is installed or committed; the kit folder and two memory files changed.

## Result

Decisions O1 to O5 are applied. The access probe is recorded. Route table, models and efforts are unchanged: no route file was touched (`policy.md`, `delegation-t3.md`, `rationale.md` keep their round 1 modification times).

## What changed per file

| File | Change |
| --- | --- |
| `communication.md` | O1: Language rule is English only; the "Text in another language" draft is deleted; "STE scope and limits" gains a Language paragraph and an out-of-scope line. O4: source [F] added; rules 9 to 18 now `sourced (secondary)`; rule 11 reworded to the source's wording; the limits section says the standard has 53 rules and the kit carries 18, and the rule text says "word list: not checked". |
| `examples/ste-source-check.md` | New section "Round 2: Wikipedia check": one row per rule 9 to 18 with the verbatim quote; word-list finding; new count. |
| `GLOBAL-DELIVERY.md` | Rewritten for O2 and O3: plain-text pointer lines for both providers; "Access and sandbox" with the probe table; protection plan (OS lock, then untested deny rule); `--add-dir` (untested, with citations); coordinator read guard and file size; round 3 test protocol (14 items); adopting-project changes; hosted-chat line. |
| `examples/probe-results-20261012.md` | New: probe table, thread configuration confirmation, facts, limits. |
| `examples/round1-report.md` | Section "Decisions" appended; the options are not rewritten. |
| `overlay-template.md` | Removed `overlay.languages` and `overlay.file-language` (the language rule is fixed); `overlay.ste-dictionary` now names the whole standard. |
| `README.md` | Round and file-map wording updated. |
| Memory folder | `feedback-explain-in-a-message-not-a-selector.md` created; one line appended to `MEMORY.md` (4 lines in total). No existing memory covered it. |

## STE check: counts

| | Round 1 | Round 2 |
| --- | --- | --- |
| sourced (ASD page) | 8 | 8 |
| sourced (secondary) | 0 | 10 |
| non verificato | 10 | 0 |

All 10 rules were on the page, each with a quote under 25 words, checked verbatim against the fetched page text (script run: all quotes found). The page does not carry the approved word list: it shows four sample entries. The word-list check stays unverified.

Three findings to read:

1. The standard has 53 writing rules (stated on the ASD About page [B] and on the secondary page [F]). The kit carries 18. "100%" therefore means 100% of the kit's 18 rules. `communication.md` says so. If the user wants rules 19 to 53, the user needs the Issue 9 PDF.
2. The page carries two maintenance banners dated September 2026 ("Tone", "cleanup MOS"). A secondary source with banners is weaker than an ASD page.
3. Rule 11 was "at most three nouns in a row". The page says "Do not write multi-word nouns that have more than three words." The rule now follows the page.

## Check outputs

1. Guard test: `python3 -I tests/test_guard.py` printed `37/37 passed`, exit code 0.
2. Banned-word grep (`thesis|wiki|<user>|lseg|proposal|supervisor`, case-insensitive) outside `examples/`: no match, after one fix in `STATE.md`.
3. Em dash in the kit and in the two memory files: none.
4. `grep -n "^@" GLOBAL-DELIVERY.md`: no line. The two pointer blocks contain no `@`.
5. `communication.md`: no Italian text; `grep -c "non verificato |"` on the table: 0.
6. `git -C <home>/Documents/Dev/llm-wiki status --short`: the same 12 entries as at the start (5 modified, 7 untracked, listed in the brief); nothing new.
7. Lock test on a temporary copy of the kit (not the kit): append and `touch` refused; guard test `37/37 passed` with the copy locked; the copy was unlocked and deleted.
8. Largest kit file: `rationale.md`, 25,041 bytes, below the 64 KiB (65,536) read-guard limit.

## Deviations and open points

- **Conflict between two acceptance rules.** Acceptance (b) bans the string "wiki" outside `examples/`, and the page name and URL contain it. `communication.md` therefore says `sourced (secondary)` with key [F] ("the encyclopedia page"), and the URL and the label "Wikipedia" are in `examples/ste-source-check.md`. If the URL should be inside `communication.md`, the grep must exempt that file.
- **Home-manager links.** `~/.claude/CLAUDE.md`, `~/.claude/settings.json` and `~/.codex/AGENTS.md` are symlinks into a read-only `/nix/store` path. Round 3 must find their source files first. Not in the brief; found with `ls -l`.
- **Probe thread ids** were not in the brief, so `probe-results-20261012.md` records the configuration confirmation without ids, for three of four threads.
- **Deny-rule syntax** and `--add-dir` behaviour are `non verificato`; both are round 3 test items.
