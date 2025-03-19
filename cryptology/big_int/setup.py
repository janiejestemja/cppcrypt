from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import setuptools

class get_pybind_include:
    def __init__(self,user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

ext_modules = [
    Extension(
        "bigint",
        ["bigint_module.cpp"],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
        ],
        libraries=["gmp"],
        language="c++"
    ),
]

class BuildExt(build_ext):
    """Custom build extension for adding compiler-specific options"""
    c_opts = {
        "msvc": ["/EHsc"],
        "unix": [],
    }
    l_opts = {
        "msvc": [],
        "unix": [],
    }

    if sys.platform == "darwin":
        darwin_opts = ["-stdlib=libx++", "-mmacosx-version-min=10.7"]
        c_opts["unix"] += darwin_opts
        l_opts["unix"] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == "unix":
            opts.append("-std=c++14")

        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts

        build_ext.build_extensions(self)

setup(
    name="bigint",
    version="0.1.0",
    author="jnja",
    author_email="",
    description="A big int lib for Python using GMP",
    long_description="",
    ext_modules=ext_modules,
    install_requires=["pybind11>=2.6.0"],
    setup_requires=["pybind11>=2.6.0"],
    cmdclass={"build_ext": BuildExt},
    zip_safe=False,
)
