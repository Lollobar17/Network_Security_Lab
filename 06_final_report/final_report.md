# Final Security Assessment Report

**Project:** Network Security Monitoring Lab
**Tester:** Lorenzo Carta
**Assessment Date:** 2026-03-26
**Last Updated:** 2026-04-21
**SIEM Version:** HomeLab SIEM v1.2.0
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
> Post-Remediation (v1.2.0): 75% detection rate — 3/4 scenarios detected.
> Remaining open gap: G-01 — Network layer visibility (planned v1.3.0).

| Scenario | Tool | Initial Detection | Post-Remediation | Verdict |
|---|---|---|---|---|
| 01 — Network Scanning | Nmap | Not detected | Not detected | G-01 Open |
| 02 — SSH Brute Force | Hydra | Partial | Full — CRITICAL | Resolved |
| 03 — SQL Injection | SQLmap | Not detected | Detected — HIGH | Resolved |
| 04 — Path Traversal | Manual | Not detected | Detected — MEDIUM | Resolved |

---

## Environment

| Component | Details |
|---|---|
| **Attacker** | Kali Linux 2025.4 — VirtualBox VM |
| **Target** | Windows 11 — Host machine |
| **SIEM** | HomeLab SIEM v1.2.0 — Python + Flask + SQLite |
| **Network** | VirtualBox NAT — 10.0.2.2 gateway |
| **Assessment Period** | 2026-03-15 to 2026-03-26 |
| **Remediation Period** | 2026-03-26 to 2026-04-21 |

---

## Scenario Results

### Scenario 01 — Network Scanning

**Tool:** Nmap 7.95
**MITRE:** T1046 — Network Service Discovery
**Status:** Not detected — G-01 Open

| Port | Service | Risk |
|---|---|---|
| 135/tcp | Microsoft RPC | Medium |
| 139/tcp | NetBIOS | Medium |
| 445/tcp | SMB | High |
| 2968/tcp | Unknown | Low |

> [!CAUTION]
> Port 445 (SMB) is exposed with no detection capability. This remains
> the most critical open finding — planned for v1.3.0 with Suricata/Zeek
> network monitoring integration.

---

### Scenario 02 — SSH Brute Force

**Tool:** Hydra 9.6
**MITRE:** T1110 — Brute Force
**Status:** Fully detected post-remediation

| Alert | Rule | Severity | MITRE | Source IP |
|---|---|---|---|---|
| Root Login Attempt | AUTH-002 | HIGH | T1110 | Present |
| SSH Brute Force High Volume | AUTH-005 | CRITICAL | T1110 | Present |
| Successful Login After Failures | AUTH-006 | CRITICAL | T1110 | Present |

> [!TIP]
> Full detection achieved post-remediation. AUTH-005 triggers CRITICAL
> after 10+ failed attempts. AUTH-006 triggers CRITICAL on post-failure
> success. Source IP present in all alerts. MITRE corrected T1078 → T1110.

---

### Scenario 03 — SQL Injection

**Tool:** SQLmap 1.9.11
**MITRE:** T1190 — Exploit Public-Facing Application
**Status:** Detected post-remediation

SQLmap confirmed injection on /vulnerable?q=1 endpoint with 54 requests:
- Boolean-based blind injection
- Time-based blind injection
- UNION query injection

| Alert | Rule | Severity | MITRE | Source IP |
|---|---|---|---|---|
| SQL Injection Attempt | WEB-003 | HIGH | T1190 | Present |

> [!TIP]
> Production endpoints are not vulnerable to SQL injection.
> WEB-003 now detects attack patterns via Flask access log parsing.
> ANSI escape code stripping added to ensure reliable log processing.

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
> WEB-001 now detects ../ patterns via Flask access log parsing.

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

### Post-Remediation (v1.2.0)

| Attack Type | MITRE | Detected | Severity | Source IP |
|---|---|---|---|---|
| Network Scanning | T1046 | No | N/A | N/A |
| SSH Brute Force | T1110 | Yes | CRITICAL | Present |
| SQL Injection | T1190 | Yes | HIGH | Present |
| Path Traversal | T1083 | Yes | MEDIUM | Present |

**Detection Rate: 75%**

---

## Gap Resolution Summary

| Gap | Description | Resolution | Version |
|---|---|---|---|
| G-01 | No network scanning detection | Pending — Suricata/Zeek | v1.3.0 |
| G-02 | MITRE misclassification | AUTH-002 T1078 → T1110 | v1.1.0 |
| G-03 | Source IP absent from alerts | source_ip added to schema | v1.2.0 |
| G-04 | No brute force volume detection | AUTH-005 CRITICAL added | v1.2.0 |
| G-05 | No web traffic detection | Flask log parsing added | v1.2.0 |
| G-06 | No path traversal detection | Resolved via G-05 fix | v1.2.0 |
| G-07 | No CRITICAL severity alerts | AUTH-005, AUTH-006, WEB-004 | v1.2.0 |

---

## Key Findings

> [!CAUTION]
> Finding 01 — No Network Layer Visibility (G-01 — Open)
> The SIEM cannot detect inbound network scanning. Planned for v1.3.0
> with Suricata/Zeek integration.

> [!TIP]
> Finding 02 — Authentication Monitoring Fully Operational
> SSH brute force now generates CRITICAL alerts with correct MITRE
> classification, source IP and high-volume correlation rules.

> [!TIP]
> Finding 03 — Web Layer Now Monitored
> Flask access log parsing enables WEB-001 and WEB-003 to detect
> path traversal and SQL injection in real time.

> [!TIP]
> Finding 04 — Alert Data Complete
> Source IP present in all alerts. CRITICAL severity thresholds defined
> and validated via stress testing.

> [!TIP]
> Finding 05 — Application Security Confirmed
> Production endpoints correctly resist SQL injection and path traversal.
> Flask architecture provides inherent protection by design.

---

## Positive Findings

> [!TIP]
> Production endpoints resist SQL injection attacks.
> Flask routing prevents path traversal by design.
> AUTH-002 correctly identifies root login attempts.
> MITRE ATT&CK mapping implemented across all rules.
> Automatic database migration ensures smooth upgrades.
> ANSI escape code stripping ensures reliable log parsing.

---

## Recommendations

| Priority | Recommendation | Gap | Status |
|---|---|---|---|
| Critical | Network monitoring layer — Suricata/Zeek | G-01 | Open — v1.3.0 |
| Complete | source_ip in alert schema | G-03 | Resolved v1.2.0 |
| Complete | T1110 brute force correlation rule | G-04 | Resolved v1.2.0 |
| Complete | MITRE classification fix AUTH-002 | G-02 | Resolved v1.1.0 |
| Complete | Flask access log parsing | G-05, G-06 | Resolved v1.2.0 |
| Complete | CRITICAL severity thresholds | G-07 | Resolved v1.2.0 |

---

## Conclusion

> [!IMPORTANT]
> This assessment demonstrates a complete security improvement cycle —
> from initial testing and gap identification to code fixes, real-world
> verification and professional documentation.
> Detection coverage improved from 25% to 75% through iterative
> remediation. The only remaining gap (G-01) requires architectural
> work planned for v1.3.0.
> This project demonstrates practical application of penetration testing
> methodology, SIEM architecture analysis, iterative improvement and
> professional documentation — skills directly applicable to enterprise
> system integration and security operations roles.

---

## References

- MITRE ATT&CK Framework: https://attack.mitre.org
- HomeLab SIEM Repository: https://github.com/Lollobar17/Homelab_SIEM
- HomeLab SIEM CHANGELOG: https://github.com/Lollobar17/Homelab_SIEM/blob/main/CHANGELOG.md
- Network Security Monitoring Lab: https://github.com/Lollobar17/Network_Security_Lab
- PTES Standard: http://www.pentest-standard.org
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide
