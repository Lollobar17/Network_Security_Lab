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

Four attack scenarios were executed across two weeks, covering network
reconnaissance, authentication attacks, web application testing and
file system enumeration. The SIEM demonstrated partial detection
capability — correctly identifying authentication-based threats while
showing significant gaps in network-level and web-layer visibility.

**Overall Assessment: Partial Detection — Improvement Required**

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

Port 445 (SMB) represents the highest risk — historically associated
with critical vulnerabilities including EternalBlue and WannaCry.
The SIEM generated no alerts, confirming a complete blind spot for
perimeter-level reconnaissance activity.

---

### Scenario 02 — SSH Brute Force

**Tool:** Hydra 9.6
**MITRE:** T1110 — Brute Force
**Result:** SIEM partially detected — 3 HIGH alerts generated

Hydra executed 3,509 login attempts at ~1,230 tries/minute against
the SSH service. The SIEM correctly detected root login attempts and
generated HIGH severity alerts via rule AUTH-002.

**SIEM Response:**

| Alert | Rule | Severity | MITRE |
|---|---|---|---|
| Root Login Attempt | AUTH-002 | HIGH | T1078 |
| Root Login Attempt | AUTH-002 | HIGH | T1078 |
| Root Login Attempt | AUTH-002 | HIGH | T1078 |

Two gaps were identified: MITRE misclassification (T1078 vs T1110)
and missing source IP in alert data.

---

### Scenario 03 — SQL Injection

**Tool:** SQLmap 1.9.11
**MITRE:** T1190 — Exploit Public-Facing Application
**Result:** No vulnerabilities found — SIEM did not detect testing activity

Three API endpoints were tested with 147 total HTTP requests.
All endpoints correctly rejected SQL injection payloads, returning
404 or 400 responses. The SIEM generated no alerts — the web layer
is not monitored by the current ruleset.

**Positive finding:** The SIEM application itself is not vulnerable
to SQL injection, demonstrating secure coding practices.

---

### Scenario 04 — Path Traversal

**Tool:** Manual testing with curl
**MITRE:** T1083 — File and Directory Discovery
**Result:** No vulnerabilities found — SIEM did not detect testing activity

Three path traversal variants were tested — basic, static path and
URL-encoded. All returned 404 Not Found, confirming Flask's built-in
routing prevents directory escape by design.

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

### Finding 01 — No Network Layer Visibility
The SIEM has no ability to detect inbound network scanning or
reconnaissance activity. This represents a critical gap for
early-stage attack detection.

### Finding 02 — Partial Authentication Monitoring
SSH brute force was detected but misclassified. The SIEM correctly
identifies individual suspicious login attempts but lacks correlation
rules to detect high-volume automated attacks as a distinct threat.

### Finding 03 — Web Layer Blind Spot
Neither SQL injection attempts nor path traversal attacks triggered
any SIEM alerts. The web application layer is completely unmonitored.

### Finding 04 — Incomplete Alert Data
Alerts do not include source IP addresses, significantly reducing
their value for incident response and forensic investigation.

### Finding 05 — No CRITICAL Severity Threshold
Despite an active brute force attack with thousands of attempts,
the maximum alert severity generated was HIGH. No conditions for
CRITICAL severity are currently defined.

---

## Positive Findings

- The SIEM application correctly resists SQL injection attacks
- Flask routing prevents path traversal by design
- AUTH-002 rule correctly identifies root login attempts
- MITRE ATT&CK mapping is partially implemented
- Dashboard provides clear visual representation of alerts

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

This assessment demonstrates a functional but incomplete security
monitoring capability. The HomeLab SIEM successfully detects
authentication-based threats but lacks visibility into network-level
and web-layer attack activity.

The identified gaps provide a clear and actionable improvement roadmap.
Implementing the recommendations — particularly network-level monitoring
and brute force correlation rules — would significantly increase the
detection coverage from 25% to an estimated 75%+ across the tested
attack scenarios.

This project demonstrates practical application of penetration testing
methodology, SIEM architecture analysis, and security gap identification
in a controlled environment — skills directly applicable to enterprise
system integration and security operations roles.

---

## References

- MITRE ATT&CK Framework: https://attack.mitre.org
- HomeLab SIEM Repository: https://github.com/Lollobar17/homelab-siem
- Network Security Monitoring Lab: https://github.com/Lollobar17/Network_Security_Lab
- PTES Standard: http://www.pentest-standard.org
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide

