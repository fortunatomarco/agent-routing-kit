# Glossary

Read when: you meet a kit term you do not know.
Reader: every session.

## Language

**kit**:
This folder of rules for routing work between AI agents.
Rule: [README.md](README.md).

**coordinator**:
The agent that talks to the user and hands tasks out; it does no work itself and cannot edit files.
Rule: [policy.md, Role](policy.md#role) and [Coordinator](policy.md#coordinator).

**worker**:
An agent that gets one written task (a brief), does it and reports back.
Rule: [policy.md, Role](policy.md#role).

**sub-worker**:
A worker started by a worker; allowed only one level down.
Rule: [delegation-t3.md, Nesting](delegation-t3.md#nesting).

**planner**:
The strongest model, used only for hard decisions that no test can check.
Rule: [policy.md, Routes](policy.md#routes), "Opus xhigh" route.

**brief**:
The written task for a worker: the user's request, six fixed items and a closing block.
Rule: [briefs-review-escalation.md](briefs-review-escalation.md).

**closed task**:
A task where every choice, the expected output and the check are already fixed.
Rule: [policy.md, Closed and open](policy.md#closed-and-open).

**open task**:
A task with a real choice left in it; it needs a person or a thinking model first.
_Avoid_: "open choice", "open point", "open items" for something not yet decided; say "undecided".
Rule: [policy.md, Closed and open](policy.md#closed-and-open).

**round**:
One pass of a worker on an open task, or one pass of a review; say which.
_Avoid_: "round" for a project phase; say "phase".
Rule: [policy.md, Closed and open](policy.md#closed-and-open); [briefs-review-escalation.md, Review](briefs-review-escalation.md#review).

**state file**:
A note that a worker keeps between rounds of an open task.
Rule: [delegation-t3.md](delegation-t3.md).

**route**:
The choice of model and effort for a task.
Rule: [policy.md](policy.md).

**route line**:
The one sentence that states the route before a task starts.
Rule: [policy.md, Before you act](policy.md#before-you-act).

**probe**:
A quick test of one fact, or the same quick test repeated over a list.
Rule: [delegation-t3.md, Running and tracking tasks](delegation-t3.md#running-and-tracking-tasks), "Probes" item.

**gate**:
The coordinator's own check of a result: run the test and confirm that only the allowed files changed.
Rule: [briefs-review-escalation.md, Review](briefs-review-escalation.md#review), "Gate" item.

**verifier**:
A separate small model that checks a result against the brief without seeing how it was made.
Rule: [briefs-review-escalation.md, Review](briefs-review-escalation.md#review), "Verifier" item.

**write set**:
The files a task is allowed to change.
Rule: [briefs-review-escalation.md](briefs-review-escalation.md).

**overlay**:
A small file in a project, `.agent-routing/overlay.md`, that sets that project's choices.
Rule: [overlay-template.md](overlay-template.md).

**selector**:
The question card with options that the user answers in the app.
Rule: [communication.md](communication.md).

**decision board**:
A local web page where the user picks options for several decisions at once.
Rule: [decision-boards.md](decision-boards.md).
