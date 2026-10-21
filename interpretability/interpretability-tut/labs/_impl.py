"""Import a lab module: the learner's stub by default, or the reference solution
when INTERP_LAB_IMPL=reference (used to verify that the tests are satisfiable)."""
import importlib
import os


def load(name):
    if os.environ.get('INTERP_LAB_IMPL') == 'reference':
        return importlib.import_module(f'reference.sol_{name}')
    return importlib.import_module(name)
