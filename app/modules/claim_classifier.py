# app/modules/claim_classifier.py

import re


def classify_claim(text: str) -> str:
    text_lower = text.lower().strip()

    speculative_patterns = [
        r"\bwill\b",
        r"\bwould\b",
        r"\bmight\b",
        r"\bcould\b",
        r"\bgoing to\b",
        r"\bnext\b",
        r"\bsoon\b"
    ]

    opinion_patterns = [
        r"\bi think\b",
        r"\bi believe\b",
        r"\bin my opinion\b"
    ]

    # Question-based inputs are speculative
    if text_lower.endswith("?"):
        return "speculative"

    # Check speculative keywords
    for pattern in speculative_patterns:
        if re.search(pattern, text_lower):
            return "speculative"

    # Check opinion keywords
    for pattern in opinion_patterns:
        if re.search(pattern, text_lower):
            return "opinion"

    # Default → factual
    return "factual"
