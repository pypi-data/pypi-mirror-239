# Copyright 2022 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import subprocess

import pytest

from pex.common import is_exe
from pex.typing import TYPE_CHECKING
from testing import IS_LINUX_ARM64, IS_MAC_ARM64, run_pex_command

if TYPE_CHECKING:
    from typing import Any


@pytest.mark.skipif(
    IS_MAC_ARM64
    or IS_LINUX_ARM64
    or not any(
        is_exe(os.path.join(entry, "docker"))
        for entry in os.environ.get("PATH", os.path.defpath).split(os.pathsep)
    ),
    reason="This test needs docker to run, and must run on an X86_64 platform.",
)
def test_musllinux_wheels_resolved(
    tmpdir,  # type: Any
    pex_project_dir,  # type: str
):
    # type: (...) -> None

    pex_pex = os.path.join(str(tmpdir), "pex.pex")
    run_pex_command(args=[pex_project_dir, "-c", "pex", "-o", pex_pex]).assert_success()
    process = subprocess.Popen(
        args=[
            "docker",
            "run",
            "--rm",
            "-v",
            "{pex_pex}:/dist/pex".format(pex_pex=pex_pex),
            "python:3.10.7-alpine3.16",
            "python3.10",
            "/dist/pex",
            "--pip-version",
            "22.2.2",
            "--resolver-version",
            "pip-2020-resolver",
            "--no-build",
            "psycopg2-binary==2.9.3",
            "--",
            "-c",
            "import psycopg2; print(psycopg2.__file__)",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    assert 0 == process.returncode, stderr.decode("utf-8")
    assert (
        # N.B.: Since docker gives us a fixed user / home dir and pinned platform, and we use a
        # pinned wheel-only requirement, we can be assured this path is stable.
        b"/root/.pex/installed_wheels/"
        b"c3ae8e75eb7160851e59adc77b3a19a976e50622e44fd4fd47b8b18208189d42/"
        b"psycopg2_binary-2.9.3-cp310-cp310-musllinux_1_1_x86_64.whl/psycopg2/__init__.py"
    ) == stdout.strip()
