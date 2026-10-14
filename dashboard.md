# Coordinator dashboard

Read when: a thread finishes important work, blocks, needs the user, yields a result others depend on, or changes the next steps; and when the user asks "status?" or "what next?".

The coordinator's conversation is the user's control tower: the user should never need to open a thread to learn its status, outcome or next step.

- Post an updated dashboard at each event above. Answer "status?" and "what next?" from the same view.
- Sections, omitting any that are empty:
  - NEXT FOR THE USER: only items needing their decision, approval, review, action or input, by priority. Number each item with a bold title, then *Status:*, *You:* (what they must do) and *Next:* (what happens after), with a link to the thread or document. Decisions go on a selector (`communication.md`).
  - IN PROGRESS: the task, the thread, what it is doing, the result awaited.
  - WAITING / EXTERNAL: work blocked on Codex, data, a third party, files, permissions or another dependency, with the exact event that unblocks it.
  - DONE / RECENTLY COMPLETED: only recent results that still affect next steps, not an archive. Give each a *Checked:* line that names gate, verifier, review or "unchecked".
- Remove items once resolved. Mark any status you could not verify as uncertain.
