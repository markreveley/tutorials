"""Lab: a linear probe with controls.

Fit a logistic-regression probe on activations, report held-out accuracy beside
the majority rate, and run shuffled-label and random-direction controls.
Spec and tests: test_probe.py (lesson 08).
"""

import numpy as np


def majority_rate(y):
    raise NotImplementedError('implement after reading the tests')


def fit_logistic(x, y, steps=300, lr=0.5, l2=1e-3):
    raise NotImplementedError('implement after reading the tests')


def predict(probe, x):
    raise NotImplementedError('implement after reading the tests')


def accuracy(probe, x, y):
    raise NotImplementedError('implement after reading the tests')


def shuffled_label_control(x_train, y_train, x_test, y_test, n=20, seed=0):
    raise NotImplementedError('implement after reading the tests')


def random_direction_control(x_train, y_train, x_test, y_test, n=20, seed=0):
    """Project onto a random unit direction, choose the best threshold and sign on
    the training split, and report held-out accuracy."""
    raise NotImplementedError('implement after reading the tests')


def verdict(test_accuracy, majority, shuffled, random_dir, margin=0.10):
    raise NotImplementedError('implement after reading the tests')
