# app/modules/rag_retriever.py

import requests


def fetch_wikipedia_summary(query: str) -> str | None:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return data.get("extract")

    except Exception:
        return None

    return None
