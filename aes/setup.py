from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os

# pybind11 setup
class get_pybind_include:
    """Helper class to determjine the pybind11 include path"""
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

ext_modules = [
    Extension(
        'pyaes',
        ['module.cpp', 'aes.cpp'],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True),
        ],
        language='c++'
    ),
]

def has_flag(compiler, flagname):
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main(int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
        
        return True
def cpp_flag(compiler):
    """Return the -std=c++... flag"""
    flags = ['-std=c++17', '-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag): return flag

    raise RuntimeError('Unsupportet compiler -- at least C++11 is needed')

class BuildExt(build_ext):
    """Custom build extension for adding compiler specific options"""
    c_opts = {
            'msvc': ['/EHsc'],
            'unix': [],
    }
    l_opts = {
            'msvc': [],
            'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc##', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO\\"%s\\"' % self.distribution.get_version())

        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts

        build_ext.build_extensions(self)

setup(
    name='pyaes',
    version='0.1.0',
    author='jnja',
    author_email='janiejestemja@web.de',
    description='Python wrapper for C++ AES implementation',
    long_description='',
    ext_modules=ext_modules,
    install_requirements=['pybind11>=2.5.0'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
