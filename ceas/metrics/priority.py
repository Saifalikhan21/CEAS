import numpy as np

def on_time_rate(delays, T):
    if len(delays) == 0:
        return 0.0
    return float(np.mean((np.array(delays) <= T)))
