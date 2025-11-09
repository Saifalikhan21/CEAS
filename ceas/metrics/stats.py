import numpy as np
from scipy import stats

def bootstrap_ci(data, stat_fn=np.median, n_boot=1000, alpha=0.05, rng=None):
    rng = np.random.default_rng(None if rng is None else rng)
    data = np.asarray(data)
    if data.size == 0:
        return (0.0, 0.0)
    boots = []
    for _ in range(n_boot):
        sample = rng.choice(data, size=data.size, replace=True)
        boots.append(stat_fn(sample))
    boots = np.sort(boots)
    lo = int((alpha/2) * n_boot)
    hi = int((1 - alpha/2) * n_boot) - 1
    return boots[lo], boots[hi]

def mann_whitney_u(a, b):
    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan
    u, p = stats.mannwhitneyu(a, b, alternative='two-sided')
    return u, p
