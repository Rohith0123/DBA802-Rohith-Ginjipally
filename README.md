# DBA 802 — K-DART research project

**Research-stage prototype; NOT ready for journal submission.**

K-DART investigates knowledge-guided AI decision intelligence for enterprise digital transformation readiness. The current experiment simulates enterprise features and outcomes. It is **not evidence from real enterprises**.

## Reproduce the experiment

```bash
python -m pip install -r requirements.txt
python experiment.py
```

Requires Python 3.10+ and writes output files to `outputs/`. These include:
- `Figure_1.pdf`, `Figure_1.png`: mean AUROC for baseline and proposed models
- `Figure_2.pdf`, `Figure_2.png`: probability calibration in one held-out synthetic run
- `table_1_metrics.csv`, `table_2_ablation.csv`: research tables
- `run_level_metrics.csv`, `ablation_runs.csv`, `summary.json`: auditable experimental outputs

## Interpretation
The original 20-seed pilot found **no improvement over logistic regression** from the proposed knowledge-rule features. Those rules are hypotheses, not independently expert-validated. The synthetic readiness outcome must not be presented as observed organizational data.

## Manuscript status
The separate editable manuscript, source-data package, and editorial audit are available in the conversation's K-DART research ZIP. The manuscript is a scientific research draft and should not be submitted to *Knowledge-Based Systems* without a real validated dataset, externally justified rules, empirical decision-utility testing, citation verification, and journal compliance review.

## Editorial requirements
The uploaded Elsevier author guide describes Short Communications as a maximum of 10 double-line-spaced manuscript pages, including figures and tables. Data/code sharing and required declarations should be checked before submission.

No personal or confidential enterprise data are used in this repository.
