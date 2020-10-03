#!/usr/bin/env python

from distutils.core import setup
from os.path import abspath, dirname, join

with open(
    join(dirname(abspath(__file__)), "tetris_human_ai", "version.py")
) as version_file:
    exec(compile(version_file.read(), "version.py", "exec"))

setup(
    name="tetris_human_ai",
    version=version,  # noqa
    author="Justin Martin",
    author_email="professional@justinm.me",
    description="A short description of the project",
    url="https://github.com/TetrisHumanAI/TetrisHumanAI",
    packages=["tetris_human_ai"],
    # 3.6 and up, but not Python 4
    python_requires="~=3.6",
    install_requires=[],
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
