#!/usr/bin/env python3
"""Finite synthetic workloads; no network, credentials, or arbitrary execution."""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def bounded_integer(minimum, maximum):
    def parse(value):
        number = int(value)
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError(
                f"expected an integer from {minimum} through {maximum}"
            )
        return number
    return parse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    exiting = modes.add_parser("exit")
    exiting.add_argument("--code", type=bounded_integer(0, 125), default=0)
    sleeping = modes.add_parser("sleep")
    sleeping.add_argument("--seconds", type=bounded_integer(1, 30), default=5)
    emitting = modes.add_parser("emit")
    emitting.add_argument("--bytes-per-stream", type=bounded_integer(0, 1048576), default=262144)
    modes.add_parser("environment")
    tree = modes.add_parser("tree")
    tree.add_argument("--seconds", type=bounded_integer(1, 30), default=15)
    burning = modes.add_parser("cpu")
    burning.add_argument("--seconds", type=bounded_integer(1, 10), default=2)
    allocation = modes.add_parser("memory")
    allocation.add_argument("--mib", type=bounded_integer(1, 64), default=16)
    args = parser.parse_args()

    if args.mode == "exit":
        print("synthetic stdout", flush=True)
        print("synthetic stderr", file=sys.stderr, flush=True)
        return args.code
    if args.mode == "sleep":
        time.sleep(args.seconds)
        return 0
    if args.mode == "emit":
        remaining = args.bytes_per_stream
        while remaining:
            count = min(4096, remaining)
            sys.stdout.buffer.write(b"O" * count)
            sys.stdout.buffer.flush()
            sys.stderr.buffer.write(b"E" * count)
            sys.stderr.buffer.flush()
            remaining -= count
        return 0
    if args.mode == "environment":
        # Only synthetic names. Never dump the complete parent environment.
        print(json.dumps({
            "SYLLABUS_ALLOWED": os.environ.get("SYLLABUS_ALLOWED"),
            "SYLLABUS_SECRET": os.environ.get("SYLLABUS_SECRET"),
            "cwd": os.getcwd(),
        }))
        return 0
    if args.mode == "tree":
        child = subprocess.Popen([
            sys.executable, str(Path(__file__).resolve()), "sleep",
            "--seconds", str(args.seconds),
        ])
        print(json.dumps({"parent_pid": os.getpid(), "child_pid": child.pid}), flush=True)
        # The child deliberately inherits stdout/stderr. Killing this parent
        # alone can leave the reader waiting for the descendant's open pipe.
        time.sleep(args.seconds)
        child.wait()
        return 0
    if args.mode == "cpu":
        deadline = time.monotonic() + args.seconds
        iterations = 0
        while time.monotonic() < deadline:
            iterations += 1
        print(json.dumps({"iterations": iterations, "wall_seconds": args.seconds}))
        return 0
    if args.mode == "memory":
        # Small finite allocation, even when invoked without the lab wrapper.
        block = bytearray(args.mib * 1024 * 1024)
        for offset in range(0, len(block), 4096):
            block[offset] = 1
        print(json.dumps({"allocated_mib": args.mib}), flush=True)
        time.sleep(2)
        return 0
    raise AssertionError("argparse accepted an unknown mode")


if __name__ == "__main__":
    raise SystemExit(main())
