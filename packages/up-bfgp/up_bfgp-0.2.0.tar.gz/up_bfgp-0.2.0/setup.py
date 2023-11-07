#!/usr/bin/env python3
import subprocess

from setuptools import setup  # type: ignore
from setuptools.command.build_py import build_py  # type: ignore
from setuptools.command.develop import develop  # type: ignore
import os
import urllib
import shutil


BFGP_dst = "./up_bfgp/bfgp_pp"
BFGP_PUBLIC = "bfgp-pp"
COMPILE_CMD = './scripts/compile.sh'
BFGP_TAG = "v0.1.0"
BFGP_REPO = "https://github.com/jsego/bfgp-pp"
PKG_NAME = "up_bfgp"

def install_BFGP():
    shutil.rmtree(BFGP_dst, ignore_errors=True)
    subprocess.run(["git", "clone", "-b", BFGP_TAG, BFGP_REPO])
    shutil.move(BFGP_PUBLIC, BFGP_dst)
    curr_dir = os.getcwd()
    os.chdir(BFGP_dst)
    subprocess.run(COMPILE_CMD, shell=True)
    os.chdir(curr_dir)


class InstallBFGP(build_py):
    """Custom installation command."""

    def run(self):
        install_BFGP()
        build_py.run(self)


class InstallBFGPdevelop(develop):
    """Custom installation command."""

    def run(self):
        install_BFGP()
        develop.run(self)

long_description = "This package makes the [BFGP++](https://github.com/jsego/bfgp-pp) generalized planner available in the [unified_planning library](https://github.com/aiplan4eu/unified-planning) by the [AIPlan4EU project](https://www.aiplan4eu-project.eu/)."


setup(
    name=PKG_NAME,
    version='v0.2.0',
    description="Unified Planning integration of the BFGP++ generalized planner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Javier Segovia-Aguas, Sergio Jiménez and Anders Jonsson",
    author_email="javier.segovia@upf.edu",
    packages=[PKG_NAME],
    package_data={
        "": ['bfgp_pp/main.bin',
             'bfgp_pp/preprocess/pddl_translator.py']
    },
    cmdclass={"build_py": InstallBFGP, "develop": InstallBFGPdevelop},
    license="GNUv3",
)
