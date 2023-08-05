from collections import *
from pyrser import fmt
from pyrser.type_system.fun import *
from pyrser.error import *


# for type translation
class Translator:
    def __init__(self, fun: Fun, notify: Notification=None):
        if not isinstance(fun, Fun):
            raise TypeError("1st parameter must be a type_system.Fun")
        if not isinstance(notify, Notification):
            raise TypeError("2nd parameter must be a error.Notification")
        if fun.arity < 1:
            raise TypeError("type_system.Fun in 1st parameter must have an arity >= 1 (here %d)" % fun.arity)
        self._type_source = fun.this_type
        self._type_target = fun.return_type
        self._fun = fun
        self._notify = notify

    def __hash__(self) -> str:
        return self._type_target.__hash__()

    @property
    def source(self) -> str:
        return self._type_source

    @property
    def target(self) -> str:
        return self._type_target

    @property
    def fun(self) -> Fun:
        return self._fun

    @property
    def notify(self) -> Notification:
        return self._notify

    def to_fmt(self, with_from=False) -> fmt.indentable:
        """
        Return a Fmt representation of Translator for pretty-printing
        """
        txt = fmt.sep("\n", [
            fmt.sep(" ", [self._type_source, "to", self._type_target, '=', self._fun.to_fmt()]),
            self._notify.get_content(with_from)
        ])
        return txt

    def __repr__(self) -> str:
        return str(self.to_fmt())


class MapTargetTranslate(dict):
    def __init__(self):
        self._internal = {}
        self._type_source = None

    @property
    def key(self) -> str:
        return self._type_source

    def to_fmt(self, with_from=False) -> fmt.indentable:
        txt = fmt.block('{\n', '\n}', [])
        items = fmt.sep('\n---\n', [])
        for k in sorted(self._internal.keys()):
            items.lsdata.append(fmt.sep(': ', [k, fmt.tab([self._internal[k].to_fmt(with_from)])]))
        txt.lsdata.append(fmt.tab([items]))
        return txt

    def __repr__(self) -> str:
        return str(self.to_fmt())

    def __len__(self) -> int:
        return len(self._internal)

    def __delitem__(self, key: str):
        del self._internal[key]

    def __contains__(self, key: str) -> bool:
        return key in self._internal

    def __iter__(self) -> iter:
        return iter(self._internal)

    def __reversed(self) -> reversed:
        return reversed(self._internal)

    def __getitem__(self, key: str) -> Translator:
        return self._internal[key]

    def __setitem__(self, key: str, val: Translator):
        if not isinstance(val, Translator):
            raise TypeError("value must be a Translator")
        if key != val.target:
            raise KeyError("Key:%s != Translator:%s, bad key of Translator" % (key, val.target))
        if self._type_source is None:
            self._type_source = val.source
        elif self._type_source != val.source:
            raise KeyError("Map.source:%s != Translator.source:%s, Translator incompatible with map" % (self._type_source, val._type_source))
        self._internal[key] = val


# forward just for annotation (not the same id that final type)
class MapSourceTranslate:
    pass


class MapSourceTranslate(dict):
    def __init__(self):
        self._internal = ChainMap()

    def set_parent(self, parent: MapSourceTranslate):
        tmp = self._internal
        self._internal = parent._internal.new_child()
        self._internal.maps[0].update(tmp)

    def to_fmt(self, with_from=False) -> fmt.indentable:
        txt = fmt.block('{\n', '\n}', [])
        items = fmt.sep('\n---\n', [])
        for k in sorted(self._internal.keys()):
            items.lsdata.append(fmt.sep(': ', [k, fmt.tab([self._internal[k].to_fmt(with_from)])]))
        txt.lsdata.append(fmt.tab([items]))
        return txt

    def __repr__(self) -> fmt.indentable:
        return str(self.to_fmt())

    def __len__(self) -> int:
        return len(self._internal)

    def __delitem__(self, key: str):
        del self._internal[key]

    def __contains__(self, key: str or tuple) -> bool:
        if isinstance(key, str):
            return key in self._internal
        if isinstance(key, tuple):
            return (key[0] in self._internal
                    and key[1] in self._internal[key[0]]
                    )
        raise TypeError("parameter must be str or tuple")

    def __iter__(self) -> iter:
        return iter(self._internal)

    def __reversed(self) -> reversed:
        return reversed(self._internal)

    def addTranslator(self, val: Translator, as_global=False):
        if not isinstance(val, Translator):
            raise TypeError("value must be a Translator")
        t1 = val.source
        t2 = val.target
        current_map = self._internal
        if as_global:
            current_map = self._internal.maps[-1]
        if t1 not in current_map:
            current_map[t1] = MapTargetTranslate()
        if t2 in current_map[t1]:
            raise KeyError("Mapping %s to %s already exist" % (t1, t2))
        current_map[t1][t2] = val

    def __getitem__(self, key: str) -> MapTargetTranslate:
        if key not in self._internal:
            self._internal[key] = MapTargetTranslate()
        return self._internal[key]

    def __setitem__(self, key: str, val: MapTargetTranslate):
        if not isinstance(val, MapTargetTranslate):
            raise TypeError("value must be a MapTargetTranslate")
        if key != val.key:
            raise KeyError("Key:%s != Translator:%s, bad key of Translator" % (key, val.key))
        if val._type_source is None:
            val._type_source = key
        elif val._type_source != key:
            raise KeyError("MapSource.key:%s != MapTarget.source:%s, MapTarget incompatible with key" % (key, val._type_source))
        self._internal[key] = val
