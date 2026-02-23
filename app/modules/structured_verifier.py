# app/modules/structured_verifier.py

import re


def extract_years(text: str):
    return re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", text)


def structured_verification(claim_text: str, property_values: list):

    if not property_values:
        return None

    claim_lower = claim_text.lower()

    # Year comparison
    claim_years = extract_years(claim_text)
    if claim_years:
        for year in claim_years:
            for value in property_values:
                if year in value:
                    return "SUPPORTED"
        return "CONTRADICTED"

    # Text comparison
    for value in property_values:
        if value.lower() in claim_lower:
            return "SUPPORTED"

    return "CONTRADICTED"
