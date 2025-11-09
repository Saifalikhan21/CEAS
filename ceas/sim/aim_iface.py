from dataclasses import dataclass
import numpy as np

@dataclass
class Scenario:
    name: str
    duration_s: int = 600
    emg_rate: float = 0.02  # fraction of emergency vehicles

class AIMToySim:
    """A toy tick-based intersection sim (AIM-like). Not physics-accurate.
    Produces per-vehicle waits and emergency on-time stats."""
    def __init__(self, scenario: Scenario, seed: int):
        self.scenario = scenario
        self.rng = np.random.default_rng(seed)

    def _rates(self):
        if "arterial" in self.scenario.name:
            return {"N": 2.0, "S": 2.0, "E": 0.8, "W": 0.8}
        else:
            return {"N": 1.2, "S": 1.2, "E": 1.2, "W": 1.2}

    def run(self, controller_fn, controller_name: str, T_on_time: float = 20.0):
        rates = self._rates()
        tick = 1.0
        T = int(self.scenario.duration_s / tick)
        queues = {a: 0 for a in rates}
        approach_waits = {a: [] for a in rates}
        emg_log = []
        throughput = 0

        for t in range(T):
            # arrivals
            for a, lam in rates.items():
                arrivals = self.rng.poisson(lam * tick)
                queues[a] += arrivals
                for _ in range(arrivals):
                    if self.rng.random() < self.scenario.emg_rate:
                        emg_log.append({"t_arr": t, "approach": a, "served": False})

            # decision
            action = controller_fn(queues, t)
            served = {a: 0 for a in rates}
            cap = 5
            if action in ["NS", "SN"]:
                for a in ["N", "S"]:
                    s = min(cap, queues[a]); queues[a] -= s; served[a] = s
            elif action in ["EW", "WE"]:
                for a in ["E", "W"]:
                    s = min(cap, queues[a]); queues[a] -= s; served[a] = s
            elif action in served:
                s = min(cap, queues[action]); queues[action] -= s; served[action] = s

            for a, s in served.items():
                throughput += s
                if s > 0:
                    # toy wait samples
                    approach_waits[a].extend(self.rng.uniform(1, 30, size=s))

            # mark emergencies as served if their approach had service
            for emg in emg_log:
                if not emg["served"] and served.get(emg["approach"], 0) > 0:
                    emg["served"] = True
                    emg["t_serv"] = t

        emg_delays = [(e["t_serv"] - e["t_arr"]) for e in emg_log if e.get("served")]
        return {
            "controller": controller_name,
            "throughput": throughput,
            "per_vehicle_waits": [w for a in approach_waits for w in approach_waits[a]],
            "approach_waits": approach_waits,
            "emg_delays": emg_delays,
        }
