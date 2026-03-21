# Scenario 01 — Network Scanning

**Date:** 2026-03-20
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab — VirtualBox NAT Network
**Tool:** Nmap 7.95
**MITRE Technique:** T1046 — Network Service Discovery
**Status:** Completed

---

## Objective

Perform a network reconnaissance scan against the host machine to identify
open ports and running services. Validate whether the SIEM system correctly
detects and logs port scanning activity as a potential threat.

---

## Target

| Field | Value |
|---|---|
| **IP Address** | 192.168.56.1 |
| **OS** | Microsoft Windows |
| **Role** | VirtualBox Host Machine |
| **Network** | VirtualBox Host-Only Adapter |

---

## Methodology

### 1. Reconnaissance — Basic Scan

Command executed from Kali Linux terminal:

nmap 192.168.56.1

Result: Host up — 4 open ports identified.

### 2. Service Version Detection

Command executed from Kali Linux terminal:

nmap -sV 192.168.56.1

Result: Service versions and OS fingerprint successfully retrieved.

---

## Findings

### Open Ports — Basic Scan

| Port | State | Service |
|---|---|---|
| 135/tcp | open | msrpc |
| 139/tcp | open | netbios-ssn |
| 445/tcp | open | microsoft-ds |
| 2968/tcp | open | enpp |

### Service Version Detection

| Port | State | Service | Version |
|---|---|---|---|
| 135/tcp | open | msrpc | Microsoft Windows RPC |
| 139/tcp | open | netbios-ssn | Microsoft Windows NetBIOS |
| 445/tcp | open | microsoft-ds | Microsoft Windows SMB |
| 2968/tcp | open | enpp | Unknown |

**OS Detection:** Windows (CPE: cpe:/o:microsoft:windows)

### Security Observations

| Port | Risk | Notes |
|---|---|---|
| 135/tcp | Medium | RPC endpoint mapper — commonly targeted for lateral movement |
| 139/tcp | Medium | NetBIOS — legacy protocol, should be disabled if not required |
| 445/tcp | High | SMB — historically vulnerable (EternalBlue, WannaCry) |
| 2968/tcp | Low | Unknown service — requires further investigation |

---

## SIEM Detection Analysis

| Check | Result | Notes |
|---|---|---|
| Port scan alert triggered | To be verified | Requires SIEM log review |
| MITRE T1046 mapped | To be verified | Rule engine check required |
| Log entry created | To be verified | Check /api/events endpoint |

---

## Evidence

| File | Description |
|---|---|
| `VirtualBox_Kali_Linux_20_03_2026_15_04_25.png` | Nmap scan output — both basic and service version scans |

---

## Conclusions

The network scan successfully identified 4 open ports on the target host,
including port 445 (SMB) which represents a significant attack surface in
enterprise environments. The presence of legacy protocols such as NetBIOS
(139) highlights the importance of network hardening in regulated contexts.

The next step is to verify whether the SIEM correctly detected and logged
the scanning activity, and to review the alert mapping against MITRE T1046.

---

## References

- MITRE ATT&CK T1046: https://attack.mitre.org/techniques/T1046/
- Nmap Documentation: https://nmap.org/docs.html
- Microsoft SMB Security: https://docs.microsoft.com/en-us/windows/security

