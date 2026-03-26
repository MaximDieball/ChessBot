

# ------------------------------------------
# Python to C++ Conversion by Gemini
# ------------------------------------------


from setuptools import setup, Extension
import pybind11

# Define the C++ extension module
ext_modules = [
    Extension(
        "libv3",          # The name of the module you will import in Python
        ["libv3.cpp"],    # Your C++ source file(s)
        include_dirs=[pybind11.get_include()], # Tells the compiler where to find pybind11
        language="c++",
        extra_compile_args=["-std=c++17", "-O3"], # -O3 turns on maximum speed optimization!
    ),
]

setup(
    name="chess_core",
    ext_modules=ext_modules,
)

# COMMAND: python3 compile.py build_ext --inplace