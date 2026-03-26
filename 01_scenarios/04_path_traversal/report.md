# Scenario 04 — Path Traversal

**Date:** 2026-03-23
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab — SIEM Flask Application
**Tool:** curl (manual testing)
**MITRE Technique:** T1083 — File and Directory Discovery
**Status:** Completed

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
| **IP Address** | 192.168.0.45 |
| **Application** | HomeLab SIEM — Flask |
| **Port** | 5000 |
| **Target File** | /etc/passwd (Linux system file) |

---

## Methodology

Three path traversal variants were tested manually using curl from
the Kali Linux terminal.

### 1. Basic Path Traversal

curl http://192.168.0.45:5000/../../../etc/passwd

### 2. Static Path Traversal

curl http://192.168.0.45:5000/static/../../../etc/passwd

### 3. URL-Encoded Path Traversal

curl http://192.168.0.45:5000/static/..%2F..%2F..%2Fetc%2Fpasswd

---

## Findings

### Test Results Summary

| Test | Technique | HTTP Response | Vulnerable | Result |
|---|---|---|---|---|
| 01 | Basic traversal | 404 Not Found | No | Not vulnerable |
| 02 | Static path traversal | 404 Not Found | No | Not vulnerable |
| 03 | URL-encoded traversal | 404 Not Found | No | Not vulnerable |

### Security Observations

| Finding | Severity | Notes |
|---|---|---|
| No path traversal vulnerability detected | Positive | All variants correctly rejected |
| Flask default routing prevents directory escape | Positive | Framework-level protection working |
| URL encoding bypass ineffective | Positive | Server correctly decodes and rejects encoded payloads |

---

## SIEM Detection Analysis

| Check | Result | Notes |
|---|---|---|
| Traversal attempts logged | To be verified | Check /api/events for suspicious requests |
| Anomalous URL patterns detected | To be verified | ../  sequences should trigger alerts |
| Source IP flagged | To be verified | Check /api/alerts endpoint |

---

## Evidence

| File | Description |
|---|---|
| `path_traversal_tests.png` | All three curl tests — basic, static and URL-encoded variants |

---

## Conclusions

All three path traversal variants were successfully blocked by the Flask
application. The server returned 404 Not Found for every attempt,
demonstrating that the application correctly prevents directory
traversal attacks.

Flask's built-in routing mechanism provides effective protection against
path traversal by design — routes are explicitly defined and the
framework does not serve arbitrary filesystem paths.

This result confirms that the SIEM application follows secure
development practices and is not susceptible to file disclosure
via path manipulation.

---

## References

- MITRE ATT&CK T1083: https://attack.mitre.org/techniques/T1083/
- OWASP Path Traversal: https://owasp.org/www-community/attacks/Path_Traversal
- Flask Security: https://flask.palletsprojects.com/en/stable/security/

