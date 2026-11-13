# Decision boards

Read when: a project sends an important decision with two or more options to a board, or you build or wait on one. A board is a local page where the user picks an option for each decision and sends the answers. `tools/lavish_board.py` runs it on the installed `lavish-axi` tool, at the path the tool reports. Set `LAVISH_AXI_BIN` to use a different install.
Reader: coordinator.

## Rule

- The project says whether boards are on and which decisions are important. With boards on, an important decision with two or more options goes on a board. The selector (`communication.md`) stays for small and yes/no questions and is the fallback.
- The build worker owns board content. It decides the questions, options, recommendations, briefs, details and mocks. The coordinator gives the topic and what needs a decision, then waits for answers itself. Only the build worker runs `doctor`, `build` and `open`.
- One board holds one batch. Collect the decisions that wait on the user, group them by topic, open one board. Open a new board when the topic changes or the last board has ended.
- The browser is the project value `overlay.board-browser`. A project without it uses the T3 preview only.

## Sequence

1. **Coordinator:** write the route line. Give the build worker the topic, what needs a decision, the user's verbatim request, the project browser value and the kit path. Delegate with `mode: async` and keep the `taskId`.
2. **Build worker:** write the payload and mocks. Run `doctor` and `build`. Open the board in the project browser and in the T3 preview when its tools allow. Leave the server and session open. Return the board folder, session URL, and one line per decision with its id and question. Never run `wait`.
3. **Coordinator:** post "Board ready" with the board address and `[title](t3-thread://v1/<childThreadId>)` of the build worker. Add "Waiting on you: board <title>" to the dashboard. In the same turn, run the command below as a background Bash call with `run_in_background: true` and `timeout: 7200000`.
4. **User:** choose options, add notes, press **Queue all chosen**, then **Send & End**. **Send** alone does not end the board.
5. **Coordinator:** when the background call exits, handle its output as described below. Map option ids to labels from `/tmp/lavish-boards/payload-<id>.json`. Check that every decision id is answered, `defer` or `unanswered`. Record each decision at its project home. Clear the dashboard line. Put `unanswered` and `defer` decisions on the next board or the selector.

```bash
python3 <kit>/tools/lavish_board.py wait /tmp/lavish-boards/<id> --until end --slice 7000 --budget 7000
```

Use this exact command form for the coordinator's Bash guard. Put no flag between `python3` and the script. The guard rejects environment prefixes, redirects, `&`, `$()` and newlines. The coordinator runs only `wait` and `close`. The build worker runs `doctor`, `build`, `update` and `open`. The build worker owns `open` because the guard cannot restrict what it opens.

- `ended:` gives the `answers/final.md` path and the answers. Run `python3 <kit>/tools/lavish_board.py close /tmp/lavish-boards/<id>`. Then read and record the answers.
- `message:` gives a free message. Handle it, then run the same background `wait` call again.
- `deadline: board stays open; run wait again for late answers` means the budget ran out. Tell the user that the board stays open. Run `wait` again only on request.
- `slice: no answer yet` means a slice ended first. With the equal slice and budget above, one call waits until an answer or the deadline.

The tool prints one status word first. `wait` prints `slice:` (no answer yet), `message:` (a free message from the board, followed by its text), `ended:` (path of `answers/final.md`, then its text), `deadline:` or `blocked:`. `final.md` lists `- <id>: <option id>; note: <text>` or `- <id>: unanswered`. A `defer` selection means the user chose "Decide later / need more input".

## Temporary boards

Boards live in `/tmp/lavish-boards/`, never in the repository. `close` ends a board but keeps its files. Each `build` sweeps ended boards whose `answers/final.md` is older than 7 days. The build worker can run `python3 -B <kit>/tools/lavish_board.py purge --dry-run` to review candidates, then `purge` to remove them manually. The coordinator records each decision at its home before 7 days pass.

## Payload

Write `/tmp/lavish-boards/payload-<id>.json`. `build` creates the board folder `/tmp/lavish-boards/<id>/` and refuses an existing one, so a new board needs a new `id`.

- Board: `id` (letters, digits, `_`, `-`; at most 64), `title`, optional `context` (one string, at most 600 characters, the header), `groups` (`id`, `title`), `decisions`, optional `layout` (`deck` by default, or `list`).
- Decision: `id`, `group`, `title`, `question` (at most 200 characters), required one-line `brief` (1 to 350 characters), optional `detail` (at most 1200 characters), `options` (at least two: `id`, `label`, `summary` at most 140 characters, optional `detail` at most 300 characters), `recommended` (an option `id`), `recommendation_reason` (at most 200 characters), `consequence` (at most 200 characters).
- Optional `mocks`: one to three objects with `file`, `caption` (at most 120 characters), and required `alt` (at most 200 characters). `file` is a PNG, JPEG or SVG under `/tmp/lavish-boards/`, at most 200 KB. The builder checks its content, copies it into the board's `assets/` folder and embeds it in the page.
- The option ids `defer` and `other` are reserved. The template adds "Decide later / need more input" and "Other: I write my own answer" to every card. Other requires a nonblank note before the answer can be queued.
- The build worker writes this content from the decision need. The coordinator does not write options. The payload holds no external URL; `build` refuses one.

## Writing a card

Name the decision in the title. In two or three short sentences, use the brief to say what the user decides and why now. Make each option summary show the concrete shape of that option. Show costs as clearly as benefits. Put the recommendation reason on the card, outside the brief. Put long evidence in `detail`, where the user can expand it.

For a visual decision, provide one mock per option or one image that compares the options. Author each mock as a self-contained SVG file under `/tmp/lavish-boards/mocks-<id>/`. Give it a `viewBox`, use text of at least 14 px and keep all references local to the SVG. Check that the SVG renders before you build the board.

## Build brief

Copy this brief and fill the angle brackets. Give the worker only these five inputs.

```
Topic: <topic>
Decisions needed: <what needs a decision>
User's request, verbatim: <the user's words>
Project browser value: <overlay.board-browser or none>
Kit path: <absolute path>
```

## Build worker

Run from the project folder, with the kit path from the brief.

1. Choose the board id, questions, options, recommendations, briefs, details and mocks. Write `/tmp/lavish-boards/payload-<id>.json`. For a visual decision, check each mock before the build.
2. Run `python3 -B <kit>/tools/lavish_board.py doctor`, then `python3 -B <kit>/tools/lavish_board.py build /tmp/lavish-boards/payload-<id>.json`. The tool sets telemetry off, host `127.0.0.1`, no browser launch and port 43871 itself. `build` prints the folder, session URL and listening sockets.
3. With a browser value, run `open -a "<browser>" "<session URL>"` (macOS). Also call `preview_open` and `preview_snapshot` when the T3 preview tools allow. The preview may report `visible:false`; the browser is the route to the user.
4. Leave the server and session open. Put the evidence report in the project's folder for reports. Return `done`, the board folder, session URL, and one line per decision with its id and question. Never run `wait`.
5. If `doctor`, `build` or the browser step fails, run `python3 -B <kit>/tools/lavish_board.py close /tmp/lavish-boards/<id>` if `build` ran. Return `blocked: board unavailable: <reason>`. A project with no browser value uses the preview only.

## Update

The build worker can revise an open board with `python3 -B <kit>/tools/lavish_board.py update /tmp/lavish-boards/<id> <payload> --message "<short reply>"`. The `--message` text appears on the board with the revision. The coordinator sends the user's message to the build worker when a revision needs new content.

## Failure cases

- **Board unavailable** (`doctor`, `build` or the browser step failed): the build worker returns `blocked: board unavailable: <reason>`. The coordinator has a worker render the same content with `html_preview` and `html_render` (read-only), then puts the decisions on the selector. The user does not choose the mechanism. Untested: no fallback run exists.
- **No answer before the 7000-second deadline:** tell the user the board stays open. Queued answers survive. Run `wait` again only on request. A stopped and restarted server was tested; a full 7000-second wait was not.
- **Background call fails or returns unexpected output:** report the exit code and output. Do not start another worker to poll.
- **Send & End did not arrive** (the user pressed it while the server was offline): ask the user to press it again. The second press arrived in the test (task brief; no log file records either press).
- **A choice not queued:** Lavish sends only queued answers. The page shows "N chosen but not queued". The choice would come back as `unanswered`. Not tested with a real send.
- **Two waits on one board:** the second exits with `blocked: another worker is already waiting on this board`. Keep one background call per board.

## Limits

The board flow was tested on one machine, with the unit tests in `tests/test_lavish_board.py` and manual runs in T3 Code. Rules above hold only if the board flow is retested after a change.
