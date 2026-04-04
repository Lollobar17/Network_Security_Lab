# Final Security Assessment Report

**Project:** Network Security Monitoring Lab
**Tester:** Lorenzo Carta
**Assessment Date:** 2026-03-26
**Last Updated:** 2026-03-28
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
> Initial Assessment (v1.0.0): Partial Detection — 25% detection rate.
> Post-remediation (v1.2.0): 6 out of 7 gaps resolved.
> Remaining open gap: G-01 — Network layer visibility (planned v1.3.0).

| Scenario | Tool | SIEM Detection | Verdict |
|---|---|---|---|
| 01 — Network Scanning | Nmap | Not detected | Gap G-01 — Open |
| 02 — SSH Brute Force | Hydra | Partial | Gaps G-02, G-03, G-04 — Resolved |
| 03 — SQL Injection | SQLmap | Not detected | Gaps G-05 — Resolved |
| 04 — Path Traversal | Manual | Not detected | Gap G-06 — Resolved |

---

## Environment

| Component | Details |
|---|---|
| **Attacker** | Kali Linux 2025.4 — VirtualBox VM |
| **Target** | Windows 11 — Host machine |
| **SIEM** | HomeLab SIEM v1.2.0 — Python + Flask + SQLite |
| **Network** | VirtualBox Host-Only Adapter — 192.168.56.0/24 |
| **Assessment Period** | 2026-03-15 to 2026-03-26 |
| **Remediation Period** | 2026-03-26 to 2026-03-28 |

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
> highest risk finding — SMB has been the vector for some of the most
> destructive attacks in recent history including EternalBlue and WannaCry.

---

### Scenario 02 — SSH Brute Force

**Tool:** Hydra 9.6
**MITRE:** T1110 — Brute Force
**Result:** SIEM partially detected — gaps now resolved in v1.2.0

Hydra executed 3,509 login attempts at ~1,230 tries/minute.

| Alert | Rule | Severity | MITRE | Status |
|---|---|---|---|---|
| Root Login Attempt | AUTH-002 | HIGH | T1110 | Fixed — T1078 → T1110 |
| SSH Brute Force High Volume | AUTH-005 | CRITICAL | T1110 | New in v1.2.0 |
| Source IP in alerts | — | — | — | Added in v1.2.0 |

> [!TIP]
> Post-remediation: AUTH-005 now correctly identifies high-volume brute
> force attacks with CRITICAL severity and includes source IP in alert data.

---

### Scenario 03 — SQL Injection

**Tool:** SQLmap 1.9.11
**MITRE:** T1190 — Exploit Public-Facing Application
**Result:** No vulnerabilities found — web layer detection now added

147 HTTP requests with malicious SQL payloads — zero alerts at time of test.

> [!TIP]
> Positive finding: the SIEM application itself is not vulnerable to
> SQL injection. Post-remediation: Flask access log parsing added in
> v1.2.0 — WEB-003 now detects SQL injection patterns in web traffic.

---

### Scenario 04 — Path Traversal

**Tool:** Manual testing with curl
**MITRE:** T1083 — File and Directory Discovery
**Result:** No vulnerabilities found — path traversal detection now added

Three path traversal variants — all returned 404 Not Found.

> [!TIP]
> Positive finding: Flask routing prevents path traversal by design.
> Post-remediation: Flask access log parsing added in v1.2.0 — WEB-001
> now detects ../ patterns in HTTP requests.

---

## Detection Coverage Matrix

### At Time of Assessment (v1.0.0)

| Attack Type | MITRE | Detected | Alert Quality | Source IP |
|---|---|---|---|---|
| Network Scanning | T1046 | No | N/A | N/A |
| SSH Brute Force | T1110 | Partial | Medium | Missing |
| SQL Injection | T1190 | No | N/A | N/A |
| Path Traversal | T1083 | No | N/A | N/A |

**Detection Rate: 25% — partial detection only**

### Post-Remediation (v1.2.0)

| Attack Type | MITRE | Detected | Alert Quality | Source IP |
|---|---|---|---|---|
| Network Scanning | T1046 | No | N/A | N/A |
| SSH Brute Force | T1110 | Yes | CRITICAL | Present |
| SQL Injection | T1190 | Yes | HIGH | Present |
| Path Traversal | T1083 | Yes | MEDIUM | Present |

**Detection Rate: 75% — significant improvement**

---

## Gap Resolution Summary

| Gap | Description | Resolution | Version |
|---|---|---|---|
| G-01 | No network scanning detection | Pending — Suricata/Zeek integration | v1.3.0 |
| G-02 | MITRE misclassification | AUTH-002 updated T1078 → T1110 | v1.1.0 |
| G-03 | Source IP absent from alerts | source_ip added to alert schema | v1.2.0 |
| G-04 | No brute force volume detection | AUTH-005 CRITICAL rule added | v1.2.0 |
| G-05 | No web traffic detection | Flask access log parser added | v1.2.0 |
| G-06 | No path traversal detection | Resolved via G-05 fix | v1.2.0 |
| G-07 | No CRITICAL severity alerts | AUTH-005, AUTH-006, WEB-004 added | v1.2.0 |

---

## Key Findings

> [!CAUTION]
> Finding 01 — No Network Layer Visibility (G-01 — Open)
> The SIEM still cannot detect inbound network scanning. This remains
> the most critical open gap — planned for v1.3.0 with Suricata/Zeek.

> [!TIP]
> Finding 02 — Authentication Monitoring Improved
> SSH brute force now generates CRITICAL alerts with correct MITRE
> classification and source IP. Detection quality significantly improved.

> [!TIP]
> Finding 03 — Web Layer Now Monitored
> Flask access log parsing added — SQL injection and path traversal
> patterns are now detected by existing WEB rules.

> [!TIP]
> Finding 04 — Alert Data Now Complete
> Source IP included in all alerts — incident response capability
> significantly improved.

> [!TIP]
> Finding 05 — CRITICAL Severity Now Active
> Three new CRITICAL rules defined and tested — AUTH-005, AUTH-006
> and WEB-004 validated via stress test.

---

## Positive Findings

> [!TIP]
> The SIEM application correctly resists SQL injection attacks.
> Flask routing prevents path traversal by design.
> AUTH-002 rule correctly identifies root login attempts.
> MITRE ATT&CK mapping implemented across all rules.
> Dashboard provides clear visual representation of alerts.
> Automatic database migration ensures smooth upgrades.

---

## Recommendations

| Priority | Recommendation | Gap | Status |
|---|---|---|---|
| Critical | Add network monitoring layer (Suricata/Zeek) | G-01 | Open |
| Complete | source_ip added to alert schema | G-03 | Resolved v1.2.0 |
| Complete | T1110 brute force correlation rule | G-04 | Resolved v1.2.0 |
| Complete | MITRE classification fix AUTH-002 | G-02 | Resolved v1.1.0 |
| Complete | Flask access log parsing | G-05, G-06 | Resolved v1.2.0 |
| Complete | CRITICAL severity thresholds | G-07 | Resolved v1.2.0 |

---

## Conclusion

> [!IMPORTANT]
> This assessment demonstrates a complete security improvement cycle —
> from initial testing and gap identification to code fixes, testing
> and documentation. Detection coverage improved from 25% to 75%.
> The only remaining gap (G-01) requires architectural work planned
> for v1.3.0.
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
