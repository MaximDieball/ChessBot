import os
import shutil
import glob
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
