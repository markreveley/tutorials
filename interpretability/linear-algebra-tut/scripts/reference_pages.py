from common import cite

REFERENCES = [
 dict(path='appendices/a-math.html',title='Notation and formulas',kicker='Appendix A',n='A',kw='formula notation symbols dot product projection norm svd pca least squares gradient',
 lede='Every formula used in the lessons, with its shapes and the lesson that explains it.',
 body='''<h2 id="symbols">Symbols</h2>
<table><tr><th>Symbol</th><th>Meaning</th></tr><tr><td>x, v, d</td><td>Vectors, 1-D arrays of length d; x is usually an activation, d a direction</td></tr><tr><td>d̂</td><td>d / ‖d‖, the unit vector along d</td></tr><tr><td>X</td><td>An activation matrix of shape (n, d): n tokens as rows</td></tr><tr><td>X_c</td><td>X with the mean row subtracted from every row</td></tr><tr><td>W</td><td>A weight matrix of shape (d_in, d_out), applied as x W in the row-vector convention</td></tr><tr><td>Aᵀ</td><td>Transpose: rows and columns swapped</td></tr><tr><td>I</td><td>Identity matrix</td></tr><tr><td>Σᵢ</td><td>Sum over the index i</td></tr><tr><td>λ, σ</td><td>An eigenvalue; a singular value</td></tr><tr><td>∇f</td><td>Gradient of a scalar function f</td></tr></table>
<h2 id="vectors">Vectors (lessons 01–03)</h2>
<div class="math">u + v = (u₁ + v₁, …);  c·u = (c·u₁, …)<br>u · v = Σᵢ uᵢvᵢ;  ‖u‖ = √(u · u);  cos θ = u · v / (‖u‖ ‖v‖)<br>projection coefficient c = v · d̂;  projection p = c d̂;  residual r = v − p, with r · d = 0 and ‖p‖² + ‖r‖² = ‖v‖²<br>batch: X d̂ has shape (n,), one coefficient per token</div>
<h2 id="maps">Maps (lessons 04–07)</h2>
<div class="math">(x W)ⱼ = x · (column j of W);  (n, k)·(k, m) → (n, m)<br>(AB)C = A(BC);  AB ≠ BA in general<br>einsum: 'nd,dh->nh' is X W; 'nh,mh->nm' is Q Kᵀ; a letter absent from the output is summed<br>coordinates in basis B (columns): solve B c = v; if B is orthonormal, cᵢ = v · bᵢ and ‖c‖ = ‖v‖<br>rank(AB) ≤ min(rank A, rank B);  rank of (n, d) ≤ min(n, d)</div>
<h2 id="subspaces">Subspaces and fitting (lessons 08–09)</h2>
<div class="math">Gram–Schmidt: wₖ = vₖ − Σⱼ&lt;ₖ (vₖ · qⱼ) qⱼ;  qₖ = wₖ / ‖wₖ‖<br>remove d from every row: X − (X d̂) d̂ᵀ = X (I − d̂ d̂ᵀ)<br>least squares: minimise ‖X w − y‖²;  normal equations XᵀX w = Xᵀy;  ridge (XᵀX + λI) w = Xᵀy<br>centred fit: w from X_c, y − ȳ;  intercept b = ȳ − x̄ · w</div>
<h2 id="spectra">Spectra (lessons 10–12)</h2>
<div class="math">A v = λ v;  symmetric A = V Λ Vᵀ with orthonormal V<br>covariance C = X_cᵀ X_c / (n − 1), shape (d, d);  Var(X_c u) = u · C u for unit u<br>PCA: components = eigenvectors of C in decreasing λ = rows of Vᵀ from the SVD of X_c;  explained(i) = λᵢ / Σλ;  scores = X_c Vₖᵀ<br>SVD: A = U Σ Vᵀ = Σᵢ σᵢ uᵢ vᵢᵀ;  A vᵢ = σᵢ uᵢ;  σᵢ² are eigenvalues of AᵀA<br>best rank-k: Aₖ = Σᵢ≤ₖ σᵢ uᵢ vᵢᵀ;  ‖A − Aₖ‖² = Σᵢ&gt;ₖ σᵢ²</div>
<h2 id="calculus">Gradients and correlation (lessons 13–14)</h2>
<div class="math">∇(v · d) = d;  ∇‖v‖ = v/‖v‖;  ∇‖v‖² = 2v;  ∇(v · d̂)² = 2 (v · d̂) d̂<br>central difference: ∂f/∂vᵢ ≈ (f(v + hεᵢ) − f(v − hεᵢ)) / 2h<br>corr(a, b) = (a − ā) · (b − b̄) / (‖a − ā‖ ‖b − b̄‖)</div>
<h2 id="library">numpy calls used</h2>
<table><tr><th>Call</th><th>Returns</th><th>Watch for</th></tr><tr><td><code>np.linalg.svd(A, full_matrices=False)</code></td><td>U, S (descending), Vt</td><td>Vt is Vᵀ: the top right singular vector is <code>Vt[0]</code> '''+cite('np-svd')+'''</td></tr><tr><td><code>np.linalg.lstsq(A, b, rcond=None)</code></td><td>x, residuals, rank, s</td><td>minimum-norm solution when underdetermined; residuals empty then '''+cite('np-lstsq')+'''</td></tr><tr><td><code>np.linalg.eigh(C)</code></td><td>eigenvalues ascending, eigenvectors as columns</td><td>reads one triangle only; never checks symmetry '''+cite('np-eigh')+'''</td></tr><tr><td><code>np.einsum('nd,dh->nh', X, W)</code></td><td>the contraction named by the letters</td><td>a letter missing from the output is summed '''+cite('np-einsum')+'''</td></tr></table>'''),
 dict(path='appendices/b-explorers.html',title='Projection and SVD explorers',kicker='Appendix B',n='B',kw='interactive explorer projection residual svd ellipse singular values drag',
 lede='Two-dimensional pictures of the two central operations. Drag the handles or type coordinates; the numbers are computed locally.',
 body='''<noscript><p>The explorers need JavaScript. The rest of the course works without it; the same computations are in <code>labs/linalg_lab.py project</code> and <code>svd</code>.</p></noscript>
<h2 id="projection">Projection onto a direction</h2>
<p>The blue arrow is v, the dashed line is the direction d, the orange segment is the projection of v onto d and the red dashed segment is the residual. Drag either handle, or type coordinates. Start with v = (3, 4) and d = (1, 1) to match the hand computation in <a href="../pages/03-projection-onto-a-direction.html">lesson 03</a>: coefficient 7/√2 ≈ 4.95, projection (3.5, 3.5), residual (−0.5, 0.5). Then rotate d until the residual vanishes, and until the coefficient turns negative.</p>
<form class="explorer" data-calculator="projection"><div class="row"><label for="vx">v, x-coordinate<input id="vx" name="vx" type="number" min="-5" max="5" step="any" value="3" required></label><label for="vy">v, y-coordinate<input id="vy" name="vy" type="number" min="-5" max="5" step="any" value="4" required></label><label for="dx">d, x-coordinate<input id="dx" name="dx" type="number" min="-5" max="5" step="any" value="1" required></label><label for="dy">d, y-coordinate<input id="dy" name="dy" type="number" min="-5" max="5" step="any" value="1" required></label></div><button type="submit">Project</button><svg class="plane" viewBox="0 0 420 420" role="img" aria-label="Projection of v onto the line through d"></svg><output aria-live="polite"></output><p>The coefficient does not change when d is scaled; the dot product v·d does. The residual is always orthogonal to d, and the squared lengths of projection and residual add up to the squared length of v.</p></form>
<h2 id="svd">A 2×2 matrix as a map</h2>
<p>Enter the four entries of a matrix A = [[a, b], [c, d]] in the row-vector convention x ↦ x A, so the first row is where (1, 0) goes. The dashed unit circle is the set of inputs of length 1; the shaded ellipse is where the matrix sends them. The dashed arrows are the right singular vectors v₁, v₂ (the input directions), and the orange arrows σ₁u₁ and σ₂u₂ are the ellipse’s semi-axes (the output directions, stretched). Try [[3, 0], [0, 2]] for a pure stretch, [[0, −1], [1, 0]] for a rotation (both singular values 1), [[1, 2], [2, 4]] for a rank-one matrix whose ellipse collapses to a line, and [[2, 1], [1, 2]] for a symmetric matrix whose singular vectors are its eigenvectors. See <a href="../pages/12-svd-and-low-rank.html">lesson 12</a>.</p>
<form class="explorer" data-calculator="svd"><div class="row"><label for="a">a (row 1, column 1)<input id="a" name="a" type="number" min="-5" max="5" step="any" value="2" required></label><label for="b">b (row 1, column 2)<input id="b" name="b" type="number" min="-5" max="5" step="any" value="1" required></label><label for="c">c (row 2, column 1)<input id="c" name="c" type="number" min="-5" max="5" step="any" value="0" required></label><label for="d">d (row 2, column 2)<input id="d" name="d" type="number" min="-5" max="5" step="any" value="1" required></label></div><button type="submit">Decompose</button><svg class="plane" viewBox="0 0 420 420" role="img" aria-label="Image of the unit circle under the matrix"></svg><output aria-live="polite"></output><p>The product of the singular values equals the absolute determinant, the area scale factor. A zero singular value means the matrix has rank one and loses a dimension. The explorer uses the closed form through AᵀA; the lab uses <code>np.linalg.svd</code>.</p></form>'''),
 dict(path='appendices/c-command-reference.html',title='Command reference',kicker='Appendix C',n='C',kw='commands cli lab reference options unittest',
 lede='Every lab command, its options, and the lesson it belongs to. All run from the course directory with numpy only.',
 body='''<h2 id="running">Running the labs</h2>
<pre class="term"><code>python3 labs/linalg_lab.py --help
python3 -m unittest discover -s labs -p 'test_*.py' -v</code></pre>
<p>The CLI uses <code>labs/reference.py</code>, so every command works before you implement anything. The tests exercise your <code>labs/linalg.py</code>: a test whose function still raises <code>NotImplementedError</code> is reported as skipped with the function’s name. The same tests also run against the reference (<code>labs/test_reference.py</code>), along with fixture integrity and CLI checks, so a fresh checkout shows 44 tests with 18 skipped. Every command’s actual output is in <code>research/verify/lab-transcript.txt</code>.</p>
<h2 id="commands">Commands</h2>
<table><tr><th>Command</th><th>Lesson</th><th>Options</th><th>What it prints</th></tr>
<tr><td><code>inspect</code></td><td>00</td><td><code>--token N</code></td><td>Shapes, label counts, one token’s coordinates, head weight shapes</td></tr>
<tr><td><code>vectors</code></td><td>01</td><td><code>--token N --other M</code></td><td>Sum, scaled copy, difference, centred vector</td></tr>
<tr><td><code>similar</code></td><td>02</td><td><code>--token N</code></td><td>Norms, most and least cosine-similar tokens, dot products</td></tr>
<tr><td><code>project</code></td><td>03</td><td><code>--label L --token N</code></td><td>Mean-difference direction, coefficient per token, Pythagoras check</td></tr>
<tr><td><code>shapes</code></td><td>04</td><td><code>--token N</code></td><td>x W_Q, linearity checks, a shape error</td></tr>
<tr><td><code>matmul</code></td><td>05</td><td><code>--token N</code></td><td>Batching, composition, einsum equivalence, raw scores</td></tr>
<tr><td><code>basis</code></td><td>06</td><td><code>--token N</code></td><td>Same vector in neuron and PCA bases</td></tr>
<tr><td><code>rank</code></td><td>07</td><td></td><td>Ranks of X, W_QK, W_OV; random near-orthogonal vectors</td></tr>
<tr><td><code>remove</code></td><td>08</td><td><code>--label L</code></td><td>Removing a direction, refitted probe, Gram–Schmidt</td></tr>
<tr><td><code>probe</code></td><td>09</td><td><code>--label L --ridge λ --seed S</code></td><td>Least-squares direction, train and held-out correlation</td></tr>
<tr><td><code>covariance</code></td><td>10</td><td></td><td>Covariance eigenvalues and checks</td></tr>
<tr><td><code>pca</code></td><td>11</td><td><code>--k K --keep-first</code></td><td>Variance explained, extreme tokens, label correlations</td></tr>
<tr><td><code>svd</code></td><td>12</td><td></td><td>SVD of W_QK and of X_c, low-rank errors</td></tr>
<tr><td><code>gradient</code></td><td>13</td><td><code>--token N</code></td><td>Analytic vs numeric gradients, one ascent step</td></tr>
<tr><td><code>correlation</code></td><td>14</td><td><code>--label L --ridge λ --seed S --perms P</code></td><td>Held-out correlation, permutation and random-direction nulls</td></tr>
<tr><td><code>review</code></td><td>15</td><td><code>--label L --ridge λ --seed S</code></td><td>The readiness pipeline</td></tr></table>
<p>Labels: <code>is_digit</code>, <code>after_period</code>, <code>starts_with_space</code>, <code>capitalised</code>, <code>position</code>. Token indices refer to the full 302-token fixture; commands that exclude position 0 say so.</p>
<h2 id="fixture">Regenerating the fixture</h2>
<p>Not needed to read or run the course. <code>labs/make_data.py</code> requires torch and transformers and downloads GPT-2 small on first use; <code>labs/data/README.md</code> documents what it writes.</p>'''),
 dict(path='appendices/d-reading-map.html',title='Reading map',kicker='Appendix D',n='D',kw='reading map 3blue1brown arena essence linear algebra chapters exercises',
 lede='For each lesson, the 3Blue1Brown chapter that gives the geometric argument and the ARENA exercise that makes you implement it on a live model.',
 body='''<p>The chapter titles and numbers below were read from each lesson page on 3blue1brown.com, and the ARENA section titles from learn.arena.education, on 2026-10-20. '''+cite('3b1b')+''' '''+cite('arena')+''' ARENA renumbers sections between iterations; search by title if a number has moved. The series has no chapter on the SVD, PCA, least squares or gradients, so those rows point to the ARENA material and to this course’s own lessons.</p>
<table><tr><th>Lesson</th><th>3Blue1Brown, Essence of linear algebra</th><th>ARENA</th></tr>
<tr><td>00 An activation is a vector</td><td>Ch. 1 Vectors, what even are they?</td><td>1.2 Intro to Mech Interp (caching activations with TransformerLens)</td></tr>
<tr><td>01 Vectors, addition, scaling</td><td>Ch. 1; Ch. 2 Linear combinations, span, and basis vectors</td><td>0.0 Prerequisites (tensor manipulation)</td></tr>
<tr><td>02 Dot product, norm, cosine</td><td>Ch. 9 Dot products and duality</td><td>0.1 Ray Tracing (batched dot products)</td></tr>
<tr><td>03 Projection onto a direction</td><td>Ch. 9</td><td>1.3.2 Function Vectors &amp; Model Steering; 1.3.3 Interpretability with SAEs (feature activations as projections)</td></tr>
<tr><td>04 Matrices as linear maps</td><td>Ch. 3 Linear transformations and matrices; Ch. 8 Nonsquare matrices as transformations between dimensions</td><td>1.1 Transformers from Scratch (weight shapes)</td></tr>
<tr><td>05 Matrix multiplication</td><td>Ch. 4 Matrix multiplication as composition</td><td>0.0 Prerequisites (einops/einsum); 1.1 Transformers from Scratch (attention scores)</td></tr>
<tr><td>06 Basis and change of basis</td><td>Ch. 13 Change of basis</td><td>1.2 Intro to Mech Interp (residual stream has no privileged basis)</td></tr>
<tr><td>07 Span, independence, rank</td><td>Ch. 2; Ch. 7 Inverse matrices, column space, and null space</td><td>1.5.4 Superposition &amp; SAEs</td></tr>
<tr><td>08 Orthogonality and removing a direction</td><td>Ch. 9</td><td>1.3.2 Function Vectors &amp; Model Steering (activation interventions)</td></tr>
<tr><td>09 Least squares and probes</td><td>none; see Appendix A</td><td>1.3.1 Linear Probes</td></tr>
<tr><td>10 Eigenvectors and covariance</td><td>Ch. 14 Eigenvectors and eigenvalues; Ch. 15 A quick trick for computing eigenvalues</td><td>1.5.2 Grokking &amp; Modular Arithmetic (Fourier basis as a change of basis)</td></tr>
<tr><td>11 PCA on activations</td><td>none; builds on Ch. 14</td><td>1.5.3 OthelloGPT (probing a learned representation)</td></tr>
<tr><td>12 SVD and low rank</td><td>none; Ch. 6 The determinant for the area-scaling picture</td><td>1.4.1 Indirect Object Identification (QK and OV circuits of GPT-2 small heads)</td></tr>
<tr><td>13 Gradients as directions</td><td>none (see the Essence of calculus series)</td><td>0.4 Backpropagation</td></tr>
<tr><td>14 Is the correlation real</td><td>none</td><td>1.3.1 Linear Probes (held-out evaluation); the statistics course’s lesson on correlation and screening</td></tr>
<tr><td>15 Readiness review</td><td>Ch. 16 Abstract vector spaces, for the view that the rules, not the coordinates, are the subject</td><td>Chapter 1 as a whole</td></tr></table>
<h2 id="papers">The two papers cited</h2>
<p><em>A Mathematical Framework for Transformer Circuits</em> is cited for three statements: the residual stream is a sum of layer outputs, it has no privileged basis, and the QK and OV products are low-rank. '''+cite('framework')+''' <em>Toy Models of Superposition</em> is cited for the definition of superposition and for the geometric fact about almost-orthogonal vectors. '''+cite('toy')+''' Read them after lesson 12; both assume exactly the material in this course and nothing more.</p>
<h2 id="routes">Shorter routes</h2>
<p><em>Reviewing someone’s direction:</em> lessons 03, 09, 14, 15. <em>Reading a circuits paper:</em> 04, 05, 07, 12. <em>Before PCA on your own activations:</em> 02, 10, 11. <em>Before steering experiments:</em> 01, 03, 08, 13.</p>'''),
]
