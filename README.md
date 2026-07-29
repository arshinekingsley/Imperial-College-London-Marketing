# Competitive Scorecard Analysis Using FDA Data

This repository contains the Python code developed to support the quantitative analysis presented in a Marketing Management final paper for the MBA program at **Imperial College London**.

Rather than representing the complete coursework submission, this repository contains the analytical framework used to collect, process, visualize, and score publicly available regulatory data as one component of a broader marketing strategy paper.

---

## Overview

The project demonstrates how publicly available regulatory data can be integrated with expert-weighted marketing criteria to evaluate the competitive positioning of **Bayer** and its peer group across the medical device and pharmaceutical industries.

Using the **openFDA APIs** (including the MAUDE and FAERS databases), the analysis retrieves publically available regulatory indicators such as:

* **Medical device recalls** (Device safety profile)
* **FDA 510(k) clearances** (Innovation & market entry activity)
* **Drug adverse event reports** (Pharma safety reporting volume)
* **Drug-related death reports** (Mortality-related safety indicator)

These quantitative measures are combined with qualitative marketing factors—including product quality, pricing, service, clinical evidence, adherence, and brand trust—to construct weighted competitive scorecards. Each company receives standardized scores on a **1–5 scale**, followed by an overall weighted score to facilitate competitor benchmarking.

---

## Repository Structure

* `raw_data.py` – Retrieves live data from the openFDA APIs, normalizes the metrics, and generates exploratory visualizations (heatmaps & radar charts).
* `scorecard.py` – Applies expert-weighted marketing criteria and produces the final weighted competitive scorecards.

---

## Technologies

* **Python 3.9+**
* `requests`
* `pandas`
* `numpy`
* `matplotlib`
* `seaborn`

---

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install requests pandas numpy matplotlib seaborn
```

---

## Usage

Retrieve the latest regulatory data and generate exploratory visuals:
```bash
python raw_data.py
```

Generate the weighted competitive scorecards:
```bash
python scorecard.py
```

---

## Methodology

Objective regulatory metrics are normalized to a common 1–5 scale (using inverse min-max scaling for safety risk metrics) and combined with qualitative marketing assessments using weighted averages. The framework demonstrates a structured approach to competitive analysis by integrating public regulatory data with strategic marketing evaluation.

*Note: The qualitative scores and weighting methodology are illustrative and were developed solely for academic analysis.*

---

## Academic Context

This repository accompanies a Marketing Management paper completed as part of the MBA curriculum at Imperial College London. It contains only the Python implementation used to support the quantitative analysis and does not include the complete written paper or its broader strategic discussion.

---

## Disclaimer

This project was developed for educational purposes. It is not affiliated with Bayer, the U.S. Food and Drug Administration (FDA), or any other organization. The analysis should not be interpreted as investment, clinical, regulatory, or commercial advice.
