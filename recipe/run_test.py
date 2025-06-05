import platform
import os
import sysconfig

is_freethreading = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
is_cpython = platform.python_implementation() == 'CPython'
is_arch = os.environ.get("use_noarch", "False") == "False"
is_compiled = is_cpython and is_arch and not is_freethreading

import Cython
import Cython.Compiler.Code
import Cython.Compiler.FlowControl
import Cython.Compiler.Lexicon
import Cython.Compiler.Parsing
import Cython.Compiler.Scanning
import Cython.Compiler.Visitor
import Cython.Plex.Actions
import Cython.Plex.Scanners

try:
    import Cython.Runtime.refnanny
    assert is_compiled
except ImportError:
    assert not is_compiled

import sys
import os
import subprocess
from pprint import pprint
from os.path import isfile

print('sys.executable: %r' % sys.executable)
print('sys.prefix: %r' % sys.prefix)
print('sys.version: %r' % sys.version)
print('PATH: %r' % os.environ['PATH'])
print('CWD: %r' % os.getcwd())

from distutils.spawn import find_executable
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

if find_executable('gcc'):
    sys.argv[1:] = ['build_ext', '--inplace']
    setup(name='fib',
          cmdclass={'build_ext': build_ext},
          ext_modules=[Extension("fib", ["fib.pyx"])])

    try:
        import fib
        assert fib.fib(10) == 55
    except ImportError:
        cmd = [sys.executable, '-c', 'import fib; print(fib.fib(10))']
        out = subprocess.check_output(cmd)
        assert out.decode('utf-8').strip() == '55'
