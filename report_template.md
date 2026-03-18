# Scenario [NUMBER] — [SCENARIO NAME]

**Date:** YYYY-MM-DD
**Tester:** Lorenzo Carta
**Environment:** Controlled Lab
**Tool:** [Tool used]
**MITRE Technique:** [T-ID] — [Technique Name]

---

## Objective

Brief description of what this scenario aims to demonstrate and why it is
relevant from a security perspective.

---

## Target

| Field | Value |
|---|---|
| **IP Address** | 192.168.x.x |
| **OS** | [Target OS] |
| **Service** | [Service / Port] |
| **Version** | [Version if known] |

---

## Methodology

### 1. Reconnaissance
Description of the information gathering phase.

```
[Commands used]
```

### 2. Threat Modeling
Attack vectors identified and approach selected.

### 3. Exploitation
Step-by-step execution of the attack.

```
[Commands used]
```

### 4. Detection — SIEM Response
Description of how the SIEM detected the attack.

- Alert triggered: [Alert name]
- MITRE technique mapped: [T-ID]
- Log source: [auth.log / access.log / syslog]

### 5. Evidence
Screenshots and logs are available in the `evidence/` folder.

| File | Description |
|---|---|
| `01_scan_output.png` | [Description] |
| `02_siem_alert.png` | [Description] |
| `03_log_extract.txt` | [Description] |

---

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| Critical / High / Medium / Low | [Finding] | [Remediation] |

---

## Conclusions

Summary of what the scenario demonstrated, what the SIEM detected correctly
and any observations on detection gaps or improvements.

---

## References

- [MITRE ATT&CK T-ID](https://attack.mitre.org/techniques/T-ID/)
- [Tool documentation]
- [CVE if applicable]
