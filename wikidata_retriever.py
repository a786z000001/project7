# app/modules/wikidata_retriever.py

import requests


def get_wikidata_qid(entity_name: str):
    """
    Resolve entity name to Wikidata QID
    """
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": entity_name,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if "search" in data and len(data["search"]) > 0:
            return data["search"][0]["id"]

    except Exception:
        return None

    return None


def fetch_time_facts(qid: str):
    """
    Fetch time-related properties (dates, independence, birth, inception, etc.)
    """

    sparql_query = f"""
    SELECT ?value WHERE {{
      wd:{qid} ?prop ?value .
      ?prop wikibase:propertyType wikibase:Time .
    }}
    LIMIT 20
    """

    url = "https://query.wikidata.org/sparql"
    headers = {"Accept": "application/sparql-results+json"}

    try:
        response = requests.get(
            url,
            params={"query": sparql_query},
            headers=headers,
            timeout=10,
        )

        data = response.json()
        results = data["results"]["bindings"]

        facts = [item["value"]["value"] for item in results]

        return facts

    except Exception:
        return []