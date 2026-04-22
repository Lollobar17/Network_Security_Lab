# Scenario 04 — Path Traversal

**Date:** 2026-03-23
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab — SIEM Flask Application
**Tool:** curl (manual testing)
**MITRE Technique:** T1083 — File and Directory Discovery
**Status:** Completed — Post-Remediation Verified

---

## Objective

Test the path traversal resilience of the custom SIEM web application.
Attempt to access files outside the application root directory using
various traversal techniques, including basic, static-path and
URL-encoded variants.

---

## Target

| Field | Value |
|---|---|
| **IP Address** | 10.0.2.2 (VirtualBox NAT gateway) |
| **Application** | HomeLab SIEM — Flask |
| **Port** | 5000 |
| **Target File** | /etc/passwd (Linux system file) |

---

## Methodology

Three path traversal variants were tested manually using curl from
the Kali Linux terminal.

### 1. Basic Path Traversal

curl http://10.0.2.2:5000/static/../../../etc/passwd

### 2. Static Path Traversal

curl http://10.0.2.2:5000/static/../../../etc/passwd

### 3. URL-Encoded Path Traversal

curl http://10.0.2.2:5000/static/..%2F..%2F..%2Fetc%2Fpasswd

> [!TIP]
> Always test URL-encoded variants — many applications sanitize literal
> ../ sequences but fail to decode and check encoded equivalents.
> Additional variants to test include double encoding (%252F) and
> mixed encoding to bypass WAF rules.

---

## Findings

### Initial Test Results (v1.0.0)

| Test | Technique | HTTP Response | Vulnerable | SIEM Alert |
|---|---|---|---|---|
| 01 | Basic traversal | 404 Not Found | No | Not detected |
| 02 | Static path traversal | 404 Not Found | No | Not detected |
| 03 | URL-encoded traversal | 404 Not Found | No | Not detected |

### Post-Remediation Test Results (v1.2.0)

| Test | Technique | HTTP Response | Vulnerable | SIEM Alert |
|---|---|---|---|---|
| 01 | Basic traversal | 404 Not Found | No | WEB-001 detected |

> [!IMPORTANT]
> Flask correctly blocks path traversal — 404 returned for all variants.
> Post-remediation: WEB-001 now detects the ../ pattern in the request
> path and generates a MEDIUM alert with source IP.

### Security Observations

| Finding | Severity | Notes |
|---|---|---|
| No path traversal vulnerability detected | Positive | All variants correctly rejected |
| Flask default routing prevents directory escape | Positive | Framework-level protection working |
| WEB-001 alert generated | Positive | Detection confirmed post-remediation |

---

## SIEM Detection Analysis

### Initial Assessment (v1.0.0)

| Check | Result | Notes |
|---|---|---|
| Traversal attempts logged | Not detected | Web layer not monitored |
| Anomalous URL patterns detected | Not detected | ../ sequences generated no alert |
| Source IP flagged | Not detected | No web traffic monitoring |

### Post-Remediation (v1.2.0)

| Check | Result | Notes |
|---|---|---|
| Traversal alert triggered | Detected | WEB-001 — MEDIUM severity |
| MITRE T1083 mapped | Detected | Correctly classified |
| Source IP logged | Detected | source_ip present in alert |

> [!TIP]
> Post-remediation fix: Flask access log parsing added to collector.py
> enables WEB-001 to detect ../ patterns in HTTP request paths.
> ANSI escape code stripping ensures reliable log parsing.

---

## Evidence

| File | Description |
|---|---|
| `path_traversal_tests.png` | Initial test — all three curl variants, no alerts |
| `web001_alert_api.png` | Post-remediation — WEB-001 alert in SIEM dashboard |

---

## Conclusions

All three path traversal variants were successfully blocked by Flask.
The server returned 404 Not Found for every attempt, confirming that
the application is not vulnerable to directory traversal attacks.

Post-remediation, the addition of Flask access log parsing enabled
WEB-001 to detect the ../ traversal pattern and generate a MEDIUM
severity alert with correct MITRE T1083 classification.

> [!TIP]
> Key takeaways:
> Flask routing prevents path traversal by design.
> WEB-001 now detects traversal attempts in real time.
> Source IP is correctly logged in all web alerts.

---

## References

- MITRE ATT&CK T1083: https://attack.mitre.org/techniques/T1083/
- OWASP Path Traversal: https://owasp.org/www-community/attacks/Path_Traversal
- Flask Security: https://flask.palletsprojects.com/en/stable/security/
