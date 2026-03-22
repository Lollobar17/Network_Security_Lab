# Scenario 02 — SSH Brute Force

**Date:** 2026-03-21
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
| Brute force alert triggered | To be verified | Requires SIEM log review |
| MITRE T1110 mapped | To be verified | Rule engine check required |
| Failed login events logged | To be verified | Check auth.log entries |
| Source IP flagged | To be verified | Check /api/alerts endpoint |

---

## Evidence

| File | Description |
|---|---|
| `hydra_bruteforce_ssh.png` | Hydra output showing active brute force — 3509 attempts in 3 minutes |

---

## Conclusions

The SSH brute force simulation successfully demonstrated how an attacker
can automate thousands of login attempts per minute against an exposed
SSH service. The absence of account lockout policies on the target
represents a critical security gap in a real enterprise environment.

Key remediation recommendations:
- Enable account lockout after N failed attempts
- Disable password authentication — use SSH key pairs instead
- Restrict SSH access to trusted IP ranges only
- Monitor and alert on repeated failed login attempts via SIEM

---

## References

- MITRE ATT&CK T1110: https://attack.mitre.org/techniques/T1110/
- Hydra Documentation: https://github.com/vanhauser-thc/thc-hydra
- OpenSSH Hardening: https://www.ssh.com/academy/ssh/security

