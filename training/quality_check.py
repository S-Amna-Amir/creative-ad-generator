def validity_score(text: str) -> float:
    """
    Simple heuristic quality score:
    - Penalize very short outputs
    - Penalize empty or repeated text
    """
    if not text or len(text) < 20:
        return 0.2
    if len(set(text.split())) < 5:
        return 0.3
    return 0.9