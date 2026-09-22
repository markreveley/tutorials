#!/usr/bin/env python3
"""Offline statistics experiments for evals. Run --help or quiz to start."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import random
from statistics import mean, stdev
import sys
from stats import (bootstrap, count_pair, exact_discordance, paired_sample_size,
                   pass_at_k, probability, quantile, standard_error, wilson,
                   zero_failure_bound)

DATA = Path(__file__).resolve().parent / 'data'


def load_tasks(path):
    rows = []
    seen = set()
    with Path(path).open() as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f'line {number}: each record must be a JSON object')
            for key in ('task_id', 'cluster_id', 'slice'):
                if not isinstance(row.get(key), str) or not row[key]:
                    raise ValueError(f'line {number}: need nonempty {key}')
            if row['task_id'] in seen:
                raise ValueError(f'line {number}: duplicate task_id')
            seen.add(row['task_id'])
            for model in ('a', 'b'):
                scores = row.get(model)
                if not isinstance(scores, list) or not scores or any(type(x) is not int or x not in (0, 1) for x in scores):
                    raise ValueError(f'line {number}: {model} must be a nonempty list of 0/1 scores; missing is not zero')
            if len(row['a']) != len(row['b']):
                raise ValueError(f'line {number}: the teaching lab requires equal A/B attempt counts per task')
            rows.append(row)
    if len(rows) < 2:
        raise ValueError('need at least two tasks')
    return rows


def command_rate(args):
    lo, hi = wilson(args.passes, args.trials)
    print(f'Observed pass rate: {args.passes}/{args.trials} = {args.passes/args.trials:.1%}')
    print(f'95% Wilson interval: [{lo:.1%}, {hi:.1%}]')
    print('Assumption: independent Bernoulli trials sampled from the declared population.')
    print('This interval does not cover grader bias, task selection bias, or distribution shift.')


def command_sample(args):
    probability(args.p)
    if args.trials < 2 or args.experiments < 2:
        raise ValueError('need trials >= 2 and experiments >= 2')
    rng = random.Random(args.seed)
    rates = []
    covered = 0
    for _ in range(args.experiments):
        x = sum(rng.random() < args.p for _ in range(args.trials))
        rates.append(x/args.trials)
        lo, hi = wilson(x, args.trials)
        covered += lo-1e-12 <= args.p <= hi+1e-12
    print(f'Synthetic iid Bernoulli population: p={args.p:.3f}; n={args.trials}; seed={args.seed}')
    print(f'Experiments: {args.experiments}; mean estimate: {mean(rates):.3f}; SD of estimates: {stdev(rates):.4f}')
    print(f'Theoretical SE: {math.sqrt(args.p*(1-args.p)/args.trials):.4f}')
    print(f'Wilson coverage in this simulation: {covered/args.experiments:.1%}')
    bins = [0]*10
    for value in rates:
        bins[min(9, int(value*10))] += 1
    for i, count in enumerate(bins):
        print(f'{i*10:2}-{(i+1)*10:3}% | {"#"*round(40*count/max(bins))} {count}')
    print('Bins include the lower endpoint; only the final bin includes its upper endpoint.')
    print('Coverage varies with n, p, and Monte Carlo error; it need not equal exactly 95%.')


def analyze(rows, unit, resamples, seed):
    ds = [mean(r['b'])-mean(r['a']) for r in rows]
    groups = defaultdict(list)
    for r, d in zip(rows, ds):
        groups[r['task_id'] if unit == 'task' else r['cluster_id']].append(d)
    lo, hi = bootstrap(list(groups.values()), resamples, seed)
    return ds, len(groups), lo, hi


def command_compare(args):
    rows = load_tasks(args.data)
    if args.slice:
        rows = [r for r in rows if r['slice'] == args.slice]
        if len(rows) < 2:
            raise ValueError('slice must contain at least two tasks')
    ds, units, lo, hi = analyze(rows, args.unit, args.resamples, args.seed)
    a, b = mean(mean(r['a']) for r in rows), mean(mean(r['b']) for r in rows)
    print(f'Tasks: {len(rows)}; attempts/model: {sum(len(r["a"]) for r in rows)}; independent resampling units assumed: {units} ({args.unit})')
    print(f'Equal-task mean: A={a:.2%}; B={b:.2%}; B-A={100*(b-a):+.2f} percentage points')
    print(f'95% paired {args.unit} percentile bootstrap: [{100*lo:+.2f}, {100*hi:+.2f}] percentage points')
    print(f'Resamples: {args.resamples}; seed: {args.seed}; task-weighted statistic recomputed in each draw.')
    if args.unit == 'task' and len({r['cluster_id'] for r in rows}) < len(rows):
        print('CAUTION: shared clusters detected. Task resampling ignores that dependence; compare --unit cluster.')
    if units < 20:
        print('CAUTION: few independent units; percentile bootstrap coverage may be poor.')
    if math.isclose(lo, hi, abs_tol=1e-12):
        print('CAUTION: degenerate bootstrap interval; an unobserved outcome cannot be resampled.')
    if all(len(r['a']) == 1 for r in rows):
        wins = sum(r['b'][0] > r['a'][0] for r in rows)
        losses = sum(r['b'][0] < r['a'][0] for r in rows)
        print(f'B-only passes: {wins}; A-only passes: {losses}')
        if args.unit == 'task' and units == len({r['cluster_id'] for r in rows}):
            print(f'Two-sided exact discordance p-value: {exact_discordance(wins, losses):.4f}')
    print('Within-task attempts are averaged, never counted as new tasks. No within-task nested bootstrap is added.')
    print('Inference assumes independent sampled units, a stable run policy, and adequate coverage of the target population.')
    print('A bootstrap interval is approximate; increasing resamples does not add evaluation evidence.')


def command_power(args):
    n = paired_sample_size(args.sd, args.delta, args.alpha, args.power)
    print(f'Approximate independent pairs needed: {n}')
    print(f'Difference to detect: {100*args.delta:g} percentage points; SD of paired differences: {args.sd:g}')
    print(f'Two-sided alpha={args.alpha:g}; target power={args.power:g}; normal approximation.')
    print('Use a pilot estimate of difference SD, not the SD of one model. Clustering requires a design-aware plan.')
    print('This plans detection against zero, not proof that the effect exceeds a deployment threshold.')


def command_multiple(args):
    if args.tests < 1 or args.experiments < 1:
        raise ValueError('tests and experiments must be positive')
    rng = random.Random(args.seed)
    raw = adjusted = 0
    for _ in range(args.experiments):
        pvalues = [rng.random() for _ in range(args.tests)]
        raw += min(pvalues) < .05
        adjusted += min(pvalues) < .05/args.tests
    print('Toy null experiment: independent Uniform(0,1) p-values, every null true.')
    print(f'Families: {args.experiments}; tests/family: {args.tests}; seed: {args.seed}')
    print(f'At least one raw p<.05: {raw/args.experiments:.1%}; theoretical: {1-.95**args.tests:.1%}')
    print(f'At least one Bonferroni rejection: {adjusted/args.experiments:.1%}')
    print('Real eval tests can be dependent. Bonferroni still bounds familywise error when each p-value is valid.')


def command_peek(args):
    if args.experiments < 1:
        raise ValueError('experiments must be positive')
    rng = random.Random(args.seed)
    ever = final = 0
    for _ in range(args.experiments):
        total, crossed = 0, False
        for n in range(1, 1001):
            total += rng.gauss(0, 1)
            if n % 20 == 0 and abs(total/math.sqrt(n)) > 1.959963984540054:
                crossed = True
        ever += crossed
        final += abs(total/math.sqrt(1000)) > 1.959963984540054
    print('Toy null: iid Normal(0,1), known SD=1. Two-sided z tests; looks at n=20,40,...,1000.')
    print(f'Experiments: {args.experiments}; seed: {args.seed}')
    print(f'Reject only at planned n=1000: {final/args.experiments:.1%}')
    print(f'Reject if any look crosses 1.96: {ever/args.experiments:.1%}')
    print('This is a demonstration of a broken stopping rule, not a sequentially valid test.')


def command_bayes(args):
    count_pair(args.passes, args.trials)
    probability(args.threshold)
    if not all(math.isfinite(x) and x > 0 for x in (args.alpha, args.beta)) or args.draws < 100:
        raise ValueError('prior shapes must be finite and positive; use draws >= 100')
    a, b = args.alpha+args.passes, args.beta+args.trials-args.passes
    rng = random.Random(args.seed)
    draws = [rng.betavariate(a, b) for _ in range(args.draws)]
    print(f'Prior: Beta({args.alpha:g},{args.beta:g}); posterior: Beta({a:g},{b:g})')
    print(f'Posterior mean: {a/(a+b):.3f}')
    print(f'Approximate 95% equal-tail credible interval: [{quantile(draws,.025):.3f}, {quantile(draws,.975):.3f}]')
    print(f'Approximate P(p>{args.threshold:g} | data, model, prior): {mean(x>args.threshold for x in draws):.3f}')
    print(f'Monte Carlo draws: {args.draws}; seed: {args.seed}. Assumes iid Bernoulli outcomes with one common p.')
    print('Try another prior. Model misspecification and biased task selection are not covered by this posterior.')


def command_rare(args):
    bound = zero_failure_bound(args.trials)
    print(f'Zero failures in {args.trials} independent trials.')
    print(f'Exact one-sided 95% upper failure-probability bound: {bound:.6f} ({bound:.3%})')
    print(f'Rule-of-three approximation: {3/args.trials:.6f} (useful for large n).')
    print('Assumes a fixed n, independent trials and constant failure probability; a red-team set is not traffic prevalence.')


def command_reliability(args):
    estimate = pass_at_k(args.passes, args.trials, args.k)
    all_pass = math.comb(args.passes,args.k)/math.comb(args.trials,args.k) if args.passes >= args.k else 0
    print(f'One task: {args.passes}/{args.trials} passes; k={args.k}')
    print(f'At-least-one success estimator (pass@k): {estimate:.4f}')
    print(f'All-k-success estimator: {all_pass:.4f}')
    print('Compute per task, then average. Assumes independent, identically distributed attempts within a task.')
    print('These are point estimates, not uncertainty intervals or a policy for selecting a correct answer.')


QUESTIONS = [
 ('A and B answered the same 200 tasks. What do you analyze?',
  ['The 200 B-A task differences', 'Two unrelated headline percentages', 'Only the tasks B passed'], 0,
  'Keep the pairs: shared task difficulty can cancel. Choose an independent unit before computing uncertainty.'),
 ('Ten tasks each ran 100 times. How many distinct tasks were sampled?',
  ['1000', '10', '100'], 1,
  'There are 10 tasks and 1000 attempts. Repeats inform within-task behavior; they do not add task coverage.'),
 ('A 95% difference interval is [-2,+6] percentage points. What follows?',
  ['The systems are equivalent', 'B is better with 95% probability', 'Both modest harm and useful benefit remain compatible'], 2,
  'Failure to reject zero is not equivalence. Compare the interval with a predeclared practical margin.'),
 ('A grader has 98% accuracy; failures occur on 2% of cases. Next step?',
  ['Deploy it', 'Inspect failure recall and false alarms', 'Round accuracy to 100%'], 1,
  'An always-pass grader already gets 98% accuracy. Inspect a confusion matrix against independently adjudicated labels.'),
 ('You keep rerunning until p<.05. What changed?',
  ['Only convenience', 'The error properties of the decision rule', 'The model became better'], 1,
  'Ordinary fixed-sample p-values do not justify this stopping rule. Plan the endpoint or use an appropriate sequential design.'),
 ('You saw zero critical failures in 100 independent random cases. Report?',
  ['Failure probability is zero', 'Safety is proven', 'Zero observed; one-sided 95% upper bound about 3% under the model'], 2,
  'An unobserved failure can still occur. The bound depends on the sampling and independence assumptions.'),
]


def command_quiz(_args):
    print('Eval statistics: six judgment checks. Type 1, 2, or 3; q to quit. No data is saved.')
    score = 0
    for index, (question, options, answer, why) in enumerate(QUESTIONS, 1):
        print(f'\n{index}. {question}')
        for i, option in enumerate(options, 1):
            print(f'  {i}. {option}')
        while True:
            try:
                choice = input('Your answer: ').strip().lower()
            except EOFError:
                print('\nStopped. Re-run quiz in an interactive terminal.'); return
            if choice == 'q':
                print('Stopped.'); return
            if choice in ('1', '2', '3'):
                break
            print('Please enter 1, 2, 3, or q.')
        correct = int(choice)-1 == answer
        score += correct
        print(('Correct. ' if correct else 'Reconsider. ') + why)
    print(f'\n{score}/{len(QUESTIONS)}. For the full readiness task, open lesson 23.')


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest='command', required=True)
    p = sub.add_parser('rate', help='Wilson interval for a pass count'); p.add_argument('passes', type=int); p.add_argument('trials', type=int); p.set_defaults(run=command_rate)
    p = sub.add_parser('sample', help='simulate repeated samples and confidence-interval coverage'); p.add_argument('--p',type=float,default=.7); p.add_argument('--trials',type=int,default=100); p.add_argument('--experiments',type=int,default=2000); p.set_defaults(run=command_sample)
    p = sub.add_parser('compare', help='paired task or cluster bootstrap on JSONL data'); p.add_argument('--data',type=Path,default=DATA/'paired_tasks.jsonl'); p.add_argument('--unit',choices=('task','cluster'),default='task'); p.add_argument('--slice'); p.add_argument('--resamples',type=int,default=4000); p.set_defaults(run=command_compare)
    p = sub.add_parser('power', help='approximate independent-pair sample size'); p.add_argument('--sd',type=float,default=.5); p.add_argument('--delta',type=float,default=.03); p.add_argument('--alpha',type=float,default=.05); p.add_argument('--power',type=float,default=.8); p.set_defaults(run=command_power)
    p = sub.add_parser('multiple', help='simulate multiple null comparisons'); p.add_argument('--tests',type=int,default=20); p.add_argument('--experiments',type=int,default=5000); p.set_defaults(run=command_multiple)
    p = sub.add_parser('peek', help='demonstrate invalid repeated fixed-sample testing'); p.add_argument('--experiments',type=int,default=2000); p.set_defaults(run=command_peek)
    p = sub.add_parser('bayes', help='Beta-Binomial update and prior sensitivity'); p.add_argument('passes',type=int); p.add_argument('trials',type=int); p.add_argument('--alpha',type=float,default=1); p.add_argument('--beta',type=float,default=1); p.add_argument('--threshold',type=float,default=.8); p.add_argument('--draws',type=int,default=20000); p.set_defaults(run=command_bayes)
    p = sub.add_parser('rare', help='upper failure-rate bound after zero failures'); p.add_argument('trials',type=int); p.set_defaults(run=command_rare)
    p = sub.add_parser('reliability', help='at-least-one and all-k success estimates'); p.add_argument('passes',type=int); p.add_argument('trials',type=int); p.add_argument('k',type=int); p.set_defaults(run=command_reliability)
    p = sub.add_parser('quiz', help='interactive judgment checks with explanations'); p.set_defaults(run=command_quiz)
    for name in ('sample','compare','multiple','peek','bayes'):
        sub.choices[name].add_argument('--seed',type=int,default=7)
    return root


def main():
    p = parser()
    args = p.parse_args()
    try:
        args.run(args)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        p.error(str(error))
    except KeyboardInterrupt:
        print('\nStopped.', file=sys.stderr)
        return 130
    return 0


if __name__ == '__main__':
    sys.exit(main())
