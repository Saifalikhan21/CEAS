def controller(queues, t):
    """Max-pressure proxy: use queue totals (toy)."""
    ns = queues["N"] + queues["S"]
    ew = queues["E"] + queues["W"]
    return "NS" if ns >= ew else "EW"
