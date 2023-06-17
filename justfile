@_default:
    just --list

@fmt:
    just --fmt --unstable

@bootstrap:
    python -m pip install --upgrade pip pip-tools
    python -m pip install --requirement=requirements.in --upgrade
    pre-commit autoupdate

@build:
    python -m build

@bump *ARGS:
    python -m bumpver update {{ ARGS }}

@bump-dry *ARGS:
    just bump --dry {{ ARGS }}

@check:
    twine check dist/*

@lint *ARGS="--all-files":
    pre-commit run {{ ARGS }}

@nox:
    python -m nox

@pip-compile:
    pip-compile

@push:
    git push origin --all

@test:
    pytest

@update:
    python -m pip install -U pip pip-tools
    python -m pip install --requirement=requirements.in --upgrade

@upload:
    python -m twine upload dist/*
