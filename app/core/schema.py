from pydantic import BaseModel
from typing import List, Optional


class Claim(BaseModel):
    claim_id: int
    text: str


class RetrievalResult(BaseModel):
    claim_id: int
    evidence: List[str]
    confidence: float


class VerificationResult(BaseModel):
    claim_id: int
    verdict: str  # ENTAILMENT | CONTRADICTION | UNKNOWN
    probability: float


class HallucinationBreakdown(BaseModel):
    hallucination_score: float
    contradiction_ratio: float
    unknown_ratio: float
    entropy_score: float
    variance_score: float
    high_risk_claims: List[str]
