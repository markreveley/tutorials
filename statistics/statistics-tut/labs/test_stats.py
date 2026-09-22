"""Behavior and mathematical invariants for the teaching lab."""
import itertools
import json
import math
from pathlib import Path
from statistics import mean
import subprocess
import sys
import tempfile
import unittest

from stats import (bootstrap, exact_discordance, paired_sample_size, pass_at_k,
                   quantile, wilson, zero_failure_bound)
from stats_lab import analyze, load_tasks
from make_data import fixtures

ROOT=Path(__file__).resolve().parent


class StatisticalChecks(unittest.TestCase):
    def test_wilson_known_case_and_boundaries(self):
        lo,hi=wilson(50,100)
        self.assertAlmostEqual(lo,0.4038315303659956)
        self.assertAlmostEqual(hi,0.5961684696340044)
        self.assertAlmostEqual(wilson(0,10)[0],0)
        self.assertAlmostEqual(wilson(10,10)[1],1)
        self.assertLess(wilson(10,10)[0],.73)
        self.assertGreater(wilson(0,10)[1],.27)
        for n in (1,2,10,100):
            for x in range(n+1):
                a,b=wilson(x,n); c,d=wilson(n-x,n)
                self.assertTrue(0<=a<=x/n<=b<=1)
                self.assertAlmostEqual(a,1-d)
                self.assertAlmostEqual(b,1-c)

    def test_wilson_exact_coverage_in_example_population(self):
        # Integrate over every possible result instead of a randomized assertion.
        n,p=100,.7
        coverage=sum(math.comb(n,x)*p**x*(1-p)**(n-x)
                     for x in range(n+1) if wilson(x,n)[0]<=p<=wilson(x,n)[1])
        # Wilson inverts the score acceptance region around the hypothesized p.
        accepted=[x for x in range(n+1) if abs(x/n-p) <= 1.959963984540054*math.sqrt(p*(1-p)/n)]
        exact=sum(math.comb(n,x)*p**x*(1-p)**(n-x) for x in accepted)
        self.assertAlmostEqual(coverage,exact)
        self.assertAlmostEqual(coverage,.9371897486104566)

    def test_zero_failure_bound_inverts_probability(self):
        for n in (1,10,100,1000):
            upper=zero_failure_bound(n)
            self.assertAlmostEqual((1-upper)**n,.05)
        self.assertLess(zero_failure_bound(2995),.001)
        self.assertGreater(zero_failure_bound(2994),.001)

    def test_reliability_matches_enumerated_subsets(self):
        values=[1,1,1,0,0]
        for k in range(1,6):
            empirical=mean(any(group) for group in itertools.combinations(values,k))
            self.assertAlmostEqual(pass_at_k(3,5,k),empirical)

    def test_discordance_matches_exact_small_outcomes(self):
        self.assertEqual(exact_discordance(0,0),1)
        self.assertEqual(exact_discordance(3,3),1)
        self.assertAlmostEqual(exact_discordance(5,0),.0625)
        self.assertAlmostEqual(exact_discordance(4,1),.375)
        self.assertAlmostEqual(exact_discordance(36,24),exact_discordance(24,36))

    def test_quantile_convention(self):
        self.assertEqual(quantile([1,1,2,2,24],.5),2)
        self.assertAlmostEqual(quantile([1,1,2,2,24],.95),19.6)
        self.assertEqual(quantile([8],.5),8)

    def test_pairing_and_cluster_behavior(self):
        # With A == B every paired difference must remain exactly zero.
        equal=[dict(task_id=str(i),cluster_id=str(i),a=[i%2],b=[i%2]) for i in range(8)]
        ds,units,lo,hi=analyze(equal,'task',100,7)
        self.assertEqual((mean(ds),units,lo,hi),(0,8,0,0))
        rows=load_tasks(ROOT/'data/clustered_tasks.jsonl')
        _,n_task,lo_task,hi_task=analyze(rows,'task',4000,7)
        ds,n_cluster,lo_cluster,hi_cluster=analyze(rows,'cluster',4000,7)
        self.assertEqual((n_task,n_cluster),(120,30))
        self.assertAlmostEqual(mean(ds),.1)
        self.assertGreater(hi_cluster-lo_cluster,hi_task-lo_task)
        self.assertLess(lo_cluster,.03)
        self.assertGreater(lo_task,.03)

    def test_unequal_cluster_sizes_keep_task_weights(self):
        # Two clusters: [0] and [1,1,1]. Every two-cluster bootstrap has mean
        # 0, .75, or 1; enough seeded draws expose both extrema.
        self.assertEqual(bootstrap([[0],[1,1,1]],1000,7),(0,1))
        # Exact duplicated constant differences stay constant even with unequal sizes.
        for endpoint in bootstrap([[.2],[.2,.2,.2]],100,7):
            self.assertAlmostEqual(endpoint,.2)
        # One large cluster and 19 small clusters: with three large-cluster
        # draws, the pooled mean is 300/317, not 3/20.
        lo,hi=bootstrap([[1]*100]+[[0] for _ in range(19)],4000,7)
        self.assertEqual(lo,0)
        self.assertAlmostEqual(hi,300/317)

    def test_planning_scaling(self):
        self.assertEqual(paired_sample_size(.5,.03),2181)
        self.assertLessEqual(abs(paired_sample_size(.5,.03)-4*paired_sample_size(.5,.06)),3)
        self.assertLess(paired_sample_size(.35,.03),paired_sample_size(.5,.03))

    def test_invalid_values(self):
        bad_calls=[lambda:wilson(11,10),lambda:wilson(0,0),lambda:wilson(1.5,4),
                   lambda:pass_at_k(2,4,5),lambda:quantile([], .5),
                   lambda:paired_sample_size(float('nan'),.03),
                   lambda:bootstrap([[0]],100,7),lambda:bootstrap([[0],[1]],99,7)]
        for call in bad_calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError): call()

    def test_fixtures_reproduce_and_margins_match(self):
        for name,expected in fixtures().items():
            self.assertEqual(load_tasks(ROOT/'data'/name),expected)
        rows=load_tasks(ROOT/'data/paired_tasks.jsonl')
        self.assertEqual(sum(r['a'][0] for r in rows),144)
        self.assertEqual(sum(r['b'][0] for r in rows),156)

    def test_loader_rejects_duplicate_and_missing_scores(self):
        row=dict(task_id='t',cluster_id='c',slice='s',a=[1],b=[0])
        cases=[[row,row],[row,[]],[row,dict(row,task_id='u',b=[])],
               [row,dict(row,task_id='u',b=[None])],
               [row,dict(row,task_id='u',b=[True])],
               [row,dict(row,task_id='u',b=[0,1])]]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.jsonl'
            for data in cases:
                p.write_text(''.join(json.dumps(r)+'\n' for r in data))
                with self.assertRaises(ValueError): load_tasks(p)

    def test_cli_from_another_working_directory(self):
        result=subprocess.run([sys.executable,str(ROOT/'stats_lab.py'),'compare','--resamples','100'],
                              cwd=ROOT.parent.parent,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('B-A=+6.00',result.stdout)

    def test_quiz_reprompts_and_explains(self):
        result=subprocess.run([sys.executable,str(ROOT/'stats_lab.py'),'quiz'],
                              input='bad\n1\n2\n3\n2\n2\n3\n',text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('Please enter',result.stdout)
        self.assertIn('6/6',result.stdout)
        self.assertIn('Correct.',result.stdout)


if __name__=='__main__': unittest.main()
