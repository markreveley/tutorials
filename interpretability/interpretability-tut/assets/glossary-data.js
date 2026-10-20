window.GLOSSARY = {
  "explanation": {
    "name": "Explanation",
    "short": "A claim that a model component (neuron, direction, head, feature) responds to, or computes, something nameable.",
    "def": "A claim that a model component (neuron, direction, head, feature) responds to, or computes, something nameable. Until tested it is a hypothesis."
  },
  "demonstrated-explanation": {
    "name": "Demonstrated explanation",
    "short": "An explanation that predicted the component’s behaviour on data chosen before the look, beat its controls, and met a threshold fixed in advance.",
    "def": "An explanation that predicted the component’s behaviour on data chosen before the look, beat its controls, and met a threshold fixed in advance."
  },
  "pre-registration": {
    "name": "Pre-registration",
    "short": "Writing the prediction, the data it will be scored on, the scoring function, the controls, and the pass threshold before running the test.",
    "def": "Writing the prediction, the data it will be scored on, the scoring function, the controls, and the pass threshold before running the test."
  },
  "prediction-test": {
    "name": "Prediction test",
    "short": "A procedure that turns an explanation into a number on held-out data: for example the correlation between activations predicted from the explanation and the activations actually observed.",
    "def": "A procedure that turns an explanation into a number on held-out data: for example the correlation between activations predicted from the explanation and the activations actually observed."
  },
  "held-out": {
    "name": "Held-out data",
    "short": "Inputs that played no part in forming or choosing the explanation.",
    "def": "Inputs that played no part in forming or choosing the explanation. Scores on them are the only ones that cannot be inflated by selection."
  },
  "screening-split": {
    "name": "Screening split",
    "short": "The portion of data used to search for candidates and form hypotheses.",
    "def": "The portion of data used to search for candidates and form hypotheses. Any score computed on it is biased upward by the search."
  },
  "control": {
    "name": "Control",
    "short": "A comparison that would also pass if the claim were empty: a random neuron, shuffled labels, a baseline explanation, a rotated stimulus.",
    "def": "A comparison that would also pass if the claim were empty: a random neuron, shuffled labels, a baseline explanation, a rotated stimulus. The claim must beat its controls."
  },
  "random-neuron-control": {
    "name": "Random-neuron control",
    "short": "Scoring the same explanation against randomly chosen other units.",
    "def": "Scoring the same explanation against randomly chosen other units. It measures how much of the score comes from the explanation fitting the data rather than the unit."
  },
  "shuffled-label-control": {
    "name": "Shuffled-label control",
    "short": "Scoring the unit against a permutation of the explanation’s predictions.",
    "def": "Scoring the unit against a permutation of the explanation’s predictions. It gives the distribution of scores a meaningless explanation would get."
  },
  "selection-bias": {
    "name": "Selection bias",
    "short": "The upward distortion of a score when the thing scored was chosen because it scored well.",
    "def": "The upward distortion of a score when the thing scored was chosen because it scored well. Searching many units and reporting the best one is the common case."
  },
  "neuron": {
    "name": "Neuron",
    "short": "One coordinate of an activation vector; in a transformer MLP, one hidden unit after its nonlinearity; in a convolutional network, one channel of a feature map.",
    "def": "One coordinate of an activation vector; in a transformer MLP, one hidden unit after its nonlinearity; in a convolutional network, one channel of a feature map."
  },
  "native-neuron": {
    "name": "Native neuron",
    "short": "A neuron of the network as trained, studied directly, as opposed to a learned feature produced by a second model such as a sparse autoencoder.",
    "def": "A neuron of the network as trained, studied directly, as opposed to a learned feature produced by a second model such as a sparse autoencoder."
  },
  "direction": {
    "name": "Direction",
    "short": "A unit vector in activation space.",
    "def": "A unit vector in activation space. Projecting activations onto it gives a scalar; a probe or a feature is a direction with a claim attached."
  },
  "residual-stream": {
    "name": "Residual stream",
    "short": "The vector each transformer block reads from and adds to; the sum of the embeddings and every block’s attention and MLP outputs so far.",
    "def": "The vector each transformer block reads from and adds to; the sum of the embeddings and every block’s attention and MLP outputs so far."
  },
  "attention-head": {
    "name": "Attention head",
    "short": "One of several parallel units in an attention layer, each computing a pattern of weights over earlier positions and moving information along it.",
    "def": "One of several parallel units in an attention layer, each computing a pattern of weights over earlier positions and moving information along it."
  },
  "attention-pattern": {
    "name": "Attention pattern",
    "short": "The matrix of weights a head assigns from each query position to each key position; rows sum to one.",
    "def": "The matrix of weights a head assigns from each query position to each key position; rows sum to one."
  },
  "mlp": {
    "name": "MLP",
    "short": "The feed-forward block of a transformer layer: a linear map up to a wider hidden layer, a nonlinearity, and a linear map back.",
    "def": "The feed-forward block of a transformer layer: a linear map up to a wider hidden layer, a nonlinearity, and a linear map back."
  },
  "activation": {
    "name": "Activation",
    "short": "The value of a unit on a given input.",
    "def": "The value of a unit on a given input. For a neuron, a scalar per token or per image position."
  },
  "polysemantic": {
    "name": "Polysemantic neuron",
    "short": "A neuron that responds to several apparently unrelated inputs.",
    "def": "A neuron that responds to several apparently unrelated inputs. Whether a given case is truly unrelated, or one concept nobody has named, is an empirical question."
  },
  "monosemantic": {
    "name": "Monosemantic",
    "short": "Responding to one nameable thing.",
    "def": "Responding to one nameable thing. A claim of monosemanticity needs the same prediction test as any other explanation."
  },
  "superposition": {
    "name": "Superposition",
    "short": "The hypothesis that a network represents more features than it has neurons by spreading features across neurons, so single neurons mix features.",
    "def": "The hypothesis that a network represents more features than it has neurons by spreading features across neurons, so single neurons mix features."
  },
  "feature": {
    "name": "Feature",
    "short": "A direction or unit claimed to correspond to one meaningful property of the input.",
    "def": "A direction or unit claimed to correspond to one meaningful property of the input. Used both for native neurons and for learned dictionary elements."
  },
  "sparse-autoencoder": {
    "name": "Sparse autoencoder",
    "short": "A second model trained to reconstruct activations from a sparse, overcomplete set of learned directions.",
    "def": "A second model trained to reconstruct activations from a sparse, overcomplete set of learned directions. Its latents are offered as more interpretable features than neurons."
  },
  "sae-feature": {
    "name": "SAE feature",
    "short": "One latent of a sparse autoencoder: a direction and a sparse activation.",
    "def": "One latent of a sparse autoencoder: a direction and a sparse activation. Its explanation is scored the same way a neuron’s is."
  },
  "max-activating-examples": {
    "name": "Max-activating examples",
    "short": "The inputs on which a unit fires most strongly.",
    "def": "The inputs on which a unit fires most strongly. They are the first thing to look at and the easiest thing to be misled by."
  },
  "quantile-sampling": {
    "name": "Quantile sampling",
    "short": "Drawing random examples from fixed bands of the unit’s activation distribution, so that weak and typical activations are seen as well as the strongest.",
    "def": "Drawing random examples from fixed bands of the unit’s activation distribution, so that weak and typical activations are seen as well as the strongest."
  },
  "simulation-scoring": {
    "name": "Simulation scoring",
    "short": "Having a simulator (a model or a rule) predict a unit’s activation on each token from the explanation alone, then scoring the predictions against the true activations.",
    "def": "Having a simulator (a model or a rule) predict a unit’s activation on each token from the explanation alone, then scoring the predictions against the true activations."
  },
  "explanation-score": {
    "name": "Explanation score",
    "short": "The correlation between simulated and true activations, as used by Bills et al.",
    "def": "The correlation between simulated and true activations, as used by Bills et al. (2023). Its value depends heavily on which text excerpts it is computed on."
  },
  "correlation": {
    "name": "Correlation",
    "short": "The Pearson coefficient between two series: 1 means a perfect linear match, 0 no linear relation, −1 a perfect inverse match.",
    "def": "The Pearson coefficient between two series: 1 means a perfect linear match, 0 no linear relation, −1 a perfect inverse match."
  },
  "precision-recall": {
    "name": "Precision and recall",
    "short": "For an explanation read as a predicate: precision is the fraction of inputs matching the predicate on which the unit fires; recall is the fraction of inputs where the unit fires that match the predicate.",
    "def": "For an explanation read as a predicate: precision is the fraction of inputs matching the predicate on which the unit fires; recall is the fraction of inputs where the unit fires that match the predicate."
  },
  "downstream-kl": {
    "name": "Downstream KL",
    "short": "The divergence between the model’s output distribution with a unit’s true activations and with simulated ones substituted.",
    "def": "The divergence between the model’s output distribution with a unit’s true activations and with simulated ones substituted. It measures whether the simulation errors matter to the model."
  },
  "feature-visualization": {
    "name": "Feature visualization",
    "short": "Optimising an input image by gradient ascent to maximise a unit’s activation.",
    "def": "Optimising an input image by gradient ascent to maximise a unit’s activation. Shows what excites the unit; does not show how often that occurs in real data."
  },
  "synthetic-stimulus": {
    "name": "Synthetic stimulus",
    "short": "A rendered input with known parameters (orientation, radius, contrast) used to measure a unit’s response as a function of those parameters.",
    "def": "A rendered input with known parameters (orientation, radius, contrast) used to measure a unit’s response as a function of those parameters."
  },
  "tuning-curve": {
    "name": "Tuning curve",
    "short": "A unit’s response plotted against one stimulus parameter, such as orientation.",
    "def": "A unit’s response plotted against one stimulus parameter, such as orientation."
  },
  "orientation-selectivity": {
    "name": "Orientation selectivity",
    "short": "How concentrated a tuning curve is around one orientation; the course uses the vector strength of the response over the circle, 0 flat to 1 single-angle.",
    "def": "How concentrated a tuning curve is around one orientation; the course uses the vector strength of the response over the circle, 0 flat to 1 single-angle."
  },
  "linear-probe": {
    "name": "Linear probe",
    "short": "A classifier fitted on activations to predict a label.",
    "def": "A classifier fitted on activations to predict a label. High held-out accuracy shows the label is linearly readable from the activations; it does not show the model uses it."
  },
  "logit-lens": {
    "name": "Logit lens",
    "short": "Applying the model’s final layer norm and unembedding to the residual stream after an intermediate block, to read what the block’s state would predict if it were the last.",
    "def": "Applying the model’s final layer norm and unembedding to the residual stream after an intermediate block, to read what the block’s state would predict if it were the last."
  },
  "direct-logit-attribution": {
    "name": "Direct logit attribution",
    "short": "Decomposing a logit into the contributions of each component’s output projected onto the target token’s unembedding row, through the final layer norm.",
    "def": "Decomposing a logit into the contributions of each component’s output projected onto the target token’s unembedding row, through the final layer norm."
  },
  "activation-patching": {
    "name": "Activation patching",
    "short": "Running a corrupted input while replacing one activation with its value from a clean input, to measure how much of the clean behaviour that activation restores.",
    "def": "Running a corrupted input while replacing one activation with its value from a clean input, to measure how much of the clean behaviour that activation restores."
  },
  "ablation": {
    "name": "Ablation",
    "short": "Removing a component’s contribution (setting it to zero or to a mean) and measuring the change in the output.",
    "def": "Removing a component’s contribution (setting it to zero or to a mean) and measuring the change in the output."
  },
  "correlational-evidence": {
    "name": "Correlational evidence",
    "short": "Evidence that a unit’s activity co-varies with a property.",
    "def": "Evidence that a unit’s activity co-varies with a property. It supports “represents”; it does not support “is used for”."
  },
  "interventional-evidence": {
    "name": "Interventional evidence",
    "short": "Evidence from changing a unit and observing the output.",
    "def": "Evidence from changing a unit and observing the output. It supports causal claims about what the unit does for the model."
  },
  "clean-corrupted-pair": {
    "name": "Clean/corrupted pair",
    "short": "Two inputs that differ in one respect the claim is about, with different expected outputs, used for patching.",
    "def": "Two inputs that differ in one respect the claim is about, with different expected outputs, used for patching."
  },
  "induction-head": {
    "name": "Induction head",
    "short": "An attention head that, on a repeated sequence, attends from a token to the token that followed its earlier occurrence and raises that token’s logit: the rule [A][B]…[A] → [B].",
    "def": "An attention head that, on a repeated sequence, attends from a token to the token that followed its earlier occurrence and raises that token’s logit: the rule [A][B]…[A] → [B]."
  },
  "prefix-matching-score": {
    "name": "Prefix-matching score",
    "short": "On a repeated random sequence, the mean attention from each second-copy token to the token after its first-copy occurrence.",
    "def": "On a repeated random sequence, the mean attention from each second-copy token to the token after its first-copy occurrence."
  },
  "in-context-learning": {
    "name": "In-context learning",
    "short": "A model predicting later tokens better because of earlier tokens in the same context, measured by the drop in loss along the sequence.",
    "def": "A model predicting later tokens better because of earlier tokens in the same context, measured by the drop in loss along the sequence."
  },
  "threshold": {
    "name": "Threshold",
    "short": "The pass line fixed before the test.",
    "def": "The pass line fixed before the test. A threshold chosen after seeing the result is not a threshold."
  },
  "base-rate": {
    "name": "Base rate",
    "short": "How often the property the explanation names occurs in the data.",
    "def": "How often the property the explanation names occurs in the data. It bounds what accuracy and correlation can achieve and must be reported beside them."
  },
  "negative-result": {
    "name": "Negative result",
    "short": "A pre-registered test that failed.",
    "def": "A pre-registered test that failed. Reported with the same detail as a success, it is a contribution; hidden, it is the reason the field cannot trust the successes."
  },
  "multiple-comparisons": {
    "name": "Multiple comparisons",
    "short": "Testing many candidates and reporting the best.",
    "def": "Testing many candidates and reporting the best. The best of n meaningless scores is not meaningless-looking; held-out data and corrected thresholds are the remedies."
  },
  "receptive-field": {
    "name": "Receptive field",
    "short": "The region of the input that can influence one position of a convolutional feature map.",
    "def": "The region of the input that can influence one position of a convolutional feature map."
  },
  "transformerlens": {
    "name": "TransformerLens",
    "short": "A library that loads transformer models with named hook points so activations can be cached and edited; version 4 boots models through TransformerBridge.",
    "def": "A library that loads transformer models with named hook points so activations can be cached and edited; version 4 boots models through TransformerBridge."
  },
  "hook-point": {
    "name": "Hook point",
    "short": "A named location in the forward pass where an activation can be read or replaced, such as blocks.5.hook_resid_post.",
    "def": "A named location in the forward pass where an activation can be read or replaced, such as blocks.5.hook_resid_post."
  },
  "cache": {
    "name": "Activation cache",
    "short": "A dictionary from hook-point names to the activations recorded during one forward pass.",
    "def": "A dictionary from hook-point names to the activations recorded during one forward pass."
  },
  "attribution-graph": {
    "name": "Attribution graph",
    "short": "A diagram of which components contributed to an output, built by tracing contributions backward from the output through the network.",
    "def": "A diagram of which components contributed to an output, built by tracing contributions backward from the output through the network."
  },
  "replication": {
    "name": "Replication",
    "short": "Repeating a published test on new data, a new model copy, or new stimuli, with the test fixed in advance, and reporting what did and did not hold.",
    "def": "Repeating a published test on new data, a new model copy, or new stimuli, with the test fixed in advance, and reporting what did and did not hold."
  }
};
