from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11

ext_modules = [
    Extension(
        "primitive_roots",
        ["prim_roots.cpp"],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(True)
        ],
        language="c++",
        extra_compile_args=["-std=c++11"]
    ),
]

class BuildExtCommand(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)

        __builtins__.__NUMPY_SETUP__ = False
        import pybind11
        self.include_dirs.append(pybind11.get_include())

        self.include_dirs.append(pybind11.get_include(True))

setup(
    name="primitive_roots",
    version="0.1",
    author="",
    author_email="",
    description="Primitive roots calculation module",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExtCommand},
    zip_safe=False,
    install_requires=[
        "pybind11>=2.6.0"
    ]
)
