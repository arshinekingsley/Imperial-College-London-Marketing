# BAYER FACTOR SCORECARD – LIVE OPENFDA DATA + QUALITATIVE EXPERT SCORES

import pandas as pd
from raw_data import df_rad, df_pharma

# Normalization function
def normalize(series, invert=False):
    x = series.astype(float)
    if x.max() == x.min():
        return pd.Series([3] * len(x))
    norm = 1 - ((x - x.min()) / (x.max() - x.min())) if invert else (x - x.min()) / (x.max() - x.min())
    return 1 + 4 * norm

# Expert/literature-based scores
expert_rad_scores = {
    "Bayer":         {"Product_Quality": 4, "Price": 3, "Service": 4},
    "GE Healthcare": {"Product_Quality": 5, "Price": 3, "Service": 3},
    "Siemens":       {"Product_Quality": 5, "Price": 3, "Service": 3},
    "Philips":       {"Product_Quality": 4, "Price": 3, "Service": 5},
    "Canon":         {"Product_Quality": 3, "Price": 4, "Service": 3},
    "ACIST":         {"Product_Quality": 2, "Price": 4, "Service": 2}
}

expert_pharma_scores = {
    "Bayer":             {"Clinical_Evidence": 4, "Price": 3, "Adherence": 4, "Brand_Trust": 4},
    "Johnson & Johnson": {"Clinical_Evidence": 5, "Price": 3, "Adherence": 4, "Brand_Trust": 5},
    "Sanofi":            {"Clinical_Evidence": 4, "Price": 4, "Adherence": 3, "Brand_Trust": 4},
    "Novartis":          {"Clinical_Evidence": 5, "Price": 3, "Adherence": 3, "Brand_Trust": 4},
    "GSK":               {"Clinical_Evidence": 4, "Price": 3, "Adherence": 3, "Brand_Trust": 3},
    "Abbott":            {"Clinical_Evidence": 4, "Price": 4, "Adherence": 3, "Brand_Trust": 3}
}

# --- RADIOLOGY SCORECARD ---
# Re-use live API scores from raw_data.py (Safety_Score & Innovation_Score)
# Map qualitative expert factors
df_rad["Product_Quality"] = df_rad["Company"].map(lambda x: expert_rad_scores[x]["Product_Quality"])
df_rad["Price"] = df_rad["Company"].map(lambda x: expert_rad_scores[x]["Price"])
df_rad["Service"] = df_rad["Company"].map(lambda x: expert_rad_scores[x]["Service"])

# Weighted final score
weights_rad = {"Safety_Score": 0.30, "Innovation_Score": 0.25, "Product_Quality": 0.20, "Price": 0.10, "Service": 0.15}
df_rad["Final_Score"] = (
    df_rad["Recall_Score"] * weights_rad["Safety_Score"] +
    df_rad["Innovation_Score"] * weights_rad["Innovation_Score"] +
    df_rad["Product_Quality"] * weights_rad["Product_Quality"] +
    df_rad["Price"] * weights_rad["Price"] +
    df_rad["Service"] * weights_rad["Service"]
)

# --- PHARMA SCORECARD ---
# Use live Mortality_Risk_Score from openFDA as the Safety_Score
df_pharma["Safety_Score"] = df_pharma["Mortality_Risk_Score"]

# Map qualitative expert factors
df_pharma["Clinical_Evidence"] = df_pharma["Company"].map(lambda x: expert_pharma_scores[x]["Clinical_Evidence"])
df_pharma["Price"] = df_pharma["Company"].map(lambda x: expert_pharma_scores[x]["Price"])
df_pharma["Adherence"] = df_pharma["Company"].map(lambda x: expert_pharma_scores[x]["Adherence"])
df_pharma["Brand_Trust"] = df_pharma["Company"].map(lambda x: expert_pharma_scores[x]["Brand_Trust"])

# Weighted final score
weights_pharma = {"Safety_Score": 0.35, "Clinical_Evidence": 0.25, "Price": 0.10, "Adherence": 0.15, "Brand_Trust": 0.15}
df_pharma["Final_Score"] = (
    df_pharma["Safety_Score"] * weights_pharma["Safety_Score"] +
    df_pharma["Clinical_Evidence"] * weights_pharma["Clinical_Evidence"] +
    df_pharma["Price"] * weights_pharma["Price"] +
    df_pharma["Adherence"] * weights_pharma["Adherence"] +
    df_pharma["Brand_Trust"] * weights_pharma["Brand_Trust"]
)

# Display Clean Terminal Output
pd.set_option('display.float_format', lambda x: '%.2f' % x)

print("\n RADIOLOGY WEIGHTED FACTOR SCORECARD:")
print(df_rad[["Company","Recall_Score","Innovation_Score","Product_Quality","Price","Service","Final_Score"]].to_string(index=False))

print("\n PHARMA WEIGHTED FACTOR SCORECARD:")
print(df_pharma[["Company","Drug","Safety_Score","Clinical_Evidence","Price","Adherence","Brand_Trust","Final_Score"]].to_string(index=False))
