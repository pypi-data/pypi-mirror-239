from __future__ import annotations

import os
from pathlib import Path

import nox

PY38 = "3.8"
PY39 = "3.9"
PY310 = "3.10"
PY311 = "3.11"
PY312 = "3.12"
PY_VERSIONS = [PY38, PY39, PY310, PY311, PY312]
PY_DEFAULT = PY38


@nox.session(python=PY_VERSIONS)
def tests(session):
    session.install(".[dev]")

    session.run("python", "-m", "pytest")


@nox.session
def coverage(session):
    session.install(".[dev]")
    session.run("python", "-m", "pytest", "--cov=pybumpver")

    try:
        summary = os.environ["GITHUB_STEP_SUMMARY"]
        with Path(summary).open("a") as output_buffer:
            output_buffer.write("")
            output_buffer.write("### Coverage\n\n")
            output_buffer.flush()
            session.run(
                "python",
                "-m",
                "coverage",
                "report",
                "--skip-covered",
                "--skip-empty",
                "--format=markdown",
                stdout=output_buffer,
            )
    except KeyError:
        session.run(
            "python", "-m", "coverage", "html", "--skip-covered", "--skip-empty"
        )

    session.run("python", "-m", "coverage", "report")


@nox.session
def lint(session):
    session.install(".[lint]")
    session.run("python", "-m", "pre_commit", "run", "--all-files")


@nox.session
def mypy(session):
    session.install(".[dev]")
    session.run("python", "-m", "mypy", ".")
