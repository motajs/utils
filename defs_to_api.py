# -*- coding: utf-8 -*-

import json

with open('test.json') as f:
    content = json.loads(f.read())

result = []
for key, value in content.items():
    result.append('========== ' + key + ' ==========\n\n')
    for funcname, detail in value.items():
        if funcname == '!doc' or '!type' not in detail: continue
        result.append(funcname + ': ' + detail['!type']+'\n')
        result.append(detail['!doc'].replace('<br/>', '\n') + '\n')
        if ('!url' in detail):
            result.append('参考资料：' + detail['!url'] + '\n')
        result.append('\n')

with open('result.txt', 'w') as f:
    f.write(''.join(result))
