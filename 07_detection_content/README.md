# 07 — Detection Content (Sigma Rules)

> Detection-engineering content developed independently from the SIEM
> custom rule engine, using the open Sigma standard. Goal: build and
> validate detection logic for current, real-world adversary techniques,
> testable against both public threat datasets and synthetic events.

---

## Overview

This section contains 8 Sigma rules across three technique categories,
each mapped to MITRE ATT&CK and validated with `pySigma` for syntax/schema
correctness. Detection logic is tested against a public dataset
(OTRF/Security-Datasets — "Mordor") and against synthetic events for
techniques not represented in the available public dataset.

| Category | Rules | Focus |
|---|---|---|
| **LOLBins** | 2 | Abuse of legitimate signed Windows binaries (PowerShell, certutil) to evade detection |
| **Ransomware Precursor** | 3 | Pre-encryption behaviors: shadow copy deletion, Defender tampering, mass file discovery |
| **Supply Chain** | 3 | CI/CD and package manager abuse: malicious install hooks, manifest tampering, build-time exfiltration |

---

## Rules Reference

### LOLBins

| Rule | MITRE | Level |
|---|---|---|
| `powershell_encoded.yml` | T1059.001 | High |
| `certutil_abuse.yml` | T1140 / T1105 | High |

### Ransomware Precursor

| Rule | MITRE | Level |
|---|---|---|
| `shadow_copy_deletion.yml` | T1490 | Critical |
| `defender_disabled.yml` | T1562.001 | High |
| `mass_file_enum.yml` | T1083 / T1486 | Medium |

### Supply Chain

| Rule | MITRE | Level |
|---|---|---|
| `supply_chain_install_hook.yml` | T1195.001 / T1059 | High |
| `supply_chain_manifest_tampering.yml` | T1195.001 | Medium |
| `supply_chain_build_exfil.yml` | T1195.002 / T1041 | High |

---

## Methodology

1. **WRITE** — Author the Sigma rule (YAML) with explicit MITRE mapping and false-positive notes.
2. **VALIDATE** — Parse and validate schema/syntax with `pySigma` (`SigmaCollection.from_yaml`).
3. **TEST** — Run detection logic against:
   - Public dataset (Mordor / Security-Datasets) where the technique is represented
   - Synthetic events for techniques not covered by the available dataset
4. **DOCUMENT** — Record true positive / false positive behavior per rule.

> [!NOTE]
> The current test runner (`tests/test_rules.py`) evaluates rule logic
> directly against Python dicts (parsed log events). `pySigma` is used
> for rule validation, not yet for query generation against a live
> backend. A backend conversion step (Elasticsearch Lucene or
> Sentinel/KQL) is the planned next iteration, to point these same
> rules at a real index instead of static datasets.

---

## Test Results

Validated against `empire_launcher_vbs` (OTRF/Security-Datasets, APT29
emulation, Day 1) — 2067 log lines, 5 Sysmon Process Creation events.

| Rule | Dataset Match | Synthetic Match | False Positives |
|---|---|---|---|
| PowerShell Encoded Command | 1/1 (true positive) | — | 0/4 other process events |
| Certutil Abuse | 0 (technique not in dataset) | 1/1 | — |
| Shadow Copy Deletion | 0 (technique not in dataset) | 1/1 | — |
| Defender Disabled | 0 (technique not in dataset) | 1/1 | — |
| Mass File Enumeration | 0 (technique not in dataset) | 1/1 | — |
| Supply Chain Install Hook | n/a (no CI/CD dataset) | 1/1 | — |
| Manifest Tampering | n/a | 1/1 positive, 0/1 whitelist (npm) | 0 |
| Build Exfiltration | n/a | 1/1 positive, 0/1 whitelist (registry.npmjs.org) | 0 |

> [!IMPORTANT]
> The PowerShell Encoded Command rule correctly identified the single
> real attack event out of 5 process creation events in the dataset,
> with zero false positives on the remaining benign processes
> (wscript, conhost).

---

## Running the Tests

```bash
pip install pysigma --break-system-packages
cd 07_detection_content/tests
python3 test_rules.py
```

---

## Roadmap

- [x] LOLBins rules (PowerShell, certutil)
- [x] Ransomware precursor rules (shadow copy, Defender, file enumeration)
- [x] Supply chain rules (install hooks, manifest tampering, build exfiltration)
- [x] Validation against public dataset (Mordor APT29 Day 1)
- [ ] Backend conversion (Elasticsearch Lucene / Sentinel KQL) for live index testing
- [ ] Additional dataset coverage for ransomware precursor and supply chain categories
- [ ] CI/CD integration — run rule validation automatically on push (GitHub Actions)
