# Routing evidence: cache and prices

Read when: you question a cache period, a thread-reuse rule or a cost comparison, or you update a price. `rationale.md` links here. Facts below were fetched or measured on the dates shown; prices and cache terms change, so re-fetch before you rely on them.

## Cache

`threads-and-cache.md` says the cache goes cold after about 60 idle minutes on Claude and about 30 on GPT-5.6 and later. Where these two figures came from: motivo non documentato; nobody recorded their source. They now have an official check (pages read 2026-10-09):

- Claude API: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." A 1-hour TTL is an opt-in "at 2x the base input token price" (https://platform.claude.com/docs/en/build-with-claude/prompt-caching; 100,000 of 160,149 characters read).
- Claude Code on a subscription: "Unless you choose a TTL yourself, Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage. There it requests the hour for the main conversation". "Subagents fall outside the main-conversation TTL bucket, so they get five minutes even on a subscription." Over the plan limit, "Claude Code drops the main conversation to the five-minute TTL" (https://code.claude.com/docs/en/prompt-caching, "Cache lifetime" and "Which TTL each request gets"). The page says "one-hour TTL"; "about 60 idle minutes" is our paraphrase.
- OpenAI API, GPT-5.6 and later: "The only supported value, `30m`, is also the default." The cache lifetime is "At least 30 minutes after the latest write or reuse" (https://developers.openai.com/api/docs/guides/prompt-caching). So 30 is a minimum, not a hard expiry.
- No official statement found for Codex on a ChatGPT plan; the only difference found is billing ("Codex credit billing has no separate cache-write charge", https://learn.chatgpt.com/docs/pricing). No page places Sol and Luna in the 30-minute rule by name; that is an inference from version order.

Measurements in the origin project (T3 Code, 2026-10-09 and 2026-10-10; the reports are not carried):

- Method: Claude Code session logs record, per request, `cache_creation.ephemeral_5m_input_tokens` and `ephemeral_1h_input_tokens`; sessions were mapped to T3 threads through the T3 database; usage numbers only, no conversation content.
- Coordinator thread (instance `claudeAgent_claude_coordinator`, Sonnet 5.5): 4 sessions, 54 requests, 208,795 tokens written at 1 hour, 0 at 5 minutes. After gaps of 8.1 and 16.4 minutes it read 81,168 and 115,619 tokens and created 2,806 and 393.
- T3 delegated workers (`delegate_task`, instance `claudeAgent`): 21 sessions (19 Sonnet 5.5, 2 Haiku 5.5), 259 requests, 1,441,279 tokens written at 1 hour, 0 at 5 minutes. They are separate top-level Claude sessions, not native subagents, so they get the main-conversation TTL. Probe on one Haiku 5.5 worker at xhigh: after a gap of 7 min 24 s the follow-up created 86 tokens and read 35,941, so the cache stayed warm.
- Contrast: one native `Task` subagent wrote 63,548 tokens at 5 minutes and 0 at 1 hour, matching the official docs above.
- Luna gap test (2026-10-10): one Codex worker, model gpt-6-luna, effort max, Standard tier per task configuration (the Codex log has no tier field; it records a plan type of edu). One shell sleep between two model requests, nothing else in the gap. First request after a gap of 25 s, 4, 6, 12, 25 and 35 minutes read 99.3, 96.7, 98.9, 98.1, 96.9 and 95.9 percent of the previous input prefix from the cache (above 90 percent counts as warm): no miss at any gap, so the claim of a cache miss after 5 minutes (seen on X) did not hold for this plan and run. Limits: one run, one account, interactive, longest gap 35 minutes, plan-usage state and Fast tier not tested.
- Limits of the Claude measurement: the log field records the TTL requested at write time; the probe does not test the full hour, and a 65-minute test was not run; the warm-read probe covers Haiku only, and Sonnet workers have the write flag but no idle gap in their logs; the result holds within plan usage and may change when plan usage runs out or with API-key use.

Result: the 60-minute figure is right for the Claude Code main conversation on a subscription within plan usage, and the 30-minute figure as an OpenAI minimum. Both are wrong for the Claude API default and for Claude native subagents. A T3 delegated worker counts as a main conversation (1 hour). Sol and API-key use on the OpenAI side are not measured. The owner chose to record this here only and leave `threads-and-cache.md` unchanged.

**Would change if:** the owner's plan usage runs out; T3 changes how it starts Claude sessions; or a 65-minute test shows expiry before one hour.

## Prices

Prices per 1M tokens, fetched 2026-10-09. Sources: https://platform.claude.com/docs/en/about-claude/pricing and https://developers.openai.com/api/docs/pricing . The gpt-6.1-sol row comes from the OpenAI page as read by a research worker, which found it missing from the first fetch; its cache read price agrees with "0.05x on GPT-6.1 Sol" in the OpenAI prompt-caching guide.

| Model | Input | Cache read | Cache write | Output |
| --- | --- | --- | --- | --- |
| Claude Sonnet 5.5 | $2 | $0.20 | $2.50 | $10 |
| Claude Opus 5.5 | $4 | $0.20 | $5 | $20 |
| Claude Haiku 5.5, prompt up to 100K | $0.10 | $0.01 | $0.125 (5 min) | $0.50 |
| Claude Haiku 5.5, prompt above 100K | $0.50 | $0.05 | $0.625 (5 min) | $2.50 |
| gpt-6-luna | $0.10 | $0.01 | $0.125 | $0.50 |
| gpt-6-sol | $2.00 | $0.20 | $2.50 | $10.00 |
| gpt-6-astra | $10 | $1 | $12.50 | $50 |
| gpt-6.1-sol | $2.00 | $0.10 | not read | $10.00 |
| gpt-5.6-sol | $4 | $0.40 | $5 | $20 |
| gpt-5.6-terra | $2 | $0.20 | $2.50 | $12 |
| gpt-5.6-luna | $0.20 | $0.02 | $0.25 | $1.20 |

- The owner's Codex runs on a ChatGPT plan allowance (`auth_mode: chatgpt` in the Codex auth file, read 2026-10-09), not per token. Read the OpenAI rows as a relative comparison only.
- The fast service tier costs 2x on the API and 2.5x of included plan usage in Codex.
- Codex credits per 1M tokens (input, cached input, output): GPT-6 Luna 2.5, 0.25, 12.5; GPT-5.6 Luna 5, 0.5, 30; GPT-6 Sol 50, 5, 250 (https://learn.chatgpt.com/docs/pricing, read by a research worker on 2026-10-09). So gpt-6-luna costs half of gpt-5.6-luna on input and cached input, about 42% on output, and one twentieth of GPT-6 Sol on all three. Plan table, local messages per five-hour period on Plus and Standard Business: GPT-6 Luna "350-3,000", GPT-6 Sol "15-150". No page gives credits per task, so a cheaper token does not prove a cheaper task.
- Quota readings do not choose routes (measurement.md, removed 2026-10-12).
