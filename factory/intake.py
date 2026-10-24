"""Factory intake (OPTIONAL): turns new tickets into unattended sessions, each one in its own branch.

Without it nothing changes: you open each session by hand (manual, the default). With it, every few minutes
(Task Scheduler or cron, see docs/FACTORY.md) it takes the new tickets with LABEL, gives each one a worktree
with its branch ai/<id> and runs your tool there without a window, with the whole harness. Where it stops:
- before-code: the diagnosis and the questions prepare would ask, without touching code (the default);
- after-review: it builds, runs the reviewer and fixes, and leaves the branch for you to approve.
Each session leaves its report in factory/reports/<id>.md. The commit, as always, is yours.

Usage (from the repo):
    py -3 <HARNESS>/factory/intake.py [--stop before-code|after-review] [--tool copilot|claude|opencode]
                                      [--max 3] [--dry-run]
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(HERE, 'reports')
STATE = os.path.join(HERE, 'state.json')
# FILL-IN: the label that lets a ticket in. You choose which ones: clear and small
LABEL = 'ai'
# The tool without a window. It can't ask for permission, so it gets it up front, minus what only the user does.
# The guard (hooks) still blocks credentials. Claude: add --allowedTools for the commands your checks need.
TOOLS = {
    'copilot': ['copilot', '-p', '{prompt}', '--allow-all-tools', '--deny-tool', 'shell(git push)',
                '--deny-tool', 'shell(git commit)', '--deny-tool', 'shell(git branch)', '--deny-tool', 'shell(git checkout)'],
    'claude': ['claude', '-p', '{prompt}', '--permission-mode', 'acceptEdits'],
    'opencode': ['opencode', 'run', '{prompt}'],
}
STOPS = {
    'before-code': ('Stop BEFORE writing code. Find the cause or the files involved (diagnose) and the questions '
                    'prepare would ask: the report is the deliverable.'),
    'after-review': ('Build it, then close as closing.md says: reviewer, fixes, the findings table and the commit '
                     'message. Skip the retro question: end the report with "Retro: pending, ask it when the user '
                     'approves this branch".'),
}
TASK = """# Ticket {id}: {title}

{body}

---
Unattended session from the factory (factory/intake.py): no one is reading. Don't use question tools: when you'd
ask, write the question in the report and go on with your best assumption, marked as such (or stop, if it blocks).
{stop}
When you're done, write the report to {report}: what you did, what you checked and what not, the open questions,
the tool and the session id. Never commit, push or touch other branches: the user approves.
"""


def fetch_tickets():
    """FILL-IN: the open tickets with LABEL, as [{'id', 'title', 'body'}]. The example: GitHub issues, with gh."""
    out = subprocess.run(['gh', 'issue', 'list', '--label', LABEL, '--state', 'open', '--json', 'number,title,body'],
                         capture_output=True, text=True, encoding='utf-8', check=True).stdout
    return [{'id': str(i['number']), 'title': i['title'], 'body': i.get('body') or ''} for i in json.loads(out)]


def load_state():
    if not os.path.isfile(STATE):
        return {}
    with open(STATE, encoding='utf-8') as f:
        return json.load(f)


def save_state(state):
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def worktree(repo, tid):
    """A copy of the repo in its own branch, next to it: the session never touches your checkout."""
    path = os.path.join(os.path.dirname(repo), f'{os.path.basename(repo)}-ai-{tid}')
    subprocess.run(['git', '-C', repo, 'worktree', 'add', '-b', f'ai/{tid}', path],
                   capture_output=True, text=True, check=True)
    return path


def run(tool, task_path, cwd, log_path):
    """The prompt only points at the task file: a long text with line breaks gets mangled by .cmd shims."""
    prompt = f'Your task is in {task_path}: read it and follow it.'
    cmd = [a.replace('{prompt}', prompt) for a in TOOLS[tool]]
    cmd[0] = shutil.which(cmd[0]) or cmd[0]
    env = dict(os.environ, HARNESS_UNATTENDED='1')   # the guard lets the reviewer run without a "closing" message
    with open(log_path, 'w', encoding='utf-8') as log:
        return subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT).returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default=os.getcwd())
    ap.add_argument('--stop', choices=sorted(STOPS), default='before-code')
    ap.add_argument('--tool', choices=sorted(TOOLS), default='copilot')
    ap.add_argument('--max', type=int, default=3, help='tickets per run, one after the other (default 3)')
    ap.add_argument('--dry-run', action='store_true', help='lists what it would take and touches nothing')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    repo, state = os.path.abspath(a.repo), load_state()
    new = [t for t in fetch_tickets() if t['id'] not in state][:a.max]
    if not new:
        print('No new tickets.')
        return 0
    os.makedirs(REPORTS, exist_ok=True)
    for t in new:
        if a.dry_run:
            print(f'would take #{t["id"]}: {t["title"]}')
            continue
        report = os.path.join(REPORTS, f'{t["id"]}.md')
        task_path = os.path.join(REPORTS, f'{t["id"]}.task.md')
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(TASK.format(id=t['id'], title=t['title'], body=t['body'], stop=STOPS[a.stop], report=report))
        try:
            cwd = worktree(repo, t['id'])
        except subprocess.CalledProcessError as e:   # the branch already exists, or it isn't a repo: skip it
            print(f'#{t["id"]}: no worktree ({e.stderr.strip()})')
            continue
        code = run(a.tool, task_path, cwd, os.path.join(REPORTS, f'{t["id"]}.log'))
        if not os.path.isfile(report):
            with open(report, 'w', encoding='utf-8') as f:
                f.write(f'# Ticket {t["id"]}\n\nThe session left no report (exit {code}): see {t["id"]}.log\n')
        state[t['id']] = {'date': datetime.date.today().isoformat(), 'stop': a.stop, 'tool': a.tool,
                          'branch': f'ai/{t["id"]}', 'worktree': cwd, 'exit': code}
        save_state(state)
        print(f'#{t["id"]} -> {report}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
