#!/usr/bin/env python
from setuptools import setup, find_packages
import imp
import os
import sys

m_info = imp.find_module("spambayes_lite", [os.path.dirname(__file__)])
m = imp.load_module("sbl", *m_info)

readme_fname = os.path.join(os.path.dirname(__file__), "README.rst")
readme_text = open(readme_fname).read()

install_requires = ["lockfile", "pymongo", "six"]
if sys.version_info[0] == 3:
    install_requires.append("dnspython3")
else:
    install_requires.append("dnspython")

setup(
    name='spambayes-lite',
    version = m.__version__,
    description = "Bare-bones spam classification library based on a modified version of SpamBayes.",
    author = "Daniel Brandt",
    author_email = "me@dbrandt.se",
    url = "https://github.com/dbrandt/spambayes-lite",
    install_requires=install_requires,
    long_description=readme_text,
    packages=find_packages(),
    license="PSFL",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing :: Filters"
        ],
    )
