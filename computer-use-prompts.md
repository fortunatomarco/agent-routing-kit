# Computer Use prompts

Read when: you write a Computer Use prompt for Codex desktop automation (macOS). The approval step before delegation is in `delegation-t3.md`, "Coordinator discipline".

Every Computer Use prompt for Codex:

- names the source of the data it extracts, and stays short;
- tells Codex to work on a separate macOS desktop (Space), such as Desktop 2 or Desktop 3, and to keep off the desktop the user is using;
- tells Codex, before starting, to open or move every app it needs onto that desktop, and to check after each new window or tab that it opened there; if one opens on the user's desktop, to move it back to the work desktop at once;
- when Codex needs a browser, tells it to open a new window of `overlay.cu-browser` (default: a browser the user does not use for their own work) and use only that, leaving the user's own browser and all their open windows untouched;
- tells Codex to close each window and tab it opened as soon as it no longer needs it, to close all of them when the task ends, and to leave every window it did not open. A window an app opens for Codex, such as a spreadsheet from an export, counts as Codex's own: it closes it, without saving changes, once it has what it needs;
- limits Computer Use to the apps the task names, because a newly launched app opens on the user's desktop; Codex writes every file with its own shell commands, from the text it read on screen;
- lists the uncommitted files Codex will find in the workspace and tells it to leave them alone.

Done when the prompt carries each of the seven items.
