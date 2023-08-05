import subprocess
from six import with_metaclass

from jac.compat import file, u, utf8_encode

from . import CompilerMeta


class SassCompiler(with_metaclass(CompilerMeta, object)):
    supported_mimetypes = ['text/sass', 'text/scss']

    @classmethod
    def compile(cls, what, mimetype='text/sass', cwd=None,
                uri_cwd=None, debug=None):
        args = ['sass', '-s']
        if mimetype == 'text/scss':
            args.append('--scss')

        if cwd:
            args += ['-I', cwd]

        handler = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=None)

        if isinstance(what, file):
            what = what.read()
        (stdout, stderr) = handler.communicate(input=utf8_encode(what))
        stdout = u(stdout)

        if handler.returncode == 0:
            return stdout
        else:
            raise RuntimeError('Test this :S %s' % stderr)
