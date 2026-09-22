#!/usr/bin/env python3
"""Read-only inventory of the tools and process interface used by M1-04."""
import json
import os
import platform
from pathlib import Path

from preflight import version


def inventory():
    release = platform.freedesktop_os_release() if platform.system() == "Linux" else {}
    return {
        "os": platform.system(),
        "architecture": platform.machine(),
        "distribution": release.get("ID"),
        "distribution_version": release.get("VERSION_ID"),
        "running_as_root": os.geteuid() == 0,
        "python": platform.python_version(),
        "git": version(["git", "--version"]),
        "ps": version(["ps", "--version"]) if platform.system() == "Linux" else None,
        "proc_status_readable": os.access(Path("/proc/self/status"), os.R_OK),
    }


if __name__ == "__main__":
    print(json.dumps(inventory(), indent=2))
