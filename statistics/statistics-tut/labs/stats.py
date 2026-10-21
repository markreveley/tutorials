"""Small, auditable teaching implementations. Python standard library only."""
import math
import random
from statistics import NormalDist, mean, stdev


def count_pair(successes, trials):
    if isinstance(successes, bool) or isinstance(trials, bool):
        raise ValueError('counts must be integers')
    if not isinstance(successes, int) or not isinstance(trials, int):
        raise ValueError('counts must be integers')
    if trials < 1 or not 0 <= successes <= trials:
        raise ValueError('require trials >= 1 and 0 <= successes <= trials')


def probability(p):
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('probability must be finite and between 0 and 1')
    return p


def wilson(successes, trials, confidence=0.95):
    """Two-sided Wilson score interval for an iid Bernoulli sample."""
    count_pair(successes, trials)
    if not 0 < confidence < 1:
        raise ValueError('confidence must be between 0 and 1, exclusively')
    p = successes / trials
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    denominator = 1 + z*z/trials
    center = (p + z*z/(2*trials)) / denominator
    half = z * math.sqrt(p*(1-p)/trials + z*z/(4*trials*trials)) / denominator
    return (0.0 if successes == 0 else max(0.0, center-half),
            1.0 if successes == trials else min(1.0, center+half))


def quantile(values, q):
    """Linear interpolation between sorted values, index (n-1)*q (type 7)."""
    probability(q)
    xs = sorted(values)
    if not xs or not all(math.isfinite(x) for x in xs):
        raise ValueError('need nonempty finite values')
    i = (len(xs)-1)*q
    lo, hi = math.floor(i), math.ceil(i)
    return xs[lo] + (xs[hi]-xs[lo])*(i-lo)


def bootstrap(groups, resamples=4000, seed=7):
    """Percentile interval for row-weighted mean; resample intact independent groups.

    Within-group observations stay together. Unequal groups are concatenated,
    so each replicate recomputes both the numerator and the denominator.
    """
    if len(groups) < 2 or any(not group for group in groups):
        raise ValueError('need at least two nonempty independent groups')
    if resamples < 100:
        raise ValueError('use at least 100 resamples')
    if any(not math.isfinite(x) for group in groups for x in group):
        raise ValueError('bootstrap values must be finite')
    rng = random.Random(seed)
    sums = [sum(group) for group in groups]
    sizes = [len(group) for group in groups]
    draws = []
    for _ in range(resamples):
        chosen = [rng.randrange(len(groups)) for _ in groups]
        draws.append(sum(sums[i] for i in chosen) / sum(sizes[i] for i in chosen))
    return quantile(draws, .025), quantile(draws, .975)


def exact_discordance(wins, losses):
    """Two-sided exact McNemar conditional test: fair binomial on discordances."""
    if not isinstance(wins, int) or not isinstance(losses, int) or min(wins, losses) < 0:
        raise ValueError('wins and losses must be nonnegative integers')
    n = wins + losses
    if n == 0:
        return 1.0
    # Integer arithmetic avoids overflow from converting 2**n to float first.
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(min(wins, losses)+1)) / 2**n)


def paired_sample_size(sd, delta, alpha=.05, power=.8):
    """Large-sample planning approximation for independent paired differences."""
    if not math.isfinite(sd) or sd <= 0 or not math.isfinite(delta) or delta <= 0:
        raise ValueError('sd and delta must be finite and positive')
    if not 0 < alpha < 1 or not .5 < power < 1:
        raise ValueError('require 0 < alpha < 1 and .5 < power < 1')
    z = NormalDist()
    return math.ceil(((z.inv_cdf(1-alpha/2)+z.inv_cdf(power))*sd/delta)**2)


def zero_failure_bound(trials, confidence=.95):
    count_pair(0, trials)
    if not 0 < confidence < 1:
        raise ValueError('confidence must be between 0 and 1')
    return -math.expm1(math.log1p(-confidence)/trials)


def pass_at_k(successes, trials, k):
    count_pair(successes, trials)
    if not isinstance(k, int) or not 1 <= k <= trials:
        raise ValueError('require integer 1 <= k <= trials')
    return 1 - math.comb(trials-successes, k)/math.comb(trials, k) if trials-successes >= k else 1.0


def standard_error(values):
    if len(values) < 2:
        raise ValueError('need at least two independent observations')
    return stdev(values) / math.sqrt(len(values))


def _paired_finite(x, y):
    if len(x) != len(y):
        raise ValueError('x and y must have the same length')
    if len(x) < 3:
        raise ValueError('need at least three paired observations')
    if any(isinstance(v, bool) or not math.isfinite(v) for v in list(x)+list(y)):
        raise ValueError('values must be finite numbers')


def pearson(x, y):
    """Sample Pearson correlation: Σ(xᵢ−x̄)(yᵢ−ȳ) / √[Σ(xᵢ−x̄)² Σ(yᵢ−ȳ)²]."""
    _paired_finite(x, y)
    mx, my = mean(x), mean(y)
    sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    sxx = sum((a-mx)**2 for a in x)
    syy = sum((b-my)**2 for b in y)
    if sxx == 0 or syy == 0:
        raise ValueError('correlation is undefined when either variable is constant')
    return sxy / math.sqrt(sxx*syy)


def ranks(values):
    """Ranks from 1; tied values share the average of the ranks they occupy."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    result = [0.0]*len(values)
    i = 0
    while i < len(order):
        j = i
        while j+1 < len(order) and values[order[j+1]] == values[order[i]]:
            j += 1
        shared = (i+j+2)/2          # average of positions i+1 .. j+1
        for k in range(i, j+1):
            result[order[k]] = shared
        i = j+1
    return result


def spearman(x, y):
    """Pearson correlation of the two rank lists (average ranks for ties)."""
    _paired_finite(x, y)
    return pearson(ranks(x), ranks(y))


def permutation_pvalue(x, y, statistic=pearson, permutations=2000, seed=7, exact=None):
    """Two-sided permutation p-value for an association statistic.

    The labels y are shuffled relative to x, the statistic recomputed, and
    |statistic| compared with the observed |statistic|. With exact=True every
    distinct ordering of y is enumerated and p is the exact fraction at least
    as extreme. Otherwise p = (count + 1)/(permutations + 1), which counts the
    observed ordering as one of the draws. Returns (observed, p, draws).
    """
    _paired_finite(x, y)
    observed = statistic(x, y)
    n = len(y)
    if exact is None:
        exact = n <= 8
    target = abs(observed) - 1e-12
    if exact:
        import itertools
        draws = math.factorial(n)
        count = sum(abs(statistic(x, list(p))) >= target for p in itertools.permutations(y))
        return observed, count/draws, draws
    if permutations < 100:
        raise ValueError('use at least 100 permutations')
    rng = random.Random(seed)
    shuffled = list(y)
    count = 0
    for _ in range(permutations):
        rng.shuffle(shuffled)
        count += abs(statistic(x, shuffled)) >= target
    return observed, (count+1)/(permutations+1), permutations


def pearson_normal_pvalue(r, n, panels=1000):
    """Two-sided P(|R| ≥ |r|) when x and y are independent bivariate-normal samples.

    Under that null the density of r is proportional to (1−r²)^((n−4)/2).
    Substituting r = sin θ turns the tail integral into ∫cos^(n−3)θ dθ, which
    Simpson's rule integrates accurately; the result is normalized by the
    same integral from 0 to π/2. Used only where the data are normal by
    construction; real data should use the permutation p-value.
    """
    if not isinstance(n, int) or n < 3 or not math.isfinite(r) or not -1 <= r <= 1:
        raise ValueError('need integer n >= 3 and -1 <= r <= 1')
    def integral(lower, upper):
        h = (upper-lower)/panels
        total = 0.0
        for i in range(panels+1):
            weight = 1 if i in (0, panels) else (4 if i % 2 else 2)
            total += weight * math.cos(lower+i*h)**(n-3)
        return total*h/3
    return min(1.0, integral(math.asin(abs(r)), math.pi/2) / integral(0, math.pi/2))


def _check_pvalues(pvalues, level):
    if not pvalues or any(not math.isfinite(p) or not 0 <= p <= 1 for p in pvalues):
        raise ValueError('p-values must be a nonempty list of numbers between 0 and 1')
    if not 0 < level < 1:
        raise ValueError('the error level must be between 0 and 1, exclusively')


def bonferroni(pvalues, alpha=.05):
    """Reject when p ≤ alpha/m. Returns a list of booleans in input order."""
    _check_pvalues(pvalues, alpha)
    return [p <= alpha/len(pvalues) for p in pvalues]


def benjamini_hochberg(pvalues, q=.05):
    """Step-up procedure: sort p-values, find the largest i with p(i) ≤ (i/m)q,
    reject the i smallest. Returns booleans in input order."""
    _check_pvalues(pvalues, q)
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    k = 0
    for rank, i in enumerate(order, 1):
        if pvalues[i] <= rank/m*q:
            k = rank
    rejected = [False]*m
    for i in order[:k]:
        rejected[i] = True
    return rejected
