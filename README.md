```markdown
# CEAS: Collective Ethics in Autonomous Traffic — MVP (Baselines)

A tiny, **reproducible** evaluation harness for intersection controllers. It reports:

- **Distributive fairness** — Delay **Gini** over per-vehicle waits  
- **Priority reliability** — Emergency/public-service **on-time rate**  
- **Efficiency** — Average **throughput**

This MVP runs a fast **AIM-style toy simulator** and compares **Actuated / FCFS / Max-Pressure**.  
*Next up:* **BWS** fairness-aware controller, **SUMO/TraCI adapter**, corridor scenarios.

---

## What’s inside

```

ceas-fair-traffic/
environment.yml        # conda/mamba env (Python 3.11)
Makefile               # convenience targets (optional)
ceas/
controllers/         # fcfs.py, actuated.py, max_pressure.py
metrics/             # fairness.py (Gini), priority.py (on_time), stats.py (bootstrap CI)
sim/                 # aim_toy.py (simple AIM-like sim)
harness/             # seed_registry.py, experiment_runner.py
scripts/
run_baselines.py     # runs Actuated/FCFS/Max-Pressure across seeds & scenarios
make_plots.py        # aggregates -> CSV + plot
results/{csv,figs,summary}  # auto-created on run
docs/{HOWTO.md, REPRODUCIBILITY.md}

````

---

## Prerequisites (macOS)

**Option A — Recommended (Conda/Mamba)**

```bash
# 1) Command Line Tools (git/make)
xcode-select --install

# 2) (Optional) Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile && eval "$(/opt/homebrew/bin/brew shellenv)"

# 3) Mambaforge (fast conda)
curl -L -o Mambaforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-MacOSX-arm64.sh
bash Mambaforge.sh -b
source ~/mambaforge/bin/activate
````

**Option B — Plain Python**

* Python **3.11+** (`python3 --version`)

---

## Quick start

> Run from the project root (folder containing `ceas/` and `scripts/`).

**A) With mamba (recommended)**

```bash
mamba env create -f environment.yml
mamba activate ceas

# Baselines: write per-run JSON/CSV to results/csv/
python -m scripts.run_baselines

# Aggregate: write summary CSV
python -m scripts.make_plots --eval-only

# Plot: write fairness_vs_throughput.png
python -m scripts.make_plots --plot-only
```

**B) With plain Python (no conda)**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install numpy scipy pandas matplotlib tqdm joblib networkx

python -m scripts.run_baselines
python -m scripts.make_plots --eval-only
python -m scripts.make_plots --plot-only
```

---

## Outputs

* **Plot:** `results/figs/fairness_vs_throughput.png`
  Scatter of **Delay Gini vs Throughput** across controllers/seeds/scenarios.

* **Table:** `results/summary/emergency_priority.csv`
  Columns: `controller, throughput_mean, gini_mean, on_time_mean, on_time_lo, on_time_hi`
  (CI = bootstrap over runs/seeds)

> Tip: To make “on-time” stricter, edit `scripts/make_plots.py` and set `T=10.0` (default 20.0).

---

## Why this exists (MVP goals)

* One-command **fairness + priority** evaluation you can re-run anywhere.
* **Policy-legible** artefacts (CSV + plot) for quick review.
* A reproducible baseline for fairness-aware controllers.

---

## Roadmap

* **v0.2** — Add **BWS** (Bounded-Wait Scheduling): show **ΔGini ↓** with **≤5–10% throughput cost**
* **v0.3** — **SUMO/TraCI** adapter (drop-in swap for the sim, same metrics)
* **v0.4** — **Corridor** (2–3 junctions) + runtime profiling

---

## Troubleshooting

* `ModuleNotFoundError: ceas` → run from repo root and use module mode:

  ```bash
  python -m scripts.run_baselines
  ```
* `mamba: command not found` → install Mambaforge or use the **Plain Python** steps.
* `make: command not found` → use the Python commands (Makefile is optional).
* First-run Matplotlib “building font cache” message is normal.

---

## Reproducibility

* Deterministic **seed registry:** `ceas/harness/seed_registry.py`
* Environment: `environment.yml` (Conda/Mamba) or `pip` list above
* Non-parametric **bootstrap CIs** for on-time mean
* All artefacts under `results/`

---

## License

MIT — see `LICENSE`.

---

## Citation

```bibtex
@software{ceas_fair_traffic_mvp,
  author  = {Saif Ali Khan},
  title   = {CEAS: Collective Ethics in Autonomous Traffic — MVP (Baselines)},
  year    = {2025},
  url     = {https://github.com/<your-username>/ceas-fair-traffic}
}
```

---

## Contact

Issues/PRs welcome. For collaborations or integration pilots, reach out via GitHub or LinkedIn.

```
::contentReference[oaicite:0]{index=0}
```
