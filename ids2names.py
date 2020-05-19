


files = ['NounType.def', 'OpType.def', 'PropertyType.def', 'IconType.def']
enum_root = 'baba-is-auto/Includes/baba-is-auto/Enums'

import re
obj = []
for fname in files:
    for l in open(enum_root + '/' + fname):
        obj += re.findall("\((.+?)\)", l.strip())

# print(obj)
obj.insert(0, '')
print(obj[4], obj[67], obj[77])
