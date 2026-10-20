# Capstone report: <unit>

Date written (protocol): <date>    Date run: <date>

## 1. Protocol (verbatim, as written before the run)

CLAIM        <one falsifiable sentence>
UNIT         <model, weights, layer, hook point, index; how it was chosen and how many candidates were searched>
HELD-OUT     <which data; why it played no part in choosing the claim>
SCORING      <the function from claim and data to a number>
PREDICTION   <the number, as an inequality>
THRESHOLD    <the pass line and its justification relative to the controls and the base rate>
CONTROLS     <at least two; for each, what passing would mean>
FAILURE      <what you will conclude if it fails>
LOOKED?      <yes/no; if yes, this is a post-hoc fit and says so>

## 2. Results

| quantity | value |
|---|---|
| held-out score | |
| base rate of the rule on held-out tokens | |
| random-unit control, 95th percentile (n = ) | |
| shuffled-label control, 95th percentile (n = ) | |
| other controls | |
| **verdict by the pre-registered rule** | demonstrated / not demonstrated |

## 3. Not tested

| claim a reader might infer | tested here? | what would test it |
|---|---|---|
| the unit does nothing else | no | |
| the model uses the unit | no | patching / ablation |
| holds on other text | no | second held-out set of a different genre |
| weak activations follow the rule | | |

## 4. Diagnosis (required if the verdict is "not demonstrated")

<what specifically the failure is evidence of: wrong model, wrong threshold, wrong claim, wrong data>

## 5. Exploratory (anything learned after the run; not pre-registered)

## 6. Revised protocol (not yet run)

## 7. How to re-run

<the exact commands and seeds; the environment versions from the transcript header>
