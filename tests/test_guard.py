#!/usr/bin/env python3
"""Synthetic PreToolUse regression check for the coordinator plugin.

Run from the kit root: python3 -I tests/test_guard.py
Parameters (environment variables, all optional):
  GUARD_TEST_PROJECT    folder used as the project root in the payloads (default: the kit root)
  GUARD_TEST_RULE_FILE  small file inside that folder that must stay readable (default: README.md)
"""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

KIT = Path(__file__).resolve().parents[1]
PLUGIN = KIT / 'guard'
ROOT = Path(os.environ.get('GUARD_TEST_PROJECT', KIT)).resolve()
RULE_FILE = ROOT / os.environ.get('GUARD_TEST_RULE_FILE', 'README.md')
RULE_DIR = RULE_FILE.parent
TEMP_DIR = tempfile.TemporaryDirectory(prefix='coordinator-guard-test-')
SCRATCH = Path(TEMP_DIR.name)
LONG = SCRATCH / 'large-result.txt'
SAVED = SCRATCH / 'tool-results' / 'result.json'
LONG.write_bytes(b'x' * 65537)
SAVED.parent.mkdir(exist_ok=True)
SAVED.write_text('{"text":"short"}\n')
LINK = SCRATCH / 'saved-link.json'
if LINK.exists() or LINK.is_symlink():
    LINK.unlink()
LINK.symlink_to(SAVED)

# A throwaway project: a marker folder, a subfolder to start in, a large file inside the project.
PROJECT = SCRATCH / 'project'
(PROJECT / '.agent-routing').mkdir(parents=True)
(PROJECT / 'sub').mkdir()
BIG_INSIDE = PROJECT / 'big-inside.txt'
BIG_INSIDE.write_bytes(b'x' * 65537)

# Guard config used by the script-runner cases: one runner with one script.
CONFIG = SCRATCH / 'guard.json'
CONFIG.write_text(json.dumps({'scriptRunners': [{'command': 'tools/python', 'scripts': ['scripts/check.py']}]}))
NO_CONFIG = SCRATCH / 'absent-guard.json'
BAD_CONFIG = SCRATCH / 'bad-guard.json'
BAD_CONFIG.write_text('{not json')
EXTRA_CONFIG = SCRATCH / 'extra-guarded.json'
EXTRA_CONFIG.write_text(json.dumps({'guardedInstances': ['claudeAgent_other_guard']}))
BAD_EXTRA_CONFIG = SCRATCH / 'bad-extra-guarded.json'
BAD_EXTRA_CONFIG.write_text(json.dumps({'guardedInstances': 'claudeAgent_other_guard'}))

# Delegation tool inputs: the explicit-target shapes the T3 schemas define.
DELEGATE = 'mcp__t3-code__delegate_task'
LAUNCH = 'mcp__t3-code__t3_thread_launch'
THREADS = 'mcp__t3-code__create_threads'
GUARDED = 'claudeAgent_claude_coordinator'

CASES = [
    ('Read small project rule', 'Read', {'file_path': str(RULE_FILE)}, 0),
    ('Read tool-results', 'Read', {'file_path': str(SAVED)}, 2),
    ('Read symlink to tool-results', 'Read', {'file_path': str(LINK)}, 2),
    ('Grep tool-results', 'Grep', {'pattern': 'text', 'path': str(SAVED), 'output_mode': 'content'}, 2),
    ('Glob tool-results', 'Glob', {'pattern': '*.json', 'path': str(SAVED.parent)}, 2),
    ('Grep project', 'Grep', {'pattern': 'coordinator', 'path': str(RULE_DIR)}, 0),
    ('Glob project', 'Glob', {'pattern': '*.md', 'path': str(RULE_DIR)}, 0),
    ('Read large external', 'Read', {'file_path': str(LONG)}, 2),
    ('thread messages short', 'mcp__t3-code__t3_thread_read', {'threadId': 'test', 'view': 'messages', 'limit': 3, 'maxCharsPerItem': 2000}, 0),
    ('thread activity 100', 'mcp__t3-code__t3_thread_read', {'threadId': 'test', 'view': 'activity', 'limit': 100}, 2),
    ('thread excessive chars', 'mcp__t3-code__t3_thread_read', {'threadId': 'test', 'view': 'messages', 'limit': 3, 'maxCharsPerItem': 100000}, 2),
    ('thread unbounded', 'mcp__t3-code__t3_thread_read', {'threadId': 'test'}, 2),
    ('thread long item', 'mcp__t3-code__t3_thread_read', {'threadId': 'test', 'itemId': 'item', 'limit': 1, 'maxCharsPerItem': 2000}, 2),
    ('Bash git status', 'Bash', {'command': 'git status'}, 0),
    ('Bash git log', 'Bash', {'command': 'git log -1'}, 0),
    ('Bash git diff', 'Bash', {'command': 'git diff'}, 0),
    ('Bash git add', 'Bash', {'command': 'git add file.txt'}, 0),
    ('Bash git commit', 'Bash', {'command': 'git commit -m test'}, 0),
    ('Bash configured script', 'Bash', {'command': 'tools/python scripts/check.py'}, 0, {'env': CONFIG}),
    ('Bash readonly', 'Bash', {'command': 'ls | wc'}, 0),
    ('Bash python -c', 'Bash', {'command': "python3 -c 'print(1)'"}, 2),
    ('Bash curl', 'Bash', {'command': 'curl example.com'}, 2),
    ('Bash redirect', 'Bash', {'command': f'echo x > {SCRATCH / "coord-test.txt"}'}, 2),
    ('Bash substitution', 'Bash', {'command': 'ls $(pwd)'}, 2),
    ('Bash newline', 'Bash', {'command': 'ls\npwd'}, 2),
    ('Bash background', 'Bash', {'command': 'ls &'}, 2),
    ('Bash bad commit', 'Bash', {'command': 'git commit --amend -m test'}, 2),
    ('malformed JSON', 'Read', None, 2),
    ('Bash malformed JSON', 'Bash', None, 2),
    # Added for the configurable parts.
    ('Bash script not in config', 'Bash', {'command': 'tools/python scripts/other.py'}, 2, {'env': CONFIG}),
    ('Bash runner without script', 'Bash', {'command': 'tools/python'}, 2, {'env': CONFIG}),
    ('Bash joined configured script', 'Bash', {'command': 'tools/python scripts/check.py && ls'}, 0, {'env': CONFIG}),
    ('Bash joined unlisted script', 'Bash', {'command': 'ls && tools/python scripts/other.py'}, 2, {'env': CONFIG}),
    ('Bash script with absent config', 'Bash', {'command': 'tools/python scripts/check.py'}, 2, {'env': NO_CONFIG}),
    ('Bash script with unreadable config', 'Bash', {'command': 'tools/python scripts/check.py'}, 2, {'env': BAD_CONFIG}),
    ('Read large file inside project, cwd in subfolder', 'Read', {'file_path': str(BIG_INSIDE)}, 0, {'cwd': PROJECT / 'sub'}),
    ('Read large file outside project, cwd in subfolder', 'Read', {'file_path': str(LONG)}, 2, {'cwd': PROJECT / 'sub'}),
    # Delegation guard: workers must not inherit the coordinator guard.
    ('delegate explicit claudeAgent', DELEGATE, {'task': 't', 'target': {'providerInstanceId': 'claudeAgent', 'model': 'claude-sonnet-5-5'}}, 0),
    ('delegate explicit codex', DELEGATE, {'task': 't', 'target': {'providerInstanceId': 'codex', 'model': 'gpt-6-luna'}}, 0),
    ('delegate no target', DELEGATE, {'task': 't'}, 2),
    ('delegate null target', DELEGATE, {'task': 't', 'target': None}, 2),
    ('delegate target without instance', DELEGATE, {'task': 't', 'target': {'model': 'claude-sonnet-5-5'}}, 2),
    ('delegate empty instance', DELEGATE, {'task': 't', 'target': {'providerInstanceId': ''}}, 2),
    ('delegate guarded instance', DELEGATE, {'task': 't', 'target': {'providerInstanceId': GUARDED, 'model': 'claude-sonnet-5-5'}}, 2),
    ('delegate instance guarded by config', DELEGATE, {'task': 't', 'target': {'providerInstanceId': 'claudeAgent_other_guard'}}, 2, {'env': EXTRA_CONFIG}),
    ('delegate built-in guard kept with config', DELEGATE, {'task': 't', 'target': {'providerInstanceId': GUARDED}}, 2, {'env': EXTRA_CONFIG}),
    ('delegate plain instance with config', DELEGATE, {'task': 't', 'target': {'providerInstanceId': 'claudeAgent'}}, 0, {'env': EXTRA_CONFIG}),
    ('delegate with unreadable config', DELEGATE, {'task': 't', 'target': {'providerInstanceId': 'claudeAgent'}}, 2, {'env': BAD_CONFIG}),
    ('delegate with malformed guardedInstances', DELEGATE, {'task': 't', 'target': {'providerInstanceId': 'claudeAgent'}}, 2, {'env': BAD_EXTRA_CONFIG}),
    ('delegate malformed JSON', DELEGATE, None, 2),
    ('launch explicit instance', LAUNCH, {'title': 't', 'modelSelection': {'instanceId': 'codex', 'model': 'gpt-6-luna'}}, 0),
    ('launch no modelSelection', LAUNCH, {'title': 't'}, 2),
    ('launch modelSelection without instance', LAUNCH, {'title': 't', 'modelSelection': {'model': 'claude-sonnet-5-5'}}, 2),
    ('launch guarded instance', LAUNCH, {'title': 't', 'modelSelection': {'instanceId': GUARDED, 'model': 'claude-sonnet-5-5'}}, 2),
    ('create_threads all explicit', THREADS, {'threads': [{'target': {'providerInstanceId': 'claudeAgent'}}, {'target': {'providerInstanceId': 'codex'}}]}, 0),
    ('create_threads one without target', THREADS, {'threads': [{'target': {'providerInstanceId': 'claudeAgent'}}, {'prompt': 'p'}]}, 2),
    ('create_threads one guarded', THREADS, {'threads': [{'target': {'providerInstanceId': 'claudeAgent'}}, {'target': {'providerInstanceId': GUARDED}}]}, 2),
    ('create_threads empty list', THREADS, {'threads': []}, 2),
    ('underscore tool name, no target', 'mcp__t3_code__delegate_task', {'task': 't'}, 2),
]

groups = json.loads((PLUGIN / 'hooks/hooks.json').read_text())['hooks']['PreToolUse']
failed = 0
for case in CASES:
    label, tool, inputs, expected = case[:4]
    options = case[4] if len(case) > 4 else {}
    cwd = options.get('cwd', ROOT)
    handlers = [h for group in groups if tool in group['matcher'].split('|') for h in group['hooks']]
    if not handlers:
        actual, message = 0, 'no matching hook'
        script_path = payload_path = Path('-')
    else:
        command = handlers[0]['command']
        script = re.search(r'\/hooks\/([^" ]+\.py)', command)
        if not script:
            raise RuntimeError(command)
        payload = '{bad' if inputs is None else json.dumps({'tool_name': tool, 'tool_input': inputs, 'cwd': str(cwd)})
        payload_path = SCRATCH / (re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-') + '.json')
        payload_path.write_text(payload)
        script_path = PLUGIN / 'hooks' / script.group(1)
        env = dict(os.environ)
        env.pop('AGENT_ROUTING_GUARD_CONFIG', None)
        if 'env' in options:
            env['AGENT_ROUTING_GUARD_CONFIG'] = str(options['env'])
        with payload_path.open() as stream:
            result = subprocess.run(['python3', '-I', str(script_path)], stdin=stream, text=True, capture_output=True, cwd=cwd, env=env)
        actual = result.returncode
        message = (result.stderr.strip() or 'allowed').splitlines()[0]
    ok = actual == expected
    failed += not ok
    print(f'{"PASS" if ok else "FAIL"} | {label} | python3 -I {script_path} < {payload_path} | exit {actual} (expected {expected}) | {message}')
TEMP_DIR.cleanup()
print(f'{len(CASES) - failed}/{len(CASES)} passed')
raise SystemExit(bool(failed))
