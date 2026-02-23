# app/core/scorer.py

import math


def compute_score(mode: str, verdict: str, confidence: float):

    confidence = max(min(confidence, 0.95), 0.05)

    if mode == "speculative":
        return {
            "contradiction_ratio": 0.0,
            "unknown_ratio": 0.6,
            "entropy_score": 0.0,
            "variance_score": 0.0,
            "hallucination_score": 0.4,
        }

    if verdict == "SUPPORTED":
        contradiction_ratio = 0.0
        unknown_ratio = 0.0
        hallucination_score = 1 - confidence

    elif verdict == "CONTRADICTED":
        contradiction_ratio = confidence
        unknown_ratio = 0.0
        hallucination_score = confidence

    else:
        contradiction_ratio = 0.0
        unknown_ratio = 1 - confidence
        hallucination_score = 0.6 + 0.3 * (1 - confidence)

    p = contradiction_ratio
    entropy = -(p * math.log(p + 1e-6) +
                (1 - p) * math.log(1 - p + 1e-6))

    variance = abs(contradiction_ratio - unknown_ratio)

    return {
        "contradiction_ratio": round(contradiction_ratio, 3),
        "unknown_ratio": round(unknown_ratio, 3),
        "entropy_score": round(entropy, 3),
        "variance_score": round(variance, 3),
        "hallucination_score": round(hallucination_score, 3),
    }