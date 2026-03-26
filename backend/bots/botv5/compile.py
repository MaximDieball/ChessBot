from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "bot_search",
        [
            "bot_search.cpp",
            "../botLib/libv3.cpp"
        ],
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=["-std=c++17", "-O3"],
    ),
]

setup(
    name="chess_engine",
    ext_modules=ext_modules,
)
# COMAND: python3 compile.py build_ext --inplace