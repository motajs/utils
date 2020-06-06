
# %% [markdown]
# # 将defs.js和chrome翻译的defs_cn.js合并
#
# 找出所有 "!doc": 且之后没有中文的行  
# 从_cn中把翻译出的中文替换进来
# %%
import re
import json
#%%

# 全局变量
class g:
    sourceFileName='defs.js'
    targetFileName='defs_cn.js'
    outputFileName='defs_output.js'
    source=['']
    target=['']
    symbol=[
        ['“','"'],
        ['”','"'],
        ['！','!'],
        ['。','.'],
        ['，',','],
        ['：',': '],
        ['？','?'],
        ['（','('],
        ['）',')'],
    ]

def readfiles():
    with open(g.sourceFileName,encoding='utf-8') as fid:
        g.source=fid.read().split('\n')
    with open(g.targetFileName,encoding='utf-8') as fid:
        g.target=fid.read().split('\n')
    assert(len(g.source)==len(g.target))

def preProcessTarget():
    for ii,line in enumerate(g.target):
        for a,b in g.symbol:
            line=b.join(line.split(a))
        g.target[ii]=line

def processLine(s,t):
    o=s
    if re.match(r'^\s*"!doc"\s*:[^\u4e00-\u9fa5]*$',s):
        if re.match(r'.*("|"\s*,)$',t):
            o=t
        else:
            o=t+'",'
        try:
            exec('abcabc={'+o+'}')
        except:
            match=re.match(r'^(\s*"!doc"\s*:)(.*)$',o)
            o=match.group(1)+json.dumps(match.group(2))
    return o

def main():
    readfiles()
    preProcessTarget()
    for lino in range(len(g.source)):
        g.source[lino]=processLine(g.source[lino],g.target[lino])
    with open(g.outputFileName,'w',encoding='utf-8') as fid:
        fid.write('\n'.join(g.source))

if __name__ == "__main__":
    main()