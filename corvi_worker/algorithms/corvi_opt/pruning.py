def should_prune(step: int, value: float) -> bool:
    if step >= 2 and value < 0.8 * (step + 1):
        return True
    return False
