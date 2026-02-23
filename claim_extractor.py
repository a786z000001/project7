import re
from typing import List
from app.core.schema import Claim
from app.config import settings


def extract_claims(response_text: str) -> List[Claim]:
    sentences = re.split(r'(?<=[.!?]) +', response_text)

    claims = []
    for idx, sentence in enumerate(sentences[: settings.MAX_CLAIMS]):
        cleaned = sentence.strip()
        if len(cleaned) > 10:
            claims.append(Claim(claim_id=idx + 1, text=cleaned))

    return claims