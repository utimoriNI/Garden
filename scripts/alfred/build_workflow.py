#!/usr/bin/env python3
"""Build an importable Alfred workflow. Does not modify Alfred preferences."""
import pathlib
import plistlib
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
objects, connections, positions = [], {}, {}
for index, (kind, title) in enumerate((('log', '作業ログ'), ('stuck', '行き詰まり'), ('task', 'Task'))):
    uid = 'PICK-' + kind
    objects.append({'uid': uid, 'type': 'alfred.workflow.input.scriptfilter', 'version': 3,
                    'config': {'keyword': kind, 'withspace': True, 'argumenttype': 1,
                               'title': title + 'をDaily Noteへ記録', 'subtext': 'プロジェクトを検索してEnter',
                               'runningsubtext': 'プロジェクトを検索中…',
                               'script': '/usr/bin/python3 daily_memo.py pick ' + kind + ' "$1"',
                               'type': 0, 'scriptargtype': 1, 'escaping': 102,
                               'alfredfiltersresults': False, 'queuedelaymode': 0,
                               'queuedelaycustom': 0, 'queuemode': 1}})
    connections[uid] = [{'destinationuid': 'CAPTURE', 'modifiers': 0, 'modifiersubtext': '', 'vitoclose': False}]
    positions[uid] = {'xpos': 30, 'ypos': 50 + index * 150}
objects.append({'uid': 'CAPTURE', 'type': 'alfred.workflow.action.script', 'version': 2,
                'config': {'script': '/usr/bin/python3 daily_memo.py capture "$1"', 'type': 0,
                           'scriptargtype': 1, 'escaping': 102, 'concurrently': False, 'scriptfile': ''}})
objects.append({'uid': 'NOTIFY', 'type': 'alfred.workflow.output.notification', 'version': 1,
                'config': {'title': 'Garden Daily Memo', 'text': '{query}', 'onlyshowifquerypopulated': True,
                           'removeextension': False, 'lastpathcomponent': False}})
connections['CAPTURE'] = [{'destinationuid': 'NOTIFY', 'modifiers': 0, 'modifiersubtext': '', 'vitoclose': False}]
positions.update({'CAPTURE': {'xpos': 350, 'ypos': 200}, 'NOTIFY': {'xpos': 650, 'ypos': 200}})
data = {'name': 'Garden Daily Memo', 'bundleid': 'local.garden.daily-memo', 'version': '1.0.0',
        'createdby': 'Garden', 'description': 'プロジェクトを選び、作業ログ・行き詰まり・TaskをDaily Noteへ追記',
        'category': 'Productivity', 'disabled': False, 'objects': objects, 'connections': connections,
        'uidata': positions, 'variables': {'vault_path': str(HERE.parent.parent),
                                          'project_folder': '800_Project/InProgress', 'recursive': '1'},
        'readme': (HERE / 'README.md').read_text(encoding='utf-8'), 'webaddress': ''}
destination = HERE / 'Garden Daily Memo.alfredworkflow'
with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('info.plist', plistlib.dumps(data))
    archive.write(HERE / 'daily_memo.py', 'daily_memo.py')
    archive.write(HERE / 'README.md', 'README.md')
print(destination)
