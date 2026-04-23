# Scenario 02 — SSH Brute Force

**Date:** 2026-03-15
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab — VirtualBox NAT Network
**Tool:** Hydra 9.6
**MITRE Technique:** T1110 — Brute Force
**Status:** Completed — Post-Remediation Verified

---

## Objective

Simulate a brute force attack against the SSH service of the host machine
to test authentication monitoring capabilities. Validate whether the SIEM
system correctly detects and alerts on repeated failed login attempts —
a classic indicator of brute force activity.

---

## Target

| Field | Value |
|---|---|
| **IP Address** | 192.168.56.1 |
| **OS** | Microsoft Windows |
| **Service** | OpenSSH Server |
| **Port** | 22/tcp |
| **Username** | MPC |

---

## Methodology

### 1. Pre-Attack Verification

SSH service availability confirmed via Nmap:

nmap -p 22 192.168.56.1

Result: 22/tcp open ssh — service confirmed active.

### 2. Brute Force Execution

Command executed from Kali Linux terminal:

hydra -l MPC -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.1

Wordlist used: rockyou.txt — 14,344,399 passwords.

### 3. Post-Remediation Verification

Threshold rules validated via controlled stress test using
simulate_logs.py --stress-test against the live SIEM instance.

> [!TIP]
> Reduce parallel tasks with -t 4 to slow down the attack and avoid
> triggering rate limiting on hardened systems. In a real engagement,
> slower attacks are less likely to be detected and blocked.

---

## Findings

### Attack Statistics

| Metric | Value |
|---|---|
| **Tool** | Hydra 9.6 |
| **Target** | ssh://192.168.56.1:22 |
| **Username** | MPC |
| **Wordlist** | rockyou.txt |
| **Parallel Tasks** | 16 |
| **Speed** | ~1230 tries/min |
| **Total Attempts** | 3509 in ~3 minutes |
| **Result** | Attack simulated — stopped after evidence capture |

### Security Observations

> [!IMPORTANT]
> Port 22 (SSH) is exposed on the VirtualBox network interface with no
> account lockout policy — unlimited login attempts are allowed.
> In an enterprise environment this would be a critical misconfiguration.

| Risk | Notes |
|---|---|
| **High** | SSH exposed on network interface — accessible from VM |
| **High** | No account lockout policy — unlimited login attempts allowed |
| **Medium** | Default username guessable — no obscurity protection |
| **Medium** | Password-based authentication enabled — key-based auth recommended |

---

## SIEM Detection Analysis

### Initial Assessment (v1.0.0)

| Check | Result | Notes |
|---|---|---|
| Brute force alert triggered | Detected | AUTH-002 Root Login Attempt — HIGH |
| MITRE mapping | Partial | Classified as T1078 instead of T1110 |
| Failed login events logged | Detected | 3 alerts at 11:11:31, 11:11:39, 11:11:44 UTC |
| Source IP flagged | Not detected | Source IP absent from /api/alerts |

### Post-Remediation (v1.2.0)

| Check | Result | Notes |
|---|---|---|
| Brute force alert triggered | Detected | AUTH-002 — HIGH severity |
| High volume alert triggered | Detected | AUTH-005 — CRITICAL severity |
| Post-failure login detected | Detected | AUTH-006 — CRITICAL severity |
| MITRE mapping | Correct | T1110 — Brute Force |
| Source IP logged | Detected | source_ip present in all alerts |

> [!TIP]
> Post-remediation: AUTH-005 now triggers CRITICAL after 10+ failed
> attempts from same IP in 60 seconds. AUTH-006 triggers CRITICAL
> on successful login after repeated failures. Source IP now present
> in all alert data. MITRE classification corrected to T1110.

> [!NOTE]
> Post-remediation threshold rules (AUTH-005, AUTH-006) were validated
> via simulate_logs.py --stress-test against the live SIEM instance.
> The stress test injects realistic SSH log patterns from a fixed IP
> to verify rule triggering behavior.

---

## Evidence

| File | Description |
|---|---|
| `hydra_bruteforce_ssh.png` | Hydra output — 3509 attempts in 3 minutes |
| `siem_dashboard_alerts.png` | SIEM dashboard — ROOT Login Attempt alerts during test |

---

## Conclusions

The SSH brute force simulation confirmed both offensive capability and
post-remediation detection improvements. The SIEM now generates CRITICAL
alerts for high-volume attacks with correct MITRE T1110 classification
and source IP in all alert data.

> [!CAUTION]
> Key gaps resolved in v1.2.0:
> AUTH-005 — high volume brute force now triggers CRITICAL.
> AUTH-006 — post-failure success now triggers CRITICAL.
> Source IP now present in all alerts.
> MITRE T1078 corrected to T1110.

> [!TIP]
> Key remediation recommendations:
> Enable account lockout after N failed attempts.
> Disable password authentication — use SSH key pairs instead.
> Restrict SSH access to trusted IP ranges only.

---

## References

- MITRE ATT&CK T1110: https://attack.mitre.org/techniques/T1110/
- Hydra Documentation: https://github.com/vanhauser-thc/thc-hydra
- OpenSSH Hardening: https://www.ssh.com/academy/ssh/security
