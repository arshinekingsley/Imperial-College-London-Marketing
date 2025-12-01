#   BAYER SCORECARD – BASED on FDA MAUDE AND FAERs DATA

import requests
import urllib3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# NORMALIZATION FUNCTION

def normalize(series, invert=False):
    x = series.astype(float)
    if x.max() == x.min():
        return pd.Series([3] * len(x))
    if invert:
        norm = 1 - ((x - x.min()) / (x.max() - x.min()))
    else:
        norm = (x - x.min()) / (x.max() - x.min())
    return 1 + 4 * norm

# DEVICE SEGMENT API FUNCTIONS (RADIOLGY)

def get_recalls(manufacturer, limit=1000):
    url = "https://api.fda.gov/device/recall.json"
    query = {"search": f"recalling_firm:{manufacturer}", "limit": limit}
    r = requests.get(url, params=query, verify=False)
    return r.json().get("results", []) if r.status_code == 200 else []

def get_510k(manufacturer, limit=1000):
    url = "https://api.fda.gov/device/510k.json"
    query = {"search": f"applicant:{manufacturer}", "limit": limit}
    r = requests.get(url, params=query, verify=False)
    return r.json().get("results", []) if r.status_code == 200 else []

# PHARMA SEGMENT API FUNCTIONS (FAERS)

def get_faers(drug, limit=1000):
    url = "https://api.fda.gov/drug/event.json"
    query = {"search": f"patient.drug.medicinalproduct:{drug}", "limit": limit}
    r = requests.get(url, params=query, verify=False)
    return r.json().get("results", []) if r.status_code == 200 else []

# RADIOLGY DATA COLLECTION 

radiology_companies = ["Bayer", "GE Healthcare", "Siemens", "Philips", "Canon", "ACIST"]

# Best-estimate overrides for FDA 1000s
best_estimates = {
    "GE Healthcare": {"Recalls": 150, "Innovation": 800},
    "Siemens": {"Recalls": 120, "Innovation": 700},
    "Philips": {"Recalls": 130, "Innovation": 964}
}

radiology = {"Company": [], "Recalls": [], "Innovation": []}

for c in radiology_companies:
    recall_data = get_recalls(c)
    innov_data = get_510k(c)

    # Apply best-estimates if API returns 1000
    recalls = len(recall_data)
    innovation = len(innov_data)
    if recalls >= 1000 or innovation >= 1000:
        recalls = best_estimates.get(c, {}).get("Recalls", recalls)
        innovation = best_estimates.get(c, {}).get("Innovation", innovation)

    radiology["Company"].append(c)
    radiology["Recalls"].append(recalls)
    radiology["Innovation"].append(innovation)

df_rad = pd.DataFrame(radiology)
print("\nRADIOLGY RAW DATA:")
print(df_rad)

# PHARMA DATA COLLECTION 

pharma_companies = {
    "Bayer": "Xarelto",
    "Johnson & Johnson": "Stelara",
    "Sanofi": "Dupixent",
    "Novartis": "Entresto",
    "GSK": "Trelegy",
    "Abbott": "Synthroid"
}

pharma = {"Company": [], "FAERS_Death": []}

for company, drug in pharma_companies.items():
    faers = get_faers(drug)
    death_count = sum(1 for e in faers if e.get("seriousnessdeath") == "1")
    pharma["Company"].append(company)
    pharma["FAERS_Death"].append(death_count)

df_pharma = pd.DataFrame(pharma)
print("\nPHARMA RAW DATA:")
print(df_pharma)

# RADIOLGY – NORMALIZATION + FINAL SCORE

df_rad["Recall_Score"] = normalize(df_rad["Recalls"], invert=True)
df_rad["Innovation_Score"] = normalize(df_rad["Innovation"], invert=False)
df_rad["Final_Score"] = (df_rad["Recall_Score"] * 0.5 + df_rad["Innovation_Score"] * 0.5)

print("\nRADIOLGY FINAL SCORECARD:")
print(df_rad)

# PHARMA – NORMALIZATION + FINAL SCORE

df_pharma["Death_Score"] = normalize(df_pharma["FAERS_Death"], invert=True)
df_pharma["Final_Score"] = df_pharma["Death_Score"]  # only metric used

print("\nPHARMA FINAL SCORECARD:")
print(df_pharma)

# VISUALIZATION

def radar_chart(df, company, title):
    categories = df.columns[1:-1]
    values = df[df["Company"] == company][categories].values.flatten().tolist()
    values += values[:1]
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]
    plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    plt.title(title)
    plt.show()

# Bayer Radars
radar_chart(df_rad, "Bayer", "Bayer Radiology Score – Radar Chart")
radar_chart(df_pharma, "Bayer", "Bayer Pharma Score – Radar Chart")

# Heatmaps
plt.figure(figsize=(10, 6))
sns.heatmap(df_rad.set_index("Company")[["Recall_Score","Innovation_Score","Final_Score"]],
            annot=True, cmap="YlGnBu")
plt.title("Radiology Competitors – Heatmap Scorecard")
plt.show()

plt.figure(figsize=(10, 6))
sns.heatmap(df_pharma.set_index("Company")[["Death_Score","Final_Score"]],
            annot=True, cmap="YlGnBu")
plt.title("Pharma Competitors – Heatmap Scorecard")
plt.show()
