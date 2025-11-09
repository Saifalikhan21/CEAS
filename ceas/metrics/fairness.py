import numpy as np

def gini(x):
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return 0.0
    if np.min(x) < 0:
        x = x - np.min(x)
    mean = np.mean(x) + 1e-12
    diff = np.abs(x[:, None] - x[None, :]).mean()
    return 0.5 * diff / mean
