"""Test helper: import the learner's lab module, or the author's reference when LAB_IMPL=reference."""
import importlib
import os
import sys
from pathlib import Path

LABS = Path(__file__).resolve().parent


def load(name):
    if os.environ.get('LAB_IMPL') == 'reference':
        sys.path.insert(0, str(LABS / 'reference'))
        return importlib.import_module(f'{name}_reference')
    sys.path.insert(0, str(LABS))
    return importlib.import_module(name)


def have(module):
    try:
        importlib.import_module(module)
        return True
    except Exception:
        return False
