"""Command-line demonstrations on the real GPT-2 fixture, one per lesson.

Every command prints numbers computed from data/activations.npy (GPT-2 small,
residual stream after block 6, 302 tokens) and data/weights.npz (layer 7,
head 0). Nothing is simulated. Run from the course directory:

  python3 labs/linalg_lab.py --help
  python3 labs/linalg_lab.py inspect

Commands use reference.py so they work before your exercises are implemented.
"""
import argparse
import sys

import numpy as np

import reference as R

np.set_printoptions(precision=3, suppress=True, linewidth=100)


def show(tokens, idx):
    return repr(tokens[idx])


def cmd_inspect(a):
    X, tokens, labels = R.load_fixture()
    print(f'activations: shape {X.shape}, dtype on disk float16, loaded as {X.dtype}')
    print(f'tokens: {len(tokens)}; first eight: {tokens[:8]}')
    print(f'labels: ' + ', '.join(f'{k} ({int(v.sum())} ones)' for k, v in labels.items() if k != 'position'))
    i = a.token
    print(f'token {i} = {show(tokens, i)}: first six of 768 coordinates {X[i, :6]}')
    print(f'  largest |coordinate| at index {int(np.argmax(np.abs(X[i])))}, value {X[i, np.argmax(np.abs(X[i]))]:.2f}')
    W = R.load_head()
    print('head weights: ' + ', '.join(f'{k} {v.shape}' for k, v in W.items()))


def cmd_vectors(a):
    X, tokens, _ = R.load_fixture()
    i, j = a.token, a.other
    u, v = X[i], X[j]
    print(f'u = token {i} {show(tokens, i)}, v = token {j} {show(tokens, j)}')
    print(f'u[:5]       = {u[:5]}')
    print(f'v[:5]       = {v[:5]}')
    print(f'(u+v)[:5]   = {(u + v)[:5]}')
    print(f'(2u)[:5]    = {(2 * u)[:5]}')
    print(f'(u-v)[:5]   = {(u - v)[:5]}')
    m = X[1:].mean(axis=0)
    print(f'mean of tokens 1..{len(tokens) - 1}, first five coordinates: {m[:5]}')
    print(f'u - mean, first five: {(u - m)[:5]}')
    print('check: (u+v)-v == u exactly in exact arithmetic; here max |((u+v)-v) - u| =', f'{np.abs((u + v) - v - u).max():.2e}')


def cmd_similar(a):
    X, tokens, _ = R.load_fixture()
    norms = np.array([R.norm(x) for x in X])
    print(f'norms: token 0 {show(tokens, 0)} {norms[0]:.1f}; median over all tokens {np.median(norms):.1f}; min {norms.min():.1f} at token {int(norms.argmin())} {show(tokens, int(norms.argmin()))}')
    i = a.token
    u = X[i]
    cos = np.array([R.cosine(u, x) for x in X])
    order = np.argsort(-cos)
    print(f'query token {i} {show(tokens, i)}, norm {norms[i]:.1f}')
    print('most similar by cosine (excluding itself):')
    for j in order[1:6]:
        print(f'  token {j:3d} {show(tokens, j):14s} cos {cos[j]:.3f}  dot {u @ X[j]:10.1f}  norm {norms[j]:.1f}')
    print('least similar:')
    for j in order[-3:]:
        print(f'  token {j:3d} {show(tokens, j):14s} cos {cos[j]:.3f}  dot {u @ X[j]:10.1f}  norm {norms[j]:.1f}')
    others = np.delete(cos, i)
    print(f'cosine to every other token: mean {others.mean():.3f}, min {others.min():.3f}, max {others.max():.3f}')


def cmd_project(a):
    X, tokens, labels = R.load_fixture(skip_first=True)
    y = labels[a.label]
    d = R.mean_difference_direction(X, y)
    coef = R.project_rows(X, d)
    print(f'direction d = mean({a.label}=1) - mean({a.label}=0); |d| = {R.norm(d):.2f}')
    print(f'projection coefficient x.d/|d| for every token: shape {coef.shape}')
    print(f'  mean over {a.label}=1 tokens: {coef[y == 1].mean():8.2f}   mean over {a.label}=0 tokens: {coef[y == 0].mean():8.2f}')
    order = np.argsort(-coef)
    print('highest coefficients:')
    for j in order[:6]:
        print(f'  {coef[j]:8.2f}  token {j + 1:3d} {show(tokens, j):12s} label {int(y[j])}')
    print('lowest coefficients:')
    for j in order[-4:]:
        print(f'  {coef[j]:8.2f}  token {j + 1:3d} {show(tokens, j):12s} label {int(y[j])}')
    i = a.token - 1
    c, p, r = R.project(X[i], d)
    print(f'token {a.token} {show(tokens, i)}: coefficient {c:.2f}, |projection| {R.norm(p):.2f}, |residual| {R.norm(r):.2f}, |x| {R.norm(X[i]):.2f}')
    print(f'  check |proj|^2 + |resid|^2 = {R.norm(p) ** 2 + R.norm(r) ** 2:.1f} vs |x|^2 = {R.norm(X[i]) ** 2:.1f}; resid.d = {r @ d:.2e}')


def cmd_shapes(a):
    X, tokens, _ = R.load_fixture()
    W = R.load_head()
    x = X[a.token]
    q = x @ W['W_Q']
    print(f'x = token {a.token} {show(tokens, a.token)}: shape {x.shape}')
    print(f"W_Q shape {W['W_Q'].shape}: maps a 768-vector to a 64-vector")
    print(f'q = x @ W_Q: shape {q.shape}; first five {q[:5]}')
    print('q is a linear map of x: check (2x) @ W_Q == 2 (x @ W_Q):', bool(np.allclose((2 * x) @ W['W_Q'], 2 * q)))
    x2 = X[a.token + 1]
    print('and (x + x2) @ W_Q == x @ W_Q + x2 @ W_Q:', bool(np.allclose((x + x2) @ W['W_Q'], q + x2 @ W['W_Q'], atol=1e-2)))
    print(f"column 0 of W_Q, first five entries {W['W_Q'][:5, 0]}: q[0] = x . column 0 = {x @ W['W_Q'][:, 0]:.3f}")
    print(f"W_O shape {W['W_O'].shape}: maps a 64-vector back to 768. (x @ W_V) @ W_O has shape {((x @ W['W_V']) @ W['W_O']).shape}")
    try:
        x @ W['W_O']
    except ValueError as e:
        print(f'x @ W_O fails: {e}')
    print(f"W_O @ x runs, shape {(W['W_O'] @ x).shape}: shapes happen to match, but it dots x with the rows of W_O, which is not the map the head applies")


def cmd_matmul(a):
    X, tokens, _ = R.load_fixture()
    W = R.load_head()
    Q = X @ W['W_Q']; K = X @ W['W_K']
    print(f"X {X.shape} @ W_Q {W['W_Q'].shape} = Q {Q.shape}; row {a.token} of Q equals X[{a.token}] @ W_Q:", bool(np.allclose(Q[a.token], X[a.token] @ W['W_Q'])))
    scores = Q @ K.T
    print(f'scores = Q @ K.T: shape {scores.shape}; entry [i, j] = q_i . k_j')
    W_QK = W['W_Q'] @ W['W_K'].T
    print(f"W_QK = W_Q @ W_K.T: shape {W_QK.shape}; X @ W_QK @ X.T equals Q @ K.T (composition):", bool(np.allclose(X @ W_QK @ X.T, scores, rtol=1e-3, atol=1e-1)))
    e1 = np.einsum('nd,dh->nh', X, W['W_Q']); e2 = np.einsum('nh,mh->nm', Q, K)
    print('einsum nd,dh->nh matches X @ W_Q:', bool(np.allclose(e1, Q, rtol=1e-4, atol=1e-3)), '; einsum nh,mh->nm matches Q @ K.T:', bool(np.allclose(e2, scores, rtol=1e-4, atol=1e-1)))
    i = a.token
    row = scores[i, :i + 1] / np.sqrt(64)
    top = np.argsort(-row)[:3]
    print(f'token {i} {show(tokens, i)} scaled scores against earlier tokens (q.k/sqrt(64)); three largest:')
    for j in top:
        print(f'  score {row[j]:7.2f} against token {j:3d} {show(tokens, j)}')
    print('(scores only; real attention adds biases, layer norm, masking and softmax, covered in the transformers course)')


def cmd_basis(a):
    X, tokens, _ = R.load_fixture(skip_first=True)
    x = X[a.token - 1]
    Xc = X - X.mean(axis=0)
    Vt = np.linalg.svd(Xc, full_matrices=True)[2]  # all 768 right singular vectors
    B = Vt.T  # columns are the principal directions, completed to a full orthonormal basis
    c = R.coordinates_in_basis(x, B)
    print(f'token {a.token} {show(tokens, a.token - 1)}')
    print(f'neuron-basis coordinates, first five: {x[:5]}')
    print(f'PCA-basis coordinates, first five:    {c[:5]}')
    print(f'same vector: B @ c reproduces x, max error {np.abs(B @ c - x).max():.2e}')
    print(f'norm in neuron basis {R.norm(x):.3f}; norm of PCA coordinates {R.norm(c):.3f} (equal: the basis is orthonormal)')
    print(f'coordinate with largest magnitude: neuron basis index {int(np.argmax(np.abs(x)))} ({np.abs(x).max():.1f}); PCA basis index {int(np.argmax(np.abs(c)))} ({np.abs(c).max():.1f})')
    skew = np.array([[1.0, 1.0], [0.0, 1.0]])
    print('a 2-D non-orthogonal basis with columns (1,0) and (1,1): coordinates of (3,2) are', R.coordinates_in_basis([3, 2], skew))


def cmd_rank(a):
    X, tokens, _ = R.load_fixture()
    W = R.load_head()
    print(f'rank of the activation matrix X {X.shape}: {R.rank(X)}  (at most min(302, 768))')
    W_QK = W['W_Q'] @ W['W_K'].T; W_OV = W['W_V'] @ W['W_O']
    print(f'rank of W_QK = W_Q @ W_K.T {W_QK.shape}: {R.rank(W_QK)};  rank of W_OV = W_V @ W_O {W_OV.shape}: {R.rank(W_OV)}  (a product through 64 dimensions has rank at most 64)')
    rng = np.random.default_rng(0)
    for d, m in [(768, 768), (768, 2000), (768, 5000)]:
        V = rng.standard_normal((m, d)); V /= np.linalg.norm(V, axis=1, keepdims=True)
        G = V @ V.T; np.fill_diagonal(G, 0)
        print(f'{m} random unit vectors in {d} dims: rank {R.rank(V)}; max |cosine| between any two {np.abs(G).max():.3f}')
    v = rng.standard_normal((3, 4)); v[2] = v[0] + 2 * v[1]
    print('three 4-D vectors where the third is v0 + 2 v1: rank', R.rank(v))


def cmd_remove(a):
    X, tokens, labels = R.load_fixture(skip_first=True)
    y = labels[a.label]
    tr, te = R.split(len(y), 0.7, seed=0)
    d = R.mean_difference_direction(X[tr], y[tr])
    coef = R.project_rows(X, d)
    print(f'direction d from the {len(tr)} training tokens; before: held-out correlation of projection on d with {a.label}: {R.correlation(coef[te], y[te]):.3f}')
    Xr = R.remove_direction(X, d)
    print(f'after removing d from every token: max |projection on d| = {np.abs(R.project_rows(Xr, d)).max():.2e}; norms shrink from median {np.median(np.linalg.norm(X, axis=1)):.2f} to {np.median(np.linalg.norm(Xr, axis=1)):.2f}')
    d2 = R.mean_difference_direction(Xr[tr], y[tr])
    print(f'refit the mean-difference direction on the edited training tokens: |d2| = {R.norm(d2):.2e} (was {R.norm(d):.2f}); the class means now coincide')
    w, b = R.least_squares(Xr[tr], y[tr], ridge=10.0)
    print(f'ridge least-squares probe refitted on the edited activations: held-out correlation {R.correlation(R.predict(Xr[te], w, b), y[te]):.3f}  (compare the probe on the unedited activations: {R.correlation(R.predict(X[te], *R.least_squares(X[tr], y[tr], ridge=10.0)), y[te]):.3f})')
    Q = R.gram_schmidt([d, labels_direction(X, labels, 'after_period'), d + 0.5 * labels_direction(X, labels, 'after_period')])
    print(f'gram_schmidt on [d, d_after_period, d + 0.5 d_after_period]: kept {Q.shape[0]} orthonormal vectors; Q @ Q.T =\n{Q @ Q.T}')


def labels_direction(X, labels, name):
    return R.mean_difference_direction(X, labels[name])


def cmd_probe(a):
    X, tokens, labels = R.load_fixture(skip_first=True)
    y = labels[a.label]
    tr, te = R.split(len(y), 0.7, seed=a.seed)
    w, b = R.least_squares(X[tr], y[tr], ridge=a.ridge)
    pred = R.predict(X, w, b)
    print(f'label {a.label}: {int(y.sum())} ones of {len(y)}; train {len(tr)} tokens, held out {len(te)}; ridge {a.ridge}')
    print(f'least-squares direction w: shape {w.shape}, |w| = {R.norm(w):.4f}, intercept b = {b:.3f}')
    print(f'train: correlation(pred, y) = {R.correlation(pred[tr], y[tr]):.3f}; mean squared error {np.mean((pred[tr] - y[tr]) ** 2):.4f}')
    print(f'held out: correlation(pred, y) = {R.correlation(pred[te], y[te]):.3f}; mean squared error {np.mean((pred[te] - y[te]) ** 2):.4f}')
    resid = y[tr] - pred[tr]
    Xc = X[tr] - X[tr].mean(0)
    if a.ridge > 0:
        print(f'ridge normal equations check on train: max |Xc.T @ residual - ridge * w| = {np.abs(Xc.T @ resid - a.ridge * w).max():.2e} (with a penalty the residual is no longer orthogonal to the columns)')
    else:
        print(f'normal equations check on train: max |Xc.T @ residual| = {np.abs(Xc.T @ resid).max():.2e} (residual is orthogonal to every column)')
    d = R.mean_difference_direction(X[tr], y[tr])
    print(f'cos(w, mean-difference direction) = {R.cosine(w, d):.3f}; held-out correlation using the mean-difference direction instead: {R.correlation(R.project_rows(X[te], d), y[te]):.3f}')


def cmd_covariance(a):
    X, tokens, _ = R.load_fixture(skip_first=True)
    C = R.covariance(X)
    print(f'covariance of X {X.shape}: shape {C.shape}; symmetric: {bool(np.allclose(C, C.T))}')
    vals, vecs = np.linalg.eigh(C)
    vals, vecs = vals[::-1], vecs[:, ::-1]
    print(f'eigenvalues (eigh, reordered largest first), top five: {vals[:5]}')
    print(f'smallest five: {vals[-5:]}  (n - 1 = {X.shape[0] - 1} < 768, so at least 768 - {X.shape[0] - 1} are zero up to rounding)')
    print(f'eigenvectors orthonormal: max |V.T V - I| = {np.abs(vecs.T @ vecs - np.eye(768)).max():.2e}')
    print(f'C v = lambda v for the top eigenvector: max |C v - lambda v| = {np.abs(C @ vecs[:, 0] - vals[0] * vecs[:, 0]).max():.2e}')
    print(f'sum of eigenvalues {vals.sum():.1f} = total variance = sum of per-dimension variances {X.var(axis=0, ddof=1).sum():.1f}')
    Xc = X - X.mean(0); S = np.linalg.svd(Xc, compute_uv=False)
    print(f'singular values^2 / (n-1), top three: {S[:3] ** 2 / (X.shape[0] - 1)}  (same numbers as the eigenvalues)')
    print(f'variance along the top eigenvector {np.var(Xc @ vecs[:, 0], ddof=1):.1f}; along neuron 447 {np.var(X[:, 447], ddof=1):.1f}; along neuron 0 {np.var(X[:, 0], ddof=1):.2f}')


def cmd_pca(a):
    which = 'all 302 tokens' if a.keep_first else 'tokens 1..301 (position 0 excluded)'
    X, tokens, labels = R.load_fixture(skip_first=not a.keep_first)
    comps, explained, scores = R.pca(X, a.k)
    print(f'PCA on {which}: {a.k} components')
    print('variance explained: ' + ' '.join(f'{e:.3f}' for e in explained))
    cum = np.cumsum(explained)
    print('cumulative:         ' + ' '.join(f'{c:.3f}' for c in cum))
    full = R.pca(X, min(X.shape))[1]
    for k in (1, 2, 5, 10, 20, 50, 100):
        print(f'  first {k:3d} components: {np.cumsum(full)[k - 1] * 100:5.1f}% of variance')
    print(f'components orthonormal: max |V V.T - I| = {np.abs(comps @ comps.T - np.eye(a.k)).max():.2e}')
    print(f'component 1, largest-magnitude neuron index {int(np.argmax(np.abs(comps[0])))} with weight {comps[0][np.argmax(np.abs(comps[0]))]:.3f}')
    order = np.argsort(scores[:, 0])
    print('tokens at the two ends of component 1:')
    print('  low: ' + ', '.join(f'{show(tokens, j)} ({scores[j, 0]:.0f})' for j in order[:5]))
    print('  high: ' + ', '.join(f'{show(tokens, j)} ({scores[j, 0]:.0f})' for j in order[-5:]))
    for name in ('position', 'is_digit', 'after_period'):
        print(f'  correlation of component-1 score with {name}: {R.correlation(scores[:, 0], labels[name]):.3f}; component 2: {R.correlation(scores[:, 1], labels[name]):.3f}')


def cmd_svd(a):
    X, tokens, _ = R.load_fixture(skip_first=True)
    W = R.load_head()
    W_QK = W['W_Q'] @ W['W_K'].T
    U, S, Vt = np.linalg.svd(W_QK)
    print(f'SVD of W_QK {W_QK.shape}: U {U.shape}, S {S.shape}, Vt {Vt.shape}')
    print(f'singular values: top five {S[:5]}; number above 1e-3 * max: {int((S > 1e-3 * S[0]).sum())}; S[64:69] = {S[64:69]}')
    print(f'U @ diag(S) @ Vt reproduces W_QK: max error {np.abs((U * S) @ Vt - W_QK).max():.2e}')
    for k in (1, 8, 32, 64):
        A = R.low_rank(W_QK, k)
        print(f'  rank-{k:2d} approximation: relative error |W_QK - A_k| / |W_QK| = {np.linalg.norm(W_QK - A) / np.linalg.norm(W_QK):.4f}')
    Xc = X - X.mean(0)
    U2, S2, Vt2 = np.linalg.svd(Xc, full_matrices=False)
    print(f'SVD of centred activations {Xc.shape}: {len(S2)} singular values; top three {S2[:3]}')
    for k in (1, 10, 50, 100, 301):
        A = R.low_rank(Xc, k)
        print(f'  rank-{k:3d}: relative reconstruction error {np.linalg.norm(Xc - A) / np.linalg.norm(Xc):.4f}; equals sqrt(sum of dropped S^2 / sum S^2) = {np.sqrt((S2[k:] ** 2).sum() / (S2 ** 2).sum()):.4f}')
    print(f'right singular vectors of Xc are the PCA components: |cos| with pca component 1 = {abs(R.cosine(Vt2[0], R.pca(X, 1)[0][0])):.6f}')


def cmd_gradient(a):
    X, tokens, labels = R.load_fixture(skip_first=True)
    x = X[a.token - 1]
    d = R.mean_difference_direction(X, labels['is_digit'])
    # numeric check on a 5-D slice to keep it fast: restrict both to the first five coordinates
    x5, d5 = x[:5].astype(np.float64), d[:5].astype(np.float64)
    print(f'token {a.token} {show(tokens, a.token - 1)}; f(v) = v.d with d the digit direction')
    print(f'analytic gradient of v.d is d; first five entries {R.grad_dot(x, d)[:5]}')
    print(f'numeric gradient (central differences) on those five coordinates {R.numeric_gradient(lambda v: float(v @ d5), x5)}')
    print(f'analytic gradient of |v| is v/|v|; first five {R.grad_norm(x)[:5]}')
    print(f'numeric on those five coordinates {R.numeric_gradient(lambda v: R.norm(np.concatenate([v, x[5:]])), x5)}')
    unit = d / R.norm(d); step = 5.0
    x_up = x + step * unit
    print(f'gradient ascent on f(v) = v.d/|d|: coefficient {float(x @ unit):.2f} -> {float(x_up @ unit):.2f} after a step of length {step} (predicted increase exactly {step})')
    x_rand = x + step * R.grad_norm(np.random.default_rng(0).standard_normal(768))
    print(f'same step length in a random direction: {float(x @ unit):.2f} -> {float(x_rand @ unit):.2f}')
    print(f'norm after the step along d: {R.norm(x):.2f} -> {R.norm(x_up):.2f}; cos(x, d) = {R.cosine(x, d):.3f}')


def cmd_correlation(a):
    X, tokens, labels = R.load_fixture(skip_first=True)
    y = labels[a.label]
    tr, te = R.split(len(y), 0.7, seed=a.seed)
    w, b = R.least_squares(X[tr], y[tr], ridge=a.ridge)
    pred = R.predict(X, w, b)
    r_tr, r_te = R.correlation(pred[tr], y[tr]), R.correlation(pred[te], y[te])
    print(f'label {a.label}; direction fitted on {len(tr)} tokens; correlation train {r_tr:.3f}, held out {r_te:.3f}')
    null = R.permutation_null(pred[te], y[te], n_perm=a.perms, seed=a.seed)
    print(f'permutation baseline on the held-out tokens ({a.perms} shuffles of the label): mean {null.mean():.3f}, 97.5th percentile {np.percentile(null, 97.5):.3f}, max {np.abs(null).max():.3f}')
    print(f'shuffles with |r| >= observed held-out |r|: {int((np.abs(null) >= abs(r_te)).sum())} of {a.perms}')
    rng = np.random.default_rng(a.seed)
    rand = [R.correlation(R.project_rows(X[te], rng.standard_normal(768)), y[te]) for _ in range(a.perms)]
    print(f'random-direction baseline (held out, {a.perms} directions): mean {np.mean(rand):.3f}, max |r| {np.max(np.abs(rand)):.3f}')
    other = [k for k in labels if k not in (a.label, 'position')]
    print('the same projection correlated with other labels on held-out tokens: ' + ', '.join(f'{k} {R.correlation(pred[te], labels[k][te]):.3f}' for k in other))


def cmd_review(a):
    X, tokens, labels = R.load_fixture(skip_first=True)
    y = labels[a.label]
    tr, te = R.split(len(y), 0.7, seed=a.seed)
    print(f'readiness run on {a.label}: {len(tr)} train, {len(te)} held out')
    w, b = R.least_squares(X[tr], y[tr], ridge=a.ridge)
    pred = R.predict(X, w, b)
    print(f'1 direction by least squares: |w| {R.norm(w):.4f}; held-out correlation {R.correlation(pred[te], y[te]):.3f}')
    null = R.permutation_null(pred[te], y[te], n_perm=200, seed=a.seed)
    print(f'2 permutation baseline: 97.5th percentile {np.percentile(null, 97.5):.3f}')
    comps, explained, scores = R.pca(X[tr], 5)
    print(f'3 PCA on train: variance explained {explained}; correlation of each component score with {a.label} on held out: ' +
          ' '.join(f'{R.correlation((X[te] - X[tr].mean(0)) @ comps[i], y[te]):.3f}' for i in range(5)))
    print(f'4 cos(w, PCA component 1) = {R.cosine(w, comps[0]):.3f}')
    Xr = R.remove_direction(X, w)
    w2, b2 = R.least_squares(Xr[tr], y[tr], ridge=a.ridge)
    print(f'5 after removing w: refit held-out correlation {R.correlation(R.predict(Xr[te], w2, b2), y[te]):.3f}')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    def add(name, fn, help, **opts):
        s = sub.add_parser(name, help=help)
        for flag, kw in opts.items():
            s.add_argument('--' + flag.replace('_', '-'), **kw)
        s.set_defaults(fn=fn)
    tok = dict(type=int, default=12, help='token index (default 12)')
    lab = dict(default='is_digit', choices=['is_digit', 'after_period', 'starts_with_space', 'capitalised', 'position'])
    add('inspect', cmd_inspect, 'lesson 00: shapes and a token vector', token=tok)
    add('vectors', cmd_vectors, 'lesson 01: add, scale, subtract activation vectors', token=tok, other=dict(type=int, default=40))
    add('similar', cmd_similar, 'lesson 02: norms, dot products, cosine similarity', token=tok)
    add('project', cmd_project, 'lesson 03: project every token onto a direction', label=lab, token=tok)
    add('shapes', cmd_shapes, 'lesson 04: a weight matrix as a map between spaces', token=tok)
    add('matmul', cmd_matmul, 'lesson 05: batching, composition, einsum', token=tok)
    add('basis', cmd_basis, 'lesson 06: the same vector in two bases', token=tok)
    add('rank', cmd_rank, 'lesson 07: rank and near-orthogonal directions')
    add('remove', cmd_remove, 'lesson 08: orthogonal projection and removing a direction', label=lab)
    add('probe', cmd_probe, 'lesson 09: least-squares direction with a held-out check', label=lab, ridge=dict(type=float, default=0.0), seed=dict(type=int, default=0))
    add('covariance', cmd_covariance, 'lesson 10: covariance and its eigenvectors')
    add('pca', cmd_pca, 'lesson 11: PCA on the activation matrix', k=dict(type=int, default=10), keep_first=dict(action='store_true'))
    add('svd', cmd_svd, 'lesson 12: SVD and low-rank approximation', )
    add('gradient', cmd_gradient, 'lesson 13: gradients of a dot product and a norm', token=tok)
    add('correlation', cmd_correlation, 'lesson 14: is the correlation real?', label=lab, ridge=dict(type=float, default=0.0), seed=dict(type=int, default=0), perms=dict(type=int, default=200))
    add('review', cmd_review, 'readiness review pipeline', label=lab, ridge=dict(type=float, default=0.0), seed=dict(type=int, default=0))
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == '__main__':
    main()
