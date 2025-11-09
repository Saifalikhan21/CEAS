def controller(queues, t):
    """Actuated: choose NS or EW by higher combined queue."""
    ns = queues["N"] + queues["S"]
    ew = queues["E"] + queues["W"]
    return "NS" if ns >= ew else "EW"
