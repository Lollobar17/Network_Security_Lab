# Detection Gap Analysis

**Project:** Network Security Monitoring Lab
**Tester:** Lorenzo Carta
**Date:** 2026-03-26
**Last Updated:** 2026-03-28
**SIEM Version:** HomeLab SIEM v1.2.0

---

## Overview

This document consolidates the detection gap analysis performed across
all four test scenarios. For each scenario, the SIEM response was evaluated
against the expected behavior, and gaps were identified and categorized.

All gaps identified in this document have been addressed in HomeLab SIEM
v1.1.0 and v1.2.0, with the exception of G-01 which requires architectural
work planned for v1.3.0.

> [!IMPORTANT]
> All gaps identified in this document are based on real test results
> from controlled attack simulations. The improvement roadmap at the
> end of this document maps each gap to a concrete remediation action.

---

## Gap Summary

| # | Gap | Scenario | Severity | Status |
|---|---|---|---|---|
| G-01 | No network scanning detection | 01 — Nmap | High | Open |
| G-02 | MITRE technique misclassification | 02 — Hydra | Medium | Resolved in v1.1.0 |
| G-03 | Source IP absent from alerts | 02 — Hydra | High | Resolved in v1.2.0 |
| G-04 | No brute force volume detection | 02 — Hydra | High | Resolved in v1.2.0 |
| G-05 | No web traffic anomaly detection | 03 — SQLmap | Medium | Resolved in v1.2.0 |
| G-06 | No path traversal detection | 04 — Path Traversal | Medium | Resolved in v1.2.0 |
| G-07 | No CRITICAL severity alerts | All | Medium | Resolved in v1.2.0 |

---

## Detailed Gap Analysis

### G-01 — No Network Scanning Detection

**Scenario:** 01 — Network Scanning
**Severity:** High
**MITRE Expected:** T1046 — Network Service Discovery
**Status:** Open — Planned for v1.3.0

> [!CAUTION]
> This is the most critical remaining gap — network scanning is the first
> phase of virtually every attack. Without detection at this stage, all
> subsequent attack phases will also go undetected until much later.

**Description:**
The SIEM did not detect the Nmap port scan executed against the host.
The current architecture monitors Windows system logs and authentication
events only — it has no visibility into inbound network traffic.

**Root Cause:**
No network-level monitoring layer is integrated with the SIEM. The
collector reads log files but does not capture raw network packets or
firewall events.

**Recommendation:**
Integrate a network monitoring tool such as Suricata or Zeek to capture
and analyze inbound traffic. Add a detection rule for T1046 based on
multiple port connection attempts from a single source IP within a
defined time window.

---

### G-02 — MITRE Technique Misclassification

**Scenario:** 02 — SSH Brute Force
**Severity:** Medium
**MITRE Detected:** T1078 — Valid Accounts
**MITRE Expected:** T1110 — Brute Force
**Status:** Resolved in v1.1.0

> [!TIP]
> Fix applied: AUTH-002 MITRE classification updated from T1078 to T1110
> in detector.py. Brute force attacks are now correctly classified.

**Description:**
The SIEM correctly detected repeated SSH login attempts but classified
them under T1078 instead of T1110.

**Fix Applied:**
Updated AUTH-002 rule MITRE field from T1078 to T1110 in detector.py.

---

### G-03 — Source IP Absent from Alerts

**Scenario:** 02 — SSH Brute Force
**Severity:** High
**Status:** Resolved in v1.2.0

> [!TIP]
> Fix applied: source_ip field added to alert schema in detector.py
> and storage.py. Automatic database migration handles existing databases.

**Description:**
The /api/alerts endpoint did not include the source IP address of the
attacker, reducing incident response capability.

**Fix Applied:**
Added source_ip to the alert object in analyze_event() in detector.py.
Added source_ip column to the alerts table in storage.py with automatic
migration for existing databases.

---

### G-04 — No Brute Force Volume Detection

**Scenario:** 02 — SSH Brute Force
**Severity:** High
**MITRE Expected:** T1110 — Brute Force
**Status:** Resolved in v1.2.0

> [!TIP]
> Fix applied: AUTH-005 rule added — triggers CRITICAL alert when more
> than 10 failed SSH attempts occur from the same IP in 60 seconds.

**Description:**
The SIEM had no rule that triggered based on the volume of failed login
attempts. Hydra generated over 3500 attempts in 3 minutes with no
dedicated high-volume alert.

**Fix Applied:**
Added AUTH-005 rule with CRITICAL severity and time-window based
correlation — fires when 10+ failed SSH attempts from same IP in 60s.

---

### G-05 — No Web Traffic Anomaly Detection

**Scenario:** 03 — SQL Injection
**Severity:** Medium
**MITRE Expected:** T1190 — Exploit Public-Facing Application
**Status:** Resolved in v1.2.0

> [!TIP]
> Fix applied: Flask/Werkzeug access log parser added to collector.py.
> Web requests are now parsed and evaluated against detection rules.

**Description:**
SQLmap sent 147 HTTP requests containing malicious SQL payloads.
None triggered a SIEM alert. The web layer was completely invisible.

**Fix Applied:**
Added Flask/Werkzeug access log format parser to parse_log_line()
in collector.py. Web traffic is now categorized and evaluated by
WEB-001, WEB-002, WEB-003 and WEB-004 rules.

---

### G-06 — No Path Traversal Detection

**Scenario:** 04 — Path Traversal
**Severity:** Medium
**MITRE Expected:** T1083 — File and Directory Discovery
**Status:** Resolved in v1.2.0

> [!TIP]
> Fix applied: same as G-05 — Flask access log parsing now feeds
> web requests into WEB-001 which detects ../ traversal patterns.

**Description:**
Three path traversal variants using ../ sequences generated no alerts
despite clearly anomalous URL patterns.

**Fix Applied:**
Flask access log parsing from G-05 fix enables WEB-001 (Directory
Traversal) to now detect ../ patterns in HTTP requests.

---

### G-07 — No CRITICAL Severity Alerts

**Scenario:** All
**Severity:** Medium
**Status:** Resolved in v1.2.0

> [!TIP]
> Fix applied: three new CRITICAL rules added — AUTH-005, AUTH-006
> and WEB-004 define concrete thresholds for CRITICAL severity alerts.

**Description:**
Across all four scenarios the maximum alert severity was HIGH despite
active brute force attacks. No conditions for CRITICAL were defined.

**Fix Applied:**
Added three new rules with CRITICAL severity:
- AUTH-005: SSH brute force exceeding 10 attempts/min
- AUTH-006: Successful login after 3+ failures in 5 minutes
- WEB-004: Web 4xx flood exceeding 50 requests/min

---

## SIEM Improvement Roadmap

> [!TIP]
> Items 1-5 have been implemented in v1.1.0 and v1.2.0.
> Item 6 remains open and is planned for v1.3.0.

| Priority | Improvement | Gap | Status |
|---|---|---|---|
| 1 | Add source_ip to alert schema | G-03 | Resolved in v1.2.0 |
| 2 | Add T1110 brute force correlation rule | G-04 | Resolved in v1.2.0 |
| 3 | Fix MITRE classification AUTH-002 | G-02 | Resolved in v1.1.0 |
| 4 | Add Flask access log parsing | G-05, G-06 | Resolved in v1.2.0 |
| 5 | Define CRITICAL severity thresholds | G-07 | Resolved in v1.2.0 |
| 6 | Integrate network monitoring layer | G-01 | Open — v1.3.0 |

---

## References

- MITRE ATT&CK Framework: https://attack.mitre.org
- HomeLab SIEM Repository: https://github.com/Lollobar17/Homelab_SIEM
- Network Security Monitoring Lab: https://github.com/Lollobar17/Network_Security_Lab
- HomeLab SIEM CHANGELOG: https://github.com/Lollobar17/Homelab_SIEM/blob/main/CHANGELOG.md
