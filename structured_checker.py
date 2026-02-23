# app/modules/structured_checker.py

import re


def extract_years(text: str):
    return re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", text)


def structured_fact_check(claim_text: str, structured_facts: list):
    """
    Deterministic year-based comparison
    """

    claim_years = extract_years(claim_text)

    if not claim_years:
        return None

    for year in claim_years:
        for fact in structured_facts:
            if year in fact:
                return "SUPPORTED"

    return "CONTRADICTED"