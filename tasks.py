#!/usr/bin/python
import os
import platform

from invoke import task


def _project_name():
    return "song"


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
def stack_build(ctx):
    ctx.run(f"sam build --region {_aws_region()} --use-container")


@task(pre=[stack_build])
def stack_deploy(ctx, cicd_bucket=_cicd_bucket(), stage=_default_stage()):
    with ctx.prefix(_activate()):
        ctx.run(f"aws s3 cp spec/api-spec.yaml s3://{cicd_bucket}/spec/api-spec.yaml")
        ctx.run(f"sam package --s3-bucket {cicd_bucket} --output-template-file packaged.yaml")
        ctx.run(f"sam deploy packaged.yaml "
                f"--capabilities CAPABILITY_IAM "
                f"--parameter-overrides "
                f"StageName={stage} "
                f"--s3-bucket {cicd_bucket} "
                f"--stack-name {_project_name()}-{stage} "
                f"--region {_aws_region()} ")


@task
def stack_delete(ctx, stage=_default_stage()):
    ctx.run(f"aws cloudformation delete-stack --stack-name {_project_name()}-{stage} --region {_aws_region()}")


@task
def test(ctx, stage=_default_stage()):
    with ctx.prefix(_activate()):
        os.environ["TABLE_NAME"] = f"musiclibrary-{stage}"
        ctx.run(f"python -m pytest")


@task
def venv(ctx):
    """Create virtualenv"""
    ctx.run("python -m venv %s" % _venv_dir(), pty=_pty())
    with ctx.prefix(_activate()):
        ctx.run("python -m pip install --upgrade pip setuptools wheel invoke wget", pty=_pty())


@task(pre=[venv])
def bootstrap(ctx):
    """Bootstrap"""
    with ctx.prefix(_activate()):
        ctx.run(" python -m pip install -e .", pty=_pty())
        if os.path.exists("dev-requirements.txt"):
            ctx.run(" python -m pip install -r dev-requirements.txt", pty=_pty())
        if os.path.exists("test-requirements.txt"):
            ctx.run(" python -m pip install -r test-requirements.txt", pty=_pty())
