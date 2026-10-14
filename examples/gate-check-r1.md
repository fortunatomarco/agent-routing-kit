# Gate check, round 1

Independent mechanical checks for the routing kit. Only this report was written.

## a. Guard tests

Command, run from `<kit-folder>`:

```text
python3 -I tests/test_guard.py
```

Result: **PASS**. The test output reports `37/37 passed` and the command exit code is `0`.

Last 10 output lines:

```text
PASS | Bash malformed JSON | python3 -I <kit-folder>/guard/hooks/coordinator-bash-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/bash-malformed-json.json | exit 2 (expected 2) | coordinator-bash-guard: unreadable payload, denied (fail closed)
PASS | Bash script not in config | python3 -I <kit-folder>/guard/hooks/coordinator-bash-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/bash-script-not-in-config.json | exit 2 (expected 2) | coordinator-bash-guard: denied (not on the allowlist: tools/python scripts/other.py). Hand the task to a worker.
PASS | Bash runner without script | python3 -I <kit-folder>/guard/hooks/coordinator-bash-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/bash-runner-without-script.json | exit 2 (expected 2) | coordinator-bash-guard: denied (not on the allowlist: tools/python). Hand the task to a worker.
PASS | Bash joined configured script | python3 -I <kit-folder>/guard/hooks/coordinator-bash-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/bash-joined-configured-script.json | exit 0 (expected 0) | allowed
PASS | Bash joined unlisted script | python3 -I <kit-folder>/guard/hooks/coordinator-bash-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/bash-joined-unlisted-script.json | exit 2 (expected 2) | coordinator-bash-guard: denied (not on the allowlist: tools/python scripts/other.py). Hand the task to a worker.
PASS | Bash script with absent config | python3 -I <kit-folder>/guard/hooks/coordinator-bash-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/bash-script-with-absent-config.json | exit 2 (expected 2) | coordinator-bash-guard: denied (not on the allowlist: tools/python scripts/check.py). Hand the task to a worker.
PASS | Bash script with unreadable config | python3 -I <kit-folder>/guard/hooks/coordinator-bash-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/bash-script-with-unreadable-config.json | exit 2 (expected 2) | coordinator-bash-guard: denied (unreadable guard config, fail closed). Hand the task to a worker.
PASS | Read large file inside project, cwd in subfolder | python3 -I <kit-folder>/guard/hooks/coordinator-read-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/read-large-file-inside-project-cwd-in-subfolder.json | exit 0 (expected 0) | allowed
PASS | Read large file outside project, cwd in subfolder | python3 -I <kit-folder>/guard/hooks/coordinator-read-guard.py < /var/folders/m0/zfrk_krd2ml_fmnqnvl20x7m0000gn/T/coordinator-guard-test-w5etky6e/read-large-file-outside-project-cwd-in-subfolder.json | exit 2 (expected 2) | coordinator-read-guard: denied (large file outside project). Hand the reading to a worker.
37/37 passed
```

Exit code: `0`.

## b. Source heading counts

Counted level 1 to 3 Markdown headings in the seven named source files, excluding lines inside fenced code blocks.

| Source file | Count |
| --- | ---: |
| `coordinator.md` | 13 |
| `routing-rationale.md` | 13 |
| `procedures.md` | 7 |
| `collaboration.md` | 7 |
| `collaboration-t3-code.md` | 5 |
| `collaboration-claude-projects.md` | 5 |
| `coordinator-guard/README.md` | 6 |
| **Total** | **56** |

Result: **PASS**, total is 56.

## c. Inventory row mapping

Audited the inventory table in `examples/round1-report.md` (the table under `## Inventory`, referenced by `Acceptance evidence` > `a. Inventory`).

- Data rows, excluding the header and separator: **56**.
- Rows whose source file or heading was not found: **0**.
- Source headings without an inventory row: **0**.

Result: **PASS**. Every inventory row names one of the seven source files and an existing heading in that file.
