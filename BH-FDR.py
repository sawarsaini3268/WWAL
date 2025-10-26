import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from statsmodels.stats.multitest import multipletests

# 1) Load your two “synthetic master” datasets
df1 = pd.read_csv("/mnt/data/WWAL_synthetic_master_dataset.csv")
df2 = pd.read_csv("/mnt/data/WWAL_synthetic_master_dataset_2.csv")

# 2) Build an analysis frame with the exact columns for H1–H7
# (these are the columns detected in your files)
combo = pd.DataFrame(index=range(max(len(df1), len(df2))))

def add_col(src_df, src_col, dest_name):
    s = src_df[src_col].reset_index(drop=True)
    combo[dest_name] = pd.to_numeric(s, errors="coerce")

# Map your actual column names → canonical names for the hypotheses
add_col(df2, "Q17 Count of conditions selected - created", "chronic_conditions")
add_col(df2, "Q34 - Count of workplace accomodations made", "work_accommodations")
add_col(df1, "Count of ADLs", "adl_limitations")
add_col(df1, "Mental Health_normalized", "mental_health")
add_col(df1, "PhysicalHealth_normalized", "physical_health")  # used as “overall health” proxy
add_col(df2, "DiffWalking_encoded", "mobility_difficulty")
add_col(df1, "PhysicalActivity_encoded", "physical_activity")
add_col(df2, "Trouble Sleeping_normalized", "sleep_problems")
add_col(df1, "Count of caregiving support activities - cargivers of children only [NEW 2020]", "support_activities")
add_col(df1, "Final number of Care Recipients", "care_recipients")

# 3) Define the seven preregistered hypothesis pairs
hypotheses = [
    ("H1", "chronic_conditions",   "work_accommodations", "positive"),
    ("H2", "chronic_conditions",   "adl_limitations",     "positive"),
    ("H3", "mental_health",        "physical_health",     "positive"),
    ("H4", "mobility_difficulty",  "physical_health",     "positive"),  # proxy for overall health
    ("H5", "physical_activity",    "mobility_difficulty", "negative"),
    ("H6", "physical_health",      "sleep_problems",      "positive"),  # note: if higher=better health, expect negative with sleep problems
    ("H7", "support_activities",   "care_recipients",     "negative"),
]

def corr_pair(df, a, b):
    sub = df[[a, b]].dropna()
    if len(sub) < 3:
        return np.nan, np.nan, len(sub)
    r, p = pearsonr(sub[a], sub[b])
    return r, p, len(sub)

rows = []
for h, a, b, exp_dir in hypotheses:
    r, p, n = corr_pair(combo, a, b)
    rows.append({"H": h, "x": a, "y": b, "n": n, "r": r, "p": p, "expected_direction": exp_dir})

res = pd.DataFrame(rows)

# 4) Benjamini–Hochberg FDR (only across these 7 preregistered tests)
rej, qvals, _, _ = multipletests(res["p"].values, alpha=0.05, method="fdr_bh")
res["q"] = qvals
res["significant_q<0.05"] = rej
res["observed_direction"] = res["r"].apply(lambda r: "positive" if pd.notna(r) and r >= 0 else ("negative" if pd.notna(r) else "NA"))

# 5) Save your final table
res = res[["H","x","y","n","r","p","q","observed_direction","expected_direction","significant_q<0.05"]]
res.to_csv("/mnt/data/familyA_FDR_results.csv", index=False)
print("Saved /mnt/data/familyA_FDR_results.csv")
