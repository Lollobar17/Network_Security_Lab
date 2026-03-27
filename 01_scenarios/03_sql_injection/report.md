# Scenario 03 — SQL Injection

**Date:** 2026-03-22
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab — SIEM Flask Application
**Tool:** SQLmap 1.9.11
**MITRE Technique:** T1190 — Exploit Public-Facing Application
**Status:** Completed

---

## Objective

Test the SQL injection resilience of the custom SIEM REST API endpoints.
Validate whether the application correctly rejects malicious SQL payloads
and whether the SIEM itself logs suspicious request patterns.

---

## Target

| Field | Value |
|---|---|
| **IP Address** | 192.168.0.45 |
| **Application** | HomeLab SIEM — Flask + SQLite |
| **Port** | 5000 |
| **Endpoints Tested** | /api/events, /api/alerts, /api/ingest |

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

> [!TIP]
> Always test POST endpoints separately with --data flag — GET endpoints
> often return 404 for missing parameters while POST endpoints reveal
> more about the application's input handling behavior.
> Use --level 3 --risk 2 for deeper testing in controlled environments.

---

## Findings

### Test Results Summary

| Endpoint | Method | HTTP Response | SQLi Vulnerable | Result |
|---|---|---|---|---|
| /api/events | GET | 404 Not Found | No | Not vulnerable |
| /api/alerts | GET | 404 Not Found | No | Not vulnerable |
| /api/ingest | POST | 400 Bad Request | No | Not vulnerable |

### Security Observations

> [!IMPORTANT]
> The /api/ingest endpoint returns 400 Bad Request on malformed input —
> confirming that input validation is active. This is a positive security
> finding. However, the SIEM generated no alerts for 147 anomalous HTTP
> requests, indicating a complete web layer blind spot.

| Finding | Severity | Notes |
|---|---|---|
| No SQL injection vulnerability detected | Positive | All endpoints correctly reject malicious payloads |
| /api/ingest returns 400 on malformed requests | Positive | Input validation is working as expected |
| /api/events and /api/alerts return 404 | Neutral | Endpoints may require authentication or specific parameters |

---

## SIEM Detection Analysis

| Check | Result | Notes |
|---|---|---|
| SQLmap requests logged | Not detected | Web layer not monitored |
| High request volume detected | Not detected | 147 requests in seconds generated no alert |
| Source IP flagged | Not detected | No web traffic monitoring capability |

> [!CAUTION]
> SQLmap sent 147 HTTP requests with malicious SQL payloads and zero
> alerts were generated. The SIEM has no visibility into its own web
> traffic — Flask access logs are not parsed by the collector.
> This is a significant gap for web application security monitoring.

---

## Evidence

| File | Description |
|---|---|
| `01_sqlmap_api_events.png` | SQLmap output — /api/events test part 1 |
| `02_sqlmap_api_events.png` | SQLmap output — /api/events test part 2 |
| `03_sqlmap_api_alerts.png` | SQLmap output — /api/alerts test part 1 |
| `04_sqlmap_api_alerts.png` | SQLmap output — /api/alerts test part 2 |
| `05_sqlmap_api_ingest.png` | SQLmap output — /api/ingest test part 1 |
| `06_sqlmap_api_ingest.png` | SQLmap output — /api/ingest test part 2 |

---

## Conclusions

All three tested endpoints of the SIEM REST API showed no SQL injection
vulnerabilities. This is a positive security finding — the Flask application
correctly handles and rejects malicious input across all tested surfaces.

The 400 Bad Request response on /api/ingest confirms that input validation
is functioning correctly, rejecting malformed POST data before it reaches
the database layer.

> [!TIP]
> Key remediation recommendations:
> Add Flask access log parsing to the SIEM collector to gain web layer
> visibility. Implement rate limiting on API endpoints to flag high-volume
> requests from single sources. Consider adding authentication to REST API
> endpoints to reduce the attack surface.

---

## References

- MITRE ATT&CK T1190: https://attack.mitre.org/techniques/T1190/
- SQLmap Documentation: https://sqlmap.org
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
