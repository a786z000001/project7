# app/modules/entity_extractor.py

import spacy

nlp = spacy.load("en_core_web_sm")

VALID_LABELS = {"PERSON", "ORG", "GPE", "EVENT", "WORK_OF_ART"}


def extract_main_entity(text: str) -> str | None:
    doc = nlp(text)

    entities = [
        ent.text for ent in doc.ents
        if ent.label_ in VALID_LABELS
    ]

    if not entities:
        return None

    # Prefer first meaningful entity (not longest random token)
    return entities[0]
