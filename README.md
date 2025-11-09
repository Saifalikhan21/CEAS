# CEAS: Collective Ethics in Autonomous Traffic (MVP)
Toy AIM-style simulator to produce baseline results (FCFS, Actuated, Max-Pressure).

## Quickstart
```bash
mamba env create -f environment.yml
mamba activate ceas
make setup
make run-baselines
make eval
make plot
```

## Outputs
- `results/figs/fairness_vs_throughput.png`
- `results/summary/emergency_priority.csv`
