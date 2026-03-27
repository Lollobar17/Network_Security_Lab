# Detection Gap Analysis

**Project:** Network Security Monitoring Lab
**Tester:** Lorenzo Carta
**Date:** 2026-03-26
**SIEM Version:** HomeLab SIEM v1.0

---

## Overview

This document consolidates the detection gap analysis performed across
all four test scenarios. For each scenario, the SIEM response was evaluated
against the expected behavior, and gaps were identified and categorized.

The findings in this document will serve as the improvement roadmap for
the HomeLab SIEM project.

> [!IMPORTANT]
> All gaps identified in this document are based on real test results
> from controlled attack simulations. The improvement roadmap at the
> end of this document maps each gap to a concrete remediation action.

---

## Gap Summary

| # | Gap | Scenario | Severity | Status |
|---|---|---|---|---|
| G-01 | No network scanning detection | 01 — Nmap | High | Open |
| G-02 | MITRE technique misclassification | 02 — Hydra | Medium | Open |
| G-03 | Source IP absent from alerts | 02 — Hydra | High | Open |
| G-04 | No brute force volume detection | 02 — Hydra | High | Open |
| G-05 | No web traffic anomaly detection | 03 — SQLmap | Medium | Open |
| G-06 | No path traversal detection | 04 — Path Traversal | Medium | Open |
| G-07 | No CRITICAL severity alerts | All | Medium | Open |

---

## Detailed Gap Analysis

### G-01 — No Network Scanning Detection

**Scenario:** 01 — Network Scanning
**Severity:** High
**MITRE Expected:** T1046 — Network Service Discovery

> [!CAUTION]
> This is the most critical gap — network scanning is the first phase
> of virtually every attack. Without detection at this stage, all
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

> [!IMPORTANT]
> While the SIEM detected the attack, incorrect MITRE classification
> affects threat intelligence quality and incident response prioritization.
> T1110 and T1078 require different response procedures.

**Description:**
The SIEM correctly detected repeated SSH login attempts but classified
them under T1078 (Valid Accounts) instead of T1110 (Brute Force).

**Root Cause:**
The AUTH-002 rule triggers on any root login attempt regardless of
frequency — it does not differentiate between a single login attempt
and a high-volume automated attack.

**Recommendation:**
Update rule AUTH-002 to include a frequency threshold — if N failed
login attempts occur within X seconds from the same source, classify
as T1110 Brute Force with CRITICAL severity instead of HIGH.

---

### G-03 — Source IP Absent from Alerts

**Scenario:** 02 — SSH Brute Force
**Severity:** High

> [!CAUTION]
> Missing source IP in alerts is a critical gap for incident response.
> Without the attacker IP, blocking the threat at the firewall level
> is not possible from the alert data alone.

**Description:**
The /api/alerts endpoint does not include the source IP address of the
attacker. The IP is available in /api/stats but not consolidated in the
alert data, requiring analysts to cross-reference multiple endpoints.

**Root Cause:**
The alert schema does not include a source_ip field.

**Recommendation:**
Update the alert schema to include source_ip as a mandatory field.
Modify the detection rules to extract the source IP from the log entry
and attach it to the generated alert.

---

### G-04 — No Brute Force Volume Detection

**Scenario:** 02 — SSH Brute Force
**Severity:** High
**MITRE Expected:** T1110 — Brute Force

> [!CAUTION]
> Hydra generated 3509 attempts in 3 minutes with no CRITICAL alert.
> In a real environment this attack rate would compromise accounts
> within minutes if weak passwords are in use.

**Description:**
The SIEM has no rule that triggers based on the volume of failed login
attempts. Each event is evaluated independently without aggregation.

**Root Cause:**
The current ruleset lacks time-window based correlation rules.

**Recommendation:**
Add a correlation rule: if more than 10 failed SSH login attempts occur
within 60 seconds from the same source IP, generate a CRITICAL alert
mapped to T1110.

---

### G-05 — No Web Traffic Anomaly Detection

**Scenario:** 03 — SQL Injection
**Severity:** Medium
**MITRE Expected:** T1190 — Exploit Public-Facing Application

> [!IMPORTANT]
> 147 malicious HTTP requests were sent with zero detection. Flask
> generates access logs but they are not parsed by the SIEM collector —
> adding this integration would close both G-05 and G-06 simultaneously.

**Description:**
SQLmap sent 147 HTTP requests containing malicious SQL payloads.
None triggered a SIEM alert.

**Root Cause:**
The SIEM does not monitor its own HTTP access logs.

**Recommendation:**
Add Flask access log parsing to the collector. Implement a rule that
detects anomalous request patterns — high request volume, SQL keywords
in URL parameters, or repeated 400/404 responses.

---

### G-06 — No Path Traversal Detection

**Scenario:** 04 — Path Traversal
**Severity:** Medium
**MITRE Expected:** T1083 — File and Directory Discovery

**Description:**
Three path traversal variants using ../ sequences generated no alerts
despite clearly anomalous URL patterns.

**Root Cause:**
Same as G-05 — web traffic is not monitored.

**Recommendation:**
Add a detection rule that flags HTTP requests containing ../ or
URL-encoded equivalents. Implement as part of the Flask access log
parsing improvement from G-05.

---

### G-07 — No CRITICAL Severity Alerts

**Scenario:** All
**Severity:** Medium

> [!IMPORTANT]
> Zero CRITICAL alerts across 800+ events and an active brute force
> attack suggests the severity thresholds need recalibration. CRITICAL
> should be reserved for confirmed active threats, not just suspicious
> activity.

**Description:**
Across all four scenarios the maximum alert severity was HIGH.
No conditions for CRITICAL severity are currently defined.

**Root Cause:**
All rules are statically assigned severity without dynamic escalation.

**Recommendation:**
Define CRITICAL thresholds: brute force exceeding 100 attempts/minute,
successful auth after multiple failures, or known malicious IP detected.

---

## SIEM Improvement Roadmap

> [!TIP]
> Implement improvements in priority order — items 1-3 can be completed
> with minimal effort and will immediately improve alert quality.
> Item 6 requires the most architectural work but closes the most
> critical detection gap.

| Priority | Improvement | Gap | Effort |
|---|---|---|---|
| 1 | Add source_ip to alert schema | G-03 | Low |
| 2 | Add T1110 brute force correlation rule | G-04 | Medium |
| 3 | Fix MITRE classification AUTH-002 | G-02 | Low |
| 4 | Add Flask access log parsing | G-05, G-06 | Medium |
| 5 | Define CRITICAL severity thresholds | G-07 | Low |
| 6 | Integrate network monitoring layer | G-01 | High |

---

## References

- MITRE ATT&CK Framework: https://attack.mitre.org
- HomeLab SIEM Repository: https://github.com/Lollobar17/homelab-siem
- Network Security Monitoring Lab: https://github.com/Lollobar17/Network_Security_Lab
