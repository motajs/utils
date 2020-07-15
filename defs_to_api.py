# -*- coding: utf-8 -*-
# Run with py3

import json

with open('test.json') as f:
    content = json.loads(f.read())

result = []

for key in sorted(content.keys()):
    value = content[key]
    result.append('## %s.js\n\n%s\n\n```text\n' % (key, value['!doc'].replace('<br/>', '\n')))
    for funcname in sorted(value.keys()):
        detail = value[funcname]
        if funcname == '!doc' or '!type' not in detail: continue
        result.append(funcname + ': ' + detail['!type']+'\n')
        result.append(detail['!doc'].replace('<br/>', '\n') + '\n')
        if ('!url' in detail):
            result.append('参考资料：' + detail['!url'] + '\n')
        result.append('\n')
    result = result[:-1]
    result.append('```\n\n')

with open('result.txt', 'w') as f:
    f.write(''.join(result))
