import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "weber_utils", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIRES = [
    "Flask-SQLAlchemy",
    "Flask",
    "Logbook",
    "sentinels",
]

setup(name="weber_utils",
      classifiers = [
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          ],
      description="Utilities for the Weber flask template",
      license="BSD3",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/vmalloc/weber-utils",

      install_requires=_INSTALL_REQUIRES,
      scripts=[],
      namespace_packages=[]
      )
