# Network Security Monitoring Lab

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
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

This approach reflects real-world security operations in enterprise and
regulated environments, where system administrators are responsible for
ensuring infrastructure resilience and compliance with security standards.

---

## Lab Architecture

| Component | Technology | Role |
|---|---|---|
| **Attacker Node** | Kali Linux (VirtualBox VM) | Simulates external threat actor |
| **Target Environment** | Controlled local network | Isolated test infrastructure |
| **SIEM System** | Custom Python + Flask + SQLite | Detection, logging and alerting |
| **Detection Rules** | MITRE ATT&CK mapped rule engine | 8 built-in detection rules |
| **Dashboard** | Live web UI — KPIs, timeline, alerts | Real-time monitoring interface |
| **REST API** | /api/events, /api/alerts, /api/stats | Programmatic access to SIEM data |

The SIEM system is documented separately in the
[HomeLab SIEM](https://github.com/Lollobar17/homelab-siem) repository.

---

## Methodology

Each scenario follows a structured **test-detect-improve** cycle:

1. PREPARE — Define the threat scenario and expected SIEM behavior
2. SIMULATE — Execute the controlled attack using standard security tools
3. MONITOR — Observe SIEM response — alerts, logs, detection accuracy
4. DOCUMENT — Record findings, evidence and gap analysis
5. IMPROVE — Identify detection gaps and propose rule improvements


This methodology mirrors the responsibilities of a system integration
professional in an enterprise environment — configuring, testing and
continuously improving security infrastructure.

---

## Test Scenarios

| # | Scenario | Tool | MITRE Technique | Objective | Status |
|---|---|---|---|---|---|
| 01 | Network Scanning | Nmap | T1046 — Network Service Discovery | Validate perimeter visibility | Completed |
| 02 | SSH Brute Force | Hydra | T1110 — Brute Force | Test authentication monitoring | Planned |
| 03 | SQL Injection | SQLmap | T1190 — Exploit Public-Facing App | Validate web layer detection | Planned |
| 04 | Path Traversal | Manual | T1083 — File and Directory Discovery | Test file access alerting | Planned |

Each scenario includes:
- Full execution documentation
- SIEM alert evidence (screenshots and log extracts)
- Gap analysis and improvement recommendations

---

## SIEM Integration

Every simulated scenario is monitored in real time by the custom SIEM system.
The integration validates:

- **Detection accuracy** — does the rule engine trigger the correct alert?
- **Log completeness** — are all relevant events captured and stored?
- **Response time** — how quickly does the alert appear on the dashboard?
- **MITRE mapping** — is the technique correctly classified?

---

## Tools Reference

| Tool | Purpose |
|---|---|
| **Nmap** | Network discovery and port scanning |
| **Hydra** | Brute force against network services |
| **SQLmap** | SQL injection detection and testing |
| **Kali Linux** | Security-focused Linux distribution |
| **Wireshark** | Network traffic analysis |

---

## Key Findings

This section will be populated progressively as scenarios are completed,
documenting detection gaps identified and improvements applied to the
SIEM rule engine.

---

## Roadmap

- [x] SIEM system operational with 8 detection rules
- [x] Lab environment configured (Kali Linux + VirtualBox)
- [x] Scenario 01 — Network Scanning
- [x] Scenario 02 — SSH Brute Force
- [x] Scenario 03 — SQL Injection
- [x] Scenario 04 — Path Traversal
- [x] Detection gap analysis and rule improvements
- [x] Final security assessment report

---

## Disclaimer

All activities documented in this repository are performed exclusively in
a controlled, isolated laboratory environment owned by the author.
No tests have been or will be conducted against systems, networks or
infrastructure without explicit authorization.

This project is intended solely for educational purposes and the
development of professional skills in network security monitoring
and system integration.

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.







