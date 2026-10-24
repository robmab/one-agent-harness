"""Credential and close guard for Claude Code (PreToolUse hook): it blocks before it happens.

Usage:
    py -3 guard.py --hook     # run by the hook: reads the tool's JSON from stdin
    py -3 guard.py --test     # self-test

It blocks a URL with user:password@ in terminal commands and in what gets written to files (the gaps
<x>, ***, {x} and $X are fine). In real sessions all three tools did it while testing against a database,
with the rule written in a .md: a check beats a sentence. The other tools have no hook; there the router
and the sensor cover it.

And launching the reviewer, or asking about the retro, before the user has closed: it looks at their last 3
messages (and what they answered with the question tool) in the session's log; if it can't find it, it lets
it through. With only the last message it blocked the retro question when the user, already closed, asked
something else first. In real sessions the agent launched it at the end of every task, with the rule in
the router. It also reads Copilot CLI's payload (toolName, toolArgs, sessionId), if you hook it there.
With HARNESS_UNATTENDED=1 (factory/intake.py sets it) the close check is off: there's no user to say
"closing", and the task already says when to close. Credentials are still blocked.
"""
import json
import os
import re
import sys

URL_WITH_PASSWORD = re.compile(r'\b[a-z][a-z0-9+.-]*://[^\s:/@"\'`]+:(?!\*+@|<[^>]*>@|\{[^}]*\}@|\$\w+@)[^\s@"\'`/]+@')
NOTICE = ('guard: blocked, it carries a URL with a user and a password. Read the connection from the project\'s '
          'config without printing it (at most the database name). If it really has to be done, ask the user to do it.')
# what the user says when closing: "I'm closing", "let's wrap up", "we're done", "commit", "PR", "review it"
CLOSING = re.compile(r'clos|wrap|finish|done|commit|\bpr\b|pull request|review', re.I)
NO_ATTACHMENTS = re.compile(r'<(?:system[-_])?reminder>|<current_datetime>')
NOTICE_CLOSE = ('guard: blocked, {what} before the user has closed the session. The reviewer and the retro question '
                'go only in the close, when the user says so (or asks before a commit or PR). Carry on with your work.')


def args(event):
    """The tool's arguments, from Claude (tool_input) or Copilot CLI (toolArgs, sometimes as JSON text)."""
    t = event.get('tool_input') or event.get('toolArgs') or {}
    if isinstance(t, str):
        try:
            t = json.loads(t)
        except ValueError:
            t = {'command': t}
    return t if isinstance(t, dict) else {}


def texts(event):
    """What the tool is about to run or write."""
    t = args(event)
    out = [t.get(k) for k in ('command', 'content', 'new_string', 'new_str', 'file_text') if isinstance(t.get(k), str)]
    out += [e.get('new_string', '') for e in t.get('edits') or [] if isinstance(e, dict)]
    return out


def blocked(event):
    return any(URL_WITH_PASSWORD.search(t) for t in texts(event))


def tool(event):
    return event.get('tool_name') or event.get('toolName') or ''


def is_reviewer(event):
    t = args(event)
    return tool(event) in ('Agent', 'Task', 'task') and 'reviewer' in (t.get('subagent_type') or t.get('agent_type') or '')


def is_retro_question(event):
    return (tool(event) in ('AskUserQuestion', 'ask_user')
            and bool(re.search(r'\bretro\b', json.dumps(args(event), ensure_ascii=False), re.I)))


def users_last(event):
    """Their last 3 messages and what they answered with the question tool; None if there's no log."""
    sid = event.get('sessionId')
    path = event.get('transcript_path') or (sid and os.path.expanduser(f'~/.copilot/session-state/{sid}/events.jsonl'))
    if not path or not os.path.exists(path):
        return None
    messages, questions = [], set()
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            d = e.get('data') or {}
            if e.get('type') == 'user' and not e.get('isSidechain'):   # Claude: their text, or answers to questions
                c = (e.get('message') or {}).get('content')
                if isinstance(c, str):
                    messages.append(c)
                elif isinstance(c, list) and any(p.get('type') == 'text' for p in c if isinstance(p, dict)):
                    messages.append(' '.join(p.get('text', '') for p in c if isinstance(p, dict) and p.get('type') == 'text'))
                elif isinstance(e.get('toolUseResult'), dict) and 'answers' in e['toolUseResult'] and messages:
                    messages[-1] += '\n' + json.dumps(e['toolUseResult']['answers'], ensure_ascii=False)
            elif e.get('type') == 'user.message' and not d.get('source'):   # Copilot CLI; with source, a subagent's brief
                messages.append(d.get('content') or '')
            elif e.get('type') == 'tool.execution_start' and d.get('toolName') == 'ask_user':
                questions.add(d.get('toolCallId'))
            elif e.get('type') == 'tool.execution_complete' and d.get('toolCallId') in questions and messages:
                messages[-1] += '\n' + str((d.get('result') or {}).get('content', ''))
    # without the attachments the tool pastes after them (<reminder>…): any word there would count as closing
    return '\n'.join(NO_ATTACHMENTS.split(m)[0] for m in messages[-3:]) if messages else None


def too_early(event, last=None):
    what = 'launching the reviewer' if is_reviewer(event) else 'asking about the retro' if is_retro_question(event) else None
    if not what or os.environ.get('HARNESS_UNATTENDED') == '1':   # a factory session: the task says when to close
        return None
    last = users_last(event) if last is None else last
    return None if last is None or CLOSING.search(last) else what


def hook_mode():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    early = too_early(event)
    notice = NOTICE if blocked(event) else NOTICE_CLOSE.format(what=early) if early else None
    if notice:
        print(notice, file=sys.stderr)
        # 2 blocks in both: Claude passes stderr to the model; Copilot CLI, the permissionDecisionReason
        print(json.dumps({'permissionDecision': 'deny', 'permissionDecisionReason': notice}))
        return 2
    return 0


def selftest():
    secret = 'se' + 'cret'   # built on the fly: this file carries no credential
    url = 'postgresql://app:' + secret + '@localhost:5432/db'
    cases = [
        ({'tool_input': {'command': f'psql "{url}"'}}, True),
        ({'tool_input': {'content': f"DSN = '{url}'\n"}}, True),
        ({'tool_input': {'edits': [{'new_string': f'x = "{url}"'}]}}, True),
        ({'tool_input': {'content': 'url = "postgresql://<user>:<password>@host/db"'}}, False),
        ({'tool_input': {'content': 'url = "postgresql://app:***@host/db"'}}, False),
        ({'tool_input': {'command': 'git log --oneline -5'}}, False),
    ]
    failures = [f'case {i}: expected {"block" if expect else "pass"}' for i, (e, expect) in enumerate(cases, 1)
                if blocked(e) != expect]
    # the close: (tool, the user's last words, does it block?)
    reviewer = {'tool_name': 'Agent', 'tool_input': {'subagent_type': 'reviewer', 'prompt': 'Scope: …'}}
    retro = {'tool_name': 'AskUserQuestion', 'tool_input': {'questions': [{'question': 'Do you want a retro?'}]}}
    close = [
        (reviewer, 'and drop the icon', True),
        (reviewer, "ok, let's wrap up", False),
        (retro, 'make the column wider', True),
        (retro, "I'm closing the session", False),
        (reviewer, None, False),   # no log: lets it through
        ({'tool_name': 'Agent', 'tool_input': {'subagent_type': 'general-purpose'}}, 'hi', False),
    ]
    failures += [f'close {i}: expected {"block" if expect else "pass"}' for i, (e, last, expect) in enumerate(close, 1)
                 if bool(too_early(e, last)) != expect]
    os.environ['HARNESS_UNATTENDED'] = '1'   # a factory session: the reviewer passes with no "closing"
    failures += [] if too_early(reviewer, 'and drop the icon') is None else ['unattended: expected pass']
    del os.environ['HARNESS_UNATTENDED']
    print('\n'.join(failures) if failures else f'selftest OK: {len(cases) + len(close) + 1} cases')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(selftest() if '--test' in sys.argv else hook_mode())
