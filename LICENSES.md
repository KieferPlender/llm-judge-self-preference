# License scope and attribution

This repository contains material with different origins. The root `LICENSE` does not override third-party rights.

| Material | License or terms |
| --- | --- |
| Original Python source code in `scripts/` | MIT License, Copyright 2026 Kiefer M. Plender |
| Thesis PDF in `docs/` | [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) |
| Original plots, metrics, and feature summaries in `results/` | [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) |
| LMArena-derived records in `data/` | Source dataset's [CC BY 4.0 license](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k), subject to the notices below |
| Model-generated text | The applicable source dataset license and the terms of the model provider may also apply |
| Fitted model files in `models/` | Provided for research reproducibility; underlying dependencies retain their own licenses |

## Required LMArena attribution

Portions of the data are adapted from `lmarena-ai/arena-human-preference-140k`, published by LMArena under CC BY 4.0:

https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k

The adaptations include filtering, sampling, field normalization, stylometric transformations, and additional LLM judge annotations. See `DATA.md` for details.

## CC BY attribution for original research materials

When reusing the thesis or original result materials, attribute:

> Kiefer M. Plender, “Self-Preference Bias in LLM-as-a-Judge Evaluation: An Empirical Study of Stylometric Interventions” (2026), CC BY 4.0.
