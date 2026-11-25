# Self-Preference Bias in LLM-as-a-Judge Evaluation

[![Reproduce results](https://github.com/KieferPlender/llm-judge-self-preference/actions/workflows/reproduce.yml/badge.svg)](https://github.com/KieferPlender/llm-judge-self-preference/actions/workflows/reproduce.yml)

> **TL;DR:** LLM judges (GPT-4o, DeepSeek-R1, Claude 3.5 Haiku) tend to favor answers that look like their own writing. I tested whether hiding each model's writing style removes that bias. Three rewrites cut a style classifier's ability to identify the author from **80.5% to as low as 47.0%**, yet self-preference barely moved: every effect was negligible (Cohen's *h* ≤ 0.12). **Self-preference is not just style recognition.** Every number below can be regenerated from the included data with no API keys, and CI checks this on every push.

Code, experimental artifacts, and results for the bachelor thesis **“Self-Preference Bias in LLM-as-a-Judge Evaluation: An Empirical Study of Stylometric Interventions.”**

Large language models are increasingly used to evaluate other models, but they can favor responses resembling their own output. This project tests whether obscuring model-specific writing styles reduces that self-preference bias.

## Main finding

Stylometric obfuscation made model outputs substantially harder to attribute, but did **not** produce a consistent or practically meaningful reduction in self-preference bias. This suggests that surface-level stylistic fingerprints alone do not explain the behavior.

![Authorship attribution accuracy before and after intervention](results/plots/classifier_accuracy_drop.png)

The baseline stylometric classifier reached **80.50%** accuracy. Markdown removal reduced accuracy to **50.47%**, back-translation to **75.26%**, and targeted paraphrasing to **47.03%**. Despite these reductions, changes in Self-Preference Rate were small and effect sizes were negligible across all conditions.

![Changes in Self-Preference Rate by model and intervention](results/plots/intervention_spr_changes.png)

## Research design

The study uses two non-overlapping samples from the [LMArena human-preference dataset](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k): 3,000 pairwise comparisons for classifier training and 3,000 for judge evaluation. It evaluates three judge models:

- ChatGPT-4o
- DeepSeek-R1
- Claude 3.5 Haiku

Three interventions target different stylometric signals:

1. **Markdown removal** removes surface-level formatting.
2. **Back-translation** rewrites responses through Chinese using Qwen3.
3. **Targeted paraphrasing** removes habitual phrasing, formatting, and conversational fillers using Qwen3.

Semantic fidelity is checked with Sentence-BERT. Changes in paired judge decisions are evaluated with McNemar's test, and practical relevance is measured using Cohen's *h*.

## Repository structure

```text
.
├── data/
│   ├── raw/              # Sampled battles and baseline judge decisions
│   ├── processed/        # Responses after each intervention
│   └── judging_results/  # Judge decisions on intervened responses
├── docs/
│   └── kiefer-plender-bsc-thesis.pdf
├── models/               # Fitted stylometric classifiers
├── results/
│   ├── feature_data/     # Extracted classifier features
│   ├── metrics/          # Machine-readable and text result summaries
│   └── plots/            # Figures used to communicate the findings
└── scripts/
    ├── 01_training/
    ├── 02_interventions/
    ├── 03_judging/
    ├── 04_analysis/
    ├── 05_verification/
    └── 06_reporting/
```

See [DATA.md](DATA.md) for provenance, content warnings, and the role of each data directory.

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Classifier training downloads the NLTK `punkt` tokenizer and English averaged-perceptron tagger on first use. Semantic-fidelity analysis downloads `sentence-transformers/all-MiniLM-L6-v2` from Hugging Face on first use.

## Verify the released results

The repository includes the exact experimental outputs used in the thesis. From the repository root, the core result tables and plots can be regenerated without API keys:

```bash
python scripts/04_analysis/calculate_per_model_intervention_effects.py
python scripts/06_reporting/verify_all_results.py
python scripts/06_reporting/statistical_significance_rigorous.py
python scripts/06_reporting/conference_plots.py
```

Additional checks are available in `scripts/05_verification/` and `scripts/06_reporting/`. Some checks load the included pickled classifiers; only load these files from a trusted copy of this repository because Python pickle files can execute code during deserialization.

## Reproduce the experimental pipeline

The following commands show the main stages. Run them from the repository root.

### 1. Train the stylometric classifier

```bash
python scripts/01_training/train_mcgovern_classifier.py \
  --train_file data/raw/classifier_training_samples.jsonl \
  --output models/mcgovern_classifier.pkl
```

### 2. Generate interventions

Markdown removal is deterministic and does not require an API key:

```bash
python scripts/02_interventions/strip_all_markdown_complete.py
```

Back-translation and paraphrasing use a paid DeepInfra endpoint. Copy `.env.example` to `.env`, add your credentials, and review provider pricing and concurrency limits before running:

```bash
cp .env.example .env
python scripts/02_interventions/run_qwen_full_intervention.py
python scripts/02_interventions/run_qwen_paraphrase_intervention.py
```

### 3. Run judge evaluations

Judge evaluation can call DeepInfra, OpenAI, and Anthropic and may incur substantial cost:

```bash
python scripts/03_judging/run_judge.py \
  --input data/raw/judge_samples.jsonl \
  --output data/raw/judge_results.jsonl
```

Pass an intervention file from `data/processed/` as `--input` and write its decisions to `data/judging_results/` to evaluate an intervention. Existing output files are treated as resumable runs, so use a new path if a clean rerun is intended.

> [!NOTE]
> API model aliases, provider behavior, and hosted model versions can change. The included artifacts are the authoritative record of the thesis experiments; a new API run should be treated as a replication rather than an exact reproduction.

## Thesis

The complete thesis is available at [docs/kiefer-plender-bsc-thesis.pdf](docs/kiefer-plender-bsc-thesis.pdf).

## Citation

Use the repository's [CITATION.cff](CITATION.cff), or cite the thesis as:

> Plender, K. M. (2026). *Self-Preference Bias in LLM-as-a-Judge Evaluation: An Empirical Study of Stylometric Interventions*. Bachelor thesis, University of Amsterdam.

## Licenses and attribution

- Original source code is released under the [MIT License](LICENSE).
- The thesis is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- LMArena-derived records remain subject to the source dataset's [CC BY 4.0 license and attribution requirements](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k).
- Generated model outputs may additionally be subject to the terms of their respective model providers.

See [LICENSES.md](LICENSES.md) for the scope of each license and the required data attribution.

## Author

Kiefer M. Plender<br>
BSc Artificial Intelligence, University of Amsterdam
