"""
1. Carica i log Mordor (JSON-lines) in un indice Elasticsearch.
2. Esegue le query Lucene generate da convert_to_lucene.py contro l'indice.
3. Salva i risultati in un report Markdown leggibile, da pubblicare come
   artifact del workflow GitHub Actions.

In CI, Elasticsearch gira come service container del job
(vedi .github/workflows/sigma-elasticsearch-validation.yml),
raggiungibile su localhost:9200.
"""
import json
from pathlib import Path

from elasticsearch import Elasticsearch, helpers

ES_URL = "http://localhost:9200"
INDEX_NAME = "mordor-logs"

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "07_detection_content" / "data"
QUERIES_FILE = REPO_ROOT / "07_detection_content" / "lucene_queries.json"
REPORT_FILE = REPO_ROOT / "07_detection_content" / "elasticsearch_validation_report.md"


def create_index_with_mapping(es: Elasticsearch):
    """Crea l'indice con mapping esplicito: i campi usati nelle regole
    devono essere 'keyword' (valore esatto), non 'text' (analizzato),
    altrimenti i wildcard letterali generati da pySigma non trovano match
    contro token spezzettati dall'analyzer di default."""
    mapping = {
        "mappings": {
            "properties": {
                "Image": {"type": "keyword"},
                "CommandLine": {"type": "keyword"},
                "ParentImage": {"type": "keyword"},
                "TargetFilename": {"type": "keyword"},
                "DestinationHostname": {"type": "keyword"},
            }
        }
    }
    es.indices.create(index=INDEX_NAME, body=mapping)


def load_and_index_logs(es: Elasticsearch):
    log_files = list(DATA_DIR.glob("*.json"))
    actions = []
    for lf in log_files:
        with open(lf, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    doc = json.loads(line)
                    actions.append({"_index": INDEX_NAME, "_source": doc})

    helpers.bulk(es, actions)
    es.indices.refresh(index=INDEX_NAME)
    count = es.count(index=INDEX_NAME)["count"]
    print(f"Indicizzati {count} documenti in '{INDEX_NAME}'")
    return count


def run_queries(es: Elasticsearch) -> list[dict]:
    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))
    report_rows = []

    for rule_file, info in queries.items():
        query_string = info["lucene_query"]
        title = info["title"]

        result = es.search(
            index=INDEX_NAME,
            query={"query_string": {"query": query_string}},
            size=10,
        )
        hits = result["hits"]["total"]["value"]
        print(f"[{title}] -> {hits} match reali su Elasticsearch")
        report_rows.append({"rule_file": rule_file, "title": title, "hits": hits})

    return report_rows


def write_report(doc_count: int, report_rows: list[dict]):
    lines = [
        "# Elasticsearch Validation Report",
        "",
        f"Generated automatically by GitHub Actions. "
        f"Indexed {doc_count} documents from the Mordor dataset "
        f"(`empire_launcher_vbs`, APT29 emulation Day 1) into a live "
        f"Elasticsearch 8.x instance.",
        "",
        "| Rule | Matches |",
        "|---|---|",
    ]
    for row in report_rows:
        lines.append(f"| {row['title']} | {row['hits']} |")

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report salvato in {REPORT_FILE}")


def main():
    es = Elasticsearch(ES_URL)
    try:
        es.cluster.health()
    except Exception as e:
        raise SystemExit(f"Elasticsearch non raggiungibile su {ES_URL}: {e}")

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
    create_index_with_mapping(es)

    doc_count = load_and_index_logs(es)
    print("-" * 60)
    report_rows = run_queries(es)
    write_report(doc_count, report_rows)


if __name__ == "__main__":
    main()
