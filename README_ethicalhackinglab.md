# Ethical Hacking Lab

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Type](https://img.shields.io/badge/Type-Penetration%20Testing-red)
![Environment](https://img.shields.io/badge/Environment-Controlled%20Lab-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> A structured penetration testing laboratory documenting real attack scenarios
> against a controlled environment, with full integration into a custom SIEM system.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Lab Architecture](#lab-architecture)
- [Methodology](#methodology)
- [Scenarios](#scenarios)
- [Tools Reference](#tools-reference)
- [SIEM Integration](#siem-integration)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Project Overview

This repository documents a hands-on ethical hacking laboratory built to
develop and demonstrate practical penetration testing skills in a fully
controlled and isolated environment.

Each scenario follows a structured methodology — reconnaissance, exploitation,
detection and reporting — and is integrated with a custom-built SIEM system
that monitors and alerts on every simulated attack in real time.

The lab covers both offensive and defensive perspectives, bridging the gap
between penetration testing and security monitoring.

---

## Lab Architecture

| Component | Technology |
|---|---|
| **Attacker Machine** | Kali Linux (VirtualBox VM) |
| **Target Environment** | Controlled local network |
| **SIEM / Detection** | Custom Python SIEM with MITRE ATT&CK mapping |
| **Dashboard** | Live web UI — KPIs, timeline, alert table |
| **Reporting** | Structured Markdown reports per scenario |

---

## Methodology

Each scenario follows the **PTES** (Penetration Testing Execution Standard)
framework, adapted for a lab environment:

1. **Reconnaissance** — information gathering and target profiling
2. **Threat Modeling** — identifying attack vectors
3. **Exploitation** — executing the attack in a controlled manner
4. **Detection** — verifying SIEM alerts and log collection
5. **Reporting** — documenting findings, evidence and remediation

---

## Scenarios

| # | Scenario | Tool | MITRE Technique | Status |
|---|---|---|---|---|
| 01 | Network Scanning | Nmap | T1046 — Network Service Discovery | Planned |
| 02 | SSH Brute Force | Hydra | T1110 — Brute Force | Planned |
| 03 | SQL Injection | SQLmap | T1190 — Exploit Public-Facing Application | Planned |
| 04 | Path Traversal | Manual | T1083 — File and Directory Discovery | Planned |

Each scenario includes a full report and evidence folder with screenshots
and captured logs.

---

## Tools Reference

| Tool | Purpose |
|---|---|
| **Nmap** | Network discovery and port scanning |
| **Hydra** | Brute force attacks against network services |
| **SQLmap** | Automated SQL injection detection and exploitation |
| **Wireshark** | Network traffic analysis |
| **Kali Linux** | Attacker machine with preinstalled security tools |

---

## SIEM Integration

This lab is directly integrated with the
[HomeLab SIEM](https://github.com/Lollobar17/homelab-siem) project.

Every simulated attack triggers detection rules mapped to MITRE ATT&CK
techniques, generating real-time alerts on the SIEM dashboard. This allows
documenting not only the offensive execution but also the defensive response.

---

## Roadmap

- [ ] Scenario 01 — Network Scanning (Nmap)
- [ ] Scenario 02 — SSH Brute Force (Hydra)
- [ ] Scenario 03 — SQL Injection (SQLmap)
- [ ] Scenario 04 — Path Traversal (Manual)
- [ ] Add scenario: ARP Spoofing
- [ ] Add scenario: Privilege Escalation
- [ ] Automated report generation script

---

## Disclaimer

All activities documented in this repository are performed exclusively in
a controlled, isolated lab environment owned by the author.
No tests have been or will be conducted against systems without explicit
authorization. This project is intended solely for educational purposes
and the development of defensive security skills.

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
