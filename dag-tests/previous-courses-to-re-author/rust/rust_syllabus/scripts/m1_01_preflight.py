#!/usr/bin/env python3
"""Optional legacy Mac tool report; the M1-01 pilot records setup in-session."""
import json
import platform

from preflight import version


def main():
    print(json.dumps({
        "os": platform.system(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "git": version(["git", "--version"]),
    }, indent=2))


if __name__ == "__main__":
    main()
