from setuptools import setup, find_packages, Extension
from os import path
import os
import numpy


def package_files(directory):
    paths = []
    for (pathhere, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", pathhere, filename))
    return paths


extra_folders = [
    "neura_swift/out",
    "neura_swift/core",
]

extra_files = []
for extra_folder in extra_folders:
    extra_files += package_files(extra_folder)

phys = Extension(
    "neura_swift.phys",
    sources=["./neura_swift/core/phys.cpp"],
    include_dirs=["./neura_swift/core/", numpy.get_include()],
)

setup(
    package_data={"neura_swift": extra_files},
    ext_modules=[phys],
)
