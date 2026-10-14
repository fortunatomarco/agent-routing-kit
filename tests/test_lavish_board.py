import importlib.util
import fcntl
import json
import os
from pathlib import Path
import tempfile
import time
import io
from contextlib import redirect_stdout
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / 'tools/lavish_board.py'
spec = importlib.util.spec_from_file_location('lavish_board', SCRIPT)
board = importlib.util.module_from_spec(spec)
spec.loader.exec_module(board)


def sample():
    return {'id': 'test', 'title': 'Test <script>alert(1)</script>', 'groups': [{'id': 'g', 'title': 'Group'}],
            'decisions': [{'id': 'D1', 'group': 'g', 'title': 'Choice', 'question': 'Which?',
                           'brief': 'Choose an option now so the work can proceed.',
                           'recommended': 'a', 'options': [{'id': 'a', 'label': 'A'}, {'id': 'b', 'label': 'B'}]}]}


class BoardTests(unittest.TestCase):
    def test_sweep_selects_only_old_ended_boards_and_companions(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(board, 'ROOT', Path(temp)):
            root = Path(temp)
            def make(ident, age, ended=True):
                folder = root / ident
                (folder / 'answers').mkdir(parents=True)
                (folder / 'payload.json').write_text('{}')
                (folder / 'board.html').write_text('page')
                if ended:
                    final = folder / 'answers/final.md'
                    final.write_text('done')
                    when = time.time() - age * 86400
                    os.utime(final, (when, when))
                return folder
            old = make('v3sweep-old', 8)
            young = make('v3sweep-new', 1)
            open_board = make('v3sweep-open', 8, False)
            (root / 'payload-v3sweep-old.json').write_text('data')
            (root / 'mocks-v3sweep-old').mkdir()
            (root / 'v3sweep-old-build-report.md').write_text('build')
            (root / 'v3sweep-old-wait-log.md').write_text('wait')
            (root / 'unrelated').mkdir()
            (root / 'v3sweep-link').symlink_to(old, target_is_directory=True)
            with redirect_stdout(io.StringIO()) as output:
                board.remove_old(7, dry_run=True)
            self.assertIn('v3sweep-old', output.getvalue())
            self.assertTrue(old.exists())
            with redirect_stdout(io.StringIO()) as output:
                board.sweep()
            self.assertIn('swept: 1 boards', output.getvalue())
            for path in (old, root / 'payload-v3sweep-old.json', root / 'mocks-v3sweep-old',
                         root / 'v3sweep-old-build-report.md', root / 'v3sweep-old-wait-log.md'):
                self.assertFalse(path.exists())
            for path in (young, open_board, root / 'unrelated', root / 'v3sweep-link'):
                self.assertTrue(path.is_symlink() or path.exists())

    def test_sweep_warns_and_continues_after_delete_failure(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(board, 'ROOT', Path(temp)):
            for ident in ('v3sweep-a', 'v3sweep-b'):
                folder = Path(temp) / ident
                (folder / 'answers').mkdir(parents=True)
                (folder / 'payload.json').write_text('{}')
                (folder / 'board.html').write_text('page')
                final = folder / 'answers/final.md'
                final.write_text('done')
                old = time.time() - 8 * 86400
                os.utime(final, (old, old))
            original = board.shutil.rmtree
            def remove(path):
                if Path(path).name == 'v3sweep-a':
                    raise OSError('test failure')
                original(path)
            with mock.patch.object(board.shutil, 'rmtree', side_effect=remove), redirect_stdout(io.StringIO()) as output:
                board.sweep()
            self.assertIn('warning: could not remove', output.getvalue())
            self.assertTrue((Path(temp) / 'v3sweep-a').exists())
            self.assertFalse((Path(temp) / 'v3sweep-b').exists())

    def test_purge_prefix_and_build_sweep_order(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(board, 'ROOT', Path(temp)):
            root = Path(temp)
            for ident in ('v3sweep-yes', 'other-old'):
                folder = root / ident
                (folder / 'answers').mkdir(parents=True)
                (folder / 'payload.json').write_text('{}')
                (folder / 'board.html').write_text('page')
                final = folder / 'answers/final.md'
                final.write_text('done')
                old = time.time() - 8 * 86400
                os.utime(final, (old, old))
            args = type('Args', (), {'older_than_days': 7, 'prefix': 'v3sweep-', 'dry_run': True})()
            with redirect_stdout(io.StringIO()) as output:
                board.purge(args)
            self.assertIn('v3sweep-yes', output.getvalue())
            self.assertNotIn('other-old', output.getvalue())
            self.assertTrue((root / 'v3sweep-yes').exists())
            args.dry_run = False
            with redirect_stdout(io.StringIO()):
                board.purge(args)
            self.assertFalse((root / 'v3sweep-yes').exists())
            self.assertTrue((root / 'other-old').exists())
            with mock.patch.object(board, 'sweep') as sweep, mock.patch.object(board, 'load_payload', side_effect=SystemExit('stop')) as load:
                with self.assertRaises(SystemExit):
                    board.build(type('Args', (), {'payload': 'unused'})())
                self.assertTrue(sweep.called and load.called)

    def test_layout_validation_and_default(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'payload.json'
            for layout in (None, 'deck', 'list'):
                with self.subTest(layout=layout):
                    data = sample()
                    if layout is not None:
                        data['layout'] = layout
                    path.write_text(json.dumps(data))
                    parsed = board.load_payload(path)
                    self.assertEqual(parsed.get('layout', 'deck'), layout or 'deck')
                    self.assertIn('const deck=board.layout', board.render(parsed))
            data['layout'] = 'grid'
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(SystemExit, 'board.layout'):
                board.load_payload(path)

    def test_deck_controls_and_list_compatibility(self):
        template = board.TEMPLATE.read_text()
        for marker in ('id="progress"', 'id="previous"', 'id="next"',
                       'setTimeout(()=>showCard(deckIndex+1),450)',
                       "event.key==='ArrowLeft'", "event.key==='ArrowRight'",
                       'card.hidden=i!==index', "const deck=board.layout!=='list'"):
            with self.subTest(marker=marker):
                self.assertIn(marker, template)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'payload.json'
            data = sample(); data['layout'] = 'list'
            path.write_text(json.dumps(data))
            rendered = board.render(board.load_payload(path))
            self.assertIn('"layout": "list"', rendered)
            self.assertIn("groupSection.append(el('h2','',group.title))", rendered)
            self.assertIn("if(!deck)$('groups').append(groupSection)", rendered)

    def test_required_brief_and_limits(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'payload.json'
            data = sample(); del data['decisions'][0]['brief']
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(SystemExit, 'decision D1 brief'):
                board.load_payload(path)
            cases = [('context', 600, 'decision D1 board.context'), ('question', 200, 'decision D1 question'),
                     ('brief', 350, 'decision D1 brief'), ('detail', 1200, 'decision D1 detail'),
                     ('recommendation_reason', 200, 'decision D1 recommendation_reason'),
                     ('consequence', 200, 'decision D1 consequence'),
                     ('summary', 140, 'decision D1 options.summary'),
                     ('option_detail', 300, 'decision D1 options.detail')]
            for field, limit, message in cases:
                with self.subTest(field=field):
                    data = sample()
                    target = data if field == 'context' else data['decisions'][0]['options'][0] if field in ('summary', 'option_detail') else data['decisions'][0]
                    target['detail' if field == 'option_detail' else field] = 'x' * (limit + 1)
                    path.write_text(json.dumps(data))
                    with self.assertRaisesRegex(SystemExit, f'{message} length {limit + 1} exceeds limit {limit}'):
                        board.load_payload(path)

    def test_mock_validation_and_embedding(self):
        with tempfile.TemporaryDirectory(dir=board.ROOT) as temp:
            root = Path(temp); image = root/'image.png'
            image.write_bytes(b'\x89PNG\r\n\x1a\n' + b'\xff' * 300)
            payload = root/'payload.json'; data = sample()
            data['decisions'][0]['mocks'] = [{'file':str(image), 'caption':'Option A', 'alt':'A preview'}]
            payload.write_text(json.dumps(data))
            parsed = board.load_payload(payload)
            self.assertIn('data:image/png;base64,', board.render(parsed))
            svg = root/'view.svg'; svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text x="1" y="20">A</text></svg>')
            data['decisions'][0]['mocks'][0]['file'] = str(svg)
            payload.write_text(json.dumps(data))
            self.assertIn('data:image/svg+xml;base64,', board.render(board.load_payload(payload)))
            for name, contents, reason in [('bad.png', b'wrong', 'wrong PNG signature'),
                                           ('large.png', b'\x89PNG\r\n\x1a\n'+b'x'*(200*1024), 'size'),
                                           ('script.svg', b'<svg><script/></svg>', 'forbidden SVG element'),
                                           ('remote.svg', b'<svg><a href="https://example.org"/></svg>', 'forbidden SVG attribute')]:
                with self.subTest(name=name):
                    bad = root/name; bad.write_bytes(contents)
                    data['decisions'][0]['mocks'][0]['file'] = str(bad)
                    payload.write_text(json.dumps(data))
                    with self.assertRaisesRegex(SystemExit, reason): board.load_payload(payload)
            data['decisions'][0]['mocks'][0]['file'] = '/tmp/outside.png'
            payload.write_text(json.dumps(data))
            with self.assertRaisesRegex(SystemExit, 'inside /tmp/lavish-boards/'):
                board.load_payload(payload)

    def test_update_uses_copied_mock_after_original_removed(self):
        with tempfile.TemporaryDirectory(dir=board.ROOT) as temp:
            root = Path(temp); source = root/'image.png'
            source.write_bytes(b'\x89PNG\r\n\x1a\n' + b'png')
            data = sample(); data['id'] = root.name
            data['decisions'][0]['mocks'] = [{'file':str(source), 'caption':'A', 'alt':'A preview'}]
            payload = root/'input.json'; payload.write_text(json.dumps(data))
            folder = root; (folder/'assets').mkdir(parents=True); (folder/'answers').mkdir()
            saved = board.load_payload(payload)
            (folder/'assets/D1-1.png').write_bytes(source.read_bytes())
            saved['decisions'][0]['mocks'][0]['file'] = 'D1-1.png'
            saved['revision'] = 1; (folder/'payload.json').write_text(json.dumps(saved))
            (folder/'board.html').write_text(board.render(saved, folder/'assets'))
            source.unlink()
            with mock.patch.object(board, 'cli') as cli:
                cli.return_value.returncode = 0
                board.update(type('Args', (), {'board':str(folder), 'payload':str(folder/'payload.json'), 'message':None}))
            self.assertIn('data:image/png;base64,', (folder/'board.html').read_text())
            self.assertEqual(json.loads((folder/'payload.json').read_text())['decisions'][0]['mocks'][0]['file'], 'D1-1.png')
    def test_payload_and_script_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'payload.json'
            path.write_text(json.dumps(sample()))
            page = board.render(board.load_payload(path))
            self.assertIn('\\u003cscript\\u003e', page)
            self.assertNotIn('<script>alert(1)</script>', page)

    def test_external_url_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            data = sample(); data['context'] = 'https://example.org/img.png'
            path = Path(temp) / 'payload.json'; path.write_text(json.dumps(data))
            with self.assertRaises(SystemExit): board.load_payload(path)

    def test_board_path_boundary(self):
        with self.assertRaises(SystemExit): board.board_dir('/tmp/outside')
        with self.assertRaises(SystemExit): board.board_dir('/tmp/lavish-boards/a/b')

    def test_environment_overrides_inherited_values(self):
        with mock.patch.dict('os.environ', {'LAVISH_AXI_HOST':'0.0.0.0', 'LAVISH_AXI_TELEMETRY':'1', 'LAVISH_AXI_ALLOWED_HOSTS':'*'}):
            env = board.environment()
        self.assertEqual(env['LAVISH_AXI_HOST'], '127.0.0.1')
        self.assertEqual(env['LAVISH_AXI_TELEMETRY'], '0')
        self.assertNotIn('LAVISH_AXI_ALLOWED_HOSTS', env)

    def test_forbidden_subcommands(self):
        import argparse
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest='command', required=True)
        for name in ('doctor','build','update','wait','status','close'): sub.add_parser(name)
        for name in ('share','setup','server','unknown'):
            with self.assertRaises(SystemExit): parser.parse_args([name])

    def test_raw_batch_saved_before_parse(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp); (folder/'answers').mkdir()
            with self.assertRaises(SystemExit): board.save_batch(folder, {}, 'not json')
            self.assertEqual((folder/'answers/batch-001.raw').read_text(), 'not json')

    def test_cli_text_output_keeps_structured_answer(self):
        raw = 'session:\n  status: feedback\n  session_ended: true\n  ended_by: user\nprompts[1]{uid,prompt,selector,tag,text}:\n  "1","Answer\\n\\nContext data:\\n{\\"schema\\":\\"lavish-board-answer.v1\\",\\"decision\\":\\"D1\\",\\"selection\\":\\"a\\"}",article#card-D1,decision,Choice\n'
        parsed = board.parse_output(raw, Path('/tmp/raw'))
        self.assertTrue(parsed['session']['session_ended'])
        self.assertEqual(parsed['prompts'][0]['data']['selection'], 'a')

    def test_close_preserves_files(self):
        with tempfile.TemporaryDirectory() as temp:
            with mock.patch.object(board, 'ROOT', Path(temp)):
                folder = Path(temp)/'b'; folder.mkdir(); (folder/'board.html').write_text('x')
                with mock.patch.object(board, 'cli') as cli:
                    cli.return_value.returncode = 0
                    cli.return_value.stdout = ''
                    board.close(type('Args', (), {'board': str(folder)}))
                self.assertTrue((folder/'board.html').exists())

    def test_free_prompt_kept_in_final_and_wait_output(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp); (folder/'answers').mkdir()
            (folder/'payload.json').write_text(json.dumps(sample()))
            raw = ('session:\n  status: feedback\n  session_ended: true\n'
                   'prompts[1]{uid,prompt,selector,tag,text}:\n'
                   '  "7",What do you mean?,article#card-D1 > h3,h3,Choice\n')
            (folder/'answers/batch-001.raw').write_text(raw)
            result = board.final_answer(folder).read_text()
            self.assertIn('Messages for the coordinator', result)
            self.assertIn('uid: 7; selector: article#card-D1 > h3; card: D1', result)
            self.assertIn('What do you mean?', result)

    def test_other_choice_and_payload_reserved(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'payload.json'
            data = sample(); data['decisions'][0]['options'].append({'id':'other','label':'Other'})
            path.write_text(json.dumps(data))
            with self.assertRaises(SystemExit): board.load_payload(path)
        template = board.TEMPLATE.read_text()
        self.assertIn("{id:'other',label:'Other: I write my own answer'", template)
        self.assertIn("selection==='other'&&!note.trim()", template)
        self.assertLess(template.index("selection==='other'&&!note.trim()"),
                        template.index('window.lavish.queuePrompt(prompt'))
        self.assertIn("$('status-'+d.id).textContent='Write your answer in the note before queueing Other'", template)
        self.assertIn('No option fits? Choose Other and write your answer in the note.', template)
        self.assertLess(template.index("{id:'other',label:"), template.index("{id:'defer',label:"))
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp); (folder/'answers').mkdir()
            (folder/'payload.json').write_text(json.dumps(sample()))
            data = {'schema':'lavish-board-answer.v1','board':'test','decision':'D1','selection':'other','note':'Purple'}
            prompt = 'Answer to D1 Choice: Other: I write my own answer - Purple\n\nContext data:\n' + json.dumps(data)
            raw = 'session:\n  status: feedback\nprompts[1]{uid,prompt,selector,tag,text}:\n  "1",'+json.dumps(prompt)+',article#card-D1,decision,Choice\n'
            (folder/'answers/batch-001.raw').write_text(raw)
            self.assertIn('- D1: other; note: Purple', board.final_answer(folder).read_text())

    def test_message_batch_returns_and_keeps_board_open(self):
        with tempfile.TemporaryDirectory() as temp:
            with mock.patch.object(board, 'ROOT', Path(temp)):
                folder = Path(temp)/'b'; (folder/'answers').mkdir(parents=True)
                (folder/'board.html').write_text('x')
                (folder/'payload.json').write_text(json.dumps({**sample(), 'id':'b'}))
                (folder/'answers/poll-1.raw').write_text('session:\n  status: feedback\nprompts[1]{uid,prompt,selector,tag,text}:\n  "7",Please explain,article#card-D1 > h3,h3,Choice\n')
                with mock.patch.object(board, 'poll_pids', return_value=[]), redirect_stdout(io.StringIO()) as out:
                    board.wait(type('Args', (), {'board':str(folder),'budget':60,'slice':1,'until':'end'}))
                self.assertIn('message:', out.getvalue())
                self.assertIn('Please explain', out.getvalue())
                self.assertFalse((folder/'answers/budget-start.json').exists())
                self.assertEqual(len(list((folder/'answers').glob('batch-*.raw'))), 1)

    def test_wait_message_from_saved_batch_restarts_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            with mock.patch.object(board, 'ROOT', Path(temp)):
                folder = Path(temp)/'b'; (folder/'answers').mkdir(parents=True)
                (folder/'board.html').write_text('x')
                (folder/'payload.json').write_text(json.dumps({**sample(), 'id':'b'}))
                (folder/'answers/batch-001.raw').write_text('session:\n  status: feedback\nprompts[1]{uid,prompt,selector,tag,text}:\n  "7",Please clarify,article#card-D1 > h3,h3,Choice\n')
                with mock.patch.object(board, 'poll_pids', return_value=[]), redirect_stdout(io.StringIO()) as out:
                    board.wait(type('Args', (), {'board':str(folder),'budget':60,'slice':1,'until':'end'}))
                self.assertIn('message:', out.getvalue())
                self.assertIn('Please clarify', out.getvalue())
                self.assertFalse((folder/'answers/budget-start.json').exists())

    def test_update_restarts_budget_with_or_without_message(self):
        for message in (None, 'The board has an update'):
            with self.subTest(message=message), tempfile.TemporaryDirectory() as temp:
                with mock.patch.object(board, 'ROOT', Path(temp)):
                    folder = Path(temp)/'b'; (folder/'answers').mkdir(parents=True)
                    (folder/'board.html').write_text('x')
                    old = {**sample(), 'id':'b', 'revision':1}
                    (folder/'payload.json').write_text(json.dumps(old))
                    payload = Path(temp)/'new-payload.json'
                    payload.write_text(json.dumps({**sample(), 'id':'b'}))
                    clock = folder/'answers/budget-start.json'
                    clock.write_text(json.dumps({'started_at':time.time()-10}))
                    with mock.patch.object(board, 'cli') as cli:
                        cli.return_value.returncode = 0
                        board.update(type('Args', (), {'board':str(folder), 'payload':str(payload), 'message':message}))
                    self.assertFalse(clock.exists())
                    expected = message or 'Board updated to revision 2: Board content updated.'
                    cli.assert_called_once_with('reply', folder.resolve()/'board.html', '--agent-reply', expected)

    def test_mixed_message_and_decision_merges_later_answer(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp); (folder/'answers').mkdir()
            (folder/'payload.json').write_text(json.dumps(sample()))
            def row(selection):
                data = {'schema':'lavish-board-answer.v1','board':'test','decision':'D1','selection':selection,'note':''}
                prompt = 'Answer to D1 Choice: '+selection+'\n\nContext data:\n'+json.dumps(data)
                return '  "2",'+json.dumps(prompt)+',article#card-D1,decision,Choice\n'
            header = 'session:\n  status: feedback\nprompts[2]{uid,prompt,selector,tag,text}:\n'
            (folder/'answers/batch-001.raw').write_text(header+row('a')+'  "3",Please clarify,article#card-D1 > h3,h3,Choice\n')
            (folder/'answers/batch-002.raw').write_text('session:\n  status: feedback\n  session_ended: true\nprompts[1]{uid,prompt,selector,tag,text}:\n'+row('b'))
            final = board.final_answer(folder).read_text()
            self.assertIn('- D1: b; note: ', final)
            self.assertIn('uid: 3; selector: article#card-D1 > h3; card: D1', final)
            self.assertIn('Please clarify', final)

    def test_lowercase_decision_ids_merge_and_keep_free_message(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp); (folder/'answers').mkdir()
            payload = sample()
            payload['decisions'][0]['id'] = 'd1'
            payload['decisions'].append({**payload['decisions'][0], 'id':'d2', 'title':'Second choice'})
            (folder/'payload.json').write_text(json.dumps(payload))
            data = {'schema':'lavish-board-answer.v1','board':'test','decision':'d1','selection':'a','note':''}
            answer = 'Answer to d1 Choice: A\n\nContext data:\n' + json.dumps(data)
            raw = ('session:\n  status: feedback\n  session_ended: true\n'
                   'prompts[2]{uid,prompt,selector,tag,text}:\n'
                   '  "1",'+json.dumps(answer)+',article#card-d1,decision,Choice\n'
                   '  "2",Please clarify,article#card-d2 > h3,h3,Second choice\n')
            batch_path = folder/'answers/batch-001.raw'
            batch_path.write_text(raw)
            batch = board.parse_output(raw, batch_path)
            self.assertTrue(board.is_answer(batch['prompts'][0], 'test'))
            messages = board.messages_in(batch, 'test')
            self.assertEqual([message['prompt'] for message in messages], ['Please clarify'])
            final_path = board.final_answer(folder)
            final = final_path.read_text()
            self.assertEqual(final_path.name, 'final.md')
            self.assertIn('- d1: a; note: ', final)
            self.assertIn('- d2: unanswered', final)
            self.assertIn('uid: 2; selector: article#card-d2 > h3; card: d2', final)
            self.assertIn('Please clarify', final)

    def test_dead_wrapper_takeover_and_budget_across_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            with mock.patch.object(board, 'ROOT', Path(temp)):
                folder = Path(temp)/'b'; (folder/'answers').mkdir(parents=True)
                (folder/'board.html').write_text('x')
                (folder/'answers/budget-start.json').write_text(json.dumps({'started_at':time.time()-70}))
                with mock.patch.object(board, 'poll_pids', return_value=[123]), mock.patch.object(board, 'stop_poll') as stop, redirect_stdout(io.StringIO()) as out:
                    board.wait(type('Args', (), {'board':str(folder),'budget':60,'slice':20,'until':'end'}))
                stop.assert_called_once_with(123, folder.resolve()/'board.html')
                self.assertTrue(out.getvalue().startswith('deadline:'))

    def test_deadline_clears_budget_and_next_wait_polls(self):
        with tempfile.TemporaryDirectory() as temp:
            with mock.patch.object(board, 'ROOT', Path(temp)):
                folder = Path(temp)/'b'; (folder/'answers').mkdir(parents=True)
                (folder/'board.html').write_text('x')
                clock = folder/'answers/budget-start.json'
                clock.write_text(json.dumps({'started_at':time.time()-70}))
                args = type('Args', (), {'board':str(folder),'budget':60,'slice':1,'until':'end'})
                with mock.patch.object(board, 'poll_pids', return_value=[123]), mock.patch.object(board, 'stop_poll') as stop, redirect_stdout(io.StringIO()) as first:
                    board.wait(args)
                stop.assert_called_once_with(123, folder.resolve()/'board.html')
                self.assertIn('deadline:', first.getvalue())
                self.assertFalse(clock.exists())

                process = mock.Mock(pid=456, returncode=0)
                process.wait.side_effect = [board.subprocess.TimeoutExpired('poll', 1), None]
                with mock.patch.object(board, 'poll_pids', return_value=[]), mock.patch.object(board.subprocess, 'Popen', return_value=process) as popen, mock.patch.object(board, 'stop_poll') as stop, redirect_stdout(io.StringIO()) as second:
                    board.wait(args)
                popen.assert_called_once()
                stop.assert_called_once_with(456, folder.resolve()/'board.html')
                self.assertIn('slice: no answer yet', second.getvalue())
                self.assertNotIn('deadline:', second.getvalue())
                self.assertTrue(clock.exists())

    def test_live_wrapper_still_blocks_second_wait(self):
        with tempfile.TemporaryDirectory() as temp:
            with mock.patch.object(board, 'ROOT', Path(temp)):
                folder = Path(temp)/'b'; (folder/'answers').mkdir(parents=True)
                (folder/'board.html').write_text('x')
                with (folder/'answers/wait.lock').open('a+') as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    with self.assertRaisesRegex(SystemExit, 'another worker is already waiting'):
                        board.wait(type('Args', (), {'board':str(folder),'budget':60,'slice':20,'until':'end'}))


if __name__ == '__main__': unittest.main()
