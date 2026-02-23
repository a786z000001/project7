HalluGuard — Research-Style Factual Verification Engine
🚀 Overview

HalluGuard is a hybrid, research-inspired factual verification engine designed to detect and score hallucination risk in natural language claims.

Unlike naive LLM-based fact checking systems, HalluGuard combines:

Transformer-based triple extraction (REBEL)

Structured knowledge graph grounding (Wikidata)

Property-aware deterministic reasoning

NLI-based semantic verification

GPT fallback for uncertain cases

Calibrated hallucination scoring

The system mimics modern research architectures used in FEVER-style fact verification systems.

🏗 System Architecture
User Input
    ↓
Claim Classification
    ↓
Triple Extraction (REBEL Transformer)
    ↓
Subject–Relation–Object Representation
    ↓
Property Mapping → Wikidata Query
    ↓
Structured Deterministic Verification
    ↓
NLI Fallback (BART-MNLI)
    ↓
LLM Fallback (OpenAI GPT)
    ↓
Hallucination Risk Scoring
🔬 Core Components
1️⃣ Transformer-Based Triple Extraction

Model: Babelscape/rebel-large

Extracts structured triples:

Argentina won the FIFA World Cup in 2022
→
{
  subject: Argentina
  relation: winner
  object: FIFA World Cup
}

This eliminates naive keyword heuristics.

2️⃣ Structured Knowledge Grounding (Wikidata)

Resolves entity to QID

Maps relation → Wikidata Property (PID)

Queries structured property values

Performs deterministic comparison

Example:

Property: P1346 (award received)
Value: FIFA World Cup 2022

If matched → SUPPORTED
If mismatched → CONTRADICTED

No LLM guessing required.

3️⃣ NLI Semantic Verification

Model: facebook/bart-large-mnli

Used when structured verification is insufficient.

Compares:

Premise: Wikipedia summary
Hypothesis: Claim

Outputs:

ENTAILMENT

CONTRADICTION

NEUTRAL

4️⃣ GPT Fallback

Model: gpt-4o-mini

Used only when:

No structured match

NLI confidence < threshold

Ensures:

Evidence-constrained reasoning

Strict JSON output

Calibrated confidence

5️⃣ Hallucination Scoring Engine

Score computed from:

Contradiction ratio

Unknown ratio

Entropy

Variance

Confidence calibration

Produces:

hallucination_score ∈ [0, 1]

Risk interpretation:

0.0–0.3 → Low Risk

0.3–0.6 → Moderate Risk

0.6–1.0 → High Risk

📂 Project Structure
app/
 ├── api/
 │    └── routes.py
 ├── core/
 │    ├── orchestrator.py
 │    └── scorer.py
 ├── modules/
 │    ├── triple_extractor.py
 │    ├── property_mapper.py
 │    ├── wikidata_property_retriever.py
 │    ├── structured_verifier.py
 │    ├── verifier.py
 │    ├── llm_verifier.py
 │    ├── entity_extractor.py
 │    └── claim_classifier.py
 └── main.py
⚙️ Installation
1. Install Dependencies
pip install fastapi uvicorn
pip install torch transformers accelerate sentencepiece
pip install requests
pip install spacy
python -m spacy download en_core_web_sm
2. Set OpenAI Key

Create .env file:

OPENAI_API_KEY=your_key_here
3. Run Backend
uvicorn app.main:app --reload --port 8001
🧪 Example Queries
Example 1
Argentina won the FIFA World Cup in 2022.

→ SUPPORTED
→ Hallucination ≈ 0.02

Example 2
Argentina won the FIFA World Cup in 2018.

→ CONTRADICTED
→ Hallucination ≈ 0.92

Example 3
Argentina has the strongest military in South America.

→ GPT fallback
→ Moderate risk

🔎 Research Characteristics

This system demonstrates:

Hybrid symbolic + neural reasoning

Knowledge graph grounding

Multi-layer verification

Transformer-based relation extraction

Deterministic + probabilistic fusion

Confidence-aware scoring

Modular research architecture

⚠️ Limitations

Property mapping is limited to predefined mappings

No multi-hop reasoning yet

No large-scale FEVER benchmarking

No entity disambiguation model

No property embedding alignment (future work)

🚀 Future Work

Dynamic relation → property embedding alignment

Multi-hop Wikidata reasoning

Entity linking via BLINK

Dense retrieval with FAISS

FEVER dataset evaluation

Calibration via temperature scaling

Ensemble verification voting

🎯 Target Use Cases

LLM output verification

Hallucination scoring pipelines

AI content moderation

Automated fact-checking prototypes

Research experimentation

📜 License

MIT License

👤 Author

Built as a research-oriented factual verification system combining structured knowledge graphs and transformer-based reasoning.
