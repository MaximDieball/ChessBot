

# ------------------------------------------
# Python to C++ Conversion by Gemini
# ------------------------------------------


import os
import shutil
import glob
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

DEST_DIR = "builds"

# Find and move all compiled .so files
for so_file in glob.glob("*.so"):
    dest_path = os.path.join(DEST_DIR, so_file)
    # If an old version exists, remove it first so shutil doesn't crash
    if os.path.exists(dest_path):
        os.remove(dest_path)
    shutil.move(so_file, dest_path)
    print(f"Moved: {so_file} -> {DEST_DIR}/")

# Move the temporary 'build' directory created by the compiler
if os.path.exists("build"):
    dest_build = os.path.join(DEST_DIR, "build")
    # Clean up the old build folder if it exists
    if os.path.exists(dest_build):
        shutil.rmtree(dest_build)
    shutil.move("build", DEST_DIR)
    print(f"Moved: build/ -> {DEST_DIR}/build/")

print("--- Build and Cleanup Complete! ---\n")

# COMMAND: python3 compile.py build_ext --inplace