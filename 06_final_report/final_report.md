# Final Security Assessment Report

**Project:** Network Security Monitoring Lab
**Tester:** Lorenzo Carta
**Date:** 2026-03-26
**SIEM Version:** HomeLab SIEM v1.0
**Classification:** Internal — Portfolio Document

---

## Executive Summary

This report presents the findings of a structured security assessment
conducted against a controlled homelab environment using industry-standard
penetration testing tools. The assessment was designed to validate the
detection capabilities of a custom-built SIEM system and identify gaps
in its current rule engine.

> [!IMPORTANT]
> Overall Assessment: Partial Detection — Improvement Required.
> Detection rate across all four scenarios: 25% (1/4).
> The SIEM correctly identifies authentication-based threats but has
> no visibility into network-level or web-layer attack activity.

| Scenario | Tool | SIEM Detection | Verdict |
|---|---|---|---|
| 01 — Network Scanning | Nmap | Not detected | Gap identified |
| 02 — SSH Brute Force | Hydra | Partial | Gap identified |
| 03 — SQL Injection | SQLmap | Not detected | Gap identified |
| 04 — Path Traversal | Manual | Not detected | Gap identified |

---

## Environment

| Component | Details |
|---|---|
| **Attacker** | Kali Linux 2025.4 — VirtualBox VM |
| **Target** | Windows 11 — Host machine |
| **SIEM** | HomeLab SIEM v1.0 — Python + Flask + SQLite |
| **Network** | VirtualBox Host-Only Adapter — 192.168.56.0/24 |
| **Test Period** | 2026-03-15 to 2026-03-26 |

---

## Scenario Results

### Scenario 01 — Network Scanning

**Tool:** Nmap 7.95
**MITRE:** T1046 — Network Service Discovery
**Result:** SIEM did not detect the scan

The Nmap scan successfully identified 4 open ports on the target:

| Port | Service | Risk |
|---|---|---|
| 135/tcp | Microsoft RPC | Medium |
| 139/tcp | NetBIOS | Medium |
| 445/tcp | SMB | High |
| 2968/tcp | Unknown | Low |

> [!CAUTION]
> Port 445 (SMB) is exposed with no detection capability. This is the
> highest risk finding of this scenario — SMB has been the vector for
> some of the most destructive attacks in recent history.

---

### Scenario 02 — SSH Brute Force

**Tool:** Hydra 9.6
**MITRE:** T1110 — Brute Force
**Result:** SIEM partially detected — 3 HIGH alerts generated

Hydra executed 3,509 login attempts at ~1,230 tries/minute.
The SIEM generated HIGH severity alerts via rule AUTH-002.

| Alert | Rule | Severity | MITRE |
|---|---|---|---|
| Root Login Attempt | AUTH-002 | HIGH | T1078 |
| Root Login Attempt | AUTH-002 | HIGH | T1078 |
| Root Login Attempt | AUTH-002 | HIGH | T1078 |

> [!IMPORTANT]
> This is the only scenario where the SIEM generated alerts.
> Detection was partial — MITRE was misclassified and source IP
> was missing from alert data.

---

### Scenario 03 — SQL Injection

**Tool:** SQLmap 1.9.11
**MITRE:** T1190 — Exploit Public-Facing Application
**Result:** No vulnerabilities found — SIEM did not detect testing

147 HTTP requests with malicious SQL payloads — zero alerts generated.

> [!TIP]
> Positive finding: the SIEM application itself is not vulnerable to
> SQL injection. Flask + SQLite with parameterized queries provides
> effective protection at the application layer.

---

### Scenario 04 — Path Traversal

**Tool:** Manual testing with curl
**MITRE:** T1083 — File and Directory Discovery
**Result:** No vulnerabilities found — SIEM did not detect testing

Three path traversal variants — all returned 404 Not Found.

> [!TIP]
> Positive finding: Flask's built-in routing prevents path traversal
> by design. No explicit input validation was needed to block these
> attacks — the framework architecture provides inherent protection.

---

## Detection Coverage Matrix

| Attack Type | MITRE | Detected | Alert Quality | Source IP |
|---|---|---|---|---|
| Network Scanning | T1046 | No | N/A | N/A |
| SSH Brute Force | T1110 | Partial | Medium | Missing |
| SQL Injection | T1190 | No | N/A | N/A |
| Path Traversal | T1083 | No | N/A | N/A |

**Detection Rate: 1/4 scenarios (25%) — partial detection only**

---

## Key Findings

> [!CAUTION]
> Finding 01 — No Network Layer Visibility
> The SIEM cannot detect inbound network scanning or reconnaissance.
> This is a critical gap — port scanning precedes virtually every attack.

> [!CAUTION]
> Finding 02 — Partial Authentication Monitoring
> SSH brute force was detected but misclassified. No correlation rules
> exist for high-volume automated attacks.

> [!CAUTION]
> Finding 03 — Web Layer Blind Spot
> Neither SQL injection nor path traversal generated any alerts.
> 147 malicious requests passed completely undetected.

> [!CAUTION]
> Finding 04 — Incomplete Alert Data
> Source IP is absent from alerts, significantly reducing incident
> response capability.

> [!CAUTION]
> Finding 05 — No CRITICAL Severity Threshold
> Zero CRITICAL alerts despite an active brute force attack with
> thousands of attempts per minute.

---

## Positive Findings

> [!TIP]
> The SIEM application correctly resists SQL injection attacks.
> Flask routing prevents path traversal by design.
> AUTH-002 rule correctly identifies root login attempts.
> MITRE ATT&CK mapping is partially implemented.
> Dashboard provides clear visual representation of alerts.

---

## Recommendations

| Priority | Recommendation | Impact |
|---|---|---|
| Critical | Add network monitoring layer (Suricata/Zeek) | Closes G-01 |
| High | Add source_ip to alert schema | Closes G-03 |
| High | Add T1110 brute force correlation rule | Closes G-04 |
| Medium | Fix MITRE classification in AUTH-002 | Closes G-02 |
| Medium | Add Flask access log parsing | Closes G-05, G-06 |
| Medium | Define CRITICAL severity thresholds | Closes G-07 |

---

## Conclusion

> [!IMPORTANT]
> This assessment demonstrates a functional but incomplete security
> monitoring capability. Implementing the recommendations would increase
> detection coverage from 25% to an estimated 75%+ across the tested
> attack scenarios.
> This project demonstrates practical application of penetration testing
> methodology, SIEM architecture analysis, and security gap identification
> in a controlled environment — skills directly applicable to enterprise
> system integration and security operations roles.

---

## References

- MITRE ATT&CK Framework: https://attack.mitre.org
- HomeLab SIEM Repository: https://github.com/Lollobar17/homelab-siem
- Network Security Monitoring Lab: https://github.com/Lollobar17/Network_Security_Lab
- PTES Standard: http://www.pentest-standard.org
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide
