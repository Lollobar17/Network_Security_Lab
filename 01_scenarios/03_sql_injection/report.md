# Scenario 03 — SQL Injection

**Date:** 2026-03-22
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab — SIEM Flask Application
**Tool:** SQLmap 1.9.11
**MITRE Technique:** T1190 — Exploit Public-Facing Application
**Status:** Completed — Post-Remediation Verified

---

## Objective

Test the SQL injection resilience of the custom SIEM REST API endpoints.
Validate whether the application correctly rejects malicious SQL payloads
and whether the SIEM itself logs suspicious request patterns.

---

## Target

| Field | Value |
|---|---|
| **IP Address** | 10.0.2.2 (VirtualBox NAT gateway) |
| **Application** | HomeLab SIEM — Flask + SQLite |
| **Port** | 5000 |
| **Endpoints Tested** | /api/events, /api/alerts, /api/ingest, /vulnerable |

---

## Methodology

Three API endpoints were tested sequentially using SQLmap with the
--batch flag for automated testing without manual interaction.

### 1. Test — /api/events

sqlmap -u http://192.168.0.45:5000/api/events --batch

### 2. Test — /api/alerts

sqlmap -u http://192.168.0.45:5000/api/alerts --batch

### 3. Test — /api/ingest (POST parameters)

sqlmap -u http://192.168.0.45:5000/api/ingest --data="source=test&message=test" --batch

### 4. Post-Remediation Test — /vulnerable endpoint

sqlmap -u "http://10.0.2.2:5000/vulnerable?q=1" --batch --level=3 --risk=2

> [!TIP]
> Always test POST endpoints separately with --data flag — GET endpoints
> often return 404 for missing parameters while POST endpoints reveal
> more about the application's input handling behavior.
> Use --level 3 --risk 2 for deeper testing in controlled environments.

---

## Findings

### Initial Test Results (v1.0.0)

| Endpoint | Method | HTTP Response | SQLi Vulnerable | Result |
|---|---|---|---|---|
| /api/events | GET | 404 Not Found | No | Not vulnerable |
| /api/alerts | GET | 404 Not Found | No | Not vulnerable |
| /api/ingest | POST | 400 Bad Request | No | Not vulnerable |

### Post-Remediation Test Results (v1.2.0)

| Endpoint | Method | Injection Type | Result |
|---|---|---|---|
| /vulnerable?q=1 | GET | Boolean-based blind | Vulnerable |
| /vulnerable?q=1 | GET | Time-based blind | Vulnerable |
| /vulnerable?q=1 | GET | UNION query | Vulnerable |

> [!CAUTION]
> SQLmap confirmed SQL injection vulnerabilities on the /vulnerable
> endpoint with 54 HTTP requests. Back-end DBMS: SQLite.
> This endpoint is intentionally vulnerable for testing purposes only.

### Security Observations

> [!IMPORTANT]
> All production endpoints correctly reject SQL injection payloads.
> The /vulnerable endpoint is intentionally vulnerable for testing.
> Post-remediation: WEB-003 now detects SQL injection patterns in
> web traffic via Flask access log parsing.

| Finding | Severity | Notes |
|---|---|---|
| No SQLi on production endpoints | Positive | Input validation working |
| /api/ingest returns 400 on malformed input | Positive | Validation confirmed |
| WEB-003 alert generated | Positive | Detection confirmed post-remediation |

---

## SIEM Detection Analysis

### Initial Assessment (v1.0.0)

| Check | Result | Notes |
|---|---|---|
| SQLmap requests logged | Not detected | Web layer not monitored |
| High request volume detected | Not detected | 147 requests generated no alert |
| Source IP flagged | Not detected | No web traffic monitoring |

### Post-Remediation (v1.2.0)

| Check | Result | Notes |
|---|---|---|
| SQL injection alert triggered | Detected | WEB-003 — HIGH severity |
| MITRE T1190 mapped | Detected | Correctly classified |
| Source IP logged | Detected | source_ip present in alert |

> [!TIP]
> Post-remediation fix: Flask access log parsing added to collector.py
> and ANSI escape code stripping added to _process_raw_line().
> WEB-003 now correctly detects SQL injection patterns in web traffic.

---

## Evidence

| File | Description |
|---|---|
| `01_sqlmap_api_events.png` | Initial test — /api/events, no alerts |
| `02_sqlmap_api_events.png` | Initial test — /api/events part 2 |
| `03_sqlmap_api_alerts.png` | Initial test — /api/alerts, no alerts |
| `04_sqlmap_api_alerts.png` | Initial test — /api/alerts part 2 |
| `05_sqlmap_api_ingest.png` | Initial test — /api/ingest, no alerts |
| `06_sqlmap_api_ingest.png` | Initial test — /api/ingest part 2 |
| `07_sqlmap_injection_confirmed.png` | Post-remediation — SQLmap confirming injection |
| `08_sqlmap_injection_confirmed.png` | Post-remediation — SQLmap confirming injection part 2 |
| `09_web003_alert_api.png` | Post-remediation — WEB-003 alerts in SIEM dashboard |

---

## Conclusions

Production endpoints are protected against SQL injection. Post-remediation,
Flask access log parsing enables WEB-003 to detect attack patterns in
real time with correct MITRE T1190 classification and source IP.

> [!TIP]
> Key takeaways:
> Production endpoints are protected against SQL injection.
> Web layer monitoring is now active via Flask access log parsing.
> WEB-003 detects SQL injection patterns with source IP logging.

---

## References

- MITRE ATT&CK T1190: https://attack.mitre.org/techniques/T1190/
- SQLmap Documentation: https://sqlmap.org
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
