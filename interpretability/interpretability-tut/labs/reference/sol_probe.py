"""Reference solution for labs/probe.py: a numpy logistic-regression probe with
shuffled-label and random-direction controls."""
import numpy as np


def majority_rate(y):
    y = np.asarray(y, dtype=np.float64)
    return float(max(y.mean(), 1 - y.mean()))


def fit_logistic(x, y, steps=300, lr=0.5, l2=1e-3):
    x = np.asarray(x, dtype=np.float64); y = np.asarray(y, dtype=np.float64)
    mu, sd = x.mean(0), x.std(0) + 1e-6
    z = (x - mu) / sd
    w = np.zeros(z.shape[1]); b = 0.0
    for _ in range(steps):
        p = 1 / (1 + np.exp(-(z @ w + b)))
        g = p - y
        w -= lr * (z.T @ g / len(y) + l2 * w); b -= lr * g.mean()
    return dict(w=w, b=b, mu=mu, sd=sd)


def predict(probe, x):
    z = (np.asarray(x, dtype=np.float64) - probe['mu']) / probe['sd']
    return (z @ probe['w'] + probe['b'] > 0).astype(np.float64)


def accuracy(probe, x, y):
    return float((predict(probe, x) == np.asarray(y, dtype=np.float64)).mean())


def shuffled_label_control(x_train, y_train, x_test, y_test, n=20, seed=0):
    rng = np.random.default_rng(seed)
    return np.array([accuracy(fit_logistic(x_train, rng.permutation(y_train)), x_test, y_test) for _ in range(n)])


def random_direction_control(x_train, y_train, x_test, y_test, n=20, seed=0):
    """Project onto a random unit direction, choose the best threshold and sign on
    the training split, and report held-out accuracy."""
    rng = np.random.default_rng(seed)
    x_train = np.asarray(x_train, dtype=np.float64); x_test = np.asarray(x_test, dtype=np.float64)
    y_train = np.asarray(y_train); y_test = np.asarray(y_test)
    out = []
    for _ in range(n):
        d = rng.standard_normal(x_train.shape[1]); d /= np.linalg.norm(d)
        s = x_train @ d
        best = (-1.0, 0.0, 1)
        for t in np.quantile(s, np.linspace(0.02, 0.98, 49)):
            for sign in (1, -1):
                acc = ((sign * (s - t) > 0) == (y_train == 1)).mean()
                if acc > best[0]:
                    best = (acc, t, sign)
        _, t, sign = best
        out.append(float(((sign * (x_test @ d - t) > 0) == (y_test == 1)).mean()))
    return np.array(out)


def verdict(test_accuracy, majority, shuffled, random_dir, margin=0.10):
    ok = test_accuracy >= majority + margin and test_accuracy > float(np.max(shuffled)) and test_accuracy > float(np.max(random_dir))
    return dict(accuracy=float(test_accuracy), majority=float(majority), shuffled_max=float(np.max(shuffled)),
                random_direction_max=float(np.max(random_dir)), margin=margin, passed=bool(ok))
