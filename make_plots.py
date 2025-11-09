import os, glob, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ceas.metrics.fairness import gini
from ceas.metrics.priority import on_time_rate
from ceas.metrics.stats import bootstrap_ci

os.makedirs("results/summary", exist_ok=True)
os.makedirs("results/figs", exist_ok=True)

def aggregate():
    rows = []
    for jf in glob.glob("results/csv/*.json"):
        with open(jf) as f:
            data = json.load(f)
        rows.append({
            "controller": data["controller"],
            "throughput": data["throughput"],
            "gini": gini(data["per_vehicle_waits"]),
            "on_time": on_time_rate(data["emg_delays"], T=20.0),
        })
    df = pd.DataFrame(rows)
    if df.empty:
        print("No results found. Run baselines first.")
        return None, None

    # group summaries
    agg = df.groupby("controller").agg(
        throughput_mean=("throughput", "mean"),
        gini_mean=("gini", "mean"),
        on_time_mean=("on_time", "mean"),
    ).reset_index()

    # bootstrap CI for on_time mean
    cis = []
    for ctrl, sub in df.groupby("controller"):
        lo, hi = bootstrap_ci(sub["on_time"].values, stat_fn=np.mean, n_boot=800, alpha=0.05)
        cis.append({"controller": ctrl, "on_time_lo": lo, "on_time_hi": hi})
    ci_df = pd.DataFrame(cis)

    out = agg.merge(ci_df, on="controller", how="left")
    out_path = "results/summary/emergency_priority.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")
    return df, out

def plot(df):
    if df is None or df.empty:
        print("Nothing to plot.")
        return
    plt.figure()
    for ctrl in sorted(df["controller"].unique()):
        sub = df[df["controller"] == ctrl]
        plt.scatter(sub["throughput"], sub["gini"], label=ctrl)
    plt.xlabel("Throughput (vehicles)")
    plt.ylabel("Delay Gini")
    plt.title("Fairness vs Throughput (toy baselines)")
    plt.legend()
    out = "results/figs/fairness_vs_throughput.png"
    plt.savefig(out, bbox_inches="tight", dpi=150)
    print(f"Wrote {out}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-only", dest="eval_only", action="store_true")
    parser.add_argument("--plot-only", dest="plot_only", action="store_true")
    args = parser.parse_args()

    df, _ = aggregate()
    # If --plot-only was passed but df is None, exit gracefully
    if args.plot_only and df is None:
        raise SystemExit(0)
    # Plot unless explicitly told to do eval-only
    if not args.eval_only:
        plot(df)
