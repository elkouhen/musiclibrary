#!/usr/bin/python
import os
import platform
import shutil
import subprocess
import sys
import wget
from invoke import task
from configobj import ConfigObj
from psutil.tests import process_namespace


def _project_name():
    return "helloworld"

def _default_stage():
    return "develop"

def _aws_region():
    return "eu-west-3"

def _cicd_bucket():
    return "cicd-bucket-eu-west-3"

def _venv_dir():
    if platform.system() == "Windows":
        return "venv"
    return ".venv"

def _activate():
    if platform.system() == "Windows":
        return "call %s/Scripts/activate.bat" % _venv_dir()
    return "source %s/bin/activate" % _venv_dir()    

def _pty():
    if platform.system() == "Windows":
        return False
    return True

@task
def venv(ctx):
    """Create virtualenv"""
    ctx.run("python -m venv %s" % _venv_dir(), pty=_pty())
    with ctx.prefix(_activate()):
        ctx.run("python -m pip install --upgrade pip", pty=_pty())
        ctx.run("python -m pip install --upgrade setuptools", pty=_pty())
        ctx.run("python -m pip install --upgrade wheel", pty=_pty())
        ctx.run("python -m pip install --upgrade invoke", pty=_pty())
        ctx.run("python -m pip install --upgrade wget", pty=_pty())

@task(pre=[venv])
def bootstrap(ctx):
    """Bootstrap"""
    with ctx.prefix(_activate()):
        ctx.run(" python -m pip install -e .", pty=_pty())
        if os.path.exists("dev-requirements.txt"):
            ctx.run(" python -m pip install -r dev-requirements.txt", pty=_pty())
        if os.path.exists("test-requirements.txt"):
            ctx.run(" python -m pip install -r test-requirements.txt", pty=_pty())