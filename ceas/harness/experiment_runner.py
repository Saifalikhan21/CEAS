import os, csv, json
from ceas.harness.seed_registry import SEEDS, DEFAULT_SCENARIOS
from ceas.sim.aim_toy import AIMToySim, Scenario
from ceas.controllers import fcfs, actuated, max_pressure

CONTROLLERS = {
    "FCFS": fcfs.controller,
    "Actuated": actuated.controller,
    "MaxPressure": max_pressure.controller,
}

def ensure_dirs():
    os.makedirs("results/csv", exist_ok=True)
    os.makedirs("results/figs", exist_ok=True)
    os.makedirs("results/summary", exist_ok=True)

def run():
    ensure_dirs()
    for scen in DEFAULT_SCENARIOS:
        for seed in SEEDS:
            scenario = Scenario(name=scen)
            for name, fn in CONTROLLERS.items():
                sim = AIMToySim(scenario, seed)
                out = sim.run(fn, name)
                # compact CSV (throughput only — details in JSON)
                csv_path = f"results/csv/{scen}_{name}_seed{seed}.csv"
                with open(csv_path, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["controller", "throughput"])
                    w.writerow([name, out["throughput"]])
                # raw JSON for evaluation/plots
                json_path = f"results/csv/{scen}_{name}_seed{seed}.json"
                with open(json_path, "w") as jf:
                    json.dump(out, jf)
    print("Runs complete → results/csv")
