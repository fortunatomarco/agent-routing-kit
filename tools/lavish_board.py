#!/usr/bin/env python3
"""Build and operate a local Lavish decision board.

Only board folders below /tmp/lavish-boards are accepted. The installed CLI is
called by absolute path with a fixed environment and a small command allowlist.
"""
import argparse
import base64
import fcntl
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT = Path('/tmp/lavish-boards')
BIN = Path.home() / '.agent-tools/lavish-axi/node_modules/.bin/lavish-axi'
TEMPLATE = Path(__file__).with_name('lavish_board_template.html')
PORT = 43871
EXTERNAL = re.compile(r'(?:https?:)?//(?!127\.0\.0\.1(?::|/)|localhost(?::|/))', re.I)
IMAGE_TYPES = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml'}
FIELD_LIMITS = {'question': 200, 'brief': 350, 'detail': 1200,
                'recommendation_reason': 200, 'consequence': 200}


def fail(message):
    raise SystemExit('blocked: ' + message)


def board_dir(value):
    path = Path(value).expanduser().resolve()
    if path.parent != ROOT.resolve() or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', path.name):
        fail('board path must be one direct child of /tmp/lavish-boards')
    return path


def environment():
    env = {k: v for k, v in os.environ.items() if not k.startswith('LAVISH_AXI_')}
    env.update(LAVISH_AXI_TELEMETRY='0', LAVISH_AXI_HOST='127.0.0.1',
               LAVISH_AXI_NO_OPEN='1', LAVISH_AXI_PORT=str(PORT),
               LAVISH_AXI_STATE_DIR=str(ROOT / 'state'),
               LAVISH_AXI_IDLE_TIMEOUT_MS='7200000',
               LAVISH_AXI_HTML_APP_API_URL='http://127.0.0.1:9')
    return env


def cli(*args, timeout=45):
    if not BIN.exists():
        fail('pinned lavish-axi install missing')
    return subprocess.run([str(BIN), *map(str, args)], text=True, capture_output=True,
                          env=environment(), timeout=timeout)


def check_length(decision, field, value, limit, required=False):
    if not isinstance(value, str) or (required and not value.strip()):
        fail(f'decision {decision} {field} must be a nonempty string' if required else
             f'decision {decision} {field} must be a string')
    if len(value) > limit:
        fail(f'decision {decision} {field} length {len(value)} exceeds limit {limit}')


def mock_path(value, decision, asset_root=None):
    if not isinstance(value, str):
        fail(f'decision {decision} mocks.file must be a path')
    path = Path(value).expanduser()
    if asset_root is not None and path.name == value:
        path = asset_root / value
    resolved = path.resolve()
    root = ROOT.resolve()
    if root not in resolved.parents:
        fail(f'decision {decision} mocks.file must be inside /tmp/lavish-boards/')
    if asset_root is not None and path.name == value and resolved.parent != asset_root.resolve():
        fail(f'decision {decision} mocks.file must be inside board assets')
    if resolved.suffix.lower() not in IMAGE_TYPES or not resolved.is_file():
        fail(f'decision {decision} mocks.file must be an existing PNG, JPEG, or SVG')
    size = resolved.stat().st_size
    if size > 200 * 1024:
        fail(f'decision {decision} mocks.file size {size} exceeds limit {200 * 1024}')
    contents = resolved.read_bytes()
    suffix = resolved.suffix.lower()
    if suffix == '.png' and not contents.startswith(b'\x89PNG\r\n\x1a\n'):
        fail(f'decision {decision} mocks.file has wrong PNG signature')
    if suffix in ('.jpg', '.jpeg') and not contents.startswith(b'\xff\xd8\xff'):
        fail(f'decision {decision} mocks.file has wrong JPEG signature')
    if suffix == '.svg':
        try:
            svg = contents.decode('utf-8')
            root_element = ET.fromstring(svg)
        except (UnicodeError, ET.ParseError):
            fail(f'decision {decision} mocks.file is not well-formed SVG')
        if root_element.tag.split('}')[-1] != 'svg':
            fail(f'decision {decision} mocks.file root must be svg')
        for element in root_element.iter():
            if element.tag.split('}')[-1].lower() in {'script', 'foreignobject', 'image'}:
                fail(f'decision {decision} mocks.file contains forbidden SVG element')
            for key, val in element.attrib.items():
                name = key.split('}')[-1].lower()
                if name.startswith('on') or (name == 'href' and not re.fullmatch(r'#[A-Za-z_][\w.:-]*', val)):
                    fail(f'decision {decision} mocks.file contains forbidden SVG attribute')
        if re.search(r'@import', svg, re.I) or any(
                not re.fullmatch(r'\s*#[A-Za-z_][\w.:-]*\s*', ref)
                for ref in re.findall(r'url\(([^)]*)\)', svg, re.I)):
            fail(f'decision {decision} mocks.file contains external SVG reference')
    return resolved


def load_payload(path, asset_root=None):
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict) or not isinstance(data.get('groups'), list) or not isinstance(data.get('decisions'), list):
        fail('payload needs groups and decisions arrays')
    if not data.get('title') or not data.get('id') or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', data['id']):
        fail('payload needs a safe id and title')
    if data.get('layout', 'deck') not in ('deck', 'list'):
        fail('board.layout must be deck or list')
    groups = {g.get('id') for g in data['groups'] if isinstance(g, dict)}
    if 'context' in data:
        first_decision = data['decisions'][0].get('id', '?') if data['decisions'] and isinstance(data['decisions'][0], dict) else '?'
        check_length(first_decision, 'board.context', data['context'], 600)
    seen = set()
    for d in data['decisions']:
        if not isinstance(d, dict) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', str(d.get('id', ''))):
            fail('decision needs a safe id')
        if d['id'] in seen or d.get('group') not in groups or not d.get('title') or not d.get('question'):
            fail('duplicate id, missing group, title, or question')
        seen.add(d['id'])
        for field, limit in FIELD_LIMITS.items():
            if field == 'brief' or field in d:
                check_length(d['id'], field, d.get(field), limit, field == 'brief')
        if '\n' in d['brief'] or '\r' in d['brief']:
            fail(f'decision {d["id"]} brief must be one line')
        mocks = d.get('mocks', [])
        if not isinstance(mocks, list) or len(mocks) > 3 or ('mocks' in d and not mocks):
            fail(f'decision {d["id"]} mocks must have 1 to 3 images')
        for item in mocks:
            if not isinstance(item, dict):
                fail(f'decision {d["id"]} mocks entry must be an object')
            check_length(d['id'], 'mocks.caption', item.get('caption'), 120)
            check_length(d['id'], 'mocks.alt', item.get('alt'), 200, True)
            mock_path(item.get('file'), d['id'], asset_root)
        options = d.get('options')
        if not isinstance(options, list) or len(options) < 2:
            fail('each decision needs two options')
        ids = [o.get('id') for o in options if isinstance(o, dict)]
        if len(ids) != len(options) or len(set(ids)) != len(ids) or {'defer', 'other'} & set(ids) or d.get('recommended') not in ids:
            fail('option ids or recommendation invalid')
        for option in options:
            for field, limit in (('summary', 140), ('detail', 300)):
                if field in option:
                    check_length(d['id'], 'options.' + field, option[field], limit)
    serialized = json.dumps(data, ensure_ascii=False)
    if EXTERNAL.search(serialized):
        fail('external URL in payload')
    return data


def render(data, asset_root=None):
    data = json.loads(json.dumps(data))
    for decision in data['decisions']:
        for item in decision.get('mocks', []):
            path = mock_path(item['file'], decision['id'], asset_root)
            item['src'] = 'data:' + IMAGE_TYPES[path.suffix.lower()] + ';base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
    raw = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    revisions = json.dumps(data.get('revisions', []), ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = TEMPLATE.read_text().replace('__BOARD_DATA__', raw).replace('__REVISIONS__', revisions)
    page_without_images = re.sub(r'data:image/(?:png|jpeg|svg\+xml);base64,[A-Za-z0-9+/=]+', '', page)
    if EXTERNAL.search(page_without_images):
        fail('external URL in rendered page')
    return page


def write_atomic(path, content):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(content)
    temp.replace(path)


def listen_check():
    result = subprocess.run(['lsof', '-nP', f'-iTCP:{PORT}', '-sTCP:LISTEN'], capture_output=True, text=True)
    lines = result.stdout.splitlines()[1:]
    if not lines or any(f'127.0.0.1:{PORT}' not in line for line in lines):
        fail('Lavish does not listen only on loopback: ' + result.stdout.strip())
    return result.stdout.strip()


def doctor(_):
    result = cli('--version')
    if result.returncode or result.stdout.strip() != '0.1.87':
        fail('wrong Lavish version: ' + result.stdout + result.stderr)
    print('done: lavish-axi 0.1.87; telemetry=0; host=127.0.0.1; port=43871')


def plain(path, kind):
    """Check an entry without following a symbolic link."""
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    return (stat.S_ISDIR(mode) if kind == 'dir' else stat.S_ISREG(mode))


def tree_safe(path):
    """Refuse a tree containing a symbolic link, including nested entries."""
    if not plain(path, 'dir'):
        return False
    for current, dirs, files in os.walk(path, followlinks=False):
        for name in dirs + files:
            entry = Path(current) / name
            if stat.S_ISLNK(entry.lstat().st_mode):
                return False
    return True


def size_of(path):
    if plain(path, 'file'):
        return path.lstat().st_size
    return sum((Path(current) / name).lstat().st_size
               for current, _, files in os.walk(path) for name in files)


def old_boards(days=7, prefix=None):
    if not plain(ROOT, 'dir'):
        return
    cutoff = time.time() - days * 86400
    for folder in ROOT.iterdir():
        ident = folder.name
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', ident) or (prefix and not ident.startswith(prefix)):
            continue
        if not tree_safe(folder) or not plain(folder / 'payload.json', 'file') or not plain(folder / 'board.html', 'file'):
            continue
        final = folder / 'answers' / 'final.md'
        if not plain(final, 'file') or final.lstat().st_mtime >= cutoff:
            continue
        companions = [ROOT / f'payload-{ident}.json', ROOT / f'mocks-{ident}',
                      ROOT / f'{ident}-build-report.md', ROOT / f'{ident}-wait-log.md']
        yield folder, companions


def remove_old(days=7, prefix=None, dry_run=False):
    count = 0
    for folder, companions in old_boards(days, prefix):
        paths = [folder] + companions
        if dry_run:
            print(f'would remove {folder} ({size_of(folder)} bytes)')
            for path in companions:
                if plain(path, 'file') or plain(path, 'dir'):
                    print(f'  companion {path} ({size_of(path)} bytes)')
            continue
        if not tree_safe(folder):
            continue
        try:
            shutil.rmtree(folder)
            print(f'removed {folder}')
            count += 1
        except OSError as exc:
            print(f'warning: could not remove {folder}: {exc}')
            continue
        for path in companions:
            if not (plain(path, 'file') or plain(path, 'dir')):
                continue
            if plain(path, 'dir') and not tree_safe(path):
                continue
            try:
                shutil.rmtree(path) if plain(path, 'dir') else path.unlink()
                print(f'removed {path}')
            except OSError as exc:
                print(f'warning: could not remove {path}: {exc}')
    return count


def sweep(days=7):
    try:
        count = remove_old(days)
        if count:
            print(f'swept: {count} boards')
    except OSError as exc:
        print(f'warning: could not sweep {ROOT}: {exc}')


def purge(args):
    remove_old(args.older_than_days, args.prefix, args.dry_run)


def build(args):
    sweep()
    data = load_payload(args.payload)
    data['revision'] = 1
    data['revisions'] = [{'id': 'r1', 'label': 'Round 1', 'timestamp': datetime.now(timezone.utc).isoformat(), 'summary': 'Board created'}]
    folder = board_dir(str(ROOT / data['id']))
    if folder.exists():
        fail('board folder already exists; use update or choose a new id')
    page = render(data)
    folder.mkdir(parents=True)
    (folder / 'answers').mkdir()
    (folder / 'assets').mkdir()
    for decision in data['decisions']:
        for index, item in enumerate(decision.get('mocks', []), 1):
            source = mock_path(item['file'], decision['id'])
            name = f'{decision["id"]}-{index}{source.suffix.lower()}'
            shutil.copyfile(source, folder / 'assets' / name)
            item['file'] = name
    (folder / 'payload.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
    write_atomic(folder / 'board.html', render(data, folder / 'assets'))
    opened = cli(folder / 'board.html', '--no-open', timeout=90)
    if opened.returncode:
        fail('open failed: ' + opened.stdout + opened.stderr)
    url = re.search(r'http://127\.0\.0\.1:43871/session/[a-f0-9]+', opened.stdout + opened.stderr)
    if not url:
        fail('open did not return a loopback URL: ' + opened.stdout + opened.stderr)
    sockets = listen_check()
    (folder / 'state.md').write_text(f'# Lavish board {data["id"]}\n\nURL: {url.group()}\nStatus: open\n')
    print('done: ' + str(folder) + '\n' + url.group() + '\n' + sockets)


def update(args):
    folder = board_dir(args.board)
    if not (folder / 'board.html').is_file():
        fail('board missing')
    data = load_payload(args.payload, folder / 'assets')
    if data['id'] != folder.name:
        fail('payload board id differs')
    old = json.loads((folder / 'payload.json').read_text())
    data['revision'] = int(old.get('revision', 1)) + 1
    old_ids = {d['id'] for d in old['decisions']}
    new_ids = [d['id'] for d in data['decisions'] if d['id'] not in old_ids]
    summary = 'Added ' + ', '.join(new_ids) if new_ids else 'Board content updated'
    data['revisions'] = old.get('revisions', []) + [{'id': f'r{data["revision"]}', 'label': f'Round {data["revision"]}', 'timestamp': datetime.now(timezone.utc).isoformat(), 'summary': summary}]
    for decision in data['decisions']:
        for index, item in enumerate(decision.get('mocks', []), 1):
            source = mock_path(item['file'], decision['id'], folder / 'assets')
            if source.parent != (folder / 'assets').resolve():
                name = f'{decision["id"]}-{index}{source.suffix.lower()}'
                shutil.copyfile(source, folder / 'assets' / name)
                item['file'] = name
    write_atomic(folder / 'board.html', render(data, folder / 'assets'))
    write_atomic(folder / 'payload.json', json.dumps(data, ensure_ascii=False, indent=2))
    (folder / 'answers' / 'budget-start.json').unlink(missing_ok=True)
    reply = cli('reply', folder / 'board.html', '--agent-reply', args.message or f'Board updated to revision {data["revision"]}: {summary}.')
    if reply.returncode:
        fail('update saved, but reply failed: ' + reply.stderr)
    print(f'done: revision {data["revision"]}')


def parse_output(raw, path):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        status = re.search(r'^  status: ([a-z_]+)$', raw, re.M)
        if status:
            session = {'status': status.group(1)}
            if re.search(r'^  session_ended: true$', raw, re.M):
                session['session_ended'] = True
            ended_by = re.search(r'^  ended_by: ([a-z_]+)$', raw, re.M)
            if ended_by:
                session['ended_by'] = ended_by.group(1)
            prompts = []
            for line in raw.splitlines():
                match = re.match(r'^  ("(?:\\.|[^"\\])*"),', line)
                if not match:
                    continue
                rest = line[match.end():]
                if rest.startswith('"'):
                    prompt, end = json.JSONDecoder().raw_decode(rest)
                    rest = rest[end + 1:]
                else:
                    prompt, rest = rest.split(',', 1)
                selector, _, remainder = rest.partition(',')
                if selector.startswith('"'):
                    try:
                        selector = json.loads(selector)
                    except json.JSONDecodeError:
                        pass
                tag, _, element_text = remainder.partition(',')
                context = prompt.split('\n\nContext data:\n', 1)
                data = {}
                if len(context) == 2:
                    try:
                        data = json.loads(context[1])
                    except json.JSONDecodeError:
                        pass
                prompts.append({'uid': json.loads(match.group(1)), 'prompt': prompt, 'selector': selector,
                                'tag': tag, 'text': element_text, 'data': data})
            return {'session': session, 'prompts': prompts}
        fail('unparsable poll output; raw saved at ' + str(path))


def save_batch(folder, response, raw):
    answers = folder / 'answers'
    number = len(list(answers.glob('batch-*.raw'))) + 1
    path = answers / f'batch-{number:03}.raw'
    path.write_text(raw)
    data = parse_output(raw, path)
    return data, path


def is_answer(prompt, board_id):
    data = prompt.get('data')
    prompt_text = prompt.get('prompt')
    if not isinstance(data, dict) or not isinstance(prompt_text, str):
        return False
    decision = data.get('decision')
    return (prompt_text.startswith('Answer to ') and
            data.get('schema') == 'lavish-board-answer.v1' and
            (board_id is None or data.get('board') == board_id) and
            isinstance(decision, str) and bool(decision))


def messages_in(batch, board_id):
    return [p for p in batch.get('prompts', []) if not is_answer(p, None)]


def format_messages(messages):
    lines = []
    for p in messages:
        lines.append(f'- uid: {p.get("uid", "")}; selector: {p.get("selector", "")}; card: '
                     f'{re.search(r"card-([A-Za-z0-9_-]+)", p.get("selector", ""))[1] if re.search(r"card-([A-Za-z0-9_-]+)", p.get("selector", "")) else ""}')
        lines.append('  text: ' + p.get('prompt', ''))
    return '\n'.join(lines)


def final_answer(folder):
    payload = json.loads((folder / 'payload.json').read_text())
    merged = {}
    messages = []
    for path in sorted((folder / 'answers').glob('batch-*.raw')):
        batch = parse_output(path.read_text(), path)
        for prompt in batch.get('prompts', []):
            answer = prompt.get('data', {})
            if is_answer(prompt, payload['id']):
                merged[answer['decision']] = answer
            elif not is_answer(prompt, None):
                messages.append(prompt)
    lines = ['# Final board answers', '']
    for d in payload['decisions']:
        answer = merged.get(d['id'])
        if answer:
            lines.append(f'- {d["id"]}: {answer["selection"]}; note: {answer.get("note", "")}')
        else:
            lines.append(f'- {d["id"]}: unanswered')
    lines.extend(['', '## Messages for the coordinator', ''])
    lines.append(format_messages(messages) if messages else 'None.')
    path = folder / 'answers/final.md'
    path.write_text('\n'.join(lines) + '\n')
    return path


def poll_pids(page):
    """Find only poll processes for this exact board and this pinned binary."""
    listing = subprocess.run(['ps', '-ax', '-o', 'pid=', '-o', 'command='], capture_output=True, text=True)
    found = []
    for line in listing.stdout.splitlines():
        match = re.match(r'\s*(\d+)\s+(.+)', line)
        if not match:
            continue
        try:
            words = shlex.split(match.group(2))
        except ValueError:
            continue
        command = words[1:] if words and Path(words[0]).name == 'node' else words
        if len(command) >= 5 and command[:3] == [str(BIN), 'poll', str(page)] and '--owner' in command:
            pos = command.index('--owner')
            if pos + 1 < len(command) and command[pos + 1] == 'lavish-board:' + page.parent.name:
                found.append(int(match.group(1)))
    return found


def stop_poll(pid, page):
    if pid not in poll_pids(page):
        return
    try:
        if os.getpgid(pid) == pid:
            os.killpg(pid, signal.SIGTERM)
        else:
            os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    for _ in range(50):
        if pid not in poll_pids(page):
            return
        time.sleep(.1)
    if pid in poll_pids(page):
        if os.getpgid(pid) == pid:
            os.killpg(pid, signal.SIGKILL)
        else:
            os.kill(pid, signal.SIGKILL)


def receive_file(folder, path):
    raw = path.read_text()
    if not raw.strip():
        path.rename(path.with_suffix('.empty'))
        return None
    try:
        response = parse_output(raw, path)
    except SystemExit:
        return None
    status = response.get('session', {}).get('status')
    if status == 'feedback':
        number = len(list((folder / 'answers').glob('batch-*.raw'))) + 1
        batch_path = folder / 'answers' / f'batch-{number:03}.raw'
        path.rename(batch_path)
        return response, batch_path
    path.rename(path.with_suffix('.seen'))
    return response, path


def wait(args):
    folder = board_dir(args.board)
    page = folder / 'board.html'
    if not page.is_file():
        fail('board missing')
    answers = folder / 'answers'
    lock = (answers / 'wait.lock').open('a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        fail('another worker is already waiting on this board')
    active = None
    old_handlers = {}
    def interrupted(signum, _frame):
        if active is not None:
            stop_poll(active.pid, page)
        raise SystemExit(128 + signum)
    try:
        for sig in (signal.SIGTERM, signal.SIGINT):
            old_handlers[sig] = signal.signal(sig, interrupted)
        for pid in poll_pids(page):
            stop_poll(pid, page)
        clock = answers / 'budget-start.json'
        if not clock.exists():
            write_atomic(clock, json.dumps({'started_at': time.time()}))
        deadline = json.loads(clock.read_text())['started_at'] + args.budget
        owner = 'lavish-board:' + folder.name
        reply_file = None
        reported_file = answers / 'messages-reported.json'
        reported = set(json.loads(reported_file.read_text())) if reported_file.exists() else set()
        previous = sorted(answers.glob('batch-*.raw'))
        if previous:
            last = parse_output(previous[-1].read_text(), previous[-1])
            ids = [p.get('data', {}).get('decision', '?') for p in last.get('prompts', []) if is_answer(p, folder.name)]
            reply_file = answers / 'receipt.md'
            reply_file.write_text('Received: ' + ', '.join(ids) + '. Press Send & End when finished.\n')
        disconnects = 0
        while True:
            for batch_path in sorted(answers.glob('batch-*.raw')):
                if batch_path.name in reported:
                    continue
                batch = parse_output(batch_path.read_text(), batch_path)
                messages = messages_in(batch, folder.name)
                if messages and not batch.get('session', {}).get('session_ended'):
                    clock.unlink(missing_ok=True)
                    print('message: ' + str(batch_path) + '\n' + format_messages(messages), flush=True)
                    reported.add(batch_path.name)
                    write_atomic(reported_file, json.dumps(sorted(reported)))
                    return
            for rawpath in sorted(answers.glob('poll-*.raw')):
                received = receive_file(folder, rawpath)
                if not received:
                    continue
                response, path = received
                status = response.get('session', {}).get('status')
                if status == 'feedback':
                    messages = messages_in(response, folder.name)
                    if response.get('session', {}).get('session_ended'):
                        final = final_answer(folder)
                        clock.unlink(missing_ok=True)
                        print('ended: ' + str(final) + '\n' + final.read_text())
                        return
                    if messages:
                        clock.unlink(missing_ok=True)
                        print('message: ' + str(path) + '\n' + format_messages(messages), flush=True)
                        reported.add(path.name)
                        write_atomic(reported_file, json.dumps(sorted(reported)))
                        return
                    if args.until == 'send':
                        print('sent: ' + str(path))
                        return
                    ids = [p['data']['decision'] for p in response['prompts'] if is_answer(p, folder.name)]
                    reply_file = answers / 'receipt.md'
                    reply_file.write_text('Received: ' + ', '.join(ids) + '. Press Send & End when finished.\n')
                elif status == 'ended':
                    final = final_answer(folder)
                    clock.unlink(missing_ok=True)
                    print('ended: ' + str(final) + '\n' + final.read_text())
                    return
                elif status == 'browser_disconnected':
                    disconnects += 1
                    if disconnects >= 3:
                        fail('browser closed; session remains open')
                    time.sleep(min(30, max(0, deadline - time.time())))
            if time.time() >= deadline:
                clock.unlink(missing_ok=True)
                print('deadline: board stays open; run wait again for late answers')
                return
            command = [str(BIN), 'poll', str(page), '--owner', owner]
            if reply_file:
                command.extend(['--agent-reply-file', str(reply_file)])
            rawpath = answers / f'poll-{time.time_ns()}.raw'
            errpath = rawpath.with_suffix('.err')
            with rawpath.open('wb') as out, errpath.open('wb') as err:
                active = subprocess.Popen(command, stdout=out, stderr=err, env=environment(), start_new_session=True)
                try:
                    active.wait(timeout=min(args.slice, max(.1, deadline - time.time())))
                except subprocess.TimeoutExpired:
                    stop_poll(active.pid, page)
                    active.wait(timeout=10)
                    active = None
                    if rawpath.stat().st_size:
                        continue
                    if time.time() >= deadline:
                        clock.unlink(missing_ok=True)
                        print('deadline: board stays open; run wait again for late answers')
                    else:
                        print('slice: no answer yet')
                    return
                code = active.returncode
                active = None
            if code:
                stderr = errpath.read_text()
                if 'LISTENER_ACTIVE' in stderr and owner in stderr:
                    for pid in poll_pids(page):
                        stop_poll(pid, page)
                    continue
                fail('poll failed: ' + stderr)
    finally:
        if active is not None:
            stop_poll(active.pid, page)
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
        lock.close()


def status(args):
    folder = board_dir(args.board)
    print((folder / 'state.md').read_text())
    result = cli()
    print(result.stdout)


def close(args):
    folder = board_dir(args.board)
    page = folder / 'board.html'
    if not page.is_file():
        fail('board missing')
    for pid in poll_pids(page):
        stop_poll(pid, page)
    ended = cli('end', page)
    if ended.returncode and 'ended' not in ended.stderr.lower():
        fail('end failed: ' + ended.stderr)
    listed = cli()
    if listed.returncode:
        fail('session listing failed: ' + listed.stderr)
    (folder / 'answers/budget-start.json').unlink(missing_ok=True)
    if not re.search(r'\bstatus: open\b', listed.stdout):
        stopped = cli('stop')
        if stopped.returncode:
            fail('stop failed: ' + stopped.stderr)
        print('done: session ended; server stopped; board files preserved')
    else:
        print('done: session ended; other open sessions remain; board files preserved')


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    b = sub.add_parser('build'); b.add_argument('payload')
    u = sub.add_parser('update'); u.add_argument('board'); u.add_argument('payload'); u.add_argument('--message', help='short reply shown on the board after updating')
    w = sub.add_parser('wait'); w.add_argument('board'); w.add_argument('--until', choices=['send','end'], default='end'); w.add_argument('--slice', type=int, default=540); w.add_argument('--budget', type=int, default=14400)
    s = sub.add_parser('status'); s.add_argument('board')
    c = sub.add_parser('close'); c.add_argument('board')
    p = sub.add_parser('purge'); p.add_argument('--older-than-days', type=int, default=7); p.add_argument('--prefix'); p.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.command == 'wait' and (args.slice < 1 or args.budget < 1):
        fail('slice and budget must be positive')
    if args.command == 'purge' and args.older_than_days < 0:
        fail('older-than-days must be nonnegative')
    globals()[args.command](args)


if __name__ == '__main__':
    main()
