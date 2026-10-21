from common import lesson, lab, cite, transcript

LESSONS = [
lesson(6,2,'vision-replication','Vision I: curve detectors on a CPU, with the test written first',
 'InceptionV1, synthetic curves, feature visualisation in plain torch, and a replication that had to change shape when the weights turned out to be different.',
 '''<h2 id="the-claim">The claim being replicated</h2>
<p>Cammarata et al. (2020) describe a family of ten units in InceptionV1’s mixed3b layer, numbered 379, 406, 385, 343, 342, 388, 324, 340, 330, and 349, and claim: “Each curve detector implements a variant of the same algorithm: it responds to a wide variety of curves, preferring curves of a particular orientation and gradually firing less as the orientation changes. Curve neurons are invariant to cosmetic properties such as brightness, texture, and color,” and “Curve detectors collectively span all orientations” '''+cite('curves')+'''. The evidence is of seven kinds, listed in Zoom In: feature visualisation, dataset examples, synthetic examples, joint tuning, feature implementation, feature use, and handwritten circuits '''+cite('zoomin')+'''. Synthetic stimuli are the kind you can run on a laptop: draw a curve with known orientation, show it, read the activation.</p>
<h2 id="setup">The model, and the first surprise</h2>
<p>The 2026 essay’s advice is that native neurons need only forward passes, and “InceptionV1 runs on a CPU” is true: <code>torchvision.models.googlenet</code> with <code>GoogLeNet_Weights.IMAGENET1K_V1</code> loads in about a second and runs a 224×224 image in well under a second. The layer the paper calls mixed3b is <code>inception3b</code>, with 480 channels on a 28×28 map. The labs draw a thin dark arc through the centre of a grey field, subtract the response to a blank grey field, and read the mean of the central 2×2 cells of the channel’s post-ReLU map.</p>
<p>The first pre-registered test was the direct one: show the ten named units arcs at 36 orientations and predict that each is orientation-selective. It was run, and it is in the transcript as <code>curve_tuning.py --units 379,…</code>. Here are the named units on the held-out stimuli of the two-stage protocol described below:</p>
'''+transcript('''  ch  scr held   peak   opp  inv    ipk   line  H1 H2 H3 H4
 379  180  120   0.05  0.00  240   0.23   0.00   -  y  -  y
 406  250  250  -0.27   nan  250  -0.24  -0.25   y  -  -  -
 385  170  170   0.53  0.51   20   0.71   0.85   y  -  -  -
 343  210  190   0.01 -22.50   90   0.18  -0.07   y  y  -  y
 342  180    0  -0.62   nan  140  -0.57  -0.62   -  -  -  -
 388  310  310   0.80  0.00  310   0.70   0.12   y  y  y  y
 324   80  100   0.57  0.37  100   0.55   0.44   y  -  y  -
 340   20  280   0.46  0.00  170   0.44   0.25   -  y  -  y
 330   70   90   0.24  0.00   80   0.30   0.62   y  y  y  -
 349  240  240   1.54  0.00  230   1.42   0.52   y  y  y  y

H1: candidates 70% (need >= 80%) -> FAIL; random-channel control 73%
H2: candidates 60% (need >= 80%) -> FAIL; random-channel control 49%
H3: candidates 40% (need >= 60%) -> FAIL; random-channel control 39%
H4: candidates 50% (need >= 80%) -> FAIL; random-channel control 48%
H1-H4 jointly: candidates 20%; random-channel control 23%''')+'''
<p>The named units are indistinguishable from random channels: 20% of them pass all four hypotheses, against 23% of 100 random channels. Peaks are tiny (the strongest, 349, reaches 1.54, where the channels found below reach 6.6), and two units go negative on every stimulus. This is not a failure of the paper. It is the expected outcome of a mistake in the replication design that the test caught: torchvision’s GoogLeNet weights are its own training run (the weight file’s recipe points to torchvision’s classification reference, and the model applies its own input transform when those weights are loaded) '''+cite('torchvision')+''', not the TensorFlow InceptionV1 the Distill work used. Channel 379 of one training run has no relation to channel 379 of another. The named-unit replication cannot be done with these weights, and the course says so rather than quietly dropping the test.</p>
<h2 id="two-stage">The replication that can be done: the family claim</h2>
<p>What transfers between training runs, if the paper is right about the architecture, is the <em>family</em>: mixed3b should contain orientation-selective curve detectors spanning the circle. That claim can be tested with a two-stage protocol that keeps the look and the test apart.</p>
<p><strong>Stage 1, screening.</strong> Show all 480 channels dark arcs at 36 orientations and two radii (25 and 45 px, 3 px thick). Rank channels by peak response times orientation selectivity. Take the top 12. This stage is looking: it chooses the hypothesis, and nothing it produces is evidence.</p>
<p><strong>Stage 2, pre-registered, on stimuli the screening never saw.</strong> Written before the held-out stimuli were rendered:</p>
<pre><code>H1  held-out radii (35, 60 px) and thickness (5 px): preferred orientation within 20° of screening, for >= 80% of candidates
H2  response at preferred+180° < 0.25 x peak, for >= 80%          (a curve bent the other way is a different curve)
H3  light arc on dark field: preference within 20°, peak >= 0.3 x dark-arc peak, for >= 60%   (cosmetic invariance)
H4  arc peak > 1.5 x the peak to a straight line of the same tangent, for >= 80%             (curve, not edge)
H5  held-out preferred orientations leave no gap > 90° around the circle                     (family spans orientations)
controls: 100 random non-candidate channels through the same tests; blank-field response subtracted everywhere</code></pre>
<p>H2 and H4 do the work a sceptic needs. A line or edge detector responds to the same stimulus at θ and θ+180° (the tangent is the same) and to a straight line as much as to an arc. A curve detector should not. The result:</p>
'''+transcript('''STAGE 1 (screening on 36x2 dark arcs): median channel peak 0.33, selectivity median 0.33
  top 12 channels by peak x selectivity: [177, 222, 158, 128, 133, 246, 284, 253, 194, 311, 140, 242]

STAGE 2 (held-out stimuli):
  ch  scr held   peak   opp  inv    ipk   line  H1 H2 H3 H4
 177  180  180   6.62  0.00  180   5.99   0.13   y  y  y  y
 222   90  100   5.79  0.00  100   5.82   0.35   y  y  y  y
 158  150  150   5.45  0.00  150   5.48   1.11   y  y  y  y
 128    0   10   5.48 -0.05   10   5.04   0.17   y  y  y  y
 133   40   40   4.96  0.00   40   5.05   0.57   y  y  y  y
 246  120  120   4.72  0.00  120   4.44   0.83   y  y  y  y
 284  270  270   4.12 -0.02  260   4.23  -0.03   y  y  y  y
 253  210  200   4.73  0.00  210   4.06   0.39   y  y  y  y
 194  310  300   3.98  0.00  310   3.21   0.30   y  y  y  y
 311  310  310   3.61  0.00  310   3.93   0.19   y  y  y  y
 140   80   80   3.91  0.00   80   3.39   0.50   y  y  y  y
 242  270  270   4.45  0.00  270   4.32   0.37   y  y  y  y

H1: candidates 100% (need >= 80%) -> pass; random-channel control 72%
H2: candidates 100% (need >= 80%) -> pass; random-channel control 47%
H3: candidates 100% (need >= 60%) -> pass; random-channel control 42%
H4: candidates 100% (need >= 80%) -> pass; random-channel control 46%
H1-H4 jointly: candidates 100%; random-channel control 22%
H5: held-out preferred orientations [10, 40, 80, 100, 120, 150, 180, 200, 270, 270, 300, 310]; largest gap 70 degrees -> pass''')+'''
<p>All twelve candidates pass all four held-out hypotheses; 22 of 100 random channels do. Every candidate is silent at the opposite orientation (<code>opp</code> 0.00), keeps its preference under inverted contrast (<code>inv</code> within 10° of <code>held</code>, peaks within a few percent), and responds between 4 and 50 times more to an arc than to a line of the same tangent. The preferred orientations cover the circle with no gap above 70°. Lesson 07 reads the controls more carefully, because 72% of random channels passing H1 is not nothing.</p>
<h2 id="feature-vis">Feature visualisation without a library</h2>
<p>The paper’s first line of evidence is feature visualisation: “optimization to find the input to a neural network that maximizes a given objective” '''+cite('curves')+'''. <code>labs/reference/feature_vis.py</code> does it in forty lines of torch: a 128×128 image parameterised through a sigmoid, random jitter each step, bilinear upsampling to 224, Adam on the negative centre activation of the channel plus a small total-variation penalty. For channel 177, the best screening candidate, the centre objective goes from 0.01 at step 0 to 9.87 at step 150, above anything a rendered arc achieved (6.62).</p>
<p><img src="../assets/img/fv-3b-177.png" alt="Feature visualisation of inception3b channel 177: a field of curved, roughly concentric stripes" width="128" height="128"> The result is a field of curved, roughly parallel stripes, which is consistent with a curve detector and would also be consistent with several other things. The paper’s view, that feature visualisation “establishes a causal link, while dataset examples test the neuron’s use in practice” '''+cite('zoomin')+''', is the right way to hold it: the image shows what can drive the unit, not what does.</p>
<div class="evals"><span class="label">In interpretability work</span><p>A replication that cannot use the paper’s unit numbers is still a replication of the paper’s architectural claim, if you say which claim you are testing. “Independent training runs of InceptionV1 develop a mixed3b curve family” is a stronger and more interesting result than “unit 379 is a curve detector,” and it is the one these weights can address.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Reusing screening stimuli as test stimuli. The screening radii were 25 and 45 px, 3 px thick; the held-out ones are 35 and 60 px, 5 px thick, plus inverted contrast and lines. Had the candidates been tested on the screening set, 100% would have been guaranteed by construction.</p></div>''',
 'The named units scored like random channels. A colleague concludes “the Curve Detectors result does not replicate.” What is wrong with that sentence, and what is the correct one?',
 'The named-unit test did not test the paper’s claim, because the units it named exist only in the paper’s weights; it tested whether torchvision’s channel 379 happens to be a curve detector, which nobody claimed. The correct sentence is: “The paper’s unit numbers do not transfer to torchvision’s independently trained GoogLeNet, as expected; the family-level claim, that mixed3b contains orientation-selective curve detectors spanning all orientations, replicated on held-out synthetic stimuli with 12/12 candidates passing four pre-registered hypotheses against 22/100 random channels.”',
 lab(['python labs/reference/curve_tuning.py','python labs/reference/feature_vis.py --unit 177 --out assets/img/fv-3b-177.png'],
 'Run the two-stage test and the feature visualisation. Then change <code>--top 12</code> to <code>--top 24</code> and predict, before running, how the pass rates will change.',
 'Candidates ranked 13–24 are weaker on screening, so some will fail H2 or H4 on held-out stimuli; the pass rate should fall toward the random-channel rate as the ranking runs out of real curve units. Whether it falls at 13 or at 20 is a measurement of how large the family is in these weights, which the paper’s count of ten (in its weights) does not settle.'), ['curves','zoomin','torchvision']),

lesson(7,2,'vision-controls','Vision II: controls for the vision claim, and what replication established',
 'Random channels, rotated stimuli, and the line comparison, read as a sceptic would read them. Then the honest summary.',
 '''<h2 id="reading-controls">What 72% means</h2>
<p>H1 (preferred orientation stable across radius and thickness) passed for 100% of candidates and 72% of random channels. A control pass rate that high says the hypothesis is weak on its own: most channels in an early vision layer are orientation-tuned to something, and a thin dark arc has an orientation, so most channels’ preferred angle survives a change of radius. H1 is a necessary condition, not a discriminating one. It was pre-registered anyway because its failure would have been decisive.</p>
<p>H2 (silent at the opposite orientation) is where curve detectors separate from edge detectors: 47% of random channels passed. H4 (arc beats line by 1.5×) is the other half of the same distinction: 46%. H3 (contrast inversion) at 42% tests the paper’s cosmetic-invariance claim. The joint rate is the number to quote: 22% of random channels pass all four, against 100% of candidates. If the candidates had been random channels dressed up by screening, you would expect their joint rate to be near 22%, not 100%. That gap is the result.</p>
<p>But notice what 22% also says: roughly a fifth of mixed3b channels behave like curve detectors on these tests without having been selected for it. Either the family is much larger than twelve, or the four tests are not strict enough to exclude units that are curve-like without being curve detectors (the paper’s own candidates for that role are “double curve detectors” and units that respond to angles). A sceptic would say: your tests admit a fifth of the layer; your candidates are the fifth that also respond strongly. The reply is that the screening score was peak × selectivity, so “respond strongly and selectively” is exactly what was selected, and the held-out tests asked four independent questions the screening did not. Both are right. The honest statement is that the tests discriminate curve-like from non-curve-like channels, and the screening picks the strongest curve-like ones.</p>
<h2 id="rotated">The rotated-stimulus control is built in</h2>
<p>A classic control for a claimed detector is to show the same stimulus transformed in a way the claim says should matter. For orientation the transform is rotation, and the tuning curve already contains it: every orientation from 0° to 350° is the same arc rotated. H2 reads one point of that curve, the 180° rotation, where the arc’s tangent is unchanged and its curvature sign is flipped. The paper describes the analogous phenomenon in its lower layers: conv2d2 curve units “also weakly activate to a range on the opposite side, 180 degrees away. We call this secondary range echoes” '''+cite('curves')+'''. In the authoring run, all twelve mixed3b candidates had an opposite-orientation response of 0.00 of peak (one was −0.05, below baseline). No echoes at this layer, in these weights, at these stimulus sizes.</p>
<h2 id="not-established">What was not established</h2>
<p>Be exact about scope, because the paper is. Its claims are causality, generality, purity, and family. Of the seven lines of evidence, this replication ran two (synthetic examples and feature visualisation) and a fragment of a third (the tuning curve, but on synthetic rather than rotated dataset examples). It did not run dataset examples at all, because the course ships no natural images; so the claim that these channels fire on curves <em>in photographs</em>, which is what makes them detectors rather than responders, is untested here. The paper’s “Purity” claim, that curve detectors “are not polysemantic and they have no meaningful secondary function,” needs the dataset analysis and attribution it was built on; the synthetic tests cannot address it. And the paper itself reports fragility: “tiny changes in orientation or curvature can cause dramatic changes in activations, which indicate that curve detectors are fragile and non-robust.” The held-out tests used a 20° tolerance and two new radii; they did not map the wisps.</p>
<table><tr><th>Paper claim</th><th>Tested here?</th><th>Result</th></tr>
<tr><td>Orientation selectivity</td><td>Yes (H1, H2)</td><td>Replicated for 12 screened channels; H2 discriminates</td></tr>
<tr><td>Cosmetic invariance (contrast)</td><td>Partly (H3)</td><td>Replicated for polarity; colour and texture untested</td></tr>
<tr><td>Curve rather than edge</td><td>Yes (H4)</td><td>Replicated; ratios 4× to 50×</td></tr>
<tr><td>Family spans orientations</td><td>Yes (H5)</td><td>Replicated; largest gap 70°</td></tr>
<tr><td>Tolerance of radius</td><td>Partly</td><td>Two screening and two held-out radii; not a radius sweep</td></tr>
<tr><td>Fires on curves in natural images</td><td>No</td><td>Untested; no image dataset shipped</td></tr>
<tr><td>Purity (no secondary function)</td><td>No</td><td>Untested</td></tr>
<tr><td>Specific unit numbers</td><td>Attempted</td><td>Do not transfer; different training run</td></tr></table>
<h2 id="essay-connection">Why this matters for the 2026 argument</h2>
<p>The essay’s argument about superposition leans on this layer. It retrains InceptionV1 with mixed3b “cut from 480 to 10 channels,” reports that the channels stay interpretable but coarser, with “one ‘curves &amp; loops’ neuron instead of ten curve detectors,” and tests whether a sparse autoencoder on the squeezed layer recovers ten curve detectors: “We don’t see anything like clean curve neurons!” '''+cite('cammarata2026')+'''. Its table gives the original ten detectors’ tuning widths as “24–56° wide and silent at the opposite angle,” measured as “the response at the centre of the image to a thin dark arc drawn at 180 angles and two curvatures.” That is the same measurement as the labs, on different weights. “Silent at the opposite angle” is H2, and in this run it held for every candidate. You now have the apparatus to check one piece of a 2026 argument with your own forward passes, which is the point of the vision half of the course.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Write the “not established” table before the “established” one. Reviewers find the gaps anyway; a write-up that names them first is read as careful, and one that omits them is read as either naive or selective.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Quoting the pass rate without the control rate. “12/12 passed” is meaningless without “22/100 random channels passed the same tests.” The pair is the result.</p></div>''',
 'You add a fifth held-out test: response to a filled disc of the same radius. Which way should a curve detector go, and what does the paper say about fill?',
 'The paper reports that curves “are invariant to fill” in its synthetic experiments, so a curve detector should respond to a filled disc’s edge about as it does to the arc at the matching orientation; a unit that drops to zero on fill would be a thin-line detector rather than a curve detector. Pre-register the direction and a tolerance before rendering the discs. Note that a disc has every orientation on its boundary, so the orientation-selective response comes from the part of the edge that falls in the receptive field.',
 lab(['python labs/reference/curve_tuning.py --random 300'],
 'Raise the random-channel control from 100 to 300 and record the joint pass rate. Then implement <code>labs/curve_detector.py</code>; its tests include a synthetic line detector that must fail H2 and H4 and a synthetic curve detector that must pass all four.',
 'The joint control rate should move only a few points with 300 channels; if it moves a lot, 100 was too few and the protocol should have said 300. The tests for evaluate_candidate are the specification of what “curve detector” means in this course: write them down in words before coding, and compare your words with the paper’s.'), ['curves','cammarata2026']),
]
