# Scenario 02 — SSH Brute Force

**Date:** 2026-03-15
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab — VirtualBox NAT Network
**Tool:** Hydra 9.6
**MITRE Technique:** T1110 — Brute Force
**Status:** Completed

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

| Risk | Notes |
|---|---|
| **High** | SSH exposed on network interface — accessible from VM |
| **High** | No account lockout policy detected — unlimited login attempts allowed |
| **Medium** | Default username (MPC) guessable — no obscurity protection |
| **Medium** | Password-based authentication enabled — key-based auth recommended |

---

## SIEM Detection Analysis

| Check | Result | Notes |
|---|---|---|
| Brute force alert triggered | Detected | AUTH-002 Root Login Attempt — severity HIGH |
| MITRE mapping | Partial | Classified as T1078 instead of T1110 |
| Failed login events logged | Detected | 3 alerts at 11:11:31, 11:11:39, 11:11:44 UTC |
| Source IP flagged | Not detected | Source IP absent from /api/alerts endpoint |

### SIEM Response Details

The SIEM correctly detected repeated SSH login attempts as root and
generated HIGH severity alerts via rule AUTH-002. However, the MITRE
technique was mapped to T1078 (Valid Accounts) instead of the more
accurate T1110 (Brute Force), indicating a gap in the detection rule
classification.

Additionally, the source IP of the attacker (Kali Linux VM) was not
included in the alert data, which would be critical information for
incident response in a real enterprise environment.

---

## Evidence

| File | Description |
|---|---|
| `hydra_bruteforce_ssh.png` | Hydra output — 3509 attempts in 3 minutes |
| `siem_dashboard_alerts.png` | SIEM dashboard showing ROOT Login Attempt alerts triggered during test |

---

## Conclusions

The SSH brute force simulation successfully demonstrated both the
offensive capability of Hydra and the partial detection capability
of the SIEM system. The SIEM correctly identified repeated SSH login
attempts and generated HIGH severity alerts, validating the core
detection logic.

However, two gaps were identified:
- MITRE technique misclassification (T1078 vs T1110)
- Missing source IP in alert data

These findings will be addressed in the SIEM improvement roadmap.

Key remediation recommendations:
- Enable account lockout after N failed attempts
- Disable password authentication — use SSH key pairs instead
- Restrict SSH access to trusted IP ranges only
- Add dedicated T1110 Brute Force detection rule to SIEM

---

## References

- MITRE ATT&CK T1110: https://attack.mitre.org/techniques/T1110/
- Hydra Documentation: https://github.com/vanhauser-thc/thc-hydra
- OpenSSH Hardening: https://www.ssh.com/academy/ssh/security
