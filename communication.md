# Communication rules

Read when: a project has `.agent-routing/overlay.md` and you write text for a person or an agent. Use the language and STE level in the overlay's `Communication` section. Without an overlay, apply no kit rule.

## Every reply

- **Language:** follow the overlay. `english` means write all text the user reads in English. The language of the user's message is not a request. `user` means write in the language the user uses.
- **Decisions on a selector:** put each decision on the environment's selector (`AskUserQuestion` in Claude Code and T3 Code) so the user picks without typing. Give short, distinct options. Mark the one the evidence favours as recommended, with a one-line reason. Exception: a project may put an important decision with two or more options on a decision board (`decision-boards.md`); the selector then stays for all other decisions and is the fallback.
- **Missing information or access:** name exactly what is missing and stop. Guess nothing and substitute nothing.
- **Context files** hold durable facts only. A one-off tip stays in the reply.
- **Agent-facing text** (briefs, prompts, `AGENTS.md`, `CLAUDE.md`, rule files, skills): write or revise it with the writing-for-agents skill when it is available; short routine briefs may skip it. Keep it plain, concise and task-focused.

## Writing levels

The overlay sets `ste-level` to `off`, `80` or `100`.

- `off`: apply none of the five kit writing rules or the 18 STE rules below.
- `80`: apply the five kit writing rules below. This level name does not mean 80% of the standard.
- `100`: apply the five kit writing rules and all 18 STE rules below. Apply the 18 STE rules only to English text. The limits below still apply.

The five kit writing rules are not part of ASD-STE100. The 18 STE rules keep their numbers and source labels.

Source key:

- [A] https://asd-ste100.org/STE_faq.html (ASD's own FAQ, read 2026-10-12)
- [B] https://asd-ste100.org/about_STE.html (ASD's own page, read 2026-10-12)
- [C] https://clickhelp.com/clickhelp-technical-writing-blog/what-is-simplified-technical-english/ (a tool vendor's summary, a secondary source, read 2026-10-12)
- [D] https://www.asd-ste100.org/assets/files/WhitePaper-ASD-STE100_and_AI.pdf (ASD's own white paper, June 2026)
- [E] https://asd-ste100.org/STE_downloads.html (ASD's own downloads page)
- [F] the encyclopedia page "Simplified Technical English", a secondary source, read 2026-10-12 as page text (URL and verbatim quotes: `examples/ste-source-check.md`)

Status `sourced` means an ASD page [A], [B], [D] or [E] states the rule. Status `sourced (secondary)` means only a secondary page ([C] or [F]) states it, and ASD's own text for it was not checked. Status `non verificato` means no page read states the rule. Count today: 8 sourced, 10 sourced (secondary), 0 non verificato.

| # | Rule | Source | Status |
| --- | --- | --- | --- |
| 1 | Use an approved word only with its approved meaning and part of speech. | [B] | sourced |
| 2 | Use one word for one concept, every time. The standard picks one synonym: "start", not "begin". | [A] | sourced |
| 3 | Technical nouns and technical verbs are allowed outside the dictionary: terms from official documents, glossaries and terminology databases. Define each in the project glossary. | [A] | sourced |
| 4 | Use American English spelling and word meanings. | [A] | sourced |
| 5 | Do not use an "-ing" form, except inside a technical noun or in a dictionary word that is a noun, adjective, pronoun or preposition (for example "opening", "during"). | [A] | sourced |
| 6 | Use the active voice. In a procedure, use the imperative ("Install the component."). In a description, use the passive only when the agent is unknown. | [A] | sourced |
| 7 | Put a condition the reader must know first at the start of the sentence. | [A] | sourced |
| 8 | Write short sentences. Give each sentence one idea. | [A] | sourced |
| 9 | Write at most 20 words in a procedural sentence and at most 25 in a descriptive sentence. | [C], [F] | sourced (secondary) |
| 10 | Write at most six sentences in a paragraph. | [C], [F] | sourced (secondary) |
| 11 | Do not write a multi-word noun of more than three words. | [C], [F] | sourced (secondary) |
| 12 | Give each instruction its own sentence. | [C], [F] | sourced (secondary) |
| 13 | Give each paragraph one topic. | [F] | sourced (secondary) |
| 14 | Use only these verb forms: infinitive, imperative, simple present, simple past, simple future, and the past participle as an adjective. | [F] | sourced (secondary) |
| 15 | Do not use an auxiliary verb to build a complex verb form. | [F] | sourced (secondary) |
| 16 | Do not drop the verb, the subject or the article to shorten a sentence. | [F] | sourced (secondary) |
| 17 | Use a vertical list for complex text. | [F] | sourced (secondary) |
| 18 | Start a safety instruction (a warning before a risky or irreversible action) with a clear command or condition. | [F] | sourced (secondary) |

Rules 1 to 18 apply at level `100` to each in-scope English sentence. Apply all 18 rules. Rules 9 to 18 rest on secondary pages. ASD's own wording for them is not checked; the quotes are in `examples/ste-source-check.md`. Rule 11 follows the wording of [F].

### Five kit writing rules

1. Define each term and symbol in one sentence the first time it appears.
2. Give each abstract claim one concrete example, from the user's own data where possible.
3. Write one idea per sentence. Limit procedural sentences to 20 words and descriptive sentences to 25 words. Put lists with more than three items in a vertical list. Put one action in each numbered step.
4. Use one term for one concept across replies and documents.
5. Use active voice. Prefer simple verbs ("use", "check") and precise words over vague ones ("various", "appropriate"). In English, do not write a multi-word noun of more than three words (rule 11).

## STE scope and limits

**Language.** ASD-STE100 is a controlled form of English with American spelling [A]. Rules 1 to 18 apply only to English text. The five kit writing rules can apply in the language set by the overlay.

**In scope:** replies, reports, dashboards, selector text, status messages, and documents that the user reads.

**Out of scope:**

- agent-facing text: briefs, prompts, `AGENTS.md`, `CLAUDE.md`, rule files and skills follow the writing-for-agents skill;
- code, commands, file paths, identifiers and configuration;
- quoted material: the user's verbatim request, source quotations, error output and logs;
- formulas and symbols: define each in one sentence, and keep the notation as it is;
- text that is not English, for the 18 STE rules;
- proper names, and project text that follows its own convention (commit messages and pull request text follow the project's git convention).

At level `100`, `overlay.ste-exceptions` can add categories. Each added category needs a reason in the overlay.

**What level 100 means.** Level `100` applies rules 1 to 18 to every in-scope English sentence, with none skipped. It also applies the five kit writing rules above. The level name does not mean 100% of the standard or certified text:

- The standard has 53 writing rules and a dictionary of about 900 approved words [B], [F]. The kit carries 18 rules. It does not carry the other 35, and their content is non verificato here.
- The approved dictionary (about 900 approved words and about 1200 not-approved words [B]) is part of ASD-STE100 Issue 9. ASD gives a free copy on request, as a PDF [A], [E]. This kit does not carry it, and [F] shows only four sample entries, not the list. The dictionary check is therefore not verified. An agent does not rebuild the list from memory.
- With a copy of the standard at `overlay.ste-dictionary`, read it before writing, and apply rule 1 and the rules the kit does not carry against it.
- Without a copy, apply rules 2 to 18, choose plain common words, and write "STE rules 1 to 18 applied, word list: not checked" in any document that claims a standard. Never write "STE-compliant".
- ASD states that AI cannot replace human oversight, and that plausible text must not be confused with verified compliance [D], [E]. ASD does not endorse or certify checking tools, and tools are optional [A].
- ASD says STE is meant for technical documentation and not for general-purpose writing such as correspondence, and that STE is not for spoken communication. It also says that anyone can use its principles in general documents [A]. Applying STE to user-facing text at level `100` is a project choice, made on top of the standard's stated purpose.

**Glossary at level 100.** STE allows technical nouns and technical verbs [A]. List each one in `overlay.glossary`, with one sentence of definition. These terms need an entry:

- names of tools, products, models, services and commands;
- domain terms and abbreviations of the project;
- names of files, folders, documents and records the user knows;
- the kit's own terms: route names (planner, Sol, Luna, Computer Use), closed, open, brief, gate, verifier, dispatcher. `policy.md` defines them.

Use a term from the glossary exactly as written. A term that is not in the glossary and not in the dictionary gets a one-sentence definition at first use.
