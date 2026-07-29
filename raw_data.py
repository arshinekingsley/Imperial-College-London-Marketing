import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

# NORMALIZATION FUNCTION (1 to 5 scale)
def normalize(series, invert=False):
    x = series.astype(float)
    if x.max() == x.min():
        return pd.Series([3.0] * len(x))
    if invert:
        norm = 1.0 - ((x - x.min()) / (x.max() - x.min()))
    else:
        norm = (x - x.min()) / (x.max() - x.min())
    return 1.0 + 4.0 * norm

# FDA API HELPERS
def get_fda_count(endpoint, search_query):
    """Uses openFDA count feature to get actual totals without hitting limits."""
    url = f"https://api.fda.gov/{endpoint}.json"
    params = {"search": search_query}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get("meta", {}).get("results", {}).get("total", 0)
    except Exception as e:
        print(f"Error querying {endpoint}: {e}")
    return 0

# RADIOLOGY DATA COLLECTION
radiology_companies = ["Bayer", "GE Healthcare", "Siemens", "Philips", "Canon", "ACIST"]

radiology_data = []
for company in radiology_companies:
    recalls = get_fda_count("device/recall", f'recalling_firm:"{company}"')
    clearances = get_fda_count("device/510k", f'applicant:"{company}"')
    
    radiology_data.append({
        "Company": company,
        "Recalls": recalls,
        "Innovation_510k": clearances
    })

df_rad = pd.DataFrame(radiology_data)

# Normalize Metrics
df_rad["Recall_Score"] = normalize(df_rad["Recalls"], invert=True)       # Fewer recalls = Higher Score
df_rad["Innovation_Score"] = normalize(df_rad["Innovation_510k"], invert=False) # More 510k = Higher Score
df_rad["Final_Score"] = (df_rad["Recall_Score"] * 0.5) + (df_rad["Innovation_Score"] * 0.5)

# PHARMA DATA COLLECTION
pharma_portfolio = [
    {"Company": "Bayer", "Drug": "Xarelto"},
    {"Company": "Johnson & Johnson", "Drug": "Stelara"},
    {"Company": "Sanofi", "Drug": "Dupixent"},
    {"Company": "Novartis", "Drug": "Entresto"},
    {"Company": "GSK", "Drug": "Trelegy"},
    {"Company": "Abbott", "Drug": "Synthroid"}
]

pharma_data = []
for item in pharma_portfolio:
    drug = item["Drug"]
    
    total_events = get_fda_count("drug/event", f'patient.drug.medicinalproduct:"{drug}"')
    deaths = get_fda_count("drug/event", f'patient.drug.medicinalproduct:"{drug}" AND seriousnessdeath:1')
    
    pharma_data.append({
        "Company": item["Company"],
        "Drug": drug,
        "Total_Events": total_events,
        "Death_Events": deaths
    })

df_pharma = pd.DataFrame(pharma_data)

# Score Calculations
df_pharma["Safety_Score"] = normalize(df_pharma["Total_Events"], invert=True)
df_pharma["Mortality_Risk_Score"] = normalize(df_pharma["Death_Events"], invert=True)
df_pharma["Final_Score"] = (df_pharma["Safety_Score"] * 0.5) + (df_pharma["Mortality_Risk_Score"] * 0.5)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
print("--- RADIOLOGY SCORECARD ---")
print(df_rad[["Company", "Recalls", "Innovation_510k", "Recall_Score", "Innovation_Score", "Final_Score"]].to_string(index=False))
print("\n--- PHARMA SCORECARD ---")
df_pharma_display = df_pharma.copy()
df_pharma_display["Total_Events"] = df_pharma_display["Total_Events"].apply(lambda x: f"{x:,}")
df_pharma_display["Death_Events"] = df_pharma_display["Death_Events"].apply(lambda x: f"{x:,}")
print(df_pharma_display[["Company", "Drug", "Total_Events", "Death_Events", "Safety_Score", "Mortality_Risk_Score", "Final_Score"]].to_string(index=False))

# VISUALIZATIONS

# Radiology Heatmap
plt.figure(figsize=(8, 4))
sns.heatmap(df_rad.set_index("Company")[["Recall_Score", "Innovation_Score", "Final_Score"]], 
            annot=True, cmap="YlGnBu", vmin=1, vmax=5, fmt=".2f")
plt.title("Radiology Segment – Competitive Scorecard (1-5 Scale)")
plt.tight_layout()
plt.show()

# Pharma Heatmap
plt.figure(figsize=(8, 4))
sns.heatmap(df_pharma.set_index("Company")[["Safety_Score", "Mortality_Risk_Score", "Final_Score"]], 
            annot=True, cmap="YlGnBu", vmin=1, vmax=5, fmt=".2f")
plt.title("Pharma Segment – Competitive Scorecard (1-5 Scale)")
plt.tight_layout()
plt.show()

# Multi-Axis Radar Chart Helper
def plot_radar_chart(df, metrics, title):
    num_vars = len(metrics)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    plt.xticks(angles[:-1], metrics)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
    plt.ylim(0, 5)
    
    for i, row in df.iterrows():
        values = row[metrics].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1.5, linestyle='solid', label=row['Company'])
        ax.fill(angles, values, alpha=0.1)
        
    plt.title(title, size=11, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.show()

# Plot Radar Charts
plot_radar_chart(df_pharma, ["Safety_Score", "Mortality_Risk_Score", "Final_Score"], "Pharma Competitor Landscape")
