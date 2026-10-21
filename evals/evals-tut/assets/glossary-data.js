// Glossary data (generated from research/gloss-part{1,2}.json — edit those and rerun assembly).
// Each entry: slug -> { name, short, def, also?, see? }
window.GLOSSARY = {
  "eval": {
    "name": "Eval",
    "short": "A repeatable test that measures how well an AI system performs a task, by running it on a set of inputs and scoring the outputs.",
    "def": "An eval (short for evaluation) is a repeatable measurement of how well an AI system does something: you run the system on a fixed set of inputs, score each output, and aggregate the scores into a number you can track over time. Evals exist because LLM outputs vary — you can't tell whether a prompt change helped by eyeballing a few responses, so you need a measurement you can rerun and compare. The term covers everything from public <a href='pages/01-what-is-an-eval.html'>benchmarks</a> that compare models to small in-house test suites that check one product feature.",
    "also": "evaluation",
    "see": [
      "benchmark",
      "metric",
      "dataset",
      "grader",
      "capability-eval",
      "product-eval"
    ]
  },
  "benchmark": {
    "name": "Benchmark",
    "short": "A standardized, published eval — a fixed dataset plus scoring rules — that lets different models or systems be compared on the same task.",
    "def": "A benchmark is an eval that has been standardized and published so that anyone can run it and compare results: a fixed <a href='pages/02-anatomy-of-an-eval.html'>dataset</a>, fixed scoring rules, and usually a public <a href='pages/23-leaderboard-illusion.html'>leaderboard</a>. Standardization is the whole point — if two labs score their models on different questions with different rules, the numbers can't be compared. The fixity that makes benchmarks comparable is also their weakness: once a test is public and fixed, models can be trained on it (<a href='pages/21-contamination.html'>contamination</a>) or tuned to it, so a benchmark score can drift away from measuring the ability it was built for.",
    "see": [
      "eval",
      "leaderboard",
      "capability-eval",
      "dataset"
    ]
  },
  "metric": {
    "name": "Metric",
    "short": "The number an eval produces — a rule for turning many individual scored outputs into a single summary figure, like percent passed.",
    "def": "A metric is the rule that turns many individual scores into one summary number — most commonly the fraction of samples that passed, but also averages, agreement rates, or cost-adjusted figures. The metric exists because a pile of per-sample judgments isn't actionable; you need a single figure to compare run A against run B. Choosing the metric is a real design decision: it decides what counts as better, and a system optimized against a metric will exploit whatever the metric fails to measure. See <a href='pages/02-anatomy-of-an-eval.html'>Anatomy of an Eval</a>.",
    "see": [
      "eval",
      "grader",
      "pass-at-k",
      "binary-judgment"
    ]
  },
  "dataset": {
    "name": "Dataset",
    "short": "The collection of test cases an eval runs on — each one an input (and often an expected answer) that the system under test must handle.",
    "def": "In evals, the dataset is the collection of test cases the system is run against. Each case (a <a href='pages/02-anatomy-of-an-eval.html'>sample</a>) holds at minimum an input, and often a reference answer or grading instructions. The dataset defines what your eval actually measures: if it doesn't contain the hard cases your users hit, your score can be high while your product fails. That's why building the dataset — from real logged failures, expert-written cases, or <a href='pages/05-from-failures-to-evals.html'>synthetic data</a> — is usually the most important and most neglected part of an eval.",
    "also": "test set, eval set",
    "see": [
      "sample",
      "golden-dataset",
      "ground-truth",
      "synthetic-data",
      "train-test-split"
    ]
  },
  "sample": {
    "name": "Sample",
    "short": "One test case in an eval dataset: a single input, plus whatever the grader needs to score the system's output on it (often a reference answer).",
    "def": "A sample is one row of an eval <a href='pages/02-anatomy-of-an-eval.html'>dataset</a>: a single input the system must handle, bundled with whatever the <a href='pages/03-types-of-evaluators.html'>grader</a> needs to score the result — a reference answer, a checklist, or grading instructions. The eval score is just an aggregate over samples, which is why both the number and the quality of samples matter: too few and the score is mostly noise; unrepresentative ones and the score measures the wrong thing. (Statisticians use 'sample' to mean a whole subset drawn from a population; in eval tooling it almost always means one test case.)",
    "also": "test case, example, item",
    "see": [
      "dataset",
      "ground-truth",
      "golden-dataset"
    ]
  },
  "trace": {
    "name": "Trace",
    "short": "The complete logged record of one LLM or agent interaction — the inputs, the model's outputs, and any intermediate steps like tool calls.",
    "def": "A trace is the complete logged record of one interaction with an LLM system: the user's input, the prompts actually sent to the model, every intermediate step (tool calls, retrieved documents, agent turns), and the final output. Traces exist because the final answer alone doesn't tell you <em>why</em> something failed — the bug might be in retrieval, in a tool call, or in the prompt the user never sees. Reading traces is the core activity of <a href='pages/04-error-analysis.html'>error analysis</a>, and capturing them in production is the job of <a href='pages/26-observability.html'>tracing and observability</a> tools.",
    "see": [
      "error-analysis",
      "open-coding",
      "annotation",
      "online-eval"
    ]
  },
  "harness": {
    "name": "Harness",
    "short": "The software that runs an eval end to end: it feeds each test case to the system, collects outputs, applies the grader, and reports the metric.",
    "def": "A harness is the software that runs an eval end to end: it loads the <a href='pages/02-anatomy-of-an-eval.html'>dataset</a>, sends each sample to the system under test, collects the outputs, applies the <a href='pages/03-types-of-evaluators.html'>grader</a>, and aggregates the results into a report. The harness exists so an eval is reproducible — running hundreds of cases by hand isn't, and small differences in how prompts are formatted or answers are parsed can change scores, so the harness pins those details down. Examples range from a short Python script to full frameworks like <a href='pages/24-inspect.html'>Inspect</a>.",
    "also": "evaluation framework",
    "see": [
      "grader",
      "metric",
      "model-graded-scorer",
      "dataset"
    ]
  },
  "grader": {
    "name": "Grader",
    "short": "The component of an eval that scores a single output — it can be code (string match, test suite), a human reviewer, or another LLM acting as judge.",
    "def": "The grader is the part of an eval that looks at one output and decides how good it is. It can be code (an exact-match check, a regex, a unit-test suite), a human reviewer, or another LLM (an <a href='pages/08-llm-as-judge.html'>LLM judge</a>). The grader exists because raw model outputs are just text — something has to turn 'here's what the model said' into 'pass' or 'fail' before you can compute a <a href='pages/02-anatomy-of-an-eval.html'>metric</a>. Your eval is only as trustworthy as its grader, which is why <a href='pages/06-validating-the-grader.html'>validating the grader</a> is a step in its own right.",
    "also": "scorer, evaluator",
    "see": [
      "llm-as-judge",
      "model-graded-scorer",
      "ground-truth",
      "judge-alignment"
    ]
  },
  "ground-truth": {
    "name": "Ground Truth",
    "short": "The known-correct answer for a test case, used as the standard the system's output is compared against during grading.",
    "def": "Ground truth is the known-correct answer for a test case — the standard a <a href='pages/03-types-of-evaluators.html'>grader</a> compares the system's output against. The term exists because grading needs an anchor: 'is this output right?' is only answerable if something defines 'right.' For some tasks ground truth is objective (the answer to a math problem); for others it's really just a trusted human's judgment, which is why building ground-truth labels often means structured <a href='pages/04-error-analysis.html'>annotation</a> by a domain expert rather than looking answers up.",
    "also": "gold label, reference answer",
    "see": [
      "reference-based",
      "golden-dataset",
      "annotation",
      "principal-domain-expert"
    ]
  },
  "reference-based": {
    "name": "Reference-Based Evaluation",
    "short": "Grading that compares the system's output against a known-correct reference answer — possible only when each test case has one.",
    "def": "Reference-based evaluation grades an output by comparing it to a known-correct reference answer (<a href='pages/03-types-of-evaluators.html'>ground truth</a>) attached to the test case. The comparison can be strict (exact match, passing a test suite) or loose (an LLM judge checking that the output says the same thing as the reference). It's the most trustworthy kind of grading when references exist — but many real tasks ('write a friendly support reply') have no single correct answer, which is what forces the alternative, <a href='pages/03-types-of-evaluators.html'>reference-free</a> evaluation.",
    "see": [
      "reference-free",
      "ground-truth",
      "reference-guided-grading",
      "grader"
    ]
  },
  "reference-free": {
    "name": "Reference-Free Evaluation",
    "short": "Grading an output on its own merits — against criteria, a rubric, or judge instructions — without comparing it to a stored correct answer.",
    "def": "Reference-free evaluation grades an output without a stored correct answer, judging it directly against criteria: does it follow the instructions, is it grounded in the provided documents, does it meet the <a href='pages/08-llm-as-judge.html'>rubric</a>? It exists because most product tasks are open-ended — there are many acceptable support replies, summaries, or plans, so no single reference can be written down. The cost is that quality now lives entirely in the grading criteria and the <a href='pages/06-validating-the-grader.html'>grader's judgment</a>, both of which must themselves be validated against human experts.",
    "see": [
      "reference-based",
      "llm-as-judge",
      "rubric",
      "judge-alignment"
    ]
  },
  "offline-eval": {
    "name": "Offline Eval",
    "short": "An eval run on a fixed test set before deployment — in development or CI — as opposed to measuring the live system on real user traffic.",
    "def": "An offline eval runs the system on a fixed <a href='pages/02-anatomy-of-an-eval.html'>dataset</a> outside of production — during development, in CI, before a release. Because the inputs are fixed and the run is repeatable, offline evals are ideal for comparing two versions of a system and for <a href='pages/07-evals-in-the-lifecycle.html'>regression testing</a>. Their blind spot is the real world: a fixed test set can't contain the inputs users will invent next week, which is why mature teams pair offline evals with <a href='pages/26-observability.html'>online evaluation</a> of live traffic.",
    "see": [
      "online-eval",
      "regression-testing",
      "golden-dataset",
      "a-b-test"
    ]
  },
  "online-eval": {
    "name": "Online Eval",
    "short": "Evaluation of a live system on real user traffic — scoring production outputs, tracking user signals, or running A/B tests.",
    "def": "An online eval measures the system in production, on real user traffic: scoring a slice of live outputs with an <a href='pages/08-llm-as-judge.html'>LLM judge</a>, tracking user signals like thumbs-down or retries, or running an <a href='pages/07-evals-in-the-lifecycle.html'>A/B test</a>. It exists because <a href='pages/26-observability.html'>offline test sets</a> always lag reality — users find inputs you never wrote test cases for. The trade-off is control: traffic isn't repeatable and there's usually no ground truth, so online results are noisier and need <a href='pages/26-observability.html'>tracing infrastructure</a> to be usable.",
    "also": "production evaluation, online monitoring",
    "see": [
      "offline-eval",
      "a-b-test",
      "trace",
      "guardrail"
    ]
  },
  "capability-eval": {
    "name": "Capability Eval",
    "short": "An eval that measures what a model can do in general (math, coding, reasoning), used to compare models — as opposed to testing one product.",
    "def": "A capability eval measures a model's general abilities — math, coding, reasoning, instruction-following — independent of any particular application. Public <a href='pages/01-what-is-an-eval.html'>benchmarks</a> are capability evals: they exist to answer 'which model is stronger?' for model builders and model choosers. The crucial caveat for practitioners is that capability scores don't transfer to your product: a model that tops coding leaderboards can still fail at your specific support-bot task, which is what <a href='pages/01-what-is-an-eval.html'>product evals</a> are for.",
    "see": [
      "product-eval",
      "benchmark",
      "leaderboard",
      "human-baseline"
    ]
  },
  "product-eval": {
    "name": "Product Eval",
    "short": "An eval built around one specific application and its real failure modes, measuring whether that product works for its users — not the model in general.",
    "def": "A product eval measures whether <em>your application</em> works: your prompts, your retrieval, your users' actual inputs, scored against what quality means for your domain. It exists because <a href='pages/01-what-is-an-eval.html'>capability evals</a> answer the wrong question for builders — knowing a model is good at competition math says nothing about whether your contract-summarizer hallucinates clause numbers. Product evals are built bottom-up: <a href='pages/04-error-analysis.html'>error analysis</a> on real traces reveals the failure modes, and those become the test cases and grading criteria.",
    "also": "application-specific eval, task-specific eval",
    "see": [
      "capability-eval",
      "error-analysis",
      "failure-mode",
      "principal-domain-expert"
    ]
  },
  "golden-dataset": {
    "name": "Golden Dataset",
    "short": "A small, carefully curated set of test cases with trusted labels — the high-quality core test set a team maintains and runs against every change.",
    "def": "A golden dataset is a curated set of test cases whose labels you genuinely trust — typically reviewed by a domain expert rather than labeled in bulk. It exists because eval results are only as good as the labels behind them: a large sloppy test set tells you less than a small one where every pass/fail is correct. Teams treat the golden set as a maintained asset, running it on every change as a <a href='pages/07-evals-in-the-lifecycle.html'>regression test</a> and adding new cases as fresh failure modes surface in production.",
    "also": "golden set, gold set",
    "see": [
      "dataset",
      "ground-truth",
      "regression-testing",
      "annotation"
    ]
  },
  "train-test-split": {
    "name": "Train/Test Split",
    "short": "Keeping the data you optimize on separate from the data you measure on, so your score reflects performance on unseen inputs rather than memorization.",
    "def": "A train/test split keeps the data you optimize against separate from the data you measure with. The reason is simple once seen: if you tune your prompts (or train a model) on the same cases you score on, the score measures how well you fit those specific cases, not how the system handles new inputs — the eval equivalent of grading students on the exact questions they practiced. In eval work this shows up as keeping a <a href='pages/05-from-failures-to-evals.html'>holdout set</a> you never iterate against, and at benchmark scale as the fight against <a href='pages/21-contamination.html'>contamination</a>.",
    "also": "holdout split",
    "see": [
      "dataset",
      "golden-dataset",
      "regression-testing"
    ]
  },
  "regression-testing": {
    "name": "Regression Testing",
    "short": "Re-running your eval suite after every change to catch things that used to work but broke — the LLM equivalent of a software test suite in CI.",
    "def": "Regression testing means re-running your eval suite after every change — a new prompt, a model upgrade, a retrieval tweak — to catch cases that used to pass and now fail. It matters more for LLM systems than for ordinary software because changes are non-local: editing a prompt to fix one behavior can silently break an unrelated one, and there's no compiler to warn you. The practice is to wire evals into CI so every change gets scored against the <a href='pages/07-evals-in-the-lifecycle.html'>golden dataset</a> before it ships.",
    "also": "regression eval",
    "see": [
      "golden-dataset",
      "offline-eval",
      "eval-driven-development",
      "harness"
    ]
  },
  "guardrail": {
    "name": "Guardrail",
    "short": "A check that runs in production at request time and blocks or fixes bad outputs before users see them — enforcement, as opposed to measurement.",
    "def": "A guardrail is a check that runs in production, at request time, and acts on the result: blocking an unsafe response, stripping leaked personal data, or forcing a retry when an output fails validation. The contrast with an eval is timing and purpose — an eval measures quality across many cases to inform development, while a guardrail enforces a rule on a single live request before the user sees it. Because guardrails sit in the response path, they must be fast and cheap, so they tend to be simple checks rather than full <a href='pages/07-evals-in-the-lifecycle.html'>judge-style grading</a>.",
    "see": [
      "online-eval",
      "grader",
      "eval-driven-development"
    ]
  },
  "a-b-test": {
    "name": "A/B Test",
    "short": "An experiment that splits live users between two versions of a system and compares real outcomes, to measure which version actually works better.",
    "def": "An A/B test randomly splits live traffic between two versions of a system — say, the old prompt and the new one — and compares real outcomes: task completion, retries, thumbs-down rates. Randomization is what makes it trustworthy: because users are assigned to versions by chance, any systematic difference in outcomes is attributable to the change itself rather than to who happened to use it. In the eval lifecycle it's the final check that offline gains are real — see <a href='pages/07-evals-in-the-lifecycle.html'>Evals in the Development Lifecycle</a>.",
    "also": "split test, online experiment",
    "see": [
      "online-eval",
      "offline-eval"
    ]
  },
  "leaderboard": {
    "name": "Leaderboard",
    "short": "A public ranking of models by their scores on a benchmark or rating system, used to compare models — and gamed for the same reason.",
    "def": "A leaderboard is a public ranking of models by their scores on some <a href='pages/01-what-is-an-eval.html'>benchmark</a> or rating system. It exists because buyers and researchers want a quick answer to 'which model is best?' — and that demand is exactly what distorts it: when rank confers prestige and revenue, labs optimize for the leaderboard's specific test, and the ranking drifts away from general quality. How that plays out in practice is the subject of <a href='pages/23-leaderboard-illusion.html'>The Political Economy of Leaderboards</a>.",
    "see": [
      "benchmark",
      "arena-rating",
      "capability-eval"
    ]
  },
  "arena-rating": {
    "name": "Arena Rating",
    "short": "A model ranking built from crowdsourced head-to-head battles: users compare two anonymous model responses, and votes feed an Elo-style rating.",
    "def": "An arena rating ranks models through crowdsourced head-to-head battles, in the style of Chatbot Arena: a user sends a prompt, two anonymous models answer side by side, the user votes for the better one, and the votes feed an Elo-style rating system (borrowed from chess) that converts win/loss records into scores. The approach exists to escape fixed test sets — real users ask real questions, and anonymity is meant to stop brand bias. Its weaknesses are that casual voters reward surface qualities like confidence and formatting, and the ranking process itself can be <a href='pages/23-leaderboard-illusion.html'>gamed by participants</a>.",
    "also": "Elo rating, Chatbot Arena ranking",
    "see": [
      "leaderboard",
      "pairwise-comparison",
      "verbosity-bias"
    ]
  },
  "human-baseline": {
    "name": "Human Baseline",
    "short": "The score humans achieve on the same eval, measured so model scores have a meaningful reference point — 80% means little until you know what people get.",
    "def": "A human baseline is the score people achieve on the same eval, measured under comparable conditions. It exists because raw model scores have no scale: 70% is meaningless until you know whether experts score 95% or struggle to reach 50%. Baselines need care to be fair — whose performance (crowd workers or domain experts), with how much time and what tools — and a sloppy baseline makes 'superhuman' claims easy and hollow. They also define ceilings: when a model exceeds the human baseline, the benchmark stops being able to measure further progress.",
    "see": [
      "benchmark",
      "capability-eval",
      "metric"
    ]
  },
  "llm": {
    "name": "LLM (Large Language Model)",
    "short": "An AI model trained on huge amounts of text to predict the next token, which makes it able to generate and follow instructions in natural language.",
    "def": "A large language model is an AI model trained on vast amounts of text to predict the next <a href='pages/01-what-is-an-eval.html'>token</a> given everything before it. That one objective, at scale, yields a system that can answer questions, write code, and follow instructions — without being explicitly programmed for any of those tasks. The same origin explains why evals are hard: an LLM's outputs are probabilistic and open-ended rather than deterministic and enumerable, so 'does it work?' becomes a measurement problem instead of a checklist.",
    "also": "large language model, language model",
    "see": [
      "token",
      "temperature",
      "prompt",
      "hallucination",
      "context-window"
    ]
  },
  "token": {
    "name": "Token",
    "short": "The unit of text an LLM reads and writes — a word fragment, word, or symbol. Models process, price, and limit text in tokens, not characters.",
    "def": "A token is the unit an LLM actually reads and writes: a chunk of text — often a word, sometimes a fragment like <code>ing</code> or a punctuation mark — produced by splitting text with a fixed vocabulary. Models work in tokens because a fixed vocabulary of chunks handles any input, including words never seen in training. Tokens matter for evals because everything is denominated in them: API pricing, <a href='pages/01-what-is-an-eval.html'>context window</a> limits, and output truncation — and some judge techniques like <a href='pages/08-llm-as-judge.html'>G-Eval</a> work with the probabilities the model assigns to individual tokens.",
    "see": [
      "llm",
      "context-window",
      "temperature",
      "g-eval"
    ]
  },
  "temperature": {
    "name": "Temperature",
    "short": "A setting controlling how random an LLM's output is: 0 makes it pick the most likely next token nearly every time; higher values add variety.",
    "def": "Temperature is a sampling setting that controls how random an LLM's output is. The model produces a probability for every possible next <a href='pages/01-what-is-an-eval.html'>token</a>; at temperature 0 it (nearly) always picks the most likely one, while higher values let less likely tokens through, producing more varied — and less repeatable — text. Evals care because temperature trades repeatability for realism: low temperature makes runs comparable, but if your product runs at a higher temperature, evaluating only at 0 misses the variability your users actually see, which is one reason for repeated trials and metrics like <a href='pages/18-pass-at-k.html'>pass@k</a>.",
    "see": [
      "llm",
      "token",
      "pass-at-k"
    ]
  },
  "context-window": {
    "name": "Context Window",
    "short": "The maximum amount of text (in tokens) an LLM can consider at once — everything it must work with has to fit, or get cut.",
    "def": "The context window is the maximum amount of text, measured in <a href='pages/01-what-is-an-eval.html'>tokens</a>, that an LLM can consider in one request: the system prompt, the conversation so far, any retrieved documents, and the response being generated all share it. It exists because the model's architecture processes a bounded sequence — beyond the limit, text must be dropped or summarized. For evals this is a real failure source: long inputs can silently push instructions or evidence out of the window, and a model's effective use of a long context is itself something worth testing.",
    "see": [
      "token",
      "rag",
      "prompt",
      "llm"
    ]
  },
  "prompt": {
    "name": "Prompt",
    "short": "The text given to an LLM to produce a response — instructions, context, and the user's request. The main thing builders change and evals measure.",
    "def": "A prompt is the text sent to an LLM to elicit a response: instructions, examples, supporting context, and the user's actual request. It's the primary lever LLM application builders have — most 'development' on an LLM product is prompt revision — which makes it the main thing <a href='pages/01-what-is-an-eval.html'>evals</a> measure the effect of. Prompts also matter on the grading side: an <a href='pages/08-llm-as-judge.html'>LLM judge</a> is itself just a model plus a carefully designed prompt, with all the same sensitivities.",
    "see": [
      "system-prompt",
      "few-shot",
      "llm",
      "eval-driven-development"
    ]
  },
  "system-prompt": {
    "name": "System Prompt",
    "short": "The standing instructions a developer gives an LLM before any user input — defining its role, rules, and style for every conversation.",
    "def": "A system prompt is the standing instruction block a developer places before any user input: who the model should be, what rules it must follow, what format to answer in. The separate slot exists to mark authority — APIs distinguish developer instructions from user messages so the model can weight them differently and (imperfectly) resist user attempts to override them. In an LLM product the system prompt is core logic, so changes to it are exactly what <a href='pages/07-evals-in-the-lifecycle.html'>regression testing</a> with evals is meant to keep safe.",
    "see": [
      "prompt",
      "regression-testing",
      "llm"
    ]
  },
  "fine-tuning": {
    "name": "Fine-Tuning",
    "short": "Further training an existing LLM on examples of a specific task so the desired behavior is baked into its weights, rather than instructed via prompts.",
    "def": "Fine-tuning is additional training applied to an existing LLM using examples of the behavior you want — input/output pairs from your task — so the behavior is baked into the model's weights instead of requested in every <a href='pages/01-what-is-an-eval.html'>prompt</a>. Teams reach for it when prompting hits a ceiling: a format too intricate to describe, a tone too subtle to instruct, or prompts grown too long and costly. It raises the stakes for evals because the training examples must be held apart from the test set (<a href='pages/05-from-failures-to-evals.html'>train/test split</a>) — otherwise the eval just measures memorization of its own answers.",
    "see": [
      "train-test-split",
      "prompt",
      "synthetic-data"
    ]
  },
  "rag": {
    "name": "RAG (Retrieval-Augmented Generation)",
    "short": "An architecture where the system first retrieves relevant documents and then has the LLM answer using them — grounding responses in real sources.",
    "def": "Retrieval-augmented generation is an architecture where the system first searches a document store for material relevant to the user's question, then includes those documents in the <a href='pages/01-what-is-an-eval.html'>prompt</a> so the LLM answers from them. It exists because models only know their training data — RAG gives them your private, current documents without retraining, and grounding answers in retrieved text reduces <a href='pages/01-what-is-an-eval.html'>hallucination</a>. For evals it splits one question into two: did retrieval find the right documents, and did the model answer faithfully from them? Each step gets its own metrics — see <a href='pages/25-tooling-survey.html'>The Tooling Landscape</a>.",
    "also": "retrieval-augmented generation",
    "see": [
      "hallucination",
      "context-window",
      "trace"
    ]
  },
  "hallucination": {
    "name": "Hallucination",
    "short": "When an LLM states something false with full confidence — fabricated facts, citations, or details — because it generates plausible text, not verified text.",
    "def": "A hallucination is an LLM output that's confidently stated but false — an invented fact, a citation to a paper that doesn't exist, a detail not in the source document. It happens because the model generates <em>plausible</em> text, not <em>verified</em> text: next-token prediction has no built-in step that checks claims against reality, so fluent fabrication is a natural output mode rather than a rare glitch. Hallucination is among the most common <a href='pages/04-error-analysis.html'>failure modes</a> teams find in error analysis, and detecting it — especially against retrieved sources in <a href='pages/25-tooling-survey.html'>RAG systems</a> — is a major use of evals.",
    "also": "confabulation, fabrication",
    "see": [
      "rag",
      "failure-mode",
      "ground-truth",
      "llm"
    ]
  },
  "error-analysis": {
    "name": "Error Analysis",
    "short": "The practice of reading your system's real outputs one by one, noting what went wrong, and grouping the notes into failure categories worth fixing and testing.",
    "def": "Error analysis is the practice of actually reading your system's outputs — real <a href='pages/04-error-analysis.html'>traces</a>, one at a time — writing a note about whatever went wrong in each, and then grouping those notes into recurring failure categories. It exists because you cannot decide what to test before knowing how your system actually fails, and intuition about that is reliably wrong: the failures that matter are discovered in the data, not predicted from the armchair. The notes become a <a href='pages/04-error-analysis.html'>failure taxonomy</a>, and the taxonomy tells you which evals to build. Most practitioners call this the highest-leverage activity in all of eval work.",
    "see": [
      "open-coding",
      "axial-coding",
      "failure-taxonomy",
      "trace",
      "annotation"
    ]
  },
  "open-coding": {
    "name": "Open Coding",
    "short": "Reading traces and writing a free-form note about what's wrong with each one, without predefined categories — letting failure patterns emerge from the data.",
    "def": "Open coding is the first pass of <a href='pages/04-error-analysis.html'>error analysis</a>: read each trace and write a short free-form note about what's wrong with it — no predefined categories, no checklist. The term comes from grounded theory, a qualitative research method built on the idea that categories should emerge from the data rather than be imposed on it. The 'open' discipline matters because predefined categories smuggle in your assumptions: if you start with a checklist, you only find the failures you already expected, and the surprising ones — usually the important ones — slip through unnamed.",
    "also": "a term from grounded theory",
    "see": [
      "axial-coding",
      "error-analysis",
      "annotation",
      "theoretical-saturation"
    ]
  },
  "axial-coding": {
    "name": "Axial Coding",
    "short": "The second pass of error analysis: grouping the free-form notes from open coding into a small set of named, recurring failure categories.",
    "def": "Axial coding is the second pass of <a href='pages/04-error-analysis.html'>error analysis</a>: take the pile of free-form notes produced by <a href='pages/04-error-analysis.html'>open coding</a> and group them into a small set of named categories — 'hallucinated order status,' 'ignored formatting instruction,' and so on. Like open coding, the term comes from grounded theory. The step exists because raw notes aren't actionable: only once failures are grouped and counted can you see which mode is most common, decide what to fix first, and turn each category into a targeted eval.",
    "also": "a term from grounded theory",
    "see": [
      "open-coding",
      "failure-taxonomy",
      "failure-mode",
      "error-analysis"
    ]
  },
  "failure-mode": {
    "name": "Failure Mode",
    "short": "A recurring, named way your system goes wrong — like 'invents citations' or 'ignores length limits' — specific enough to count and test for.",
    "def": "A failure mode is a recurring, named way your system goes wrong — 'invents citations,' 'ignores the length limit,' 'answers in the wrong language.' The name matters: until a pattern of failures has a label, you can't count how often it happens, prioritize it against other problems, or write an eval that targets it. Failure modes are discovered through <a href='pages/04-error-analysis.html'>error analysis</a> rather than brainstormed in advance, and the full catalog of them for a system is its <a href='pages/04-error-analysis.html'>failure taxonomy</a>.",
    "see": [
      "failure-taxonomy",
      "error-analysis",
      "axial-coding",
      "product-eval"
    ]
  },
  "failure-taxonomy": {
    "name": "Failure Taxonomy",
    "short": "The organized catalog of a system's failure modes, with counts — showing which problems are common and which evals are worth building.",
    "def": "A failure taxonomy is the organized catalog of a system's <a href='pages/04-error-analysis.html'>failure modes</a>, usually with counts of how often each appears in reviewed traces. It's the deliverable of <a href='pages/04-error-analysis.html'>error analysis</a> and the input to everything after: the counts tell you which problems are frequent enough to fix, and each category points at a specific eval to build. A taxonomy is also a living document — fix the top failure modes and new ones surface, so teams revisit it as the system and its users evolve.",
    "see": [
      "failure-mode",
      "error-analysis",
      "axial-coding",
      "eval-driven-development"
    ]
  },
  "theoretical-saturation": {
    "name": "Theoretical Saturation",
    "short": "The point in trace review when new traces stop revealing new failure types — the signal that you've seen enough and can stop coding.",
    "def": "Theoretical saturation is the stopping signal for <a href='pages/04-error-analysis.html'>trace review</a>: the point where reading additional traces keeps turning up failures you've already categorized, and nothing new. The term comes from grounded theory, where it answers the question every qualitative researcher faces — 'how much data is enough?' — without picking an arbitrary number in advance: you stop when the data stops teaching you. In practice teams review traces in batches and watch for the batch where every note lands in an existing category.",
    "also": "a term from grounded theory",
    "see": [
      "open-coding",
      "error-analysis",
      "failure-taxonomy"
    ]
  },
  "criteria-drift": {
    "name": "Criteria Drift",
    "short": "The phenomenon that grading outputs changes your grading criteria — reviewing examples surfaces standards you didn't know you had.",
    "def": "Criteria drift is the observed phenomenon that the act of grading outputs changes the grader's own criteria: you start labeling with one standard, and seeing concrete examples surfaces requirements you didn't know you had — an output is technically correct but you realize the tone is wrong, so 'tone' quietly joins the criteria. The term comes from the EvalGen study of how people actually build evals. Its practical consequence is that grading criteria can't be fully specified up front; they must be developed <em>by</em> labeling, and <a href='pages/06-validating-the-grader.html'>graders need re-validation</a> as the criteria settle.",
    "see": [
      "annotation",
      "judge-alignment",
      "rubric",
      "error-analysis"
    ]
  },
  "principal-domain-expert": {
    "name": "Principal Domain Expert",
    "short": "The single designated expert whose judgment officially defines quality for a product eval — one trusted voice instead of a committee's averaged opinions.",
    "def": "The principal domain expert is the one designated person whose judgment officially defines quality for a product eval — Hamel Husain's term. Designating a single expert solves a real problem: when several reviewers share labeling, they disagree, and averaging their conflicting standards bakes noise into your <a href='pages/03-types-of-evaluators.html'>ground truth</a>; a single consistent voice gives the eval a coherent standard to aim at. The expert's pass/fail labels and written critiques become the target an <a href='pages/10-aligning-judges.html'>LLM judge is aligned to</a> via critique shadowing.",
    "also": "a term from Hamel Husain",
    "see": [
      "critique-shadowing",
      "judge-alignment",
      "ground-truth",
      "inter-annotator-agreement"
    ]
  },
  "critique-shadowing": {
    "name": "Critique Shadowing",
    "short": "Building an LLM judge by having it shadow a human expert: the expert labels outputs pass/fail with written critiques, and the judge prompt is iterated until it agrees.",
    "def": "Critique shadowing is an iterative process for building a trustworthy <a href='pages/08-llm-as-judge.html'>LLM judge</a>, described by Hamel Husain: a domain expert labels real outputs pass/fail and writes a short critique explaining each call; you draft a judge prompt (using some labeled examples as few-shot demonstrations), run it on held-out labeled cases, study the disagreements, and revise — repeating until the judge tracks the expert. The expert's critiques are the key ingredient: they capture <em>why</em> outputs fail, which is exactly what the judge prompt needs to encode. The process is the subject of <a href='pages/10-aligning-judges.html'>Aligning Judges with Human Experts</a>.",
    "see": [
      "principal-domain-expert",
      "judge-alignment",
      "llm-as-judge",
      "binary-judgment",
      "few-shot"
    ]
  },
  "binary-judgment": {
    "name": "Binary Judgment",
    "short": "Grading each output as simply pass or fail instead of on a numeric scale — a forced clear decision that graders can apply consistently.",
    "def": "A binary judgment grades each output as simply pass or fail, rather than on a numeric scale. The case for it is consistency: people (and LLM judges) can rarely agree on what separates a 4 from a 5 on a <a href='pages/05-from-failures-to-evals.html'>Likert scale</a>, and disagreement you can't resolve is just noise in your metric — whereas 'would you ship this answer?' forces a decision graders can make repeatably. Pass/fail also aggregates cleanly (percent passing) and pairs naturally with a written critique explaining each failure, which preserves the nuance the scale was supposed to capture.",
    "also": "pass/fail grading",
    "see": [
      "likert-scale",
      "critique-shadowing",
      "metric",
      "inter-annotator-agreement"
    ]
  },
  "likert-scale": {
    "name": "Likert Scale",
    "short": "A numeric rating scale (e.g. 1–5) for grading outputs. Familiar from surveys, but adjacent points are hard to tell apart consistently.",
    "def": "A Likert scale rates each output on an ordered numeric scale — 1 to 5, 1 to 10 — and is the format most people reach for first because it's familiar from surveys and feels more informative than pass/fail. The trouble is that the extra resolution is largely illusory: no one can define the boundary between a 3 and a 4 in a way two graders apply identically, so the middle of the scale fills with inconsistent judgments, and averages over them are built on noise. That's why eval practitioners widely prefer <a href='pages/05-from-failures-to-evals.html'>binary judgments</a> with written critiques.",
    "also": "rating scale, 1–5 scale",
    "see": [
      "binary-judgment",
      "inter-annotator-agreement",
      "single-answer-grading"
    ]
  },
  "annotation": {
    "name": "Annotation",
    "short": "Humans labeling data — marking outputs pass/fail, tagging failure types, writing critiques — to create the ground truth that evals and judges are built on.",
    "def": "Annotation is the work of humans labeling data: marking outputs pass or fail, tagging which <a href='pages/04-error-analysis.html'>failure mode</a> a trace exhibits, writing critiques. It's the source of nearly all <a href='pages/03-types-of-evaluators.html'>ground truth</a> — somebody's judgment, recorded — which makes its quality the ceiling on everything built from it, including <a href='pages/10-aligning-judges.html'>LLM judges</a> validated against the labels. Good annotation practice is deliberate: clear guidelines, a designated expert or measured <a href='pages/04-error-analysis.html'>inter-annotator agreement</a>, and tooling that makes labeling fast enough to actually happen.",
    "also": "labeling, data labeling",
    "see": [
      "ground-truth",
      "inter-annotator-agreement",
      "principal-domain-expert",
      "open-coding"
    ]
  },
  "inter-annotator-agreement": {
    "name": "Inter-Annotator Agreement",
    "short": "How often independent human labelers give the same label to the same item — a check on whether your grading criteria are well-defined at all.",
    "def": "Inter-annotator agreement measures how often independent human labelers assign the same label to the same item. It matters because it tests the criteria, not just the people: if trained annotators reading the same guidelines disagree constantly, the task itself is underspecified, and no grader — human or <a href='pages/08-llm-as-judge.html'>LLM judge</a> — can be 'right' against such labels. Agreement is usually reported with chance-corrected statistics like <a href='appendices/e-agreement-metrics.html'>Cohen's kappa</a>, because two labelers using a 90/10 label split will agree often by luck alone. Low agreement is a signal to sharpen definitions or switch to <a href='pages/05-from-failures-to-evals.html'>binary judgments</a>.",
    "also": "IAA, inter-rater reliability",
    "see": [
      "annotation",
      "binary-judgment",
      "judge-alignment",
      "principal-domain-expert"
    ]
  },
  "synthetic-data": {
    "name": "Synthetic Data",
    "short": "Test cases generated by an LLM rather than collected from real usage — a way to get coverage of inputs you don't have enough real examples of.",
    "def": "Synthetic data is test data generated by an LLM rather than collected from real users — for evals, typically test inputs: rare edge cases, adversarial phrasings, or coverage of scenarios you have no logs for yet. It exists because real data is scarce exactly when you need evals most (before launch) and rarely covers the long tail. The standing caveats: generated inputs drift toward what the model finds typical rather than what real users do, so synthetic cases need human review, and grading labels should not be generated by the same model being evaluated. See <a href='pages/05-from-failures-to-evals.html'>From Failure Modes to Evals</a>.",
    "see": [
      "dataset",
      "golden-dataset",
      "self-preference"
    ]
  },
  "eval-driven-development": {
    "name": "Eval-Driven Development",
    "short": "Building LLM products with evals at the center of the loop: define failure, build the measure, then iterate on prompts and models against the score.",
    "def": "Eval-driven development builds LLM products around a measurement loop: discover failures through <a href='pages/04-error-analysis.html'>error analysis</a>, turn them into evals, then iterate on prompts, retrieval, and model choice against the scores — analogous to test-driven development in software. The reason it works is iteration velocity: without evals every change requires manual eyeballing and gut calls, while with them you can try ten prompt variants in an afternoon and know which one won. The full loop — including <a href='pages/07-evals-in-the-lifecycle.html'>CI, monitoring, and feeding production failures back into the eval set</a> — is what makes LLM development systematic instead of vibes-based.",
    "also": "EDD",
    "see": [
      "regression-testing",
      "error-analysis",
      "golden-dataset",
      "metric"
    ]
  },
  "llm-as-judge": {
    "name": "LLM-as-Judge",
    "short": "Using an LLM, given a grading prompt, to score another LLM's outputs — scaling up evaluation of open-ended tasks where code can't grade and humans are too slow.",
    "def": "LLM-as-judge means using an LLM, equipped with a grading prompt, to score another LLM's outputs. It exists to fill a gap: open-ended outputs (summaries, support replies, essays) can't be graded by string-matching code, and human review doesn't scale to thousands of cases per experiment — a judge model offers human-like judgment at code-like speed. The catch is that the judge is itself an LLM, with its own <a href='pages/09-judge-biases.html'>biases</a> and failure modes, so a judge must be <a href='pages/06-validating-the-grader.html'>validated against human judgment</a> before its scores can be trusted. The approach was popularized alongside the MT-Bench evaluation.",
    "also": "LLM judge, AI judge, autograder",
    "see": [
      "grader",
      "judge-alignment",
      "position-bias",
      "pairwise-comparison",
      "single-answer-grading",
      "g-eval"
    ]
  },
  "pairwise-comparison": {
    "name": "Pairwise Comparison",
    "short": "A judging format where the grader sees two responses to the same input and picks the better one, rather than scoring each alone.",
    "def": "Pairwise comparison is a judging format where the grader — human or <a href='pages/08-llm-as-judge.html'>LLM judge</a> — sees two responses to the same input side by side and picks the better one (or calls a tie). It exists because relative judgments are easier to make consistently than absolute ones: deciding which of two summaries is better is more reliable than assigning each a defensible score alone. It's the format behind <a href='pages/23-leaderboard-illusion.html'>arena-style rankings</a>. Its costs: results only say which is better, not whether either is good enough, and LLM judges show <a href='pages/09-judge-biases.html'>position bias</a> — favoring an answer because of where it appears — so careful setups swap the order and check both ways.",
    "also": "A/B grading, preference comparison",
    "see": [
      "single-answer-grading",
      "position-bias",
      "arena-rating",
      "llm-as-judge"
    ]
  },
  "single-answer-grading": {
    "name": "Single-Answer Grading",
    "short": "A judging format where the grader scores one response on its own — against a rubric or pass/fail criteria — without comparing it to an alternative.",
    "def": "Single-answer grading has the judge score one response on its own — against a <a href='pages/08-llm-as-judge.html'>rubric</a>, pass/fail criteria, or sometimes a reference answer — rather than comparing it to an alternative. It's the natural format for product evals, where the question is 'is this output good enough to ship?', not 'which of two is better?', and it produces absolute scores you can track over time. The trade-off cuts the other way from <a href='pages/08-llm-as-judge.html'>pairwise comparison</a>: absolute judgments are harder to make consistently, which is why they lean on tight rubrics and <a href='pages/05-from-failures-to-evals.html'>binary judgments</a>.",
    "also": "pointwise grading, direct assessment",
    "see": [
      "pairwise-comparison",
      "rubric",
      "binary-judgment",
      "llm-as-judge"
    ]
  },
  "rubric": {
    "name": "Rubric",
    "short": "The explicit written criteria a grader uses to score outputs — what to check, what counts as failing — so judgments are consistent and reviewable.",
    "def": "A rubric is the explicit written criteria a grader applies: what to check, what counts as a failure, how to decide borderline cases. It exists because 'grade this response' is underspecified — without written criteria, every grader (and every run of an <a href='pages/08-llm-as-judge.html'>LLM judge</a>) fills the gap with its own taste, and the scores stop meaning one thing. A rubric makes grading consistent, makes disagreements debuggable (you can point at the criterion in dispute), and is where lessons from <a href='pages/04-error-analysis.html'>error analysis</a> get encoded. Expect to revise it as labeling reveals criteria you didn't know you had (<a href='pages/06-validating-the-grader.html'>criteria drift</a>).",
    "also": "grading criteria",
    "see": [
      "criteria-drift",
      "single-answer-grading",
      "binary-judgment",
      "judge-alignment"
    ]
  },
  "position-bias": {
    "name": "Position Bias",
    "short": "An LLM judge's tendency to favor a response based on where it appears (often the first) in a side-by-side comparison, regardless of quality.",
    "def": "Position bias is an <a href='pages/08-llm-as-judge.html'>LLM judge's</a> tendency, in a side-by-side comparison, to favor a response because of where it appears — often the one shown first — independent of quality. It was documented in the MT-Bench work on LLM judging, and it matters because it silently corrupts <a href='pages/08-llm-as-judge.html'>pairwise</a> results: if the judge leans first-position, whichever system you happen to list first wins extra ties. The standard defense is symmetry: run every comparison twice with the order swapped, and treat verdicts that flip with the order as ties. See <a href='pages/09-judge-biases.html'>Judge Biases and Failure Modes</a>.",
    "also": "order bias",
    "see": [
      "pairwise-comparison",
      "verbosity-bias",
      "self-enhancement-bias",
      "llm-as-judge"
    ]
  },
  "verbosity-bias": {
    "name": "Verbosity Bias",
    "short": "An LLM judge's tendency to rate longer, more detailed-looking responses higher, even when the extra length adds no real substance.",
    "def": "Verbosity bias is an <a href='pages/08-llm-as-judge.html'>LLM judge's</a> tendency to score longer, more elaborate responses higher, even when the added length is padding rather than substance. It plausibly traces to training: models are tuned on human preference data, and human raters also tend to reward thoroughness-looking answers, so the judge inherits and amplifies the habit. It matters because it's exploitable — a system can climb your eval by getting wordier, not better. Defenses include rubrics that explicitly value concision, checking whether score correlates with length in your results, and spot-checking long winners by hand. See <a href='pages/09-judge-biases.html'>Judge Biases</a>.",
    "also": "length bias",
    "see": [
      "position-bias",
      "self-enhancement-bias",
      "llm-as-judge",
      "rubric"
    ]
  },
  "self-enhancement-bias": {
    "name": "Self-Enhancement Bias",
    "short": "An LLM judge's tendency to rate outputs produced by itself (or models like it) higher than equally good outputs from other models.",
    "def": "Self-enhancement bias is the tendency of an <a href='pages/08-llm-as-judge.html'>LLM judge</a> to rate outputs from itself — or from models similar to it — higher than comparable outputs from other models; the term comes from the MT-Bench evaluation work. The mechanism is intuitive: a judge scores what matches its own sense of a good answer, and its own outputs match that sense by construction. It matters whenever the judge model is also a contestant, as in model-comparison studies. The literature splits the phenomenon into <a href='pages/09-judge-biases.html'>self-preference</a> (the behavior) and <a href='pages/09-judge-biases.html'>self-recognition</a> (a proposed mechanism: identifying its own text).",
    "see": [
      "self-preference",
      "self-recognition",
      "position-bias",
      "llm-as-judge"
    ]
  },
  "self-preference": {
    "name": "Self-Preference",
    "short": "The measured behavior of an LLM judge scoring its own outputs above others' — the effect that self-recognition is proposed to explain.",
    "def": "Self-preference is the measured behavior of an LLM judge favoring its own outputs over comparable outputs from other models — what you observe when you put a judge's own generations into the pool it grades. The term is used in research that pulls <a href='pages/09-judge-biases.html'>self-enhancement bias</a> apart into two pieces: the preference itself, and <a href='pages/09-judge-biases.html'>self-recognition</a> — the judge's ability to identify text as its own — studied as a possible cause. The practical upshot: avoid grading a system with the same model that powers it, or validate carefully against human labels if you must.",
    "see": [
      "self-recognition",
      "self-enhancement-bias",
      "judge-alignment",
      "llm-as-judge"
    ]
  },
  "self-recognition": {
    "name": "Self-Recognition",
    "short": "An LLM's ability to identify which texts it wrote itself — studied as a possible mechanism behind judges favoring their own outputs.",
    "def": "Self-recognition is an LLM's ability to tell which of several texts it produced itself, without being told. It's studied because it offers a mechanism for <a href='pages/09-judge-biases.html'>self-preference</a>: if a judge can implicitly recognize its own style, that recognition could drive the favoritism, the way a teacher might unconsciously favor an essay that sounds like their own writing. The distinction matters for fixing the problem — a recognition-driven bias might be reduced by paraphrasing outputs before judging, while a taste-driven one wouldn't be. See <a href='pages/09-judge-biases.html'>Judge Biases and Failure Modes</a>.",
    "see": [
      "self-preference",
      "self-enhancement-bias",
      "llm-as-judge"
    ]
  },
  "chain-of-thought": {
    "name": "Chain-of-Thought",
    "short": "Prompting an LLM to write out step-by-step reasoning before its answer — used in judging to make the model evaluate before it scores.",
    "def": "Chain-of-thought is the technique of prompting an LLM to write out step-by-step reasoning before giving its final answer, rather than answering immediately. It helps because the model generates one <a href='pages/01-what-is-an-eval.html'>token</a> at a time with no hidden scratchpad — writing the reasoning out <em>is</em> its way of working through a problem. In <a href='pages/08-llm-as-judge.html'>LLM judging</a> it's standard practice: ask the judge to analyze the response against the criteria first and only then emit a verdict, which both improves the verdicts and leaves a readable rationale you can audit when you disagree with a score.",
    "also": "CoT",
    "see": [
      "llm-as-judge",
      "g-eval",
      "prompt",
      "few-shot"
    ]
  },
  "few-shot": {
    "name": "Few-Shot",
    "short": "Including worked examples of the task in the prompt so the model learns the pattern from them — for judges, examples of graded outputs.",
    "def": "Few-shot prompting includes a handful of worked examples of the task directly in the <a href='pages/01-what-is-an-eval.html'>prompt</a> — input, correct output, input, correct output — so the model picks up the pattern from demonstrations instead of from instructions alone ('zero-shot' means no examples). It works because LLMs are pattern continuers: examples pin down format and standards more precisely than descriptions can. In judge-building it's a key tool — showing the judge expert-graded examples, complete with critiques, is much of how <a href='pages/10-aligning-judges.html'>critique shadowing</a> transfers an expert's standards into the judge prompt. Benchmark scores also depend on the shot count, so it's always reported.",
    "also": "in-context learning, n-shot",
    "see": [
      "prompt",
      "chain-of-thought",
      "critique-shadowing",
      "llm-as-judge"
    ]
  },
  "reference-guided-grading": {
    "name": "Reference-Guided Grading",
    "short": "Giving an LLM judge a known-correct reference answer to consult while grading, anchoring its judgment instead of trusting it to know the answer.",
    "def": "Reference-guided grading gives the <a href='pages/08-llm-as-judge.html'>LLM judge</a> a known-correct reference answer alongside the response it's scoring, so it judges by comparison rather than from its own knowledge. The point is anchoring: on tasks with definite answers — math, factual questions — an unanchored judge can be confidently wrong about the answer itself and grade a correct response as a failure; the reference removes that failure mode. It's the judge-flavored version of <a href='pages/03-types-of-evaluators.html'>reference-based evaluation</a>, and it only works where a reference can be written — open-ended tasks still need rubric-based judging.",
    "see": [
      "reference-based",
      "ground-truth",
      "llm-as-judge",
      "rubric"
    ]
  },
  "judge-alignment": {
    "name": "Judge Alignment",
    "short": "How closely an LLM judge's verdicts match a trusted human expert's on the same outputs — measured before the judge's scores are trusted at scale.",
    "def": "Judge alignment is the degree to which an <a href='pages/08-llm-as-judge.html'>LLM judge's</a> verdicts match a trusted human's verdicts on the same outputs — and the process of measuring and improving that match. It's the answer to the obvious objection to LLM judging: if a fallible model does the grading, why believe the scores? You believe them only after checking the judge against expert labels on a held-out set, using agreement measures like <a href='appendices/e-agreement-metrics.html'>Cohen's kappa</a> or per-class rates rather than raw percent agreement, which flatters judges on lopsided data. Alignment is ongoing — judges get re-checked as criteria evolve. See <a href='pages/10-aligning-judges.html'>Aligning Judges with Human Experts</a>.",
    "also": "judge validation",
    "see": [
      "critique-shadowing",
      "inter-annotator-agreement",
      "principal-domain-expert",
      "criteria-drift"
    ]
  },
  "g-eval": {
    "name": "G-Eval",
    "short": "An LLM-judging technique that has the judge reason step by step, fill out a scoring form, and weight scores by token probabilities for finer-grained results.",
    "def": "G-Eval is a named LLM-judging technique that combines three pieces: the judge first generates <a href='pages/08-llm-as-judge.html'>chain-of-thought</a> evaluation steps from the criteria, then fills out a scoring form by following them, and the final score is computed by weighting the possible score <a href='pages/01-what-is-an-eval.html'>tokens</a> by the probability the model assigns each — so instead of a flat '4', you get a probability-weighted average like 3.7. The weighting exists because judges asked for a single number cluster on a few favorites; using the full probability distribution recovers finer distinctions. The catch: it needs token probabilities from the API, which not all providers expose.",
    "see": [
      "llm-as-judge",
      "chain-of-thought",
      "token",
      "single-answer-grading"
    ]
  },
  "model-graded-scorer": {
    "name": "Model-Graded Scorer",
    "short": "Harness terminology (e.g. in Inspect) for a scorer that calls an LLM to grade outputs — LLM-as-judge, packaged as a pluggable component.",
    "def": "A model-graded scorer is eval-harness terminology — used by frameworks like <a href='pages/24-inspect.html'>Inspect</a> — for a <a href='pages/02-anatomy-of-an-eval.html'>scorer</a> component that calls an LLM to do the grading, as opposed to scorers that match strings or run code. It's <a href='pages/08-llm-as-judge.html'>LLM-as-judge</a> packaged as a pluggable part: the harness handles running samples and aggregating results, and you slot in a model-graded scorer with a grading prompt where deterministic checks can't judge the output. Same concept, infrastructure vocabulary — and the same obligation to <a href='pages/06-validating-the-grader.html'>validate the grader</a> applies.",
    "see": [
      "grader",
      "llm-as-judge",
      "harness",
      "judge-alignment"
    ]
  },
  "agent": {
    "name": "Agent",
    "short": "An LLM-powered system that takes multiple steps toward a goal — calling tools, observing results, and deciding what to do next — rather than producing a single response.",
    "def": "An <strong>agent</strong> is an LLM wrapped in a loop: it reads the current situation, decides on an action (often a <code>tool call</code> like running a command or querying an API), observes the result, and repeats until the task is done or it gives up. Agents exist because many real tasks — fixing a bug, booking a trip, researching a question — can't be done in one shot; they require acting on the world and reacting to what comes back. This loop structure is exactly what makes agents hard to evaluate: there are many paths to success, failures compound across steps, and the same agent can succeed one run and fail the next. See <a href='pages/11-evaluating-agents.html'>What Makes Agents Different</a>.",
    "see": [
      "trajectory",
      "tool-call",
      "environment",
      "scaffold"
    ]
  },
  "trajectory": {
    "name": "Trajectory",
    "short": "The full step-by-step record of an agent run: every model response, tool call, and result from start to finish.",
    "def": "A <strong>trajectory</strong> is the complete sequence of everything an agent did during one run: each reasoning step, each tool call, each result that came back, in order. It is the agent-world equivalent of a <em>trace</em>, and it matters because an agent's final answer alone tells you almost nothing about <em>why</em> it succeeded or failed — the interesting information (wrong tool, bad plan, recovered from an error) lives in the steps. Evaluating agents usually means either scoring the end result (<a href='pages/11-evaluating-agents.html'>outcome-based</a>) or scoring the trajectory itself (process-based).",
    "see": [
      "agent",
      "tool-call",
      "outcome-based-evaluation",
      "process-based-evaluation",
      "tracing"
    ]
  },
  "tool-call": {
    "name": "Tool call",
    "short": "A single action an agent takes on the outside world — running a shell command, calling an API, querying a database — requested by the model and executed by the harness.",
    "def": "A <strong>tool call</strong> is the mechanism by which an LLM acts instead of just talking: the model emits a structured request (\"run <code>ls</code>\", \"search the web for X\", \"update row 12\"), the surrounding program executes it, and the result is fed back into the model's context. Tool calls are what turn a text generator into an <a href='pages/11-evaluating-agents.html'>agent</a>. For evaluation, they are both the unit you inspect when reading a trajectory (did it call the right tool with the right arguments?) and a major source of failure modes — agents can pick the wrong tool, malform the arguments, or misread the result.",
    "also": "function call, action",
    "see": [
      "agent",
      "trajectory",
      "environment"
    ]
  },
  "environment": {
    "name": "Environment",
    "short": "The simulated or real world an agent acts in during an eval — a codebase, a website, a computer desktop, a database — that responds to the agent's actions.",
    "def": "The <strong>environment</strong> is everything the agent can act on and observe: a Git repository it can edit, a browser it can click around in, an operating system, a mock airline-booking database. Agent benchmarks differ from ordinary question-answering benchmarks chiefly in that they must ship an environment, not just questions — and the environment's fidelity and graders determine what the score actually means. A buggy or too-forgiving environment quietly measures the wrong thing. See <a href='pages/13-agentic-benchmark-landscape.html'>The Agentic Benchmark Landscape</a> for how major benchmarks build theirs.",
    "see": [
      "agent",
      "sandbox",
      "state-based-evaluation"
    ]
  },
  "outcome-based-evaluation": {
    "name": "Outcome-based evaluation",
    "short": "Grading an agent only on whether the end result is correct, ignoring how it got there.",
    "def": "<strong>Outcome-based evaluation</strong> scores an agent by checking the final result — do the tests pass, is the right row in the database, did the user get a correct answer — without judging the steps taken. Its appeal is objectivity: a passing test suite is a passing test suite, no judge required. Its blind spot is everything in between: an agent can reach the right outcome through reckless or destructive intermediate steps, or fail at the last moment after a nearly perfect run, and outcome grading sees only pass or fail. Most serious agent evals pair it with <a href='pages/11-evaluating-agents.html'>process-based</a> inspection of trajectories.",
    "see": [
      "process-based-evaluation",
      "state-based-evaluation",
      "trajectory"
    ]
  },
  "process-based-evaluation": {
    "name": "Process-based evaluation",
    "short": "Grading an agent on the quality of its steps — the trajectory — not just the final result.",
    "def": "<strong>Process-based evaluation</strong> looks inside the run: did the agent make a sensible plan, call appropriate tools, avoid forbidden actions, recover from errors? It exists because outcomes alone can mislead — a correct answer reached by luck or by a dangerous shortcut is not the same as a correct answer reached well, and a near-miss failure contains diagnostic gold that a 0/1 outcome score throws away. The cost is subjectivity: judging a trajectory usually requires a rubric and often an <a href='pages/08-llm-as-judge.html'>LLM judge</a>, which brings its own biases. See <a href='pages/11-evaluating-agents.html'>What Makes Agents Different</a>.",
    "see": [
      "outcome-based-evaluation",
      "trajectory",
      "llm-as-judge"
    ]
  },
  "user-simulation": {
    "name": "User simulation",
    "short": "Using an LLM to play the human user in a multi-turn agent eval, so conversations can be run automatically at scale.",
    "def": "Many agent tasks involve a back-and-forth with a person (\"I want to change my flight\" … \"which flight?\" … \"the Tuesday one\"). <strong>User simulation</strong> replaces that person with another LLM, prompted with the user's goal and persona, so thousands of conversations can run unattended. This is what lets benchmarks like tau-bench evaluate conversational agents at all — but it adds a second model whose own mistakes (revealing too much, misunderstanding, going off-script) get tangled into the agent's score. See <a href='pages/14-reliability-pass-hat-k.html'>Reliability: pass^k and Repeated Trials</a>.",
    "see": [
      "agent",
      "environment",
      "pass-hat-k"
    ]
  },
  "pass-hat-k": {
    "name": "pass^k",
    "short": "The probability that an agent succeeds on ALL k independent attempts at the same task — a reliability metric. Contrast with pass@k, where any one success counts.",
    "def": "<strong>pass^k</strong> (\"pass-hat-k\") asks: if you run the same task <em>k</em> times, what fraction of tasks does the agent get right <em>every single time</em>? It is the metric tau-bench introduced for measuring reliability, and it is the mirror image of <a href='pages/18-pass-at-k.html'>pass@k</a>, which counts a task as solved if <em>any</em> of <em>k</em> attempts succeeds. The distinction matters because deployment cares about consistency: a customer-service agent that succeeds on a task half the time looks fine under pass@k but is unusable, and pass^k makes that visible — it falls fast as <em>k</em> grows unless the agent is genuinely consistent. See <a href='pages/14-reliability-pass-hat-k.html'>Reliability: pass^k and Repeated Trials</a>.",
    "also": "pass-hat-k, pass^k reliability metric",
    "see": [
      "pass-at-k",
      "user-simulation",
      "epoch"
    ]
  },
  "state-based-evaluation": {
    "name": "State-based evaluation",
    "short": "Grading an agent by comparing the final state of its environment (e.g. a database) against the known goal state, regardless of the path taken.",
    "def": "<strong>State-based evaluation</strong> checks the world, not the words: after the agent finishes, the harness compares the environment's final state — database rows, files on disk, a calendar — to the goal state the task defines. If the task was \"cancel the Tuesday flight,\" the grader just checks whether the booking record now says cancelled. This sidesteps judging conversation quality or step choices entirely, which makes it cheap and objective, and it naturally allows multiple valid paths to the same goal. Its limits are the flip side: it can't tell a graceful run from a chaotic one, and it only works when the goal state can be specified precisely. See <a href='pages/14-reliability-pass-hat-k.html'>Reliability: pass^k and Repeated Trials</a>.",
    "see": [
      "outcome-based-evaluation",
      "environment",
      "agent"
    ]
  },
  "sandbox": {
    "name": "Sandbox",
    "short": "An isolated, disposable execution environment (often a container or VM) where an agent can run code and modify files without affecting anything real.",
    "def": "A <strong>sandbox</strong> is a walled-off copy of the world — typically a Docker container or virtual machine — where the agent can execute commands, edit files, and break things freely. Evals need sandboxes for two reasons: safety (agents run arbitrary model-generated code, which you do not want touching your real machine) and reproducibility (every run starts from the same clean snapshot, so results are comparable across runs and across models). Harnesses like <a href='pages/24-inspect.html'>Inspect</a> build sandbox management in as a first-class feature.",
    "see": [
      "environment",
      "agent",
      "harness"
    ]
  },
  "scaffold": {
    "name": "Scaffold",
    "short": "The program structure around a model — prompts, tools, retries, control flow — that turns a raw LLM into a working agent. Different scaffolds give the same model very different scores.",
    "def": "A <strong>scaffold</strong> is everything you wrap around the model to make it function as an agent: the system prompt, the set of tools it can call, the loop that feeds results back, retry logic, stopping rules. The same model under different scaffolds can perform wildly differently, which creates a chronic evaluation problem: when a leaderboard entry beats another, is the model better or just the scaffold? Careful benchmark reporting separates the two (e.g. SWE-bench results are properly read as model-plus-scaffold results). See <a href='pages/12-swe-bench-case-study.html'>Case Study: SWE-bench</a> and <a href='pages/15-cost-and-capability.html'>Cost Frontiers and Time Horizons</a>.",
    "also": "agent harness, agent framework",
    "see": [
      "agent",
      "elicitation",
      "harness",
      "cost-controlled-evaluation"
    ]
  },
  "elicitation": {
    "name": "Elicitation",
    "short": "The effort spent getting a model's best possible performance — better prompts, tools, scaffolding — before measuring it. Low elicitation makes a capable model look weak.",
    "def": "<strong>Elicitation</strong> (a term used heavily in the METR evaluation methodology) is the work of drawing out what a model can actually do before you score it: tuning prompts, fixing tool bugs, adjusting the scaffold, giving it a fair number of attempts. It matters because an eval is supposed to measure the model's capability, but what it directly measures is model-plus-setup — and a sloppy setup produces a false negative about capability. This cuts both ways: for safety-motivated evals, <em>under</em>-elicitation is the dangerous error, because \"the model couldn't do it\" might really mean \"we didn't try hard enough.\" See <a href='pages/15-cost-and-capability.html'>Cost Frontiers and Time Horizons</a>.",
    "see": [
      "scaffold",
      "time-horizon",
      "construct-validity"
    ]
  },
  "time-horizon": {
    "name": "Time horizon",
    "short": "A way of expressing agent capability as the length of human task (in human time-to-complete) the agent can finish reliably — e.g. 'tasks that take a person an hour.'",
    "def": "A <strong>time horizon</strong> measures agent capability on a human-meaningful scale: instead of \"scored X% on benchmark Y,\" it says \"can complete tasks that take a skilled human about this long.\" The idea, from the METR time-horizon work, is to make capability comparable across very different tasks and trackable over time — task length in human hours is a single axis on which both a five-minute lookup and a multi-day engineering project sit. The reliability threshold matters enormously: the length of task an agent finishes half the time is very different from one it finishes almost always. See <a href='pages/15-cost-and-capability.html'>Cost Frontiers and Time Horizons</a>.",
    "see": [
      "elicitation",
      "agent",
      "pass-hat-k"
    ]
  },
  "cost-controlled-evaluation": {
    "name": "Cost-controlled evaluation",
    "short": "Comparing agents at equal cost (dollars or tokens), not just on accuracy — because rerunning an agent many times buys accuracy that says nothing about the model.",
    "def": "<strong>Cost-controlled evaluation</strong> reports accuracy together with what it cost to achieve, and compares systems at comparable spend. The argument, made forcefully in the \"AI Agents That Matter\" critique, is that agent accuracy is purchasable: wrap any model in enough retries and ensembling and its score rises, so a leaderboard sorted by accuracy alone rewards burning money rather than building better agents. Plotting accuracy against cost and looking at the <a href='pages/15-cost-and-capability.html'>Pareto frontier</a> shows which systems are genuinely better and which are just more expensive.",
    "see": [
      "pareto-frontier",
      "scaffold",
      "overfitting"
    ]
  },
  "pareto-frontier": {
    "name": "Pareto frontier",
    "short": "On an accuracy-vs-cost plot, the set of systems that no other system beats on both axes at once — the only ones worth choosing.",
    "def": "When you plot eval results on two axes — say accuracy versus cost — a system is <strong>Pareto-optimal</strong> if nothing else is both more accurate <em>and</em> cheaper. The <strong>Pareto frontier</strong> is the curve through those undominated points, and everything below or right of it is strictly worse than some available alternative. The concept (borrowed from economics) matters for evals because single-number leaderboards hide trade-offs: the \"best\" agent by accuracy may be dominated in practice by one that gets nearly there at a fraction of the cost. See <a href='pages/15-cost-and-capability.html'>Cost Frontiers and Time Horizons</a>.",
    "see": [
      "cost-controlled-evaluation"
    ]
  },
  "holdout-set": {
    "name": "Holdout set",
    "short": "A portion of eval data kept aside and never used during development, so it can give an honest score that iteration hasn't quietly optimized toward.",
    "def": "A <strong>holdout set</strong> is data you deliberately don't look at while building: you iterate on prompts, scaffolds, and graders against one slice of your eval, then measure the finished system once on the held-out slice. The reason is a quiet failure mode: every time you tweak your system to fix failures you saw, you fit it a little more to those specific cases — and the dev-set score drifts upward without the underlying system getting better on anything else. The holdout score is the honest one precisely because nothing was tuned against it. Note that a holdout you re-check after every change stops being a holdout. See <a href='pages/05-from-failures-to-evals.html'>From Failure Modes to Evals</a>.",
    "also": "held-out set, test split",
    "see": [
      "overfitting",
      "train-test-split",
      "private-holdout"
    ]
  },
  "overfitting": {
    "name": "Overfitting",
    "short": "When a system (or your prompt/scaffold tuning) gets good at the specific examples it was developed against, without getting better at the general task they represent.",
    "def": "<strong>Overfitting</strong> is fitting the quirks of your data rather than the pattern it samples: a model, prompt, or agent scaffold tuned until it aces a particular set of test cases may have learned those cases, not the task. In eval work this bites twice — models can overfit public benchmarks (everyone optimizes toward the same famous test sets), and <em>you</em> can overfit your own eval by iterating against it until the score is meaningless. The standard defense in both cases is the same: keep a <a href='pages/05-from-failures-to-evals.html'>holdout</a> you don't iterate against, and refresh test data periodically. See <a href='pages/21-contamination.html'>Data Contamination</a> for the training-data version of this problem.",
    "see": [
      "holdout-set",
      "contamination",
      "saturation",
      "train-test-split"
    ]
  },
  "random-variable": {
    "name": "Random variable",
    "short": "A quantity whose value depends on chance — like 'whether this eval sample passes' or 'this run's score.' The basic object probability theory works with.",
    "def": "A <strong>random variable</strong> is a number determined by a chance process: the result of a die roll, or — closer to home — whether a given eval sample passes (1) or fails (0) when you run it. The concept exists so we can reason precisely about uncertain quantities: once \"this sample's outcome\" is a random variable, we can talk about its average behavior (<a href='appendices/a-probability.html'>expectation</a>), its spread (variance), and how those propagate into the uncertainty of a whole benchmark score. Eval scores are built out of many small random variables, which is why statistics applies to them at all. Gentle introduction in <a href='appendices/a-probability.html'>Appendix A</a>.",
    "see": [
      "expectation",
      "variance",
      "bernoulli-trial"
    ]
  },
  "expectation": {
    "name": "Expectation",
    "short": "The long-run average value of a random quantity — what you'd get if you could repeat the experiment forever and average the results.",
    "def": "The <strong>expectation</strong> (or expected value, or mean) of a random variable is its probability-weighted average: the value its average converges to over infinitely many repetitions. For evals it is the quantity you actually care about but can never observe directly — a model's \"true\" pass rate on a task distribution is an expectation, and the score from any finite eval run is just an estimate of it. Almost all of eval statistics is about how far that estimate might sit from the expectation it is estimating. See <a href='appendices/a-probability.html'>Appendix A</a>.",
    "also": "expected value, mean",
    "see": [
      "random-variable",
      "variance",
      "unbiased-estimator",
      "standard-error"
    ]
  },
  "variance": {
    "name": "Variance",
    "short": "A measure of how spread out a random quantity is around its average — high variance means individual results land far from the mean.",
    "def": "<strong>Variance</strong> measures spread: it is the expected squared distance between a random variable and its mean. A high-variance eval score bounces around a lot from run to run; a low-variance one is stable. The squaring is a mathematical convenience (it makes variances of independent things add up nicely), but it puts the number in awkward squared units — which is why in practice you usually take its square root, the <a href='appendices/a-probability.html'>standard deviation</a>, to get back to interpretable units. Variance is the raw ingredient behind every error bar in this course. See <a href='appendices/a-probability.html'>Appendix A</a>.",
    "see": [
      "standard-deviation",
      "expectation",
      "standard-error"
    ]
  },
  "standard-deviation": {
    "name": "Standard deviation",
    "short": "The square root of variance: the typical distance between an individual observation and the average, in the same units as the data.",
    "def": "The <strong>standard deviation</strong> is the square root of the <a href='appendices/a-probability.html'>variance</a>, restoring the units of the original quantity: if scores are percentages, the standard deviation is in percentage points. Read it as \"roughly how far a typical single observation sits from the mean.\" Keep it distinct from the <a href='appendices/b-sampling.html'>standard error</a>, which measures uncertainty in an <em>average</em> of many observations — the standard deviation describes the data's spread and doesn't shrink as you collect more, while the standard error shrinks with sample size. See <a href='appendices/a-probability.html'>Appendix A</a>.",
    "see": [
      "variance",
      "standard-error"
    ]
  },
  "standard-error": {
    "name": "Standard error",
    "short": "How much an estimate (like a benchmark score) would typically vary if you reran the whole measurement — the basic unit of an error bar.",
    "def": "The <strong>standard error</strong> answers: if I could repeat this entire eval with a fresh sample of tasks, how much would the resulting score typically move? It is the standard deviation of the <em>estimate</em> rather than of individual data points, and it shrinks as the sample grows — averaging more tasks cancels out more of the per-task luck. This single number is what separates \"Model A scored two points higher\" from \"Model A scored two points higher, but the scores wobble by three points run to run, so this means nothing.\" It is the foundation of <a href='pages/16-error-bars.html'>error bars on eval scores</a>; the mechanics live in <a href='appendices/b-sampling.html'>Appendix B</a>.",
    "also": "SEM, standard error of the mean",
    "see": [
      "standard-deviation",
      "confidence-interval",
      "central-limit-theorem",
      "sample-size",
      "clustered-standard-errors"
    ]
  },
  "central-limit-theorem": {
    "name": "Central limit theorem",
    "short": "The result that averages of many independent measurements follow a predictable bell-curve pattern, regardless of what the individual measurements look like.",
    "def": "The <strong>central limit theorem</strong> (CLT) says that when you average many independent random quantities, the average itself follows an approximately normal (bell-curve) distribution — even if each individual quantity is as un-bell-like as a 0/1 pass-fail outcome. This is the load-bearing wall under eval statistics: it is why a benchmark score (an average of many per-sample results) has predictable uncertainty, and why the simple formulas for <a href='pages/16-error-bars.html'>standard errors and confidence intervals</a> work for pass rates. The approximation needs enough samples and reasonable <a href='appendices/b-sampling.html'>independence</a> between them. See <a href='appendices/b-sampling.html'>Appendix B</a>.",
    "also": "CLT",
    "see": [
      "standard-error",
      "confidence-interval",
      "independence",
      "sample-size"
    ]
  },
  "confidence-interval": {
    "name": "Confidence interval",
    "short": "A range around an estimate (e.g. 'score 72%, give or take 3') built so that the procedure captures the true value most of the time across repeated experiments.",
    "def": "A <strong>confidence interval</strong> turns a point estimate plus its <a href='appendices/b-sampling.html'>standard error</a> into a range: \"the measured pass rate is 72%, and the plausible range for the true pass rate is roughly 69–75%.\" The careful interpretation is about the <em>procedure</em>: a 95% interval is constructed by a recipe that brackets the truth in 95% of repeated experiments — it is not a 95% probability statement about this one interval, though the practical reading (\"values in this range are consistent with the data\") serves well. For evals, the headline use is overlap: when two models' intervals heavily overlap, the data may not distinguish them. See <a href='pages/16-error-bars.html'>Error Bars on Eval Scores</a> and <a href='appendices/b-sampling.html'>Appendix B</a>.",
    "also": "CI",
    "see": [
      "standard-error",
      "hypothesis-test",
      "central-limit-theorem"
    ]
  },
  "clustered-standard-errors": {
    "name": "Clustered standard errors",
    "short": "A standard-error correction for when eval samples come in related groups (e.g. several questions about the same document), which makes naive error bars too small.",
    "def": "Standard error formulas assume each sample contributes independent information. But eval datasets often have <strong>clusters</strong> — several questions drawn from the same document, several turns from the same conversation, several tasks from the same repository — and samples within a cluster tend to succeed or fail together. Treating them as independent overcounts your evidence and produces error bars that are too narrow, making noise look like signal. <strong>Clustered standard errors</strong> fix this by computing variability at the cluster level rather than the sample level. See <a href='pages/16-error-bars.html'>Error Bars on Eval Scores</a> and <a href='appendices/f-resampling.html'>Appendix F</a>.",
    "see": [
      "standard-error",
      "independence",
      "bootstrap"
    ]
  },
  "paired-comparison": {
    "name": "Paired comparison",
    "short": "Comparing two models on the same questions and analyzing the per-question differences — which cancels question difficulty and detects smaller gaps with the same data.",
    "def": "A <strong>paired comparison</strong> runs Model A and Model B on the identical set of samples and looks at the difference <em>per sample</em>, instead of comparing two overall averages. The point is noise cancellation: much of an eval score's variability comes from which questions happen to be hard, and since both models face exactly the same questions, that shared difficulty subtracts out of the differences. The result is a far more sensitive test — gaps that are statistically invisible when you compare unpaired averages become clearly detectable when paired. This is the single highest-leverage statistical trick in <a href='pages/17-comparing-models.html'>comparing two models</a>; mechanics in <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "also": "paired differences, paired t-test",
    "see": [
      "hypothesis-test",
      "standard-error",
      "statistical-power"
    ]
  },
  "hypothesis-test": {
    "name": "Hypothesis test",
    "short": "A formal procedure for asking whether an observed difference (e.g. between two models' scores) is too large to be plausibly explained by random noise.",
    "def": "A <strong>hypothesis test</strong> starts from a skeptical default — the <a href='appendices/c-hypothesis-testing.html'>null hypothesis</a>, usually \"there is no real difference\" — and asks how surprising the observed data would be if that default were true. If the data would be very surprising under \"no difference\" (a small <a href='appendices/c-hypothesis-testing.html'>p-value</a>), you treat the difference as real. The procedure exists because eval scores are noisy and humans are eager: without a discipline for distinguishing signal from luck, every two-point wiggle becomes a press release. See <a href='pages/17-comparing-models.html'>Comparing Two Models</a> and <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "also": "significance test",
    "see": [
      "null-hypothesis",
      "p-value",
      "statistical-power",
      "type-i-error",
      "type-ii-error",
      "paired-comparison"
    ]
  },
  "null-hypothesis": {
    "name": "Null hypothesis",
    "short": "The skeptical default assumption in a hypothesis test — typically 'these two models are actually equally good and the observed gap is just noise.'",
    "def": "The <strong>null hypothesis</strong> is the boring explanation a hypothesis test tries to rule out: no real difference, no real effect, the observed gap is sampling luck. Tests are built around it because \"prove there's a difference\" is hard but \"show the data would be very unlikely if there were none\" is tractable — you can compute exactly how much wiggle pure noise produces and check whether the observed gap exceeds it. Failing to reject the null is not proof the models are equal; it just means the data couldn't tell them apart, which is often a <a href='appendices/c-hypothesis-testing.html'>sample-size</a> problem. See <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "see": [
      "hypothesis-test",
      "p-value",
      "statistical-power"
    ]
  },
  "p-value": {
    "name": "p-value",
    "short": "The probability of seeing a difference at least as large as the one observed if there were really no difference at all. Small p-value = hard to explain as noise.",
    "def": "A <strong>p-value</strong> answers one specific question: <em>if</em> the null hypothesis were true (no real difference), how often would random noise alone produce a gap this big or bigger? A small p-value means \"noise rarely does this,\" which is evidence the difference is real. It is famously misread: a p-value is <em>not</em> the probability the null is true, and \"statistically significant\" is <em>not</em> the same as \"large\" or \"important\" — with enough samples, trivially small differences become significant. Pair it with the <a href='appendices/c-hypothesis-testing.html'>effect size</a> to judge whether a real difference also matters. See <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "see": [
      "hypothesis-test",
      "null-hypothesis",
      "effect-size",
      "type-i-error"
    ]
  },
  "statistical-power": {
    "name": "Statistical power",
    "short": "The probability your test will detect a real difference of a given size if one exists. Low power means real improvements look like 'no significant difference.'",
    "def": "<strong>Statistical power</strong> is the chance that your experiment finds an effect that is genuinely there. An underpowered eval — too few samples for the size of difference you care about — will routinely report \"no significant difference\" between models that really do differ, and worse, the differences it <em>does</em> flag will tend to be flukes that happened to be exaggerated. Power is what you buy with <a href='appendices/c-hypothesis-testing.html'>sample size</a> and with variance-reducing designs like <a href='pages/17-comparing-models.html'>paired comparisons</a>; planning it before running the eval is how you avoid spending compute on an experiment that couldn't have answered your question. See <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "also": "power",
    "see": [
      "type-ii-error",
      "sample-size",
      "effect-size",
      "paired-comparison"
    ]
  },
  "type-i-error": {
    "name": "Type I error",
    "short": "A false alarm: concluding there's a real difference when there isn't one — the noise fooled you.",
    "def": "A <strong>Type I error</strong> is rejecting the null hypothesis when it was actually true: declaring Model B better than Model A when the gap was pure sampling luck. The conventional significance threshold is essentially a cap on how often you're willing to make this mistake. The eval-specific trap is multiplicity: if you compare many models, many subsets, or re-test after every tweak, each look is another chance for a false alarm, and \"we found a significant improvement\" becomes nearly guaranteed by sheer volume of looking. See <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "also": "false positive",
    "see": [
      "type-ii-error",
      "p-value",
      "hypothesis-test"
    ]
  },
  "type-ii-error": {
    "name": "Type II error",
    "short": "A miss: failing to detect a difference that really exists — usually because the sample was too small for the size of the effect.",
    "def": "A <strong>Type II error</strong> is the opposite failure to a false alarm: the difference between models was real, but your test didn't have the resolution to see it, so you concluded \"no significant difference.\" Its probability is one minus the test's <a href='appendices/c-hypothesis-testing.html'>statistical power</a>. In eval practice this error is quietly common — small eval sets simply cannot detect modest improvements, so teams discard genuinely better prompts or models because the eval shrugged. The fix is more samples, paired designs, or honestly reporting \"inconclusive\" rather than \"no difference.\" See <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "also": "false negative",
    "see": [
      "type-i-error",
      "statistical-power",
      "sample-size"
    ]
  },
  "pass-at-k": {
    "name": "pass@k",
    "short": "The probability that at least one of k independent attempts at a task succeeds. The standard metric for code generation, where one working solution is all you need.",
    "def": "<strong>pass@k</strong> measures: given <em>k</em> tries at a problem, what's the chance at least one succeeds? It fits settings where a single success is all that matters — code generation, where you can run the tests and keep the attempt that passes. It was popularized by the HumanEval benchmark, which also introduced the now-standard <a href='appendices/d-combinatorics-pass-at-k.html'>unbiased estimator</a> for it: naively running exactly <em>k</em> samples gives a noisy, biased estimate, so instead you generate more than <em>k</em> and compute the combinatorial formula. Don't confuse it with <a href='pages/14-reliability-pass-hat-k.html'>pass^k</a>, which requires <em>all</em> k attempts to succeed and measures reliability rather than best-case ability. See <a href='pages/18-pass-at-k.html'>pass@k Done Right</a>.",
    "see": [
      "pass-hat-k",
      "unbiased-estimator",
      "binomial-distribution"
    ]
  },
  "unbiased-estimator": {
    "name": "Unbiased estimator",
    "short": "A way of estimating a quantity from data whose errors average out to zero — it's right on average, even though any single estimate may be off.",
    "def": "An estimator is any recipe for guessing a true quantity from a finite sample; it is <strong>unbiased</strong> if, averaged over many repetitions of the experiment, its guesses center exactly on the truth — no systematic lean high or low. Unbiasedness matters in evals because biased estimators corrupt comparisons in a way more data doesn't fix: the famous example is the naive pass@k computation, which systematically misestimates, versus the combinatorial estimator from the HumanEval work, which is provably unbiased. Note an unbiased estimator can still be <em>noisy</em>; bias and variance are separate problems. Derivation in <a href='appendices/d-combinatorics-pass-at-k.html'>Appendix D</a>.",
    "see": [
      "pass-at-k",
      "expectation",
      "variance"
    ]
  },
  "bootstrap": {
    "name": "Bootstrap",
    "short": "Estimating uncertainty by resampling your own data with replacement many times and seeing how much the statistic of interest varies across resamples.",
    "def": "The <strong>bootstrap</strong> answers \"how much would my number wobble if I reran the experiment?\" without rerunning anything: you draw many fake datasets by sampling your real data <em>with replacement</em> (the same sample can appear multiple times), recompute your statistic on each, and read the spread of the results as your uncertainty. Its appeal for evals is generality — it works for awkward statistics like medians, win rates, or judge-aggregated scores where no tidy <a href='appendices/b-sampling.html'>standard-error</a> formula exists, and it adapts naturally to <a href='appendices/f-resampling.html'>clustered data</a> by resampling whole clusters. The cost is compute and care with dependence structure. See <a href='appendices/f-resampling.html'>Appendix F</a>.",
    "also": "bootstrapping, resampling",
    "see": [
      "standard-error",
      "confidence-interval",
      "clustered-standard-errors"
    ]
  },
  "binomial-distribution": {
    "name": "Binomial distribution",
    "short": "The probability distribution of the number of successes in n independent yes/no trials — the natural model for 'how many of my 200 eval samples pass.'",
    "def": "The <strong>binomial distribution</strong> describes the count of successes in <em>n</em> independent pass/fail trials that each succeed with the same probability. It is the default statistical model for an eval score: if a model truly passes each task with some probability, the number of passes in your test set is binomial, and everything else — the standard error of a pass rate, why error bars shrink with more samples, the wobble you see between runs — follows from its math. The independence assumption is the part that breaks in practice (see <a href='pages/16-error-bars.html'>clustered standard errors</a>). Gentle treatment in <a href='appendices/a-probability.html'>Appendix A</a>.",
    "see": [
      "bernoulli-trial",
      "standard-error",
      "independence",
      "central-limit-theorem"
    ]
  },
  "bernoulli-trial": {
    "name": "Bernoulli trial",
    "short": "A single chance event with exactly two outcomes (success/failure) — the statistical model of one eval sample passing or failing.",
    "def": "A <strong>Bernoulli trial</strong> is the simplest random variable there is: one event, two outcomes, success with some probability <em>p</em>. It is the atom of eval statistics — \"does this sample pass?\" is a Bernoulli trial, and a benchmark score is just the average of hundreds of them. The reason the term earns a name at all is composability: stack <em>n</em> independent Bernoulli trials and you get the <a href='appendices/a-probability.html'>binomial distribution</a>, from which standard errors, confidence intervals, and pass@k all flow. See <a href='appendices/a-probability.html'>Appendix A</a>.",
    "see": [
      "binomial-distribution",
      "random-variable",
      "pass-at-k"
    ]
  },
  "spearman-correlation": {
    "name": "Spearman correlation",
    "short": "A measure of how well two rankings agree — used, e.g., to check whether an LLM judge ranks outputs in the same order humans do.",
    "def": "<strong>Spearman correlation</strong> measures agreement between two <em>rankings</em>: convert each set of scores to ranks (best, second-best, …) and ask how similar the orderings are, from perfect agreement through no relationship to perfectly reversed. It exists because raw score agreement is often the wrong question — a judge whose scores run systematically high but sort outputs in the right order is still useful for picking winners, and Spearman captures exactly that while ignoring the offset. In eval work it shows up when validating judges against humans and when comparing one leaderboard's ordering to another's. See <a href='appendices/e-agreement-metrics.html'>Appendix E</a>.",
    "also": "rank correlation, Spearman's rho",
    "see": [
      "cohens-kappa",
      "judge-alignment",
      "inter-annotator-agreement"
    ]
  },
  "cohens-kappa": {
    "name": "Cohen's kappa",
    "short": "An agreement score between two raters that subtracts out the agreement they'd get by random chance — raw percent-agreement flatters easy labeling tasks.",
    "def": "<strong>Cohen's kappa</strong> measures how often two raters (two humans, or a human and an LLM judge) give the same label, <em>corrected for chance</em>. The correction is the whole point: if most outputs pass, two raters who label nearly everything \"pass\" will show high raw agreement while contributing almost no real judgment — kappa asks how much better than that baseline coincidence the agreement actually is. It is a standard tool for checking <a href='pages/10-aligning-judges.html'>judge-human alignment</a> and inter-annotator agreement before trusting labels. See <a href='appendices/e-agreement-metrics.html'>Appendix E</a>.",
    "also": "kappa, κ",
    "see": [
      "inter-annotator-agreement",
      "judge-alignment",
      "spearman-correlation",
      "confusion-matrix"
    ]
  },
  "confusion-matrix": {
    "name": "Confusion matrix",
    "short": "A 2×2 table counting a classifier's (or judge's) hits and misses: true positives, false positives, true negatives, false negatives.",
    "def": "A <strong>confusion matrix</strong> tabulates predictions against truth: how many real positives were caught (true positives), how many were missed (false negatives), how many negatives were correctly left alone (true negatives), and how many were falsely flagged (false positives). It exists because a single accuracy number hides which <em>kind</em> of mistake dominates — and the two kinds usually have very different costs. In eval work the \"classifier\" is often an LLM judge being checked against human labels: the matrix shows whether it tends to wave bad outputs through or fail good ones, which a headline agreement rate can't. Nearly every metric in <a href='appendices/e-agreement-metrics.html'>Appendix E</a> — precision, recall, TPR, TNR, F1 — is read off this table.",
    "see": [
      "precision",
      "recall",
      "true-positive-rate",
      "true-negative-rate",
      "f1-score",
      "cohens-kappa"
    ]
  },
  "precision": {
    "name": "Precision",
    "short": "Of everything the system flagged as positive, what fraction actually was? High precision means few false alarms.",
    "def": "<strong>Precision</strong> answers: when the classifier (or judge, or guardrail) says \"positive,\" how often is it right? It is computed from the <a href='appendices/e-agreement-metrics.html'>confusion matrix</a> as true positives divided by all predicted positives. It matters whenever acting on a flag is costly — a hallucination detector with low precision drowns reviewers in false alarms until they stop reading it. Precision says nothing about what was <em>missed</em>; that is <a href='appendices/e-agreement-metrics.html'>recall</a>'s job, and the two trade off against each other, which is why they are always reported together. See <a href='appendices/e-agreement-metrics.html'>Appendix E</a>.",
    "see": [
      "recall",
      "f1-score",
      "confusion-matrix"
    ]
  },
  "recall": {
    "name": "Recall",
    "short": "Of all the actual positives out there, what fraction did the system catch? High recall means few misses.",
    "def": "<strong>Recall</strong> answers: of everything that truly was positive, how much did the classifier find? From the <a href='appendices/e-agreement-metrics.html'>confusion matrix</a>: true positives divided by all actual positives. It is the metric to watch when misses are expensive — a safety guardrail with low recall lets real harms through no matter how clean its alerts look. Recall is trivially gamed in isolation (flag everything and you catch everything), which is exactly why it is paired with <a href='appendices/e-agreement-metrics.html'>precision</a>; the same quantity under the name <em>true positive rate</em> or <em>sensitivity</em> appears in judge-alignment work. See <a href='appendices/e-agreement-metrics.html'>Appendix E</a>.",
    "also": "sensitivity, true positive rate (same quantity)",
    "see": [
      "precision",
      "true-positive-rate",
      "f1-score",
      "confusion-matrix"
    ]
  },
  "true-positive-rate": {
    "name": "True positive rate (TPR)",
    "short": "The fraction of actual positives correctly identified — same quantity as recall. In judge validation: of the outputs a human passed, what share did the judge also pass?",
    "def": "The <strong>true positive rate</strong> (TPR) is the proportion of genuine positives the system correctly labels positive — mathematically identical to <a href='appendices/e-agreement-metrics.html'>recall</a>, but the TPR/TNR framing is the one used when validating <a href='pages/10-aligning-judges.html'>LLM judges against human experts</a>: treating the human label as truth, TPR asks \"of the outputs the human passed, what fraction did the judge pass too?\" Reporting TPR and <a href='appendices/e-agreement-metrics.html'>TNR</a> as a pair reveals a judge's directional lean — lenient judges show high TPR but low TNR — which a single overall agreement number conceals. See <a href='appendices/e-agreement-metrics.html'>Appendix E</a>.",
    "also": "TPR, sensitivity",
    "see": [
      "true-negative-rate",
      "recall",
      "judge-alignment",
      "confusion-matrix"
    ]
  },
  "true-negative-rate": {
    "name": "True negative rate (TNR)",
    "short": "The fraction of actual negatives correctly identified. In judge validation: of the outputs a human failed, what share did the judge also fail?",
    "def": "The <strong>true negative rate</strong> (TNR) is the proportion of genuine negatives the system correctly labels negative. In <a href='pages/10-aligning-judges.html'>judge validation</a> it is usually the harder, more telling half of the TPR/TNR pair: most LLM judges lean lenient, so they sail through the \"agree on good outputs\" test (high TPR) while waving through outputs the human expert rejected (low TNR). Since catching bad outputs is typically the whole reason the judge exists, a low TNR can disqualify a judge that looks fine on overall agreement. See <a href='appendices/e-agreement-metrics.html'>Appendix E</a>.",
    "also": "TNR, specificity",
    "see": [
      "true-positive-rate",
      "confusion-matrix",
      "judge-alignment"
    ]
  },
  "f1-score": {
    "name": "F1 score",
    "short": "A single number combining precision and recall (their harmonic mean), high only when both are high — a convenient but lossy summary.",
    "def": "The <strong>F1 score</strong> compresses <a href='appendices/e-agreement-metrics.html'>precision</a> and <a href='appendices/e-agreement-metrics.html'>recall</a> into one number using the harmonic mean, which punishes imbalance: a system great at one and poor at the other scores closer to its weak side than a simple average would. It exists because leaderboards and dashboards want one number per system. Use it knowing what it hides — F1 weighs false alarms and misses equally, and in most real applications they are not equally costly, so when the trade-off matters, report precision and recall separately. See <a href='appendices/e-agreement-metrics.html'>Appendix E</a>.",
    "see": [
      "precision",
      "recall",
      "confusion-matrix"
    ]
  },
  "sample-size": {
    "name": "Sample size",
    "short": "The number of test cases in your eval. It directly controls how small a real difference you can reliably detect — and the cost of more resolution grows fast.",
    "def": "<strong>Sample size</strong> — the number of eval cases, usually written <em>n</em> — is the main lever on statistical resolution: error bars shrink proportionally to the <em>square root</em> of <em>n</em>, so quadrupling your dataset only halves the noise. This square-root law explains a lot of eval practice: why tiny eval sets can only detect huge differences, why detecting a small improvement needs a disproportionately large set, and why <a href='pages/17-comparing-models.html'>paired comparisons</a> (which cancel noise instead of out-massing it) are so valuable. Planning <em>n</em> from the size of difference you care about, rather than from whatever data was lying around, is the discipline called power analysis. See <a href='appendices/b-sampling.html'>Appendix B</a> and <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "also": "n",
    "see": [
      "standard-error",
      "statistical-power",
      "effect-size"
    ]
  },
  "effect-size": {
    "name": "Effect size",
    "short": "How big a difference actually is (e.g. five percentage points), as opposed to whether it's statistically detectable. Significance without size can be meaningless.",
    "def": "<strong>Effect size</strong> is the magnitude of a difference in real terms — Model B passes five percentage points more tasks than Model A — kept deliberately separate from whether the difference is <em>statistically significant</em>. The separation matters because significance is a function of both size and <a href='appendices/c-hypothesis-testing.html'>sample size</a>: with enough samples, a difference too small to matter to any user becomes \"significant,\" and with too few, a difference big enough to change your model choice doesn't register. Good eval reporting gives both: the size of the gap, and the uncertainty around it. See <a href='appendices/c-hypothesis-testing.html'>Appendix C</a>.",
    "see": [
      "p-value",
      "sample-size",
      "statistical-power",
      "confidence-interval"
    ]
  },
  "independence": {
    "name": "Independence",
    "short": "The assumption that one sample's outcome tells you nothing about another's. Most eval statistics quietly depend on it, and grouped or related samples violate it.",
    "def": "Two random outcomes are <strong>independent</strong> if knowing one tells you nothing about the other. Nearly every formula in basic eval statistics — standard errors, confidence intervals, the binomial model of a pass rate — assumes your samples are independent, and the assumption fails quietly: ten questions about the same document, multiple turns from one conversation, or several tasks in one repository tend to succeed or fail together. Correlated samples carry less information than their count suggests, so naive error bars come out too narrow and noise masquerades as signal. The fixes are <a href='pages/16-error-bars.html'>clustered standard errors</a> or cluster-aware resampling. See <a href='appendices/b-sampling.html'>Appendix B</a>.",
    "also": "statistical independence, i.i.d. assumption",
    "see": [
      "clustered-standard-errors",
      "binomial-distribution",
      "central-limit-theorem"
    ]
  },
  "contamination": {
    "name": "Contamination",
    "short": "When a benchmark's test data ended up in a model's training data, so the model may have memorized answers — and the score measures memory, not ability.",
    "def": "<strong>Data contamination</strong> happens when the questions (or answers) of a benchmark appear in the data a model was trained on. LLMs train on enormous web scrapes, and popular benchmarks are all over the web — in papers, blog posts, GitHub repos, tutorial sites — so contamination is the default condition for any public test set, not an exotic accident. A contaminated score is invalid in a specific way: it measures the model's ability to recall this particular test, which says nothing about performance on new problems. Detecting it (fresh parallel questions, <a href='pages/21-contamination.html'>n-gram overlap, log-likelihood probes</a>) and defending against it (<a href='pages/22-contamination-defenses.html'>live benchmarks, private holdouts, canary strings</a>) are whole subfields.",
    "also": "data contamination, benchmark contamination, train-test contamination",
    "see": [
      "memorization",
      "data-leakage",
      "training-cutoff",
      "live-benchmark",
      "private-holdout",
      "n-gram-overlap"
    ]
  },
  "memorization": {
    "name": "Memorization",
    "short": "A model reproducing specific content it saw during training (like a benchmark answer) rather than solving the problem — the mechanism behind contamination.",
    "def": "<strong>Memorization</strong> is when a model's output comes from recalling training data rather than from generalizable skill. LLMs genuinely do store and reproduce specific sequences they trained on, especially ones repeated often in the data — and famous benchmark problems are repeated very often. This is the mechanism that makes <a href='pages/21-contamination.html'>contamination</a> ruinous: a model that memorized a benchmark's answers performs like an expert on those exact items and like its true self everywhere else. Telltale signs include acing a famous test while flunking lightly reworded versions of the same problems.",
    "see": [
      "contamination",
      "log-likelihood",
      "n-gram-overlap",
      "overfitting"
    ]
  },
  "construct-validity": {
    "name": "Construct validity",
    "short": "Whether a test actually measures the ability it claims to measure — e.g. whether a coding benchmark score really reflects coding skill.",
    "def": "<strong>Construct validity</strong> asks: does this measurement measure the thing it claims to? The \"construct\" is the abstract ability you care about — coding skill, factual accuracy, agentic competence — and the benchmark is just a proxy for it, built from specific tasks, graders, and assumptions. Validity breaks whenever the proxy can be satisfied without the ability (weak tests that pass wrong solutions, answers leaked in the prompt, memorized solutions) or the ability fails the proxy (formatting trips up a capable model). The term comes from psychometrics, the field that has spent a century learning how hard it is to measure abilities through tests. It is the central concept of <a href='pages/20-validity.html'>What Does a Score Mean?</a>.",
    "see": [
      "internal-validity",
      "external-validity",
      "solution-leakage",
      "contamination"
    ]
  },
  "internal-validity": {
    "name": "Internal validity",
    "short": "Whether an eval's results are correct on their own terms — the grading is right, the harness isn't buggy, the comparison is apples-to-apples.",
    "def": "<strong>Internal validity</strong> is about the integrity of the measurement itself: were the answers graded correctly, did the harness run what you think it ran, were both models given the same inputs under the same conditions? An eval can fail internally in mundane ways — a parsing bug that marks correct answers wrong, tests too weak to catch incorrect solutions, different prompt formats for different models — and these errors corrupt the score before any deeper question of meaning arises. Internal validity is the precondition for <a href='pages/20-validity.html'>external validity</a>: a measurement must first be right before it can generalize.",
    "see": [
      "external-validity",
      "construct-validity",
      "data-leakage"
    ]
  },
  "external-validity": {
    "name": "External validity",
    "short": "Whether eval results generalize beyond the test itself — does scoring well on the benchmark predict performing well on real tasks in the wild?",
    "def": "<strong>External validity</strong> asks whether results transfer: a model aces a benchmark of self-contained Python puzzles, but does that predict anything about its performance on your team's sprawling legacy codebase? Every benchmark makes simplifications — curated tasks, clean environments, unambiguous grading — and external validity is the question of how much those simplifications cost when you extrapolate to messier reality. It is why high benchmark scores routinely coexist with disappointing real-world performance, and why <a href='pages/04-error-analysis.html'>evals built from your own product's failures</a> beat generic benchmarks for product decisions. See <a href='pages/20-validity.html'>What Does a Score Mean?</a>.",
    "also": "generalizability",
    "see": [
      "internal-validity",
      "construct-validity",
      "saturation"
    ]
  },
  "data-leakage": {
    "name": "Data leakage",
    "short": "Any path by which information a system shouldn't have at test time reaches it anyway — training on test data, answers visible in inputs, hints in the setup.",
    "def": "<strong>Data leakage</strong> is the umbrella term for information sneaking across a boundary it shouldn't cross, inflating measured performance. In LLM evals it shows up in several forms: test data in the training set (<a href='pages/21-contamination.html'>contamination</a>), answers embedded in the task input itself (<a href='pages/12-swe-bench-case-study.html'>solution leakage</a>), future information available to an agent that wouldn't exist in the real scenario, or dev-set knowledge bleeding into a supposedly held-out test. The common thread: the system passes the test using a side channel rather than the ability being measured, so the score overstates what it will do when the channel is absent.",
    "also": "leakage",
    "see": [
      "contamination",
      "solution-leakage",
      "holdout-set",
      "internal-validity"
    ]
  },
  "solution-leakage": {
    "name": "Solution leakage",
    "short": "When a benchmark task's input accidentally contains its own answer — e.g. a GitHub issue that spells out exactly what code fix to make.",
    "def": "<strong>Solution leakage</strong> is contamination inside a single task: the answer, or a near-complete recipe for it, sits in the input the model is given. The canonical example comes from SWE-bench-style benchmarks built on real GitHub issues — some issue reports describe the exact fix, sometimes including the code, so \"solving\" the task means transcription rather than software engineering. It differs from training-data <a href='pages/21-contamination.html'>contamination</a> in that no memorization is involved; the task itself is broken. It is one of the core reasons benchmark instances need manual auditing before their scores are trusted. See <a href='pages/12-swe-bench-case-study.html'>Case Study: SWE-bench</a>.",
    "see": [
      "data-leakage",
      "contamination",
      "construct-validity"
    ]
  },
  "canary-string": {
    "name": "Canary string",
    "short": "A unique marker token embedded in benchmark files so anyone can later check whether a model trained on them — if the model knows the string, the data leaked in.",
    "def": "A <strong>canary string</strong> is a long, globally unique random identifier (a GUID) embedded in a benchmark's files, a convention popularized by BIG-bench. It serves two purposes: training-data pipelines can filter out any document containing the canary, keeping the benchmark out of training sets; and after the fact, anyone can probe a model for knowledge of the string — since it appears nowhere else on earth, recognition is proof the benchmark text entered training. Like its namesake in the coal mine, it detects the problem rather than preventing it: filtering only works if data pipelines actually look for it. See <a href='pages/22-contamination-defenses.html'>Defenses: Live Sets, Private Splits, Canaries</a>.",
    "also": "canary GUID",
    "see": [
      "contamination",
      "private-holdout",
      "live-benchmark"
    ]
  },
  "private-holdout": {
    "name": "Private holdout",
    "short": "A benchmark's secret test set, never published, so models can't have trained on it — scoring requires submitting to the benchmark's owners.",
    "def": "A <strong>private holdout</strong> defends a benchmark against contamination by simply never publishing part of the test data: a public split lets people develop and self-evaluate, while official scores come from a hidden split that only the benchmark maintainers can run (ARC-AGI is a well-known example of this design). What can't be downloaded can't be trained on or tuned against. The costs are real, though: scoring depends on the maintainers' availability and honesty, the community can't audit hidden tasks for errors, and every official evaluation risks leaking a bit — the model provider sees the tasks even if the public doesn't. See <a href='pages/22-contamination-defenses.html'>Defenses: Live Sets, Private Splits, Canaries</a>.",
    "also": "private test set, hidden test set",
    "see": [
      "holdout-set",
      "canary-string",
      "live-benchmark",
      "contamination"
    ]
  },
  "live-benchmark": {
    "name": "Live benchmark",
    "short": "A benchmark that continually adds fresh test questions created after models' training cutoffs, so the current questions can't be in any model's training data.",
    "def": "A <strong>live benchmark</strong> fights contamination with freshness: instead of a fixed test set that inevitably leaks onto the web, it regularly mints new questions — from recent competitive-programming contests, recent news, freshly generated puzzles — dated after every current model's <a href='pages/21-contamination.html'>training cutoff</a> (LiveBench and LiveCodeBench are the namesake examples). A question that didn't exist when the training data was collected cannot have been memorized. The trade-offs: scores from different time windows aren't directly comparable, question quality must be maintained forever rather than audited once, and the approach only suits domains with a steady supply of fresh material. See <a href='pages/22-contamination-defenses.html'>Defenses: Live Sets, Private Splits, Canaries</a>.",
    "also": "rolling benchmark, refreshing benchmark",
    "see": [
      "training-cutoff",
      "contamination",
      "private-holdout",
      "saturation"
    ]
  },
  "training-cutoff": {
    "name": "Training cutoff",
    "short": "The date after which a model saw no training data. Content created after the cutoff can't be memorized — the dividing line live benchmarks exploit.",
    "def": "A model's <strong>training cutoff</strong> is the freshness boundary of its knowledge: the latest date represented in its training data. For evaluation it doubles as a contamination dividing line — any benchmark question created and published after a model's cutoff is provably absent from its training data, which is exactly the property <a href='pages/22-contamination-defenses.html'>live benchmarks</a> are built on. Two caveats keep it from being a clean guarantee: vendors' stated cutoffs are approximate and data collection isn't a single sharp date, and models are often updated after release through fine-tuning that can introduce newer data.",
    "also": "knowledge cutoff",
    "see": [
      "live-benchmark",
      "contamination",
      "memorization"
    ]
  },
  "n-gram-overlap": {
    "name": "n-gram overlap",
    "short": "A contamination check that searches for benchmark text appearing word-for-word (in chunks of n consecutive words) inside a training corpus.",
    "def": "An <strong>n-gram</strong> is just a run of <em>n</em> consecutive words or tokens; <strong>n-gram overlap</strong> checks for contamination by scanning a training corpus for chunks that exactly match chunks of benchmark text. Long verbatim matches are strong evidence the benchmark leaked into training. It is the workhorse first-pass check because it's cheap and mechanical — but it only catches <em>verbatim</em> copying: paraphrased, translated, or reformatted versions of a test question slip through entirely, and running the check at all requires access to the training corpus, which outsiders rarely have. That is why it's complemented by behavioral probes like <a href='pages/21-contamination.html'>log-likelihood</a> tests. See <a href='pages/21-contamination.html'>Data Contamination</a>.",
    "see": [
      "contamination",
      "log-likelihood",
      "memorization"
    ]
  },
  "log-likelihood": {
    "name": "Log-likelihood",
    "short": "A score for how probable a model finds a given piece of text. Suspiciously high probability on benchmark text suggests the model saw it in training.",
    "def": "A language model can assign a probability to any text — how likely it would be to produce exactly those tokens — and the <strong>log-likelihood</strong> is that probability on a logarithmic scale (logs turn the product of many tiny per-token probabilities into a manageable sum). Beyond its everyday roles in how models are trained and how some multiple-choice evals are scored, it serves as a contamination probe: text a model trained on tends to get conspicuously higher likelihood than fresh text of the same kind, so a model that finds one benchmark's exact phrasing unusually probable — especially compared to reworded versions — has likely seen it before. See <a href='pages/21-contamination.html'>Data Contamination</a>.",
    "also": "log-probability, logprob",
    "see": [
      "memorization",
      "n-gram-overlap",
      "contamination"
    ]
  },
  "saturation": {
    "name": "Saturation",
    "short": "When top models all score near a benchmark's ceiling, leaving no headroom — the benchmark can no longer distinguish good models from better ones.",
    "def": "A benchmark <strong>saturates</strong> when frontier models approach its maximum score: once everyone is bunched near the ceiling, remaining differences are mostly noise, label errors, and ambiguous items rather than capability gaps, and the benchmark stops carrying information. Saturation is the natural life cycle of every successful benchmark — models improve, and the field's optimization pressure points straight at whatever is being measured — and it is frequently entangled with <a href='pages/21-contamination.html'>contamination</a>, since an aging public benchmark has had years to leak into training data. A saturated benchmark isn't \"solved\" so much as retired: it gets replaced by a harder successor. See <a href='pages/20-validity.html'>What Does a Score Mean?</a>.",
    "also": "benchmark saturation",
    "see": [
      "contamination",
      "live-benchmark",
      "external-validity",
      "overfitting"
    ]
  },
  "tracing": {
    "name": "Tracing",
    "short": "Recording the full execution of an LLM application — every model call, tool call, and intermediate step with inputs, outputs, timing, and cost — for inspection and evaluation.",
    "def": "<strong>Tracing</strong> instruments an LLM application to capture everything that happened during a request: each model call's exact prompt and response, each tool invocation, each retrieval, with timings and token costs, organized into a tree of <a href='pages/26-observability.html'>spans</a>. It exists because LLM systems fail in ways logs of inputs and outputs alone can't explain — the bug is usually in an intermediate step (a mangled prompt, a bad retrieval, a misparsed tool result) that only the full trace reveals. Traces are also the raw material of the eval flywheel: <a href='pages/04-error-analysis.html'>error analysis</a> reads them, and production traces become test cases. The term and tooling are borrowed from distributed-systems observability.",
    "see": [
      "span",
      "observability",
      "trajectory",
      "error-analysis"
    ]
  },
  "span": {
    "name": "Span",
    "short": "One timed operation inside a trace — a single model call, tool call, or retrieval step, with its inputs, outputs, duration, and metadata.",
    "def": "A <strong>span</strong> is the unit a trace is built from: one named, timed operation — \"call the model,\" \"search the vector store,\" \"run this tool\" — recording its inputs, outputs, start and end times, and metadata like token counts. Spans nest: a request's root span contains child spans for each step, forming a tree that shows both what happened and what invoked what. The structure (inherited from distributed-tracing standards like OpenTelemetry) is what lets observability tools answer pointed questions — which step burned the latency, what exact prompt did the third model call receive — instead of presenting one undifferentiated blob. See <a href='pages/26-observability.html'>Tracing and Online Evaluation</a>.",
    "see": [
      "tracing",
      "observability"
    ]
  },
  "observability": {
    "name": "Observability",
    "short": "The practice (and tooling) of being able to see what your LLM application is doing in production — traces, scores, costs, latencies — so you can find and fix failures.",
    "def": "<strong>Observability</strong> is the ability to answer \"what is my system actually doing, and why did this output happen?\" from recorded evidence — traces, metrics, logs, and scores — rather than guesswork. For LLM applications it earns special attention because the systems are nondeterministic and fail silently: there is no stack trace for a confidently wrong answer, so without recorded traces and <a href='pages/26-observability.html'>online evaluation</a> scores you simply don't know how often production is failing or where. Platforms in this space (Langfuse, Braintrust, and others) combine trace capture with scoring and dataset curation, closing the loop between production behavior and offline evals. See <a href='pages/26-observability.html'>Tracing and Online Evaluation</a>.",
    "also": "LLM observability",
    "see": [
      "tracing",
      "span",
      "online-eval",
      "experiment"
    ]
  },
  "assertion": {
    "name": "Assertion",
    "short": "A simple programmatic check applied to an LLM output — contains this string, valid JSON, under this length, passes this regex — the cheapest kind of grader.",
    "def": "An <strong>assertion</strong> is a deterministic, code-based check on an output: does it contain the required phrase, parse as JSON, match a regex, stay under a length limit, avoid a forbidden term? Assertions are the cheapest and most trustworthy graders — instant, free, perfectly consistent — and tools like promptfoo organize entire eval suites around lists of them. Their limit is that they check <em>surface properties</em>: an answer can pass every assertion and still be wrong, unhelpful, or fabricated. The craft is decomposing quality into whatever <em>is</em> assertable and reserving expensive graders (humans, <a href='pages/03-types-of-evaluators.html'>LLM judges</a>) for what remains. See <a href='pages/25-tooling-survey.html'>The Tooling Landscape</a>.",
    "see": [
      "grader",
      "scorer",
      "llm-as-judge"
    ]
  },
  "solver": {
    "name": "Solver",
    "short": "In the Inspect harness, the component that produces a candidate answer for a task — anything from a single model call to a full multi-step agent.",
    "def": "<strong>Solver</strong> is the term the Inspect eval framework (from the UK AI Safety Institute) uses for the \"attempt the task\" half of an eval: the pluggable component that takes a task's input and produces an answer, whether that means one prompt-and-respond call, a chain-of-thought recipe, or a tool-using agent loop running in a <a href='pages/24-inspect.html'>sandbox</a>. Separating the solver from the <a href='pages/24-inspect.html'>scorer</a> (which grades the result) is the framework's key design move: you can swap solving strategies while holding the grading fixed, or vice versa, and know exactly which change moved the score. See <a href='pages/24-inspect.html'>Inspect: A Harness in Depth</a>.",
    "see": [
      "scorer",
      "harness",
      "epoch",
      "sandbox"
    ]
  },
  "scorer": {
    "name": "Scorer",
    "short": "The component of an eval harness that grades a candidate answer — by exact match, code checks, or a model-graded judgment — producing the per-sample result.",
    "def": "A <strong>scorer</strong> is the grading half of an eval harness: it takes the output a <a href='pages/24-inspect.html'>solver</a> produced (plus the target answer, if there is one) and emits a verdict — pass/fail, a numeric score, sometimes an explanation. Scorers range from trivial (exact match, <code>includes</code>) through programmatic (run the unit tests) to model-graded (an <a href='pages/08-llm-as-judge.html'>LLM judge</a> applies a rubric). The term is Inspect's, but the role exists in every framework, and it is where an eval's validity concentrates: per-sample scores get aggregated into the metric, so a systematically wrong scorer corrupts everything downstream no matter how good the dataset is. See <a href='pages/24-inspect.html'>Inspect: A Harness in Depth</a> and <a href='pages/06-validating-the-grader.html'>Validating the Grader</a>.",
    "see": [
      "solver",
      "grader",
      "assertion",
      "metric"
    ]
  },
  "epoch": {
    "name": "Epoch",
    "short": "In eval harness terminology (Inspect), one of several repeated runs of the same sample — used to average out the randomness in model outputs.",
    "def": "In Inspect's terminology, an <strong>epoch</strong> is one complete pass over the eval's samples; running multiple epochs means attempting every sample several times. The reason is nondeterminism: a model generating with nonzero <a href='pages/24-inspect.html'>temperature</a> can pass a sample on one try and fail it on the next, so a single attempt per sample tangles the model's ability up with per-run luck. Repeated trials let the harness both report a steadier average and compute reliability metrics — multiple attempts per task are exactly what <a href='pages/18-pass-at-k.html'>pass@k</a> and <a href='pages/14-reliability-pass-hat-k.html'>pass^k</a> are computed from. (Unrelated to the ML-training sense of \"epoch,\" one pass over training data.)",
    "see": [
      "pass-at-k",
      "pass-hat-k",
      "solver",
      "temperature"
    ]
  },
  "experiment": {
    "name": "Experiment",
    "short": "In eval platforms (Braintrust usage), one recorded eval run — a system version scored against a dataset — stored so it can be diffed against other runs.",
    "def": "In eval-platform terminology (notably Braintrust's), an <strong>experiment</strong> is one tracked eval run: a particular version of your system (prompt, model, scaffold) executed against a dataset with scorers, with every output and score stored. The point is comparison over time — because experiments are persisted with their configuration, the platform can diff any two: which samples improved after the prompt change, which regressed, how the aggregate moved. This turns evaluation from a one-off score into <a href='pages/07-evals-in-the-lifecycle.html'>regression testing for model behavior</a>, where every proposed change gets an experiment and a diff before it ships. See <a href='pages/26-observability.html'>Tracing and Online Evaluation</a>.",
    "also": "eval run",
    "see": [
      "regression-testing",
      "observability",
      "eval-driven-development"
    ]
  },
  "faithfulness": {
    "name": "Faithfulness",
    "short": "A RAG metric: is every claim in the generated answer actually supported by the retrieved documents? Low faithfulness means the model added things its sources don't say.",
    "def": "<strong>Faithfulness</strong> — one of the four core RAG metrics popularized by the Ragas framework — checks whether the generated answer sticks to its sources: each claim in the answer is extracted and verified against the retrieved context, and claims the context doesn't support count against the score. It targets the failure RAG exists to prevent: the model ignoring (or embellishing beyond) the documents it was handed and generating from its own parametric memory instead. Note what it doesn't check — an answer can be perfectly faithful to retrieved documents that were themselves wrong or irrelevant, which is why it's paired with the retrieval-side metrics <a href='pages/25-tooling-survey.html'>context precision and context recall</a>.",
    "also": "groundedness",
    "see": [
      "answer-relevancy",
      "context-precision",
      "context-recall",
      "rag",
      "hallucination"
    ]
  },
  "answer-relevancy": {
    "name": "Answer relevancy",
    "short": "A RAG metric: does the generated answer actually address the question that was asked, rather than wandering off or answering something adjacent?",
    "def": "<strong>Answer relevancy</strong> — another of the four Ragas RAG metrics — measures whether the answer is on-topic for the question: complete answers to the question asked score high; evasive, rambling, or tangential responses score low. A common implementation inverts the problem: ask a model what question this answer would be answering, and compare that reconstruction to the question actually asked. It complements <a href='pages/25-tooling-survey.html'>faithfulness</a>, which alone is gameable — an answer faithfully grounded in the documents can still fail to address what the user wanted, and relevancy is the metric that catches it. See <a href='pages/25-tooling-survey.html'>The Tooling Landscape</a>.",
    "also": "answer relevance",
    "see": [
      "faithfulness",
      "context-precision",
      "context-recall",
      "rag"
    ]
  },
  "context-precision": {
    "name": "Context precision",
    "short": "A RAG metric for the retrieval step: of the documents retrieved, how many were actually relevant to the question — and were the relevant ones ranked on top?",
    "def": "<strong>Context precision</strong> evaluates the retrieval half of a RAG system: of the chunks the retriever fetched, what share are actually relevant to the question, with extra weight on the relevant ones being ranked first (since models attend most reliably to what appears early in context)? It is <a href='appendices/e-agreement-metrics.html'>precision</a> applied to retrieved documents. Low context precision means stuffing the prompt with off-topic material — which wastes the context window and actively invites the generator to ground its answer in the wrong text. Its partner metric, <a href='pages/25-tooling-survey.html'>context recall</a>, asks the opposite question: did anything necessary get missed? Both come from the Ragas family of RAG metrics.",
    "see": [
      "context-recall",
      "precision",
      "faithfulness",
      "rag"
    ]
  },
  "context-recall": {
    "name": "Context recall",
    "short": "A RAG metric for the retrieval step: did the retrieved documents contain all the information needed to answer correctly, or did retrieval miss something essential?",
    "def": "<strong>Context recall</strong> asks whether retrieval found <em>everything needed</em>: taking a reference answer as the standard, it checks how much of that answer's content is actually supported by the retrieved chunks. It is <a href='appendices/e-agreement-metrics.html'>recall</a> applied to retrieval, and it catches the silent RAG failure that generation-side metrics can't see: if the key document was never fetched, even a perfectly <a href='pages/25-tooling-survey.html'>faithful</a> generator must answer incompletely or refuse — and the trace looks fine unless you check what retrieval missed. Unlike its partner context precision, it typically needs a <a href='pages/03-types-of-evaluators.html'>ground-truth</a> reference answer to grade against. Part of the Ragas family of RAG metrics.",
    "see": [
      "context-precision",
      "recall",
      "faithfulness",
      "answer-relevancy",
      "rag"
    ]
  },
  "neuron": {
    "name": "Neuron",
    "short": "A single unit inside one layer of a neural network; for every input token it produces one number, its activation.",
    "def": "In a transformer language model, a <strong>neuron</strong> is one unit of an MLP (feed-forward) layer. For every token the model processes, the neuron outputs a single number, its <a href='glossary.html#activation'>activation</a>; most neurons sit near zero most of the time and rise on particular tokens or contexts. GPT-2 XL has 307,200 of them. Interpretability work tries to say in words when a neuron fires (a <a href='glossary.html#neuron-explanation'>neuron explanation</a>), and <a href='pages/27-scoring-an-explanation.html'>Module 8</a> is about how such a statement is tested. Many neurons respond to several unrelated things at once (<a href='glossary.html#polysemanticity'>polysemanticity</a>), which is why some work explains learned directions called features instead.",
    "see": [
      "activation",
      "neuron-explanation",
      "polysemanticity",
      "sae-feature"
    ]
  },
  "activation": {
    "name": "Activation",
    "short": "The number a neuron (or feature) outputs for one token; the quantity an explanation of that neuron is supposed to predict.",
    "def": "An <strong>activation</strong> is the value a <a href='glossary.html#neuron'>neuron</a> or feature produces on one token of one text. A neuron's activations across a text are the raw data of interpretability: an explanation such as 'fires on legal citations' is a prediction that activations will be high on citation tokens and near zero elsewhere. In <a href='pages/27-scoring-an-explanation.html'>simulation scoring</a>, activations are normalized to a 0–10 integer scale (the neuron's largest value ever observed maps to 10, negatives to 0) so that a language model can read and predict them.",
    "see": [
      "neuron",
      "simulation-scoring",
      "max-activating-examples"
    ]
  },
  "neuron-explanation": {
    "name": "Neuron explanation",
    "short": "A natural-language description of when a neuron or feature fires; treated in this course as a hypothesis that predicts activations on unseen text.",
    "def": "A <strong>neuron explanation</strong> is a sentence like 'fires on four-digit years' that claims to describe a <a href='glossary.html#neuron'>neuron</a>'s behavior. Usually it is written from the neuron's <a href='glossary.html#max-activating-examples'>max-activating examples</a>, which makes it a description of a handful of texts. Read as a claim about the neuron it is a hypothesis: it predicts an <a href='glossary.html#activation'>activation</a> for every token of every text, and it is validated the way a <a href='pages/06-validating-the-grader.html'>grader</a> is, on held-out data against ground truth. The two tests the course covers are <a href='glossary.html#simulation-scoring'>simulation scoring</a> (observational) and <a href='glossary.html#intervention'>intervention</a> (causal); see <a href='pages/27-scoring-an-explanation.html'>page 27</a>.",
    "also": "feature explanation",
    "see": [
      "simulation-scoring",
      "max-activating-examples",
      "control-neuron",
      "intervention"
    ]
  },
  "simulation-scoring": {
    "name": "Simulation scoring",
    "short": "Testing a neuron explanation by having a model predict the neuron's activations on held-out text from the explanation alone, then correlating the predictions with the real activations.",
    "def": "<strong>Simulation scoring</strong> (Bills et al. 2023) is the standard held-out test for a <a href='glossary.html#neuron-explanation'>neuron explanation</a>. An explainer model writes the explanation from example activations; a separate simulator model, shown only the explanation and new text excerpts, predicts an <a href='glossary.html#activation'>activation</a> for every token; the score is the correlation between the simulated and real activations across those tokens, 1 for a perfect match and about 0 for an unrelated explanation. The score depends on the scoring set: 'top-and-random' mixes top-activating and random excerpts and is nearly blind to false positives, so a broad explanation can score well. <a href='pages/27-scoring-an-explanation.html'>Page 27</a> gives the method and its numbers; <a href='pages/28-controls-for-interpretability-claims.html'>page 28</a> the controls it needs.",
    "also": "explanation score, automated interpretability score",
    "see": [
      "neuron-explanation",
      "control-neuron",
      "spearman-correlation",
      "precision",
      "recall"
    ]
  },
  "max-activating-examples": {
    "name": "Max-activating examples",
    "short": "The texts on which a neuron fires hardest; the usual raw material for writing an explanation, and a biased sample of what the neuron does.",
    "def": "A neuron's <strong>max-activating examples</strong> (top examples, top dataset examples) are the excerpts, out of a large corpus, that produce its largest <a href='glossary.html#activation'>activations</a>. Explanations are usually written by reading them, which is why they are a hazard: they show the neuron at its most certain and hide the long middle of its range, where a unit that looks single-purpose at the top may respond to other things. Scoring an explanation on the same examples that produced it is a training-set score. Anthropic's 'Towards Monosemanticity' sampled across eleven activation intervals instead; see <a href='pages/28-controls-for-interpretability-claims.html'>page 28</a>.",
    "also": "top examples, top dataset examples",
    "see": [
      "neuron-explanation",
      "polysemanticity",
      "holdout-set",
      "overfitting"
    ]
  },
  "polysemanticity": {
    "name": "Polysemanticity",
    "short": "A neuron or unit responding to several unrelated things; the main reason one-sentence explanations of neurons score poorly, and something top examples alone cannot reveal.",
    "def": "A unit is <strong>polysemantic</strong> when it fires on several unrelated kinds of input (the classic example is a vision neuron for both cat faces and car fronts). Bills et al. 2023 found the typical GPT-2 XL neuron 'appeared quite polysemantic', and Huang et al. 2023 measured the same thing as recall failures, neurons firing on strings their explanation did not cover. Because the secondary jobs rarely produce a neuron's very largest activations, an explanation written from <a href='glossary.html#max-activating-examples'>max-activating examples</a> cannot detect them; you have to sample across the activation range. Whether polysemanticity is pervasive in modern models is the subject of the 2026 dispute in <a href='pages/29-case-study-demonstrated-explanation.html'>page 29</a>. <a href='glossary.html#sparse-autoencoder'>Sparse autoencoders</a> are one proposed remedy.",
    "also": "polysemantic neuron, superposition (related)",
    "see": [
      "neuron",
      "max-activating-examples",
      "sae-feature",
      "sparse-autoencoder"
    ]
  },
  "control-neuron": {
    "name": "Control neuron",
    "short": "A randomly chosen neuron the explanation is not about, scored with the same explanation on the same held-out text; the baseline that gives an explanation score its scale.",
    "def": "A <strong>control neuron</strong> is the interpretability version of the control check from <a href='pages/20-validity.html'>page 20</a>: take the explanation and its simulated activations, but correlate them with the real activations of a random unit from the same layer. If the score barely drops, the score was measuring the text, not the neuron. Huang et al. 2023 used exactly this baseline (random pairings scored an F1 of zero against 0.56 for the real pairings). The same control applies to causal claims: ablate a random neuron and compare the behavioral effect. <a href='pages/28-controls-for-interpretability-claims.html'>Page 28</a> works one by hand, alongside the shuffled-label control and a baseline explanation.",
    "also": "random-neuron baseline",
    "see": [
      "simulation-scoring",
      "permutation-test",
      "intervention",
      "construct-validity"
    ]
  },
  "permutation-test": {
    "name": "Permutation test",
    "short": "A hypothesis test that builds the null distribution by shuffling the labels (here, the real activations) and recomputing the statistic many times; the p-value is the fraction of shuffles that match or beat the observed value.",
    "def": "A <strong>permutation test</strong> asks how often a statistic would be as large as observed if the pairing between two lists carried no information. Shuffle one list (for an explanation score, the real activations across tokens), recompute the correlation, repeat thousands of times, and the fraction of shuffles at or above the observed score is a <a href='glossary.html#p-value'>p-value</a> under the <a href='glossary.html#null-hypothesis'>null hypothesis</a> of no relationship. It needs no distributional assumptions and is the shuffled-label control on <a href='pages/28-controls-for-interpretability-claims.html'>page 28</a>. It is the cousin of the <a href='glossary.html#bootstrap'>bootstrap</a> (<a href='appendices/f-resampling.html'>Appendix F</a>): the bootstrap resamples to estimate uncertainty, the permutation test reshuffles to test a null.",
    "also": "shuffled-label control, randomization test",
    "see": [
      "p-value",
      "null-hypothesis",
      "hypothesis-test",
      "bootstrap"
    ]
  },
  "intervention": {
    "name": "Intervention",
    "short": "Changing a unit's activation inside the running model (ablating it, or swapping in its value from another input) and measuring whether behavior changes; the test that separates a causal explanation from a correlational description.",
    "def": "An <strong>intervention</strong> edits the model's internal state and watches the output. Ablation sets a unit to zero or to its mean; an interchange intervention replaces its value with the value it took on a different input. Huang et al. 2023 read a neuron explanation as the causal claim that the neuron mediates the concept, and tested it with interchange interventions on tasks the model solves perfectly: GPT-4's explanations selected neurons with about the same causal effect as random selection. Bills et al. 2023 defined an 'ablation score' that substitutes simulated activations into the model and measures output divergence. A correlational score can be high while an interventional one is low; see <a href='pages/28-controls-for-interpretability-claims.html'>page 28</a>. It is the ablation probe of <a href='pages/20-validity.html'>page 20</a> pointed inward.",
    "also": "ablation, interchange intervention, causal mediation",
    "see": [
      "neuron-explanation",
      "control-neuron",
      "simulation-scoring"
    ]
  },
  "sae-feature": {
    "name": "Feature (SAE feature)",
    "short": "A learned direction in a model's activation space, found by a sparse autoencoder, intended to be more single-purpose than a raw neuron; explained and scored exactly as a neuron is.",
    "def": "A <strong>feature</strong>, in the sparse-autoencoder sense, is one of a large set of directions learned so that each activation vector is approximately a sparse sum of them. The hope is that features are monosemantic where neurons are <a href='glossary.html#polysemanticity'>polysemantic</a>; Anthropic's 'Towards Monosemanticity' reported a median rubric score of 12 for feature intervals against 0 for neurons. For evaluation purposes a feature is a hypothesis like any other: it gets a <a href='glossary.html#neuron-explanation'>explanation</a>, a held-out <a href='glossary.html#simulation-scoring'>simulation score</a>, precision and recall, and the controls on <a href='pages/28-controls-for-interpretability-claims.html'>page 28</a>. Gao et al. 2024 add downstream loss, probe loss and ablation sparsity as feature-quality metrics.",
    "also": "latent, dictionary feature",
    "see": [
      "sparse-autoencoder",
      "polysemanticity",
      "neuron-explanation"
    ]
  },
  "sparse-autoencoder": {
    "name": "Sparse autoencoder",
    "short": "A model trained to rewrite a layer's activations as a sparse combination of many learned directions (features), used to find more interpretable units than raw neurons.",
    "def": "A <strong>sparse autoencoder</strong> (SAE) is trained on a model's activations to reconstruct them through a wide bottleneck in which only a few units are active at a time; the units are the <a href='glossary.html#sae-feature'>features</a>. Anthropic's 'Towards Monosemanticity' (2023) applied one to a one-layer transformer; Gao et al. (2024) trained one with 16 million features on GPT-4 activations and introduced metrics for judging whether the features are any good, including explanation precision and recall. Reconstruction quality alone is not the goal, and Gao et al. warn that a baseline of zeroing the layer makes almost any reconstruction look excellent (98.2%). See <a href='pages/28-controls-for-interpretability-claims.html'>page 28</a> and <a href='pages/29-case-study-demonstrated-explanation.html'>page 29</a>.",
    "also": "SAE, dictionary learning",
    "see": [
      "sae-feature",
      "polysemanticity",
      "neuron"
    ]
  }
};
