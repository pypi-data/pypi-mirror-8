import imp
import logging
import sys

from ..api.common import SessionHook, DecodeHook
from ..compat import NUM_TYPES, IS_PYTHON3


logger = logging.getLogger(__name__)
debug, warn = (logger.debug, logger.warn,)

if IS_PYTHON3:
    basestring = str

class ScriptHost(object):
    """
    Plugin that provides the 'python' feature, emulating an environment for
    python code similar to the one provided by python-vim bindings.
    """
    def __init__(self, nvim):
        self.provides = ['python']
        self.nvim = nvim
        # context where all code will run
        self.module = imp.new_module('__main__')
        nvim.script_context = self.module
        # it seems some plugins assume 'sys' is already imported, so do it now
        exec('import sys', self.module.__dict__)
        sys.modules['vim'] = nvim.with_hook(LegacyEvalHook())
        if IS_PYTHON3:
            sys.modules['vim'] = sys.modules['vim'].with_hook(DecodeHook(encoding=nvim.options['encoding'].decode('ascii')))
        self.legacy_vim = sys.modules['vim']

    def python_execute(self, script, range_start, range_end):
        self._set_current_range(range_start, range_end)
        exec(script, self.module.__dict__)

    def python_execute_file(self, file_path, range_start, range_end):
        self._set_current_range(range_start, range_end)
        with open(file_path) as f:
            script = compile(f.read(), file_path, 'exec')
            exec(script, self.module.__dict__)

    def _set_current_range(self, range_start, range_end):
        self.legacy_vim.current.range = \
                self.legacy_vim.current.buffer.range(range_start, range_end)

    def python_do_range(self, start, stop, code):
        nvim = self.nvim
        start -= 1
        stop -= 1
        fname = '_vim_pydo'

        # Python3 code (exec) must be a string, mixing bytes with
        # function_def would use bytes.__repr__ instead
        if isinstance and isinstance(code, bytes):
            code = code.decode(nvim.options['encoding'].decode('ascii'))
        # define the function
        function_def = 'def %s(line, linenr):\n %s' % (fname, code,)
        exec(function_def, self.module.__dict__)
        # get the function
        function = self.module.__dict__[fname]
        while start <= stop:
            # Process batches of 5000 to avoid the overhead of making multiple
            # API calls for every line. Assuming an average line length of 100
            # bytes, approximately 488 kilobytes will be transferred per batch,
            # which can be done very quickly in a single API call.
            sstart = start
            sstop = min(start + 5000, stop)
            lines = nvim.current.buffer.get_line_slice(sstart, sstop, True, True)

            exception = None
            newlines = []
            linenr = sstart + 1
            for i, line in enumerate(lines):
                result = function(line, linenr)
                if result == None:
                    # Update earlier lines, and skip to the next
                    if newlines:
                        nvim.current.buffer.set_line_slice(sstart, sstart + len(newlines) -1, True, True, newlines)
                    sstart += len(newlines) + 1
                    newlines = []
                    pass
                elif isinstance(result,basestring):
                    newlines.append(result)
                else:
                    exception = TypeError('pydo should return a string or None, found %s instead' % result.__class__.__name__)
                    break
                linenr += 1

            start = sstop + 1
            if newlines:
                nvim.current.buffer.set_line_slice(sstart, sstart + len(newlines)-1, True, True, newlines)
            if exception:
                raise exception
        # delete the function
        del self.module.__dict__[fname]

    def python_eval(self, expr):
        return eval(expr, self.module.__dict__)


class LegacyEvalHook(SessionHook):

    """Injects legacy `vim.eval` behavior to a Nvim instance."""

    def __init__(self):
        super(LegacyEvalHook, self).__init__(from_nvim=self._string_eval)

    def _string_eval(self, obj, session, method, kind):
        if method == 'vim_eval' and isinstance(obj, NUM_TYPES):
            return str(obj)
        return obj
