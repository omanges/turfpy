"""Project setup file."""
import sys
from codecs import open
from os import path

from setuptools import find_packages, setup

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

here = path.abspath(path.dirname(__file__))

# get the core dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")
install_requires = [x.strip() for x in all_reqs if "git+" not in x]

packages = find_packages(exclude=["docs", "tests"])
version = {}
with open('{}/__version__.py'.format(packages[0])) as f:
    exec(f.read(), version)

download_url = (
    "https://github.com/omanges/turfpy"
    "/archive/" + version['__version__'] + ".zip"
)

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# The text of the README file
with open(path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="turfpy",
    version=version['__version__'],
    description="A Python library for performing geospatial data analysis which reimplements turf.js.",
    long_description=README,
    long_description_content_type="text/markdown",
    download_url=download_url,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={
        "Documentation": "https://turfpy.readthedocs.io",
        "Source": "https://github.com/omanges/turfpy"
    },
    packages=packages,
    keywords="Python Library for Turf",
    include_package_data=True,
    author="Omkar Mestry, Sachin Kharude",
    install_requires=install_requires,
    author_email="om.m.mestry@gmail.com, sachinkharude10@gmail.com",
    setup_requires=[] + pytest_runner,
    tests_require=["pytest"],
    py_modules=["turfpy"]
)
