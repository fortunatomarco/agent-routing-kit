# Routing evidence: cache and prices

Read when: you question a cache period, a thread-reuse rule or a cost comparison, or you update a price. `rationale.md` links here. Facts below were fetched or measured on the dates shown; prices and cache terms change, so re-fetch before you rely on them.
Reader: maintainer.

## Cache

`threads-and-cache.md` says the cache goes cold after about 60 idle minutes on Claude and about 30 on GPT-5.6 and later. Where these two figures came from: reason not documented; nobody recorded their source. They now have an official check (pages read 2026-10-09):

- Claude API: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." A 1-hour TTL is an opt-in "at 2x the base input token price" (https://platform.claude.com/docs/en/build-with-claude/prompt-caching; 100,000 of 160,149 characters read).
- Claude Code on a subscription: "Unless you choose a TTL yourself, Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage. There it requests the hour for the main conversation". "Subagents fall outside the main-conversation TTL bucket, so they get five minutes even on a subscription." Over the plan limit, "Claude Code drops the main conversation to the five-minute TTL" (https://code.claude.com/docs/en/prompt-caching, "Cache lifetime" and "Which TTL each request gets"). The page says "one-hour TTL"; "about 60 idle minutes" is our paraphrase.
- OpenAI API, GPT-5.6 and later: "The only supported value, `30m`, is also the default." The cache lifetime is "At least 30 minutes after the latest write or reuse" (https://developers.openai.com/api/docs/guides/prompt-caching). So 30 is a minimum, not a hard expiry.
- No official statement found for Codex on a ChatGPT plan; the only difference found is billing ("Codex credit billing has no separate cache-write charge", https://learn.chatgpt.com/docs/pricing). No page places Sol and Luna in the 30-minute rule by name; that is an inference from version order.

Measurements taken on the maintainer's setup, dated where the test was run:

- Method: Claude Code session logs record, per request, `cache_creation.ephemeral_5m_input_tokens` and `ephemeral_1h_input_tokens`; sessions were mapped to T3 threads through the T3 database; usage numbers only, no conversation content.
- Coordinator thread (its provider instance, Sonnet 5.5): every cache write was at the 1-hour TTL and none at 5 minutes. After idle gaps it read most of its prefix from the cache and created little new cache.
- T3 delegated workers (`delegate_task`, instance `claudeAgent`; Sonnet 5.5 and Haiku 5.5 sessions): every cache write was at the 1-hour TTL and none at 5 minutes. They are separate top-level Claude sessions, not native subagents, so they get the main-conversation TTL. A probe on one Haiku worker found the cache still warm after a gap of about seven minutes.
- Contrast: one native `Task` subagent wrote only at 5 minutes and nothing at 1 hour, matching the official docs above.
- A gap test on one Codex worker found no cache miss at gaps up to 35 minutes; the 5-minute-miss claim did not hold in that run. Limits: one run, one account, interactive, plan-usage state and Fast tier not tested.
- Limits of the Claude measurement: the log field records the TTL requested at write time; the probe does not test the full hour, and a 65-minute test was not run; the warm-read probe covers Haiku only, and Sonnet workers have the write flag but no idle gap in their logs; the result holds within plan usage and may change when plan usage runs out or with API-key use.

Result: the 60-minute figure is right for the Claude Code main conversation on a subscription within plan usage, and the 30-minute figure as an OpenAI minimum. Both are wrong for the Claude API default and for Claude native subagents. A T3 delegated worker counts as a main conversation (1 hour). Sol and API-key use on the OpenAI side are not measured. This is recorded here only; `threads-and-cache.md` is unchanged.

**Would change if:** plan usage runs out; T3 changes how it starts Claude sessions; or a 65-minute test shows expiry before one hour.

## Prices

USD prices per 1M tokens, re-verified 2026-10-18 on official pages only. OpenAI rows use Standard processing for prompts up to 272K input tokens. Claude rows use standard global pricing. Source IDs below resolve to URLs and fetch dates; exact numerical quotes and locators are in the maintainer's working notes, which this repository does not carry.

| Model | Input | Cache read | Cache write | Output |
| --- | --- | --- | --- | --- |
| Claude Sonnet 5.5 [A] | $2 | $0.10 | $2.50 (5 min); $4 (1 hour) | $10 |
| Claude Opus 5.5 [A] | $4 | $0.20 | $5 (5 min); $8 (1 hour) | $20 |
| Claude Haiku 5.5, prompt up to 100K [A, B] | $0.10 | $0.01 | $0.125 (5 min); $0.20 (1 hour) | $0.50 |
| Claude Haiku 5.5, prompt above 100K [A, B] | $0.50 | $0.05 | $0.625 (5 min); $1 (1 hour) | $2.50 |
| Claude Fable 5.1 [A] | $10 | $0.25 | $12.50 (5 min); $20 (1 hour) | $50 |
| Claude Opus 5 [A] | $5 | $0.50 | $6.25 (5 min); $10 (1 hour) | $25 |
| gpt-6-luna [F] | $0.10 | $0.01 | $0.125 | $0.50 |
| gpt-6-sol [E] | $2.00 | $0.20 | $2.50 | $10.00 |
| gpt-6-astra [G] | $10 | $1 | $12.50 | $50 |
| gpt-6.1-sol [D] | $2.00 | $0.10 | $2.50 | $10.00 |
| gpt-5.6-sol [C, H] | $4 | $0.40 | $5 | $20 |
| gpt-5.6-terra [I] | $2 | $0.20 | $2.50 (derived from published 1.25x write multiplier) | $12 |
| gpt-5.6-luna [J] | $0.20 | $0.02 | $0.25 (derived from published 1.25x write multiplier) | $1.20 |

- Codex on a ChatGPT plan runs on a plan allowance, not per token. Read the OpenAI rows as a relative comparison only.
- API modifiers: GPT-6.1 Sol, GPT-6 Sol, GPT-6 Luna and GPT-6 Astra charge 2x input and cache rates and 1.5x output for the full request above 272K input tokens [D-G]. The GPT-5.6 model pages state 2x input and 1.5x output above 272K [H-J]. Fast is 2x Standard for the GPT-6 models [D-G] and GPT-5.6 Sol [M]. An explicit Fast API multiplier for GPT-5.6 Terra or Luna is not published on https://developers.openai.com/api/docs/guides/fast-mode or their model pages checked. Batch and Flex are 50% lower than Standard for the GPT-6 models [D-G]. GPT-6.1 Sol Ultrafast is 6x Standard [D]. Regional processing adds a 10% premium where eligible [C, D-F]. GPT-6.1 Sol has a 1,050,000-token context window and 128,000 max output tokens [D].
- Codex Fast uses 2.5x included subscription usage and 2x purchased credits or Enterprise pay-as-you-go usage, where supported [K, L]. This applies to supported GPT-6 models, including GPT-6.1 Sol and GPT-6 Sol; speed labels in the model catalog do not establish a billing multiplier. The Speed page also covers GPT-5.6 but does not individually enumerate Terra and Luna Fast availability. Ultrafast for GPT-6 Astra and GPT-6.1 Sol uses 8x included usage and 6x purchased credits [K, L].
- Codex Standard credits per 1M tokens (input, cached input, output), fetched 2026-10-18 [K]: GPT-6 Astra 250, 25, 1,250; GPT-6.1 Sol 50, 2.5, 250; GPT-6 Sol 50, 5, 250; GPT-6 Luna 2.5, 0.25, 12.5; GPT-5.6 Sol 100, 10, 500; GPT-5.6 Terra 50, 5, 300; GPT-5.6 Luna 5, 0.5, 30. Codex credit billing has no separate cache-write charge. API-key use follows API pricing. Credit rates do not establish included subscription usage or task cost.
- Plan allowance, estimated local messages per five-hour period, fetched 2026-10-18 [K]: Plus and Standard Business each list GPT-6 Astra 5-45, GPT-6.1 Sol 15-160, GPT-6 Sol 15-150, and GPT-6 Luna 350-3,000. These are estimates, not fixed message limits; local messages and cloud chats share usage, cloud tasks can consume more, and weekly limits may apply. Pro plans currently have no five-hour limit. Enterprise/Edu with flexible pricing have no fixed rate limits; without flexible pricing they use Plus per-seat limits for most features. Model-specific GPT-5.6 Sol, Terra and Luna allowance estimates, and numeric Free/Go estimates, are not published on https://learn.chatgpt.com/docs/pricing checked.
- The Haiku 5.5 announcement's Pricing table confirms both prompt-length price bands [B]. Its Further updates section announces the Sonnet cache-read reduction.
- Quota readings do not choose routes.

### Corrections

- Sonnet 5.5 cache read: the old table said $0.20, attributed to https://platform.claude.com/docs/en/about-claude/pricing (recorded fetch 2026-10-09; no historical page snapshot carried). That same official pricing URL now lists $0.10 [A]. The official announcement https://www.anthropic.com/claude-haiku-5-5 explicitly says "$0.10 per million tokens rather than $0.20" [B]. This corrects the old evidence; it does not prove what the page showed on the earlier fetch date.
- GPT-6.1 Sol cache write was "not read"; the model page explicitly publishes $2.50 [D]. All other existing token table values were confirmed, with the two GPT-5.6 derived write values marked above. The Fast cost multipliers were confirmed; the credit multiplier and support caveats are now explicit.
- The old blanket claim that no page gives credits per task was too broad: [K] gives an indicative range for GPT-5.6 Sol. Per-token prices still do not establish the cost of a task on another model.

### Sources

- [A] https://platform.claude.com/docs/en/about-claude/pricing - fetched 2026-10-18, Model pricing.
- [B] https://www.anthropic.com/claude-haiku-5-5 - fetched 2026-10-18, Pricing; Further updates.
- [C] https://developers.openai.com/api/docs/pricing - fetched 2026-10-18, Flagship models; Cyber models; regional processing note.
- [D] https://developers.openai.com/api/docs/models/gpt-6.1-sol - fetched 2026-10-18, Pricing; context specifications.
- [E] https://developers.openai.com/api/docs/models/gpt-6-sol - fetched 2026-10-18, Pricing.
- [F] https://developers.openai.com/api/docs/models/gpt-6-luna - fetched 2026-10-18, Pricing.
- [G] https://developers.openai.com/api/docs/models/gpt-6-astra - fetched 2026-10-18, Pricing.
- [H] https://developers.openai.com/api/docs/models/gpt-5.6-sol - fetched 2026-10-18, Pricing.
- [I] https://developers.openai.com/api/docs/models/gpt-5.6-terra - fetched 2026-10-18, Pricing.
- [J] https://developers.openai.com/api/docs/models/gpt-5.6-luna - fetched 2026-10-18, Pricing.
- [K] https://learn.chatgpt.com/docs/pricing - fetched 2026-10-18, Usage limits; Token rates.
- [L] https://learn.chatgpt.com/docs/agent-configuration/speed - fetched 2026-10-18 through the official Speed link, Fast mode; Ultrafast mode.
- [M] https://developers.openai.com/api/docs/guides/fast-mode - fetched 2026-10-18, How is Fast mode billed?
