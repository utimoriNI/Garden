#!/usr/bin/env python3
"""Alfred project picker and Daily Note capture; no third-party dependencies."""
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys

KINDS = {'log': ('やったこと', '#📝Log'), 'stuck': ('行き詰まったこと', '#🪨Stack'),
         'task': ('これからやること', '#📎Task')}


def inside(root, relative):
    path = (root / relative).resolve()
    if path != root and root not in path.parents:
        raise ValueError('保存先・プロジェクトはVault内を指定してください。')
    return path


def projects(root, folder, recursive=True):
    directory = inside(root, folder)
    if not directory.is_dir():
        raise ValueError('プロジェクトフォルダがありません: ' + folder)
    paths = directory.rglob('*.md') if recursive else directory.glob('*.md')
    return sorted((p.relative_to(root).with_suffix('').as_posix()
                   for p in paths if p.is_file() and root in p.resolve().parents), key=str.casefold)


def picker(root, kind, query):
    folder = os.environ.get('project_folder', '800_Project/InProgress')
    recursive = os.environ.get('recursive', '1') != '0'
    def item(title, project):
        return {'title': title, 'subtitle': project or KINDS[kind][0] + 'を入力',
                'arg': json.dumps({'kind': kind, 'project': project}, ensure_ascii=False),
                'valid': True}
    items = [item('プロジェクトを指定しない', '')]
    terms = query.casefold().split()
    items += [item(Path(p).name, p) for p in projects(root, folder, recursive)
              if all(term in p.casefold() for term in terms)]
    return {'items': items}


def one_line(text):
    return ' '.join(text.split())


def markdown(kind, project, body, memo, now):
    body, memo = one_line(body), one_line(memo)
    if not body:
        raise ValueError('本文が空欄なので記録しませんでした。')
    if any(c in project for c in ('\n', '\r', '[', ']', '|', '#')):
        raise ValueError('プロジェクト名にリンクで使用できない文字があります。')
    prefix = '- [ ]' if kind == 'task' else '-'
    parts = [prefix, now.strftime('%H:%M')]
    if project:
        parts.append('[[' + project + ']]')
    parts += [KINDS[kind][1], body]
    if kind == 'log' and memo:
        parts.append('／ メモ：' + memo)
    return ' '.join(parts)


def template_content(root, settings, now):
    template = settings.get('template', '')
    if not template:
        return ''
    content = inside(root, template).read_text(encoding='utf-8')
    pattern = r'<%\s*tp\.date\.now\("YYYY-MM-DD",\s*(-?\d+),\s*tp\.file\.title,\s*"YYYY-MM-DD"\)\s*%>'
    content = re.sub(pattern, lambda m: (now + dt.timedelta(days=int(m[1]))).strftime('%Y-%m-%d'), content)
    for token, value in (('{{date}}', now.strftime('%Y-%m-%d')),
                         ('{{time}}', now.strftime('%H:%M')),
                         ('{{title}}', now.strftime('%Y-%m-%d'))):
        content = content.replace(token, value)
    if '<%' in content or '{{' in content:
        raise ValueError('未対応のテンプレート式があります。Obsidianで今日のDaily Noteを先に作成してください。')
    return content


def append_daily(root, line, now):
    settings = json.loads((root / '.obsidian/daily-notes.json').read_text(encoding='utf-8'))
    if settings.get('format', 'YYYY-MM-DD') != 'YYYY-MM-DD':
        raise ValueError('Daily Noteの日付形式はYYYY-MM-DDに対応しています。')
    folder = inside(root, settings.get('folder', ''))
    folder.mkdir(parents=True, exist_ok=True)
    path = inside(root, str(folder.relative_to(root) / (now.strftime('%Y-%m-%d') + '.md')))
    # Serialize this workflow's captures without rewriting existing note content.
    state = Path(os.environ.get('alfred_workflow_data', '~/Library/Application Support/GardenDailyMemo')).expanduser()
    state.mkdir(parents=True, exist_ok=True)
    with (state / 'append.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        initial = template_content(root, settings, now) if not path.exists() else None
        if initial is not None:
            try:
                with path.open('x', encoding='utf-8') as stream:
                    stream.write(initial.rstrip() + '\n' if initial else '')
            except FileExistsError:
                pass
        with path.open('rb') as stream:
            stream.seek(0, 2)
            size = stream.tell()
            stream.seek(max(0, size - 1))
            last = stream.read(1)
        with path.open('a', encoding='utf-8') as stream:
            stream.write(('\n' if size and last != b'\n' else '') + line + '\n')
    return path


PROMPT = '''on run argv
    tell application "System Events"
        activate
        set resultDialog to display dialog (item 1 of argv) with title "Garden Daily Memo" default answer "" buttons {"キャンセル", "記録"} default button "記録" cancel button "キャンセル"
        return text returned of resultDialog
    end tell
end run'''


def prompt(label):
    result = subprocess.run(['/usr/bin/osascript', '-e', PROMPT, label], capture_output=True, text=True)
    if result.returncode:
        if '(-128)' in result.stderr:
            return None
        raise RuntimeError(result.stderr.strip())
    return result.stdout.rstrip('\n')


def capture(root, payload):
    kind, project = payload['kind'], payload.get('project', '')
    label = KINDS[kind][0] + ('\n' + project if project else '')
    body = prompt(label)
    if body is None or not one_line(body):
        return
    memo = prompt('任意のメモ（空欄でも記録できます）') if kind == 'log' else ''
    if memo is None:
        return
    now = dt.datetime.now().astimezone()
    line = markdown(kind, project, body, memo, now)
    path = append_daily(root, line, now)
    print('記録しました：' + path.name)


def main():
    root = Path(os.environ['vault_path']).expanduser().resolve()
    if not root.is_dir():
        raise ValueError('Vaultがありません: ' + str(root))
    if sys.argv[1] == 'pick':
        try:
            output = picker(root, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '')
        except Exception as error:
            output = {'items': [{'title': str(error), 'valid': False}]}
        print(json.dumps(output, ensure_ascii=False))
    else:
        capture(root, json.loads(sys.argv[2]))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('記録できませんでした：' + str(error))
        sys.exit(1)
