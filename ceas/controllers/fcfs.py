def controller(queues, t):
    """Serve the approach with the largest queue (toy FCFS-ish)."""
    return max(queues, key=queues.get)
