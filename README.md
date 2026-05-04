# Network Security Monitoring Lab

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Type](https://img.shields.io/badge/Type-System%20Integration-blue)
![Environment](https://img.shields.io/badge/Environment-Controlled%20Lab-lightgrey)
![SIEM](https://img.shields.io/badge/SIEM-Custom%20Python-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> A practical homelab project simulating real-world threat scenarios to test,
> validate and improve the detection capabilities of a custom SIEM system.
> Built as a learning environment for network security monitoring and
> system integration in regulated enterprise contexts.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Lab Architecture](#lab-architecture)
- [Methodology](#methodology)
- [Test Scenarios](#test-scenarios)
- [Quick Reference](#quick-reference)
- [SIEM Integration](#siem-integration)
- [Tools Reference](#tools-reference)
- [Key Findings](#key-findings)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Project Overview

This laboratory simulates controlled attack scenarios against an isolated
network environment to evaluate the response of a custom-built SIEM system.

The primary objective is not offensive — it is **defensive validation**.
Each scenario is designed to answer a specific question:

> "Does the monitoring system correctly detect, log and alert on this
> type of threat? If not, why — and how can it be improved?"

> [!IMPORTANT]
> This project bridges offensive simulation and defensive monitoring —
> every attack scenario is paired with a SIEM detection analysis and
> a concrete improvement recommendation. All 7 detection gaps identified
> during the initial assessment have been resolved across SIEM v1.1.0
> through v1.5.0, achieving 100% detection coverage.

This approach reflects real-world security operations in enterprise and
regulated environments, where system administrators are responsible for
ensuring infrastructure resilience and compliance with security standards.

---

## Lab Architecture

| Component | Technology | Role |
|---|---|---|
| **Attacker Node** | Kali Linux (WSL2) | Simulates external threat actor |
| **Target Environment** | Controlled local network | Isolated test infrastructure |
| **SIEM System** | Custom Python + Flask + SQLite | Detection, logging and alerting |
| **Network IDS** | Suricata — eve.json ingestion | Network-level threat detection |
| **Detection Rules** | MITRE ATT&CK mapped rule engine | 11 built-in detection rules |
| **Dashboard** | Live web UI — KPIs, timeline, alerts | Real-time monitoring interface |
| **REST API** | /api/events, /api/alerts, /api/stats | Programmatic access to SIEM data |

The SIEM system is documented separately in the
[HomeLab SIEM](https://github.com/Lollobar17/Homelab_SIEM) repository.

---

## Methodology

Each scenario follows a structured **test-detect-improve** cycle:

1. PREPARE — Define the threat scenario and expected SIEM behavior
2. SIMULATE — Execute the controlled attack using standard security tools
3. MONITOR — Observe SIEM response — alerts, logs, detection accuracy
4. DOCUMENT — Record findings, evidence and gap analysis
5. IMPROVE — Identify detection gaps and propose rule improvements

> [!TIP]
> Each scenario folder contains a full report, evidence screenshots and
> a SIEM detection analysis. Start from 01_scenarios to follow the
> assessment in chronological order.

---

## Test Scenarios

| # | Scenario | Tool | MITRE Technique | Objective | Status | Detection |
|---|---|---|---|---|---|---|
| 01 | Network Scanning | Nmap | T1046 — Network Service Discovery | Validate perimeter visibility | Completed | Detected via Suricata |
| 02 | SSH Brute Force | Hydra | T1110 — Brute Force | Test authentication monitoring | Completed | Detected — CRITICAL |
| 03 | SQL Injection | SQLmap | T1190 — Exploit Public-Facing App | Validate web layer detection | Completed | Detected — HIGH |
| 04 | Path Traversal | Manual | T1083 — File and Directory Discovery | Test file access alerting | Completed | Detected — MEDIUM |

Each scenario includes:
- Full execution documentation with initial and post-remediation results
- SIEM alert evidence (screenshots and log extracts)
- Gap analysis and improvement recommendations

---

## Quick Reference

### Network Scanning — Nmap

Basic port scan: `nmap 192.168.56.1`

Service version detection: `nmap -sV 192.168.56.1`

Full scan with OS detection: `nmap -A 192.168.56.1`

### SSH Brute Force — Hydra

Brute force SSH with wordlist: `hydra -l username -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.1`

Reduce parallel tasks: `hydra -l username -P wordlist.txt -t 4 ssh://192.168.56.1`

### SQL Injection — SQLmap

Test vulnerable endpoint: `sqlmap -u "http://10.0.2.2:5000/vulnerable?q=1" --batch --level=3 --risk=2`

### Path Traversal — curl

Basic traversal: `curl http://10.0.2.2:5000/static/../../../etc/passwd`

URL-encoded traversal: `curl http://10.0.2.2:5000/static/..%2F..%2F..%2Fetc%2Fpasswd`

> [!TIP]
> All commands above were executed from Kali Linux in a WSL2 controlled
> environment. Never run these tools against systems you do not own or
> have explicit authorization to test.

---

## SIEM Integration

Every simulated scenario is monitored in real time by the custom SIEM system.
The integration validates:

- **Detection accuracy** — does the rule engine trigger the correct alert?
- **Log completeness** — are all relevant events captured and stored?
- **Response time** — how quickly does the alert appear on the dashboard?
- **MITRE mapping** — is the technique correctly classified?
- **GeoIP enrichment** — is the source IP correctly geolocated?

> [!IMPORTANT]
> Final Detection Rate: 100% — 4/4 scenarios fully detected.
> Initial detection rate was 25% (v1.0.0). All 7 gaps resolved across
> v1.1.0 through v1.5.0. Full gap analysis and improvement roadmap
> documented in 05_gap_analysis/gap_analysis.md

---

## Tools Reference

| Tool | Purpose |
|---|---|
| **Nmap** | Network discovery and port scanning |
| **Hydra** | Brute force against network services |
| **SQLmap** | SQL injection detection and testing |
| **Kali Linux** | Security-focused Linux distribution (WSL2) |
| **Suricata** | Network intrusion detection system |

---

## Key Findings

> [!IMPORTANT]
> Final Detection Rate: 100% — all 4 scenarios fully detected.
> The SIEM correctly identifies authentication, web-layer and network-level
> threats with CRITICAL/HIGH/MEDIUM severity and GeoIP enrichment.
> Full findings are documented in 06_final_report/final_report.md

---

## Roadmap

- [x] SIEM system operational with 11 detection rules
- [x] Lab environment configured (Kali Linux + WSL2)
- [x] Scenario 01 — Network Scanning
- [x] Scenario 02 — SSH Brute Force
- [x] Scenario 03 — SQL Injection
- [x] Scenario 04 — Path Traversal
- [x] Detection gap analysis and rule improvements
- [x] Final security assessment report

---

## Disclaimer

> [!IMPORTANT]
> All activities documented in this repository are performed exclusively
> in a controlled, isolated laboratory environment owned by the author.
> No tests have been or will be conducted against systems, networks or
> infrastructure without explicit authorization.
> This project is intended solely for educational purposes and the
> development of professional skills in network security monitoring
> and system integration.

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
