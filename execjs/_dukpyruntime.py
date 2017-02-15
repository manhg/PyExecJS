import json
import contextlib

from execjs._abstract_runtime import AbstractRuntime
from execjs._abstract_runtime_context import AbstractRuntimeContext

try:
    import dukpy
    _dukpy_available = True
except:
    _dukpy_available = False


class DukpyRuntime(AbstractRuntime):

    def __init__(self):
        pass

    @property
    def name(self):
        return "Dukpy"

    def _compile(self, source, cwd=None):
        return self.Context(source)

    def is_available(self):
        return _dukpy_available

    class Context(AbstractRuntimeContext):
        def __init__(self, source=""):
            self._source = source

        def is_available(self):
            return _dukpy_available

        def _exec_(self, source):
            interpreter = dukpy.JSInterpreter()
            return interpreter.evaljs(self._source + source)

        def _eval(self, source):
            return self.exec_(source)

        def _call(self, identifier, *args):
            args = json.dumps(args)
            return self.eval("{identifier}.apply(this, {args})".format(identifier=identifier, args=args))

        @classmethod
        def convert(cls, obj):
            return obj
