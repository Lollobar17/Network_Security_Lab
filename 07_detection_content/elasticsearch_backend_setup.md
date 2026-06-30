# Elasticsearch Backend — Validation Notes

> This file documents that the 8 Sigma rules in this directory were
> converted into real Lucene queries (via `pysigma-backend-elasticsearch`)
> and executed against a live Elasticsearch instance, not just matched
> with a hand-written Python evaluator.

The actual backend setup (Docker Compose, conversion scripts, test
data) lives outside this repository, as local development tooling —
it is not part of the portfolio artifact itself, only used to validate
that the rules translate correctly into a real detection engine query
language.

---

## Why this step matters

The offline test runner (`tests/test_rules.py`) evaluates rule logic
directly against Python dicts — useful for fast iteration, but it is
a custom evaluator, not a production detection engine. This step closes
that gap: the same Sigma YAML rules are converted by `pySigma` into
Lucene query strings and executed by a real Elasticsearch instance,
proving the rules are engine-compatible, not just logically consistent
in a bespoke script.

---

## Setup (local, not versioned)

```bash
pip install pysigma pysigma-backend-elasticsearch elasticsearch --break-system-packages
docker compose up -d   # single-node Elasticsearch, ~1GB RAM
```

## Conversion

Each rule is converted from Sigma YAML to a Lucene `query_string`:

```python
from sigma.collection import SigmaCollection
from sigma.backends.elasticsearch import LuceneBackend

rule = SigmaCollection.from_yaml(open("rules/lolbins/powershell_encoded.yml").read())
backend = LuceneBackend()
query = backend.convert(rule)[0]
```

Example output for `powershell_encoded.yml`:

```
(Image:(*\\powershell.exe OR *\\pwsh.exe)) AND
(CommandLine:(*\-enc* OR *\-EncodedCommand* OR *\-e\ *)) AND
(CommandLine:(*\-w\ hidden* OR *\-windowstyle\ hidden* OR *\-nop* OR *\-noni* OR *\-noP* OR *\-w\ 1*))
```

All 8 rules converted cleanly, including the rules using `NOT` logic
for whitelist filtering (`supply_chain_manifest_tampering.yml`,
`supply_chain_build_exfil.yml`).

## Execution

The converted queries were indexed and executed against the same
Mordor dataset (`empire_launcher_vbs`, APT29 emulation Day 1) used in
the offline test. The `powershell_encoded.yml` rule correctly matched
the single real attack event present in the dataset, with the
Elasticsearch engine returning the result via `query_string` search —
confirming consistency between the offline evaluator and a real
detection backend.

---

## Next steps

- Swap `LuceneBackend` for a KQL backend to target Microsoft
  Sentinel / Log Analytics directly, consistent with the Azure
  integration already built in Homelab_SIEM.
- Expand validation with broader Mordor datasets covering ransomware
  precursor and supply chain techniques (currently validated only via
  synthetic events for those categories).
