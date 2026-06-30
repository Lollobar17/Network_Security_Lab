"""
Converte tutte le regole Sigma in query Lucene per Elasticsearch usando
il backend ufficiale pysigma-backend-elasticsearch.

Versione adattata per esecuzione in GitHub Actions: path relativi alla
root del repo (07_detection_content/rules/), non alla cartella dello script.
"""
import json
from pathlib import Path

from sigma.collection import SigmaCollection
from sigma.backends.elasticsearch import LuceneBackend

REPO_ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = REPO_ROOT / "07_detection_content" / "rules"
OUTPUT_FILE = REPO_ROOT / "07_detection_content" / "lucene_queries.json"


def main():
    backend = LuceneBackend()
    results = {}

    for rule_file in sorted(RULES_DIR.glob("**/*.yml")):
        rule_yaml = rule_file.read_text(encoding="utf-8")
        collection = SigmaCollection.from_yaml(rule_yaml)
        queries = backend.convert(collection)
        rule_title = collection.rules[0].title
        results[rule_file.name] = {"title": rule_title, "lucene_query": queries[0]}
        print(f"--- {rule_file.name} ({rule_title}) ---")
        print(queries[0])
        print()

    OUTPUT_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Query salvate in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
