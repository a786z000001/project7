# app/modules/property_mapper.py

PROPERTY_MAP = {
    "independence": "P571",        # inception
    "founded": "P571",
    "established": "P571",
    "born": "P569",
    "birth": "P569",
    "died": "P570",
    "death": "P570",
    "capital": "P36",
    "president": "P35",
    "prime minister": "P6",
    "population": "P1082",
    "world cup": "P1346",          # award received
    "ceo": "P169",
}


def map_relation_to_property(claim_text: str):
    text = claim_text.lower()

    for keyword, pid in PROPERTY_MAP.items():
        if keyword in text:
            return pid

    return None