from __future__ import print_function, absolute_import

from . import _typeconv


class TypeManager(object):
    def __init__(self):
        self._ptr = _typeconv.new_type_manager()
        self._types = set()

    def select_overload(self, sig, overloads, allow_unsafe):
        sig = [t._code for t in sig]
        overloads = [[t._code for t in s] for s in overloads ]
        return _typeconv.select_overload(self._ptr, sig, overloads, allow_unsafe)

    def check_compatible(self, fromty, toty):
        return _typeconv.check_compatible(self._ptr, fromty._code, toty._code)

    def set_compatible(self, fromty, toty, by):
        _typeconv.set_compatible(self._ptr, fromty._code, toty._code, by)
        # Ensure the types don't die, otherwise they may be recreated with
        # other type codes and pollute the hash table.
        self._types.add(fromty)
        self._types.add(toty)

    def set_promote(self, fromty, toty):
        self.set_compatible(fromty, toty, ord("p"))

    def set_unsafe_convert(self, fromty, toty):
        self.set_compatible(fromty, toty, ord("u"))

    def set_safe_convert(self, fromty, toty):
        self.set_compatible(fromty, toty, ord("s"))

    def get_pointer(self):
        return _typeconv.get_pointer(self._ptr)
