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
