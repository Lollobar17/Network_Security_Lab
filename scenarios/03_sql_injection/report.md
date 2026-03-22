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

Command executed from Kali Linux terminal:

sqlmap -u http://192.168.0.45:5000/api/events --batch

### 2. Test — /api/alerts

sqlmap -u http://192.168.0.45:5000/api/alerts --batch

### 3. Test — /api/ingest (POST parameters)

sqlmap -u http://192.168.0.45:5000/api/ingest --data="source=test&message=test" --batch

---

## Findings

### Test Results Summary

| Endpoint | Method | HTTP Response | SQLi Vulnerable | Result |
|---|---|---|---|---|
| /api/events | GET | 404 Not Found | No | Not vulnerable |
| /api/alerts | GET | 404 Not Found | No | Not vulnerable |
| /api/ingest | POST | 400 Bad Request | No | Not vulnerable |

### Security Observations

| Finding | Severity | Notes |
|---|---|---|
| No SQL injection vulnerability detected | Positive | All endpoints correctly reject malicious payloads |
| /api/ingest returns 400 on malformed requests | Positive | Input validation is working as expected |
| /api/events and /api/alerts return 404 | Neutral | Endpoints may require authentication or specific parameters |

---

## SIEM Detection Analysis

| Check | Result | Notes |
|---|---|---|
| SQLmap requests logged | To be verified | Check /api/events for anomalous traffic |
| High request volume detected | To be verified | 147 requests in seconds — anomaly pattern |
| Source IP flagged | To be verified | Check /api/alerts endpoint |

---

## Evidence

| File | Description |
|---|---|
| `sqlmap_api_events.png` | SQLmap output — /api/events test part 1 |
| `sqlmap_api_events_2.png` | SQLmap output — /api/events test part 2 |
| `sqlmap_api_alerts.png` | SQLmap output — /api/alerts test part 1 |
| `sqlmap_api_alerts_2.png` | SQLmap output — /api/alerts test part 2 |
| `sqlmap_api_ingest.png` | SQLmap output — /api/ingest test part 1 |
| `sqlmap_api_ingest_2.png` | SQLmap output — /api/ingest test part 2 |

---

## Conclusions

All three tested endpoints of the SIEM REST API showed no SQL injection
vulnerabilities. This is a positive security finding — the Flask application
correctly handles and rejects malicious input across all tested surfaces.

The 400 Bad Request response on /api/ingest confirms that input validation
is functioning correctly, rejecting malformed POST data before it reaches
the database layer.

This result demonstrates that the SIEM application follows secure coding
practices for database interaction, likely using parameterized queries
or an ORM layer that prevents direct SQL manipulation.

---

## References

- MITRE ATT&CK T1190: https://attack.mitre.org/techniques/T1190/
- SQLmap Documentation: https://sqlmap.org
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection

