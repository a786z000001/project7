import re

def extract_years(text):
    return [int(y) for y in re.findall(r'\b(1[0-9]{3}|20[0-9]{2})\b', text)]

def century_from_year(year):
    return (year - 1) // 100 + 1

def compute_contradiction_ratio(claim, evidence):

    claim_years = extract_years(claim)
    evidence_years = extract_years(evidence)

    # Check explicit year contradiction
    if claim_years and evidence_years:
        if claim_years[0] not in evidence_years:
            return 0.7
        return 0.0

    # Check century logic
    century_match = re.search(r'(\d+)(st|nd|rd|th)\s+century', claim.lower())

    if century_match and evidence_years:
        claim_century = int(century_match.group(1))
        evidence_century = century_from_year(evidence_years[0])

        if claim_century != evidence_century:
            return 0.7
        return 0.0

    # fallback
    return 0.4