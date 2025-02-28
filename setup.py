from setuptools import setup, Extension

aes_module = Extension("aes_module", 
    sources=["aes_module.cpp", "aes.h"],
)

setup(
    name="aes_module",
    version="1.0",
    ext_modules=[aes_module],
)
