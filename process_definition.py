# -*- coding: utf-8 -*-

import re
import json

with open('runtime.d.ts') as f:
    lines = f.readlines()

name = None
comment = None

result = {}

def add_comment(line):
    if name is None or comment is None: return
    line = line.strip()
    if line == '': return
    line = re.sub(r'@param (\w+)', r'\1:', line)
    line = re.sub(r'@example ', '例如：', line)
    comment.append(line)

def process_method(line):
    start = line.find('(')
    end = line.rfind(')')
    content = line[start+1:end]

    # step 1: remove function
    content = content.replace('=>', '->')
    content = content.replace('(', 'fn(')
    # Step 2: remove Array
    content = content.replace('Array<', '[')
    content = re.sub(r'([^-])>', r'\1]', content)

    line = 'fn(' + content + line[end:].replace(':', ' ->')
    line = line.replace(' -> void', '')
    line = line.replace(' -> any', '')
    line = line.replace('any', '?')
    line = line.replace('boolean', 'bool')
    line = line.replace(': direction', ': string')
    line = line.replace(' | ', '|')
    line = re.sub(r' (\'.*?\')([,\)])', r' string\2', line)
    return line

for line in lines:
    line = line.strip()
    if line == '': continue
    match = re.match('^declare class (\w+) {$', line)
    if match is not None:
        name = match.group(1)
        result[name] = {}
        continue
    if name is not None and line == '}': name = None
    if name is None: continue
    if line.startswith('/**'):
        comment = []
        line = line[3:].strip()
        if line.endswith('*/'):
            line = line[:-2].strip()
        add_comment(line)
        continue
    if line == '*/': continue
    if line.startswith('*'):
        add_comment(line[1:])
        continue
    method = line[:line.find('(')]
    result[name][method] = {
        '!type': process_method(line),
        "!doc": '<br/>'.join(comment)
    }

with open('result.js', 'w') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

