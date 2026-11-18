"""Manifest labs: describe saved activations so a reader can check them.

Implement the stubs so that labs/test_manifest.py passes. NumPy only; convert
a torch tensor with `t.detach().cpu().numpy()` before passing it here. Run
from the course directory:

    python3 -m unittest discover -s labs -p 'test_manifest.py' -v
"""
import hashlib
import json

import numpy as np


def tensor_digest(array):
    """Return the SHA-256 hex digest of an array's bytes in C order.

    Two arrays with equal values, dtype, and shape must give the same digest
    even if one is a non-contiguous view (use np.ascontiguousarray).
    """
    raise NotImplementedError("Implement tensor_digest with hashlib.sha256")


def build_manifest(model_name, prompts, tensors, seed, versions):
    """Describe a run as a JSON-serialisable dict.

    tensors is a dict name -> np.ndarray. Return exactly these keys:
      model: model_name
      prompts: list of the prompts, in order
      seed: the integer seed
      versions: the dict given (for example {"torch": "2.x", "numpy": "2.x"})
      tensors: a dict name -> {"shape": [ints], "dtype": "float32",
               "sha256": digest} in the same order as `tensors`
    No timestamps, paths, or hostnames: the manifest must be the same whenever
    the run is the same. The result must survive json.dumps unchanged.
    """
    raise NotImplementedError("Implement build_manifest; it must be json.dumps-able")


def check_manifest(manifest, tensors):
    """Compare a manifest against actual arrays and return a list of problems.

    Return [] when everything matches. Otherwise return one readable string
    per problem: a tensor named in the manifest but missing from `tensors`,
    an array present but not described, a shape mismatch, a dtype mismatch,
    or a digest mismatch. Never raise for a mismatch; only report it.
    """
    raise NotImplementedError("Implement check_manifest; report, do not raise")


def write_manifest(manifest, path):
    """Write the manifest as UTF-8 JSON with sorted keys and a trailing newline."""
    raise NotImplementedError("Implement write_manifest with json.dump(sort_keys=True)")
