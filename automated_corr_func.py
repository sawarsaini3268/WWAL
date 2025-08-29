# corr_within.py
# Run: python corr_within.py
from pathlib import Path
import pandas as pd
import numpy as np

# settings
DATA_DIR   = Path(r"C:\Users\sawar_as58gjw\OneDrive\dataset_analysis\WWAL_Code")  
CSV_GLOB   = "*normalized_trimmed.csv"   # which files to grab
OUTPUT_DIR = Path(DATA_DIR / "WWAL_within_corr")  # results folder
METHODS    = ["pearson", "spearman"]     # both correlation types

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def numeric_only(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only numeric cols and drop ones with no variance."""
    num = df.select_dtypes(include=[np.number]).copy()
    const = [c for c in num.columns if num[c].nunique(dropna=True) <= 1]
    if const:
        num.drop(columns=const, inplace=True, errors="ignore")
    return num

def corr_long(df_num: pd.DataFrame, method: str, dataset_name: str) -> pd.DataFrame:
    """
    Compute all pairwise correlations inside one dataset.
    Returns a tidy dataframe with one row per variable pair.
    """
    C = df_num.corr(method=method)
    C.values[np.diag_indices_from(C)] = np.nan  # ignore self correlations
    long = (
        C.stack()
         .reset_index()
         .rename(columns={"level_0":"col_A","level_1":"col_B",0:"corr"})
    )
    # keep each pair only once (A,B with A < B)
    long = long[long["col_A"] < long["col_B"]]
    long["dataset"]  = dataset_name
    long["method"]   = method
    long["abs_corr"] = long["corr"].abs()
    return long[["dataset","col_A","col_B","method","corr","abs_corr"]] \
             .sort_values("abs_corr", ascending=False)

# main
files = sorted(DATA_DIR.glob(CSV_GLOB))
if not files:
    raise SystemExit(f"No CSVs found in {DATA_DIR} with pattern '{CSV_GLOB}'")

all_results = []

for f in files:
    print(f"Processing {f.name} ...")
    df = pd.read_csv(f)
    num = numeric_only(df)
    if num.empty:
        print(f"  [skip] no numeric cols")
        continue

    for m in METHODS:
        result = corr_long(num, m, f.stem)
        all_results.append(result)
        # save per-dataset CSV
        result.to_csv(OUTPUT_DIR / f"{f.stem}__{m}_within.csv", index=False)

# combine all into one big CSV
if all_results:
    combined = pd.concat(all_results, ignore_index=True)
    combined.to_csv(OUTPUT_DIR / "ALL_within_correlations.csv", index=False)
    print(f"\nDone! Results in {OUTPUT_DIR}")
else:
    print("No correlations computed.")
