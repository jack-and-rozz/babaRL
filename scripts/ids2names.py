


files = ['NounType.def', 'OpType.def', 'PropertyType.def', 'IconType.def']
files = ['NounType.def', 'OpType.def', 'PropertyType.def', 'IconType.def']
enum_root = 'baba-is-auto/Includes/baba-is-auto/Enums'

import re
obj = []
for fname in files:
    obj += ['<unk>']
    for l in open(enum_root + '/' + fname):
        obj += re.findall("\((.+?)\)", l.strip())

for i, o in enumerate(obj):
    print(o)
