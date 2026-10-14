# STE source check (round 1 evidence)

Read when: you need to know what was verified for the rules in `communication.md`, and where. All pages were read on 2026-10-12 with `curl` and a text stripper; the pages are public.

## Official ASD pages

| URL | What it states (used in `communication.md`) |
| --- | --- |
| https://asd-ste100.org/about_STE.html | Current version is Issue 9, January 2025. The standard has a set of writing rules and a controlled dictionary. "In general, each word has only one meaning and is approved with only one part of speech." 53 writing rules in 9 sections. About 900 approved words and about 1200 not-approved words. STE permits company or project terms that are not in the dictionary (technical nouns and technical verbs). ASD owns the copyright. |
| https://asd-ste100.org/STE_faq.html | STE is a controlled natural language; approved meanings and spelling follow American English and Merriam-Webster. STE picks one synonym ("start", not "begin"). Passive only in descriptions when the agent is unknown; procedures use the imperative. "-ing" forms are usually not permitted, except as technical nouns or dictionary words that are nouns, adjectives, pronouns or prepositions. A condition the reader must know first goes at the start of the sentence. Technical nouns and verbs may contain unapproved terms when they come from official documents, glossaries or terminology databases. STE "is not intended for general-purpose writing, such as international correspondence", but "short sentences, one topic per sentence, and the use of the active voice" can be applied elsewhere. "Can STE be used for oral communication? No." Checking tools are optional and not endorsed. The standard is free; the only format is PDF, on request. |
| https://asd-ste100.org/STE_downloads.html | Issue 9 is available by request form. "Plausibility must not be confused with verified compliance." |
| https://www.asd-ste100.org/assets/files/WhitePaper-ASD-STE100_and_AI.pdf | June 2026 white paper: AI tools "can support STE-compliant writing and translation but cannot replace human oversight"; responsibility remains with the human author. |

## Not obtained

- The text of ASD-STE100 Issue 9 itself, and its dictionary: only available by request form. Not read. Everything about the exact wording of the 53 rules and about dictionary entries is non verificato.
- The Issue 7 PDF named by a secondary page (`robertobertuol.com/.../ASD-STE100-ISSUE-7.pdf`) returned an HTML page, not a PDF. Not used.
- Any ASD statement on languages other than English: none found on the About, FAQ or Downloads pages (non verificato).
- Whether the kit may redistribute the standard: non verificato; ASD owns the copyright.

## Secondary sources

| URL | Used for |
| --- | --- |
| https://clickhelp.com/clickhelp-technical-writing-blog/what-is-simplified-technical-english/ | 20 words in a procedural sentence and 25 in a descriptive sentence ("recommended maximum"), at most six sentences in a paragraph, at most three nouns in a row, one instruction or topic per sentence. A tool vendor's blog. Rules 9 to 12 in `communication.md` now also cite the Wikipedia page below. |
| https://en.wikipedia.org/wiki/Simplified_Technical_English | Round 1 listed this page from a search result and did not read it in full. Round 2 read it in full: see "Round 2: Wikipedia check" below. |

## Round 2: Wikipedia check (2026-10-12)

Source: https://en.wikipedia.org/wiki/Simplified_Technical_English, a secondary source, key [F] in `communication.md`. Method: the full page text was fetched as wikitext (`action=raw`, 22,150 bytes) with `curl`, saved in a new folder outside the kit, and read in full. Each quote below is verbatim from that text. The wording of the table rules in `communication.md` was compared with the quote.

Caveats on the page:

- It carries two maintenance banners dated September 2026: "Tone" and "cleanup MOS".
- It calls its list of writing rules "A non-exhaustive list of the writing rules".
- It states the current edition: "published in January 2025, consists of 53 writing rules and a dictionary of approximately 900 approved words".
- Its lead sentence for the verb rule reads "Use the approved forms of the verb to make only:" and a bullet list follows.

| # | Rule in `communication.md` | Quote from the page (verbatim) | Result |
| --- | --- | --- | --- |
| 9 | At most 20 words in a procedural sentence, 25 in a descriptive sentence | "Write short sentences: no more than 20 words in instructions (procedures) and 25 words in descriptive texts." | sourced (secondary) |
| 10 | At most six sentences in a paragraph | "Do not write more than six sentences in each paragraph." | sourced (secondary) |
| 11 | Multi-word noun limit | "Do not write multi-word nouns that have more than three words." | sourced (secondary); round 1 worded the rule "at most three nouns in a row", changed to the page's wording |
| 12 | One instruction per sentence | "Write one instruction per sentence." | sourced (secondary) |
| 13 | One topic per paragraph | "Write only one topic per paragraph." | sourced (secondary) |
| 14 | Allowed verb forms | "Use the approved forms of the verb to make only:" then the bullets infinitive, imperative, simple present, simple past, simple future, "The past participle (only as an adjective)" | sourced (secondary) |
| 15 | No auxiliary verb for a complex verb form | "Do not use auxiliary verbs to make complex verb constructions." | sourced (secondary) |
| 16 | Do not drop verb, subject or article | "Do not omit parts of the sentence (e.g. verb, subject, article) to make the text shorter." | sourced (secondary) |
| 17 | Vertical list for complex text | "Use vertical lists for complex text." | sourced (secondary) |
| 18 | Safety instruction starts with a command or condition | "Start safety instructions with a clear command or condition." | sourced (secondary) |

Result: 10 of 10 rules found on the page. The page does not state which rule numbers of the standard these are; it gives no rule numbers except "writing rules 1.5 and 1.12" for technical nouns and verbs.

**Approved word list (Issue 9).** The page does not carry it. It shows an extract of four dictionary entries (acceptance, access, accessible, accident) and says the dictionary has "approximately 900 approved words". The dictionary check stays unverified. The rule text in `communication.md` says "word list: not checked".

**Rules 1 to 8 on the same page.** The page also states rules 1 (approved word, part of speech and meaning), 5 (the "-ing" form), 6 (active voice; passive "only when the agent is unknown") and 3 (technical nouns and verbs, "writing rules 1.5 and 1.12"). Those rules already rest on ASD pages and keep their status.

**Other page facts used.**

- "Although it was not initially intended for use as a general writing standard, it has been successfully adopted by other industries": supports the remark in `communication.md` that applying STE to every reply is a project choice.
- ASD front-matter disclaimer quoted on the page: "Can STE be used alone? No." The page says STE needs other style guides and professional skill. The kit keeps the writing-for-agents skill for agent-facing text.

## Count in `communication.md` (after round 2)

18 rules in the table: 8 `sourced` (rules 1 to 8, each on an ASD page), 10 `sourced (secondary)` (rules 9 to 18, each found on the page above; rules 9 to 12 also on the vendor blog), 0 `non verificato`. Round 1 count was 8 and 10. The limits section keeps these `non verificato` items: the dictionary content, the 35 writing rules the kit does not carry (53 in the standard, 18 in the kit), whether the kit may redistribute the standard. "Other languages" is closed by decision O1: the kit rule is English only.
