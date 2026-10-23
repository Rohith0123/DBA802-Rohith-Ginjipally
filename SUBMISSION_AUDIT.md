# K-DART — Scientific and journal-submission audit

**Editorial status: MAJOR REVISIONS — NOT READY FOR SUBMISSION.**

## What is present
- A documented Python pipeline with seeded synthetic enterprise generation.
- Baselines: logistic regression and histogram gradient boosting.
- Candidate K-DART rule-derived features and ablation experiments.
- Two reproducible result figures, exported to PDF and PNG.
- Two results tables and run-level CSVs.
- An editable Word manuscript builder.
- Transparent reporting of null/inconclusive predictive benefit.

## Journal requirements from uploaded Elsevier guide (23 October 2026)
- *Knowledge-Based Systems* accepts Short Communications, maximum 10 double-line-spaced manuscript pages **including figures and tables**.
- Abstract no longer than 250 words; 1–7 keywords.
- Editable Word or LaTeX; single-column Word layout.
- Tables should be editable, numbered and cited; figures supplied separately with captions and appropriate resolution.
- Data statement and repository deposit/link are needed, or explicit justification where unavailable.
- AI-use disclosure where applicable, CRediT, funding and conflicts declarations, and corresponding author details.
- Reference metadata and citations must be checked against source publications.

## Major blockers
1. The outcome is synthetic and not an independently established enterprise digital-transformation readiness indicator.
2. The proposed knowledge rules are not elicited or validated from domain experts.
3. Results did not show a statistically supported gain over logistic regression.
4. No real-world decision usefulness or cost-sensitive managerial evaluation is demonstrated.
5. The 10-page length and final typesetting must be revalidated after any changes.
6. Cited sources, author metadata, claims of novelty, Q1 status and submission declarations remain to be fully verified.
7. Final graphical abstract is not prepared; verify whether it is requested for the selected submission type.
8. The manuscript generated here is explicitly a research draft, not a journal-ready paper.

## Reproduction
```sh
pip install -r requirements.txt
python experiment.py
python build_manuscript.py
```
Figures/tables and intermediate evidence are written into `outputs/`.
