# app/modules/llm_verifier.py

from openai import OpenAI
import json
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

VALID_VERDICTS = {"SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE"}


def verify_claim_with_llm(claim: str, evidence: str):

    if not evidence:
        return {
            "verdict": "INSUFFICIENT_EVIDENCE",
            "confidence": 0.5
        }

    system_prompt = """
You are a strict factual verification engine.
Use ONLY the provided evidence.
Respond only in JSON:
{
  "verdict": "SUPPORTED",
  "confidence": 0.82
}
"""

    user_prompt = f"""
CLAIM:
{claim}

EVIDENCE:
{evidence}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        parsed = json.loads(response.choices[0].message.content)

        verdict = parsed.get("verdict", "INSUFFICIENT_EVIDENCE").upper()
        confidence = float(parsed.get("confidence", 0.5))

        if verdict not in VALID_VERDICTS:
            verdict = "INSUFFICIENT_EVIDENCE"

        confidence = max(min(confidence, 0.95), 0.05)

        return {
            "verdict": verdict,
            "confidence": round(confidence, 3)
        }

    except Exception:
        return {
            "verdict": "INSUFFICIENT_EVIDENCE",
            "confidence": 0.5
        }