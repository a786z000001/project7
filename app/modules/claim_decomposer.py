# app/modules/claim_decomposer.py

import spacy

nlp = spacy.load("en_core_web_sm")


def decompose_into_claims(text: str):
    """
    Break text into atomic factual claims.
    """

    doc = nlp(text)

    claims = []

    for sent in doc.sents:
        sentence = sent.text.strip()

        # Split coordinated clauses (and, but, while)
        for token in sent:
            if token.dep_ == "cc":  # coordinating conjunction
                left = sent[:token.i - sent.start].text.strip()
                right = sent[token.i - sent.start + 1:].text.strip()

                if left:
                    claims.append(left)
                if right:
                    claims.append(right)
                break
        else:
            claims.append(sentence)

    # Remove very short fragments
    claims = [c for c in claims if len(c) > 10]

    return claims
