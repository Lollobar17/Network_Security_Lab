# Final Security Assessment Report

**Project:** Network Security Monitoring Lab
**Tester:** Lorenzo Carta
**Assessment Date:** 2026-03-26
**Last Updated:** 2026-05-03
**SIEM Version:** HomeLab SIEM v1.5.0
**Classification:** Internal — Portfolio Document

---

## Executive Summary

This report presents the findings of a structured security assessment
conducted against a controlled homelab environment using industry-standard
penetration testing tools. The assessment was designed to validate the
detection capabilities of a custom-built SIEM system and identify gaps
in its current rule engine.

> [!IMPORTANT]
> Initial Assessment (v1.0.0): 25% detection rate — 1/4 scenarios detected.
> Final Status (v1.5.0): 100% detection rate — 4/4 scenarios detected.
> All 7 detection gaps identified during assessment have been resolved.

| Scenario | Tool | Initial Detection | Final Detection | Verdict |
|---|---|---|---|---|
| 01 — Network Scanning | Nmap | Not detected | Detected — HIGH | Resolved — G-01 |
| 02 — SSH Brute Force | Hydra | Partial | Full — CRITICAL | Resolved — G-02/03/04 |
| 03 — SQL Injection | SQLmap | Not detected | Detected — HIGH | Resolved — G-05 |
| 04 — Path Traversal | Manual | Not detected | Detected — MEDIUM | Resolved — G-06 |

---

## Environment

| Component | Details |
|---|---|
| **Attacker** | Kali Linux — WSL2 native instance |
| **Target** | Windows 11 — Host machine |
| **SIEM** | HomeLab SIEM v1.5.0 — Python + Flask + SQLite |
| **Network IDS** | Suricata — eve.json live ingestion |
| **Network** | WSL2 virtual network — localhost bridge |
| **Assessment Period** | 2026-03-15 to 2026-03-26 |
| **Remediation Period** | 2026-03-26 to 2026-05-03 |

> [!NOTE]
> The lab environment was migrated from VirtualBox to WSL2 + Docker during
> the remediation phase, resolving a critical Hyper-V conflict that caused
> VM instability. Kali Linux now runs natively via WSL2 with direct Docker
> socket integration, improving stability and network visibility.

---

## Scenario Results

### Scenario 01 — Network Scanning

**Tool:** Nmap 7.95
**MITRE:** T1046 — Network Service Discovery
**Status:** Detected post-remediation via Suricata integration

| Port | Service | Risk |
|---|---|---|
| 135/tcp | Microsoft RPC | Medium |
| 139/tcp | NetBIOS | Medium |
| 445/tcp | SMB | High |
| 2968/tcp | Unknown | Low |

> [!TIP]
> Suricata integration added in v1.5.0 provides network-level visibility.
> Port scanning activity is now detected in real time via eve.json ingestion.
> This closes G-01 — the last remaining detection gap.

---

### Scenario 02 — SSH Brute Force

**Tool:** Hydra 9.6
**MITRE:** T1110 — Brute Force
**Status:** Fully detected — CRITICAL severity

| Alert | Rule | Severity | MITRE | Source IP |
|---|---|---|---|---|
| Root Login Attempt | AUTH-002 | HIGH | T1110 | Present |
| SSH Brute Force High Volume | AUTH-005 | CRITICAL | T1110 | Present |
| Successful Login After Failures | AUTH-006 | CRITICAL | T1110 | Present |

> [!TIP]
> Full detection achieved in v1.2.0. AUTH-005 triggers CRITICAL after
> 10+ failed attempts. AUTH-006 triggers CRITICAL on post-failure success.
> Source IP and GeoIP data present in all alerts.

---

### Scenario 03 — SQL Injection

**Tool:** SQLmap 1.9.11
**MITRE:** T1190 — Exploit Public-Facing Application
**Status:** Detected post-remediation

SQLmap confirmed injection on /vulnerable?q=1 with 54 requests:
- Boolean-based blind injection
- Time-based blind injection
- UNION query injection

| Alert | Rule | Severity | MITRE | Source IP |
|---|---|---|---|---|
| SQL Injection Attempt | WEB-003 | HIGH | T1190 | Present |

> [!TIP]
> Production endpoints are not vulnerable to SQL injection.
> WEB-003 detects attack patterns via Flask access log parsing added in v1.2.0.

---

### Scenario 04 — Path Traversal

**Tool:** Manual testing with curl
**MITRE:** T1083 — File and Directory Discovery
**Status:** Detected post-remediation

Three variants tested — all returned 404 Not Found. Flask routing
prevents directory traversal by design.

| Alert | Rule | Severity | MITRE | Source IP |
|---|---|---|---|---|
| HTTP Scanner / Directory Traversal | WEB-001 | MEDIUM | T1083 | Present |

> [!TIP]
> Flask routing prevents path traversal by design.
> WEB-001 detects ../ patterns via Flask access log parsing added in v1.2.0.

---

## Detection Coverage Matrix

### Initial Assessment (v1.0.0)

| Attack Type | MITRE | Detected | Severity | Source IP |
|---|---|---|---|---|
| Network Scanning | T1046 | No | N/A | N/A |
| SSH Brute Force | T1110 | Partial | HIGH | Missing |
| SQL Injection | T1190 | No | N/A | N/A |
| Path Traversal | T1083 | No | N/A | N/A |

**Detection Rate: 25%**

### Final Status (v1.5.0)

| Attack Type | MITRE | Detected | Severity | Source IP | GeoIP |
|---|---|---|---|---|---|
| Network Scanning | T1046 | Yes | HIGH | Present | Present |
| SSH Brute Force | T1110 | Yes | CRITICAL | Present | Present |
| SQL Injection | T1190 | Yes | HIGH | Present | Present |
| Path Traversal | T1083 | Yes | MEDIUM | Present | Present |

**Detection Rate: 100%**

---

## Gap Resolution Summary

| Gap | Description | Resolution | Version |
|---|---|---|---|
| G-01 | No network scanning detection | Suricata integration + eve.json ingestion | v1.5.0 |
| G-02 | MITRE misclassification | AUTH-002 T1078 → T1110 | v1.1.0 |
| G-03 | Source IP absent from alerts | source_ip added to alert schema | v1.2.0 |
| G-04 | No brute force volume detection | AUTH-005 CRITICAL rule added | v1.2.0 |
| G-05 | No web traffic detection | Flask access log parser added | v1.2.0 |
| G-06 | No path traversal detection | Resolved via G-05 fix | v1.2.0 |
| G-07 | No CRITICAL severity alerts | AUTH-005, AUTH-006, WEB-004 added | v1.2.0 |

---

## Key Findings

> [!TIP]
> Finding 01 — Network Layer Visibility Achieved (G-01 — Resolved)
> Suricata integration provides real-time network-level detection.
> Port scanning and intrusion attempts are now detected via eve.json ingestion.

> [!TIP]
> Finding 02 — Authentication Monitoring Fully Operational
> SSH brute force generates CRITICAL alerts with correct MITRE classification,
> source IP, GeoIP enrichment and high-volume correlation rules.

> [!TIP]
> Finding 03 — Web Layer Fully Monitored
> Flask access log parsing enables WEB-001 and WEB-003 to detect path
> traversal and SQL injection in real time with source IP and GeoIP data.

> [!TIP]
> Finding 04 — Alert Data Complete
> Source IP and GeoIP enrichment present in all alerts. CRITICAL severity
> thresholds defined and validated via stress testing.

> [!TIP]
> Finding 05 — Application Security Confirmed
> Production endpoints correctly resist SQL injection and path traversal.
> Flask architecture provides inherent protection by design.

---

## Positive Findings

> [!TIP]
> Production endpoints resist SQL injection attacks.
> Flask routing prevents path traversal by design.
> All detection rules mapped to MITRE ATT&CK techniques.
> GeoIP enrichment provides geographic context for all alerts.
> Discord webhook delivers real-time notifications for HIGH/CRITICAL alerts.
> Automatic database migration ensures smooth upgrades.
> Docker Compose enables reproducible deployment on any platform.
> Backup and recovery scripts ensure operational resilience.

---

## Recommendations

| Priority | Recommendation | Gap | Status |
|---|---|---|---|
| Complete | Suricata network monitoring | G-01 | Resolved v1.5.0 |
| Complete | source_ip in alert schema | G-03 | Resolved v1.2.0 |
| Complete | T1110 brute force correlation rule | G-04 | Resolved v1.2.0 |
| Complete | MITRE classification fix AUTH-002 | G-02 | Resolved v1.1.0 |
| Complete | Flask access log parsing | G-05, G-06 | Resolved v1.2.0 |
| Complete | CRITICAL severity thresholds | G-07 | Resolved v1.2.0 |

---

## Conclusion

> [!IMPORTANT]
> This assessment demonstrates a complete security improvement cycle —
> from initial testing and gap identification to architectural changes,
> code fixes, real-world verification and professional documentation.
> Detection coverage improved from 25% to 100% through iterative
> remediation across five releases (v1.1.0 through v1.5.0).
> All 7 gaps identified during the initial assessment have been resolved.
> This project demonstrates practical application of penetration testing
> methodology, SIEM architecture analysis, network intrusion detection,
> iterative improvement and professional documentation — skills directly
> applicable to enterprise system integration and security operations roles.

---

## References

- MITRE ATT&CK Framework: https://attack.mitre.org
- HomeLab SIEM Repository: https://github.com/Lollobar17/Homelab_SIEM
- HomeLab SIEM CHANGELOG: https://github.com/Lollobar17/Homelab_SIEM/blob/main/CHANGELOG.md
- Network Security Monitoring Lab: https://github.com/Lollobar17/Network_Security_Lab
- Suricata Documentation: https://suricata.readthedocs.io
- PTES Standard: http://www.pentest-standard.org
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide
