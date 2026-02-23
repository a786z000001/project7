# app/modules/verifier.py

from transformers import pipeline
from app.core.schema import VerificationResult
from typing import List
import torch

nli_pipeline = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli",
    device=0 if torch.cuda.is_available() else -1,
)

LABEL_MAP = {
    "ENTAILMENT": "ENTAILMENT",
    "CONTRADICTION": "CONTRADICTION",
    "NEUTRAL": "UNKNOWN",
}


def verify_claim(claim_id: int, claim_text: str, evidence: List[str]) -> VerificationResult:

    if not evidence:
        return VerificationResult(
            claim_id=claim_id,
            verdict="UNKNOWN",
            probability=0.5,
        )

    premise = evidence[0]
    hypothesis = claim_text

    result = nli_pipeline(
        {"text": premise, "text_pair": hypothesis}
    )

    label = LABEL_MAP.get(result[0]["label"], "UNKNOWN")
    probability = float(result[0]["score"])

    return VerificationResult(
        claim_id=claim_id,
        verdict=label,
        probability=round(probability, 3),
    )