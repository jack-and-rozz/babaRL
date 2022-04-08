import pyBaba
import config

import re

def _name(baba_def):
    # X(ALGAE) -> ALGAE
    m = re.match("X\(([A-Z]+)\)", baba_def.strip())
    if m:
        return m.group(1)

icon_id2name = dict([
    (getattr(pyBaba.ObjectType, "ICON_" + _name(l)), _name(l))
    for l in open(config.ENUM_ROOT + '/NounType.def')
    if hasattr(pyBaba.ObjectType, "ICON_" + _name(l))
])


text_id2name = [
    (getattr(pyBaba.ObjectType, _name(l)), _name(l))
    for l in open(config.ENUM_ROOT + '/NounType.def')
    if hasattr(pyBaba.ObjectType, _name(l))
]
text_id2name += [
    (getattr(pyBaba.ObjectType, _name(l)), _name(l))
    for l in open(config.ENUM_ROOT + '/OpType.def')
    if hasattr(pyBaba.ObjectType, _name(l))
]
text_id2name += [
    (getattr(pyBaba.ObjectType, _name(l)), _name(l))
    for l in open(config.ENUM_ROOT + '/PropertyType.def')
    if hasattr(pyBaba.ObjectType, _name(l))
]
text_id2name = dict(text_id2name)

# icon_id2name = {
#     pyBaba.ObjectType.ICON_BABA: 'BABA',
#     pyBaba.ObjectType.ICON_DOOR: 'DOOR',
#     pyBaba.ObjectType.ICON_FLAG: 'FLAG',
#     pyBaba.ObjectType.ICON_GHOST: 'GHOST',
#     pyBaba.ObjectType.ICON_GRASS: 'GRASS',
#     pyBaba.ObjectType.ICON_KEY: 'KEY',
#     pyBaba.ObjectType.ICON_LAVA: 'LAVA',
#     pyBaba.ObjectType.ICON_ROCK: 'ROCK',
#     pyBaba.ObjectType.ICON_TILE: 'TILE',
#     pyBaba.ObjectType.ICON_WATER: 'WATER',
#     pyBaba.ObjectType.ICON_WALL: 'WALL',

# }

# text_id2name = {
#     pyBaba.ObjectType.BABA: 'BABA',
#     pyBaba.ObjectType.IS: 'IS',
#     pyBaba.ObjectType.YOU: 'YOU',
#     pyBaba.ObjectType.FLAG: 'FLAG',
#     pyBaba.ObjectType.GHOST: 'GHOST',
#     pyBaba.ObjectType.WIN: 'WIN',
#     pyBaba.ObjectType.DEFEAT: 'DEFEAT',
#     pyBaba.ObjectType.WALL: 'WALL',
#     pyBaba.ObjectType.STOP: 'STOP',
#     pyBaba.ObjectType.ROCK: 'ROCK',
#     pyBaba.ObjectType.PUSH: 'PUSH',
#     pyBaba.ObjectType.WATER: 'WATER',
#     pyBaba.ObjectType.SINK: 'SINK',
#     pyBaba.ObjectType.LAVA: 'LAVA',
#     pyBaba.ObjectType.MELT: 'MELT',
#     pyBaba.ObjectType.HOT: 'HOT',
#     pyBaba.ObjectType.SHUT: 'SHUT',
#     pyBaba.ObjectType.OPEN: 'OPEN',
#     pyBaba.ObjectType.TELE: 'TELE',
#     pyBaba.ObjectType.MOVE: 'MOVE',
#     pyBaba.ObjectType.SHIFT: 'SHIFT',
# }

direction_id2name = {
    pyBaba.Direction.UP: 'upArrow',
    pyBaba.Direction.DOWN: 'downArrow',
    pyBaba.Direction.RIGHT: 'rightArrow',
    pyBaba.Direction.LEFT: 'leftArrow',
}

object_id2name = [l.strip() for l in open('./objects.list')]
