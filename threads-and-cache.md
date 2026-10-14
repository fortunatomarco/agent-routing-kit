# Threads and cache cost

Read when: you reuse or start a thread, a thread has been idle, or a coordinator context grows long.

A prompt cache goes cold after about 60 idle minutes for Claude and 30 for OpenAI GPT-5.6 and later (Sol, Luna); a cold, long thread then re-reads its history at full price. A change of model or effort also empties a thread's cache, so a thread keeps its assigned model and effort. (`rationale-evidence.md` holds the evidence and its limits.)

For the coordinator and every worker, before new work or a follow-up:

- Idle within its cache period, or short: reuse it.
- Idle past it and long: save its durable results to their project home, then start a fresh thread with a compact handoff (goal, decisions, state, file paths, open points).
- Idle past it, but the work needs detail a handoff cannot carry (unfinished edits, a long chain of reasoning): reuse it and accept the re-read.

Auto-compaction runs at `overlay.rotation` (default 300k tokens). A coordinator that reaches it writes the compact handoff and asks the user to continue in a fresh coordinator thread.
