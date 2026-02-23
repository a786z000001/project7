# app/core/orchestrator.py

from app.modules.claim_classifier import classify_claim
from app.modules.entity_extractor import extract_main_entity
from app.modules.property_mapper import map_relation_to_property
from app.modules.wikidata_property_retriever import (
    get_wikidata_qid,
    fetch_property_value,
)
from app.modules.structured_verifier import structured_verification
from app.modules.verifier import verify_claim
from app.modules.llm_verifier import verify_claim_with_llm
from app.modules.rag_retriever import fetch_wikipedia_summary
from app.core.scorer import compute_score


def run_hallucination_pipeline(text: str):

    claim_type = classify_claim(text)

    if claim_type in ["speculative", "opinion"]:
        score = compute_score("speculative", "SPECULATIVE", 0.5)
        return {
            "mode": "prediction",
            "verdict": "SPECULATIVE",
            "confidence": 0.5,
            **score,
        }

    entity = extract_main_entity(text)

    if not entity:
        score = compute_score("factual", "INSUFFICIENT_EVIDENCE", 0.4)
        return {"verdict": "ENTITY_NOT_FOUND", **score}

    # -----------------------------------------
    # 1️⃣ Structured Knowledge Verification
    # -----------------------------------------

    pid = map_relation_to_property(text)

    if pid:
        qid = get_wikidata_qid(entity)

        if qid:
            property_values = fetch_property_value(qid, pid)

            structured_result = structured_verification(
                text, property_values
            )

            if structured_result:
                confidence = 0.95
                score = compute_score(
                    "factual", structured_result, confidence
                )

                return {
                    "mode": "fact_verification",
                    "verdict": structured_result,
                    "confidence": confidence,
                    "entity": entity,
                    "property_checked": pid,
                    "property_values": property_values,
                    **score,
                }

    # -----------------------------------------
    # 2️⃣ NLI Fallback
    # -----------------------------------------

    evidence = fetch_wikipedia_summary(entity)

    if evidence:
        nli_result = verify_claim(1, text, [evidence])

        if nli_result.probability > 0.8:
            verdict_map = {
                "ENTAILMENT": "SUPPORTED",
                "CONTRADICTION": "CONTRADICTED",
                "UNKNOWN": "INSUFFICIENT_EVIDENCE",
            }

            verdict = verdict_map.get(
                nli_result.verdict, "INSUFFICIENT_EVIDENCE"
            )

            score = compute_score(
                "factual", verdict, nli_result.probability
            )

            return {
                "mode": "fact_verification",
                "verdict": verdict,
                "confidence": nli_result.probability,
                "entity": entity,
                **score,
            }

    # -----------------------------------------
    # 3️⃣ GPT Final Fallback
    # -----------------------------------------

    verification = verify_claim_with_llm(text, evidence or "")
    verdict = verification["verdict"]
    confidence = verification["confidence"]

    score = compute_score("factual", verdict, confidence)

    return {
        "mode": "fact_verification",
        "verdict": verdict,
        "confidence": confidence,
        "entity": entity,
        **score,
    }
