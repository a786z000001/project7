# app/modules/triple_extractor.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_NAME = "Babelscape/rebel-large"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.to(DEVICE)
model.eval()


def extract_triples(text: str):
    """
    Extract subject–relation–object triples using REBEL.
    Research-style structured extraction.
    """

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            max_length=256,
            num_beams=4,
        )

    decoded = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=False,
    )[0]

    triples = []

    # REBEL outputs structured tokens like:
    # <triplet> Argentina <subj> Argentina <obj> FIFA World Cup <relation> winner

    triplets = decoded.split("<triplet>")

    for triplet in triplets:
        subj = None
        obj = None
        relation = None

        subj_match = re.search(r"<subj>(.*?)<obj>", triplet)
        obj_match = re.search(r"<obj>(.*?)<relation>", triplet)
        rel_match = re.search(r"<relation>(.*)", triplet)

        if subj_match:
            subj = subj_match.group(1).strip()

        if obj_match:
            obj = obj_match.group(1).strip()

        if rel_match:
            relation = rel_match.group(1).strip()

        if subj and relation and obj:
            triples.append({
                "subject": subj,
                "relation": relation,
                "object": obj,
            })

    return triples
