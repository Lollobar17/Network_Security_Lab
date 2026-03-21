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

