# app/modules/wikidata_property_retriever.py

import requests


def get_wikidata_qid(entity_name: str):
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

        if "search" in data and data["search"]:
            return data["search"][0]["id"]

    except Exception:
        return None

    return None


def fetch_property_value(qid: str, pid: str):

    sparql_query = f"""
    SELECT ?valueLabel WHERE {{
      wd:{qid} wdt:{pid} ?value .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 10
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

        values = []
        for result in data["results"]["bindings"]:
            values.append(result["valueLabel"]["value"])

        return values

    except Exception:
        return []
