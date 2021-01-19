import os
import subprocess

from setuptools import setup, find_packages


def install_requirements() -> [str]:
    return read_requirements_file("requirements.txt")


def read_requirements_file(file_name: str):
    with open(file_name, encoding="utf-8") as f:
        requirements_file = f.readlines()
    return [r.strip() for r in requirements_file]


setup(
    name="alerticular",
    version="0.0.1",
    description="Handle incoming Alertmanager alerts and send them to Telegram",
    long_description="ToDo",
    license="AGPLv3+",
    author="Max Rosin",
    author_email="git@hackrid.de",
    url="https://github.com/ekeih/alerticular",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=install_requirements(),
    entry_points={"console_scripts": ["alerticular = alerticular.cli:cli"]},
)
