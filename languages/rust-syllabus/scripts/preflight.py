#!/usr/bin/env python3
"""Report lab capabilities without changing host state or printing secrets."""
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path


def version(command):
    if not shutil.which(command[0]):
        return "not installed"
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        lines = result.stdout.splitlines()
        return lines[0] if lines else "present; version unavailable"
    except (OSError, subprocess.TimeoutExpired):
        return "present; version check failed"


def main():
    linux = platform.system() == "Linux"
    distribution = {}
    os_release = Path("/etc/os-release")
    if linux and os_release.exists():
        for line in os_release.read_text().splitlines():
            key, separator, value = line.partition("=")
            if separator and key in {"ID", "VERSION_ID"}:
                distribution[key.lower()] = value.strip('"')
    controllers = Path("/sys/fs/cgroup/cgroup.controllers")
    result = {
        "os": platform.system(),
        "architecture": platform.machine(),
        "distribution": distribution,
        "python": platform.python_version(),
        "git": version(["git", "--version"]),
        "rust": version(["rustc", "--version"]),
        "cargo": version(["cargo", "--version"]),
        "systemd": version(["systemd", "--version"]) if linux else "Linux only",
        "running_as_root": os.geteuid() == 0 if hasattr(os, "geteuid") else None,
        "systemd_is_pid1": (
            Path("/proc/1/comm").read_text().strip() == "systemd"
            if linux and Path("/proc/1/comm").exists() else False
        ),
        "cgroup_v2": controllers.exists() if linux else False,
        "cgroup_controllers": (
            controllers.read_text().strip().split() if linux and controllers.exists() else []
        ),
        "linux_tools": {
            name: shutil.which(name) is not None
            for name in ["ip", "unshare", "systemd-run", "systemctl", "timeout"]
        } if linux else {},
        "kvm_read_write": (
            os.access("/dev/kvm", os.R_OK | os.W_OK) if linux else False
        ),
        "note": (
            "Read-only inventory. Privileged lab permission is not tested. KVM is for next-month planning."
            if linux else
            "Suitable for authoring and many Rust exercises. Run Linux labs on the designated Linux host."
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
