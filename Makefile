SHELL := /bin/bash

.PHONY: setup run-baselines eval plot clean

setup:
	python -m pip install --upgrade pip

run-baselines:
	python scripts/run_baselines.py

eval:
	python scripts/make_plots.py --eval-only

plot:
	python scripts/make_plots.py --plot-only

clean:
	rm -rf results/csv/* results/figs/* results/summary/*
	mkdir -p results/csv results/figs results/summary
