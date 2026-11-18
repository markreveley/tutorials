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

from stats import (benjamini_hochberg, bonferroni, bootstrap, exact_discordance,
                   paired_sample_size, pass_at_k, pearson, pearson_normal_pvalue, permutation_pvalue,
                   quantile, ranks, spearman, wilson, zero_failure_bound)
from stats_lab import analyze, load_candidates, load_tasks
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
                   lambda:pearson([1,2,3],[1,2]),lambda:pearson([1,1,1],[1,2,3]),
                   lambda:pearson([1,2,float('nan')],[1,2,3]),lambda:spearman([1,2],[1,2]),
                   lambda:permutation_pvalue([1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],permutations=10),
                   lambda:bonferroni([.5,1.5]),lambda:benjamini_hochberg([],.05),lambda:benjamini_hochberg([.1],1),
                   lambda:pearson_normal_pvalue(1.5,10),lambda:pearson_normal_pvalue(.5,2),
                   lambda:pass_at_k(2,4,5),lambda:quantile([], .5),
                   lambda:paired_sample_size(float('nan'),.03),
                   lambda:bootstrap([[0]],100,7),lambda:bootstrap([[0],[1]],99,7)]
        for call in bad_calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError): call()

    def test_pearson_hand_computed(self):
        # Lesson 24 example: deviations of x are ±3.5,±2.5,±1.5,±0.5; Σdxdy=80, Σdx²=42, Σdy²=252.
        x=[1,2,3,4,5,6,7,8]; y=[3,1,2,5,4,6,7,20]
        self.assertAlmostEqual(pearson(x,y),80/math.sqrt(42*252))
        # Four points: Σdxdy=4, Σdx²=Σdy²=5, so r=0.8.
        self.assertAlmostEqual(pearson([1,2,3,4],[1,3,2,4]),.8)
        self.assertAlmostEqual(pearson([1,2,3],[3,2,1]),-1)
        self.assertAlmostEqual(pearson([1,2,3],[2,4,6]),1)
        # Symmetry and invariance to shifting and positive scaling.
        self.assertAlmostEqual(pearson(x,y),pearson(y,x))
        self.assertAlmostEqual(pearson([10*v+3 for v in x],y),pearson(x,y))

    def test_spearman_ranks_and_ties(self):
        self.assertEqual(ranks([30,10,20]),[3,1,2])
        self.assertEqual(ranks([1,2,2,3]),[1,2.5,2.5,4])
        self.assertEqual(ranks([5,5,5]),[2,2,2])
        # Lesson 24 example without ties: 1−6Σd²/(n(n²−1)) with Σd²=8 gives 38/42.
        x=[1,2,3,4,5,6,7,8]; y=[3,1,2,5,4,6,7,20]
        self.assertAlmostEqual(spearman(x,y),1-6*8/(8*63))
        self.assertAlmostEqual(spearman(x,y),38/42)
        # Ties use average ranks: ranks [1,2.5,2.5,4] against [1,2,3,4] give 4.5/√22.5.
        self.assertAlmostEqual(spearman([1,2,2,3],[10,20,30,40]),4.5/math.sqrt(22.5))
        # Any increasing transform leaves Spearman at 1 while Pearson drops.
        self.assertAlmostEqual(spearman(x,[math.exp(v) for v in x]),1)
        self.assertLess(pearson(x,[math.exp(v) for v in x]),1)

    def test_exact_permutation_enumeration(self):
        # Perfect order on four points: only the ascending and descending orderings
        # reach |r|=1, so p = 2/24.
        observed,p,draws=permutation_pvalue([1,2,3,4],[1,2,3,4],pearson,exact=True)
        self.assertEqual((observed,draws),(1,24))
        self.assertAlmostEqual(p,2/24)
        # Enumerate by hand with itertools and compare for a nontrivial case.
        x=[1,2,3,4,5]; y=[2,5,1,4,3]
        observed,p,draws=permutation_pvalue(x,y,pearson,exact=True)
        count=sum(abs(pearson(x,list(perm)))>=abs(observed)-1e-12 for perm in itertools.permutations(y))
        self.assertEqual(draws,120)
        self.assertAlmostEqual(p,count/120)
        # Randomized version: p is at least 1/(permutations+1) and never above 1.
        _,p,draws=permutation_pvalue([1,2,3,4,5,6,7,8,9,10],[1,2,3,4,5,6,7,8,9,10],pearson,permutations=200,exact=False)
        self.assertEqual(draws,200)
        self.assertAlmostEqual(p,1/201)
        _,p,_=permutation_pvalue(list(range(10)),[0,1]*5,pearson,permutations=200,exact=False)
        self.assertLessEqual(p,1)

    def test_normal_theory_tail_matches_closed_forms(self):
        # n=3: (r+1)/2 is arcsine distributed, so P(|r|>=.5)=2(1−(2/π)asin(√.75))=2/3.
        self.assertAlmostEqual(pearson_normal_pvalue(.5,3),2/3,places=6)
        # n=4: r is uniform on [−1,1], so P(|r|>=.5)=.5 and P(|r|>=.2)=.8.
        self.assertAlmostEqual(pearson_normal_pvalue(.5,4),.5,places=9)
        self.assertAlmostEqual(pearson_normal_pvalue(-.2,4),.8,places=9)
        # n=6: density 3(1−r²)/4, so P(|r|>=.5)=2×3/4×(.5−.875/3)=.3125.
        self.assertAlmostEqual(pearson_normal_pvalue(.5,6),.3125,places=9)
        self.assertEqual(pearson_normal_pvalue(0,10),1)
        self.assertAlmostEqual(pearson_normal_pvalue(1,10),0,places=12)
        self.assertLess(pearson_normal_pvalue(.5,50),pearson_normal_pvalue(.5,10))

    def test_bonferroni_and_benjamini_hochberg_known_lists(self):
        # Lesson 24 table: m=8, q=.05, thresholds i/8×.05; five pass BH, two pass Bonferroni.
        ps=[.0004,.003,.009,.02,.03,.06,.4,.8]
        self.assertEqual(benjamini_hochberg(ps,.05),[True]*5+[False]*3)
        self.assertEqual(bonferroni(ps,.05),[True,True]+[False]*6)
        # Step-up matters: p(2)=.045 exceeds 2/3×.05 but p(3)=.05 meets 3/3×.05, so all three are rejected.
        self.assertEqual(benjamini_hochberg([.001,.045,.05],.05),[True,True,True])
        self.assertEqual(bonferroni([.001,.045,.05],.05),[True,False,False])
        # Input order is preserved and nothing is rejected when nothing is small.
        self.assertEqual(benjamini_hochberg([.2,.005,.04,.01],.05),[False,True,False,True])
        self.assertEqual(benjamini_hochberg([.3,.5,.9],.05),[False]*3)
        # BH never rejects fewer than Bonferroni.
        for seed in range(5):
            import random
            rng=random.Random(seed); ps=[rng.random()**3 for _ in range(50)]
            self.assertTrue(all(b<=h for b,h in zip(bonferroni(ps),benjamini_hochberg(ps))))

    def test_candidates_fixture_and_loader(self):
        rows=load_candidates(ROOT/'data/candidates.jsonl')
        self.assertEqual(len(rows),60)
        self.assertEqual([r['candidate_id'] for r in rows if r['planted']],
                         ['unit-003','unit-013','unit-023','unit-033','unit-043','unit-053'])
        self.assertTrue(all(len(r['activation'])==len(r['label'])==40 for r in rows))
        self.assertTrue(all(r['label']==rows[0]['label'] for r in rows))
        row=dict(candidate_id='u',activation=[1,2,3],label=[1,2,3])
        cases=[[row,row],[row,dict(row,candidate_id='v',label=[1,2])],
               [row,dict(row,candidate_id='v',activation=[1,None,3])],
               [row,dict(row,candidate_id='v',activation=[True,2,3])]]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'c.jsonl'
            for data in cases:
                p.write_text(''.join(json.dumps(r)+'\n' for r in data))
                with self.assertRaises(ValueError): load_candidates(p)

    def test_correlate_and_screen_cli(self):
        result=subprocess.run([sys.executable,str(ROOT/'stats_lab.py'),'correlate','--x','1 2 3 4 5 6 7 8','--y','3 1 2 5 4 6 7 20'],
                              cwd=ROOT.parent.parent,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('Pearson r: +0.7776',result.stdout)
        self.assertIn('Spearman rho: +0.9048',result.stdout)
        self.assertIn('40,320 orderings',result.stdout)
        result=subprocess.run([sys.executable,str(ROOT/'stats_lab.py'),'screen','--candidates','200','--n','20'],
                              cwd=ROOT.parent.parent,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('Expected count passing p<0.05 if every candidate were null: 10',result.stdout)
        self.assertIn('held-out',result.stdout)

    def test_fixtures_reproduce_and_margins_match(self):
        for name,expected in fixtures().items():
            loader=load_candidates if name=='candidates.jsonl' else load_tasks
            self.assertEqual(loader(ROOT/'data'/name),expected)
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
