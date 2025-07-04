from setuptools import setup, Extension
import pybind11
import sys

# Define the C++ extension module
# The name here 'edit_distance_cpp' MUST match the name given in PYBIND11_MODULE in bindings.cpp
ext_modules = [
    Extension(
        'edit_distance_cpp',
        ['bindings.cpp'], # Source file for the bindings
        include_dirs=[
            pybind11.get_include(),
            # Add other include directories if your edit_distance.cpp had other dependencies
            # For example, if edit_distance.h was separate from edit_distance.cpp
            # and in a different directory. In our case, edit_distance.cpp includes everything.
        ],
        language='c++',
        extra_compile_args=['-std=c++11'] # Or c++14, c++17, etc., as needed
    ),
]

setup(
    name='edit_distance_cpp',
    version='0.1.0',
    author='Jules AI Agent',
    description='Python package with C++ extension for fast edit distance calculation',
    ext_modules=ext_modules,
    # If you have Pybind11 as a build-time dependency
    setup_requires=['pybind11>=2.5'],
    # If you want to ensure pybind11 is installed when your package is installed
    # install_requires=['pybind11>=2.5'], # Usually not needed if only used for building
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires='>=3.6',
)

# To build the module:
# python setup.py build_ext --inplace
#
# This will create a file like:
# edit_distance_cpp.cpython-38-x86_64-linux-gnu.so (on Linux)
# edit_distance_cpp.cp38-win_amd64.pyd (on Windows)
# in the current directory.
#
# After building, you can run main.py.

# Note on compiler:
# On Linux, this usually uses g++.
# On macOS, this usually uses clang++.
# On Windows, you'll need Microsoft Visual C++ Build Tools.
# Make sure appropriate C++ compiler is installed and in PATH.
# For Pybind11, a C++11 compatible compiler is required.
