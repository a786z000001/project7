from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.core.schema import RetrievalResult

# Load embedding model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Dummy knowledge base (replace with real corpus)
DOCUMENTS = [
    "Tesla was founded in 2003 by Martin Eberhard and Marc Tarpenning.",
    "Argentina won the FIFA World Cup in 2022.",
    "Elon Musk became CEO of Tesla in 2008.",
]

doc_embeddings = embedder.encode(DOCUMENTS)

index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(np.array(doc_embeddings).astype("float32"))


def retrieve_evidence(claim_id: int, claim_text: str) -> RetrievalResult:

    query_embedding = embedder.encode([claim_text])
    distances, indices = index.search(
        np.array(query_embedding).astype("float32"), k=1
    )

    top_doc = DOCUMENTS[indices[0][0]]
    confidence = float(1 / (1 + distances[0][0]))

    return RetrievalResult(
        claim_id=claim_id,
        evidence=[top_doc],
        confidence=round(confidence, 3),
    )