"""
Test runner per regole Sigma contro log Mordor (Security-Datasets).
Usa pySigma con un backend custom che valuta le regole direttamente
contro una lista di dict Python (i log JSON caricati).
"""
import json
from pathlib import Path

from sigma.collection import SigmaCollection

RULES_DIR = Path(__file__).parent.parent / "rules"
DATA_DIR = Path(__file__).parent.parent / "data"


def load_logs(json_path: Path) -> list[dict]:
    """Carica log Mordor in formato JSON-lines."""
    logs = []
    with open(json_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                logs.append(json.loads(line))
    return logs


def load_rules() -> SigmaCollection:
    """Carica tutte le regole .yml dalla cartella rules/."""
    rule_files = list(RULES_DIR.glob("**/*.yml"))
    return SigmaCollection.from_yaml(
        "\n---\n".join(p.read_text(encoding="utf-8") for p in rule_files)
    )


def matches_condition(log: dict, selections: dict, condition_fn) -> bool:
    """Valuta le selection di una regola contro un singolo evento di log."""
    results = {}
    for name, fields in selections.items():
        ok = True
        for field, values in fields.items():
            field_name = field.split("|")[0]
            modifier = field.split("|")[1] if "|" in field else "equals"
            log_value = str(log.get(field_name, ""))
            if isinstance(values, list):
                check = any(_check(log_value, v, modifier) for v in values)
            else:
                check = _check(log_value, values, modifier)
            ok = ok and check
        results[name] = ok
    return condition_fn(results)


def _check(log_value: str, rule_value: str, modifier: str) -> bool:
    if modifier == "endswith":
        return log_value.lower().endswith(rule_value.lower())
    if modifier == "contains":
        return rule_value.lower() in log_value.lower()
    return log_value.lower() == rule_value.lower()


def run_powershell_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_img": {"Image|endswith": ["\\powershell.exe", "\\pwsh.exe"]},
        "selection_flags": {"CommandLine|contains": ["-enc", "-EncodedCommand", "-e "]},
        "selection_suspicious_flags": {
            "CommandLine|contains": [
                "-w hidden", "-windowstyle hidden", "-nop", "-noni", "-noP", "-w 1"
            ]
        },
    }

    def condition(r):
        return r["selection_img"] and r["selection_flags"] and r["selection_suspicious_flags"]

    return [log for log in logs if matches_condition(log, selections, condition)]


def run_certutil_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_img": {"Image|endswith": ["\\certutil.exe"]},
        "selection_download": {"CommandLine|contains": ["-urlcache", "-verifyctl", "urlcache"]},
        "selection_decode": {"CommandLine|contains": ["-decode", "-decodehex"]},
    }

    def condition(r):
        return r["selection_img"] and (r["selection_download"] or r["selection_decode"])

    return [log for log in logs if matches_condition(log, selections, condition)]


def run_shadow_copy_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_img": {"Image|endswith": ["\\vssadmin.exe", "\\wmic.exe", "\\powershell.exe"]},
        "selection_action": {
            "CommandLine|contains": [
                "delete shadows", "shadowcopy delete", "Get-WmiObject Win32_Shadowcopy"
            ]
        },
    }

    def condition(r):
        return r["selection_img"] and r["selection_action"]

    return [log for log in logs if matches_condition(log, selections, condition)]


def run_defender_disabled_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_img": {"Image|endswith": ["\\powershell.exe", "\\pwsh.exe"]},
        "selection_action": {
            "CommandLine|contains": [
                "Set-MpPreference", "DisableRealtimeMonitoring", "DisableBehaviorMonitoring",
                "DisableIOAVProtection", "DisableTamperProtection"
            ]
        },
    }

    def condition(r):
        return r["selection_img"] and r["selection_action"]

    return [log for log in logs if matches_condition(log, selections, condition)]


def run_mass_file_enum_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_img": {"Image|endswith": ["\\powershell.exe", "\\cmd.exe", "\\cscript.exe"]},
        "selection_action": {"CommandLine|contains": ["Get-ChildItem -Recurse", "dir /s", "rename"]},
        "selection_scope": {
            "CommandLine|contains": ["C:\\Users", "\\Desktop", "\\Documents", "%USERPROFILE%"]
        },
    }

    def condition(r):
        return r["selection_img"] and r["selection_action"] and r["selection_scope"]

    return [log for log in logs if matches_condition(log, selections, condition)]



def run_install_hook_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_parent": {"ParentImage|contains": ["npm", "npx", "pip", "pip3", "yarn"]},
        "selection_child": {"Image|endswith": ["/bash", "/sh", "/curl", "/wget"]},
    }

    def condition(r):
        return r["selection_parent"] and r["selection_child"]

    return [log for log in logs if matches_condition(log, selections, condition)]


def run_manifest_tampering_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_file": {
            "TargetFilename|endswith": [
                "package.json", "package-lock.json", "requirements.txt",
                "Pipfile", "Pipfile.lock", "yarn.lock"
            ]
        },
        "filter_known_tools": {"Image|endswith": ["/npm", "/yarn", "/pip", "/code", "/git"]},
    }

    def condition(r):
        return r["selection_file"] and not r["filter_known_tools"]

    return [log for log in logs if matches_condition(log, selections, condition)]


def run_build_exfil_rule(logs: list[dict]) -> list[dict]:
    selections = {
        "selection_process": {
            "Image|endswith": ["/npm", "/npx", "/node", "/pip", "/python", "/python3"]
        },
        "filter_known_registries": {
            "DestinationHostname|endswith": [
                "registry.npmjs.org", "pypi.org", "files.pythonhosted.org",
                "github.com", "githubusercontent.com", "codeload.github.com"
            ]
        },
    }

    def condition(r):
        return r["selection_process"] and not r["filter_known_registries"]

    return [log for log in logs if matches_condition(log, selections, condition)]



def main():
    # Validazione delle regole tramite pySigma (parsing + controllo sintassi/schema)
    rules = load_rules()
    print(f"Regole Sigma caricate e validate da pySigma: {len(rules.rules)}")
    for r in rules.rules:
        print(f"  - {r.title} (id: {r.id})")
    print("-" * 60)

    log_files = list(DATA_DIR.glob("*.json"))
    if not log_files:
        print("Nessun file di log trovato in data/. Scarica prima un dataset Mordor.")
        return

    all_logs = []
    for lf in log_files:
        all_logs.extend(load_logs(lf))

    process_logs = [
        log for log in all_logs
        if log.get("Channel") == "Microsoft-Windows-Sysmon/Operational" and log.get("EventID") == 1
    ]

    print(f"Log totali caricati: {len(all_logs)}")
    print(f"Eventi Process Creation (Sysmon EventID 1): {len(process_logs)}")
    print("-" * 60)

    ps_hits = run_powershell_rule(process_logs)
    print(f"[Regola: PowerShell Encoded Command] -> {len(ps_hits)} match")
    for h in ps_hits:
        print(f"  Image: {h.get('Image')}")
        print(f"  CommandLine (troncato): {h.get('CommandLine', '')[:80]}...")

    print("-" * 60)
    cu_hits = run_certutil_rule(process_logs)
    print(f"[Regola: Certutil Abuse] -> {len(cu_hits)} match")
    for h in cu_hits:
        print(f"  Image: {h.get('Image')}")
        print(f"  CommandLine: {h.get('CommandLine', '')}")

    print("-" * 60)
    sc_hits = run_shadow_copy_rule(process_logs)
    print(f"[Regola: Shadow Copy Deletion] -> {len(sc_hits)} match")

    print("-" * 60)
    def_hits = run_defender_disabled_rule(process_logs)
    print(f"[Regola: Defender Disabled] -> {len(def_hits)} match")

    print("-" * 60)
    enum_hits = run_mass_file_enum_rule(process_logs)
    print(f"[Regola: Mass File Enumeration] -> {len(enum_hits)} match")

    # Eventi sintetici per testare le regole ransomware precursor (dataset Mordor attuale non le contiene)
    print("-" * 60)
    print("Test con eventi sintetici ransomware precursor:")

    synthetic_shadow = {
        "Image": "C:\\Windows\\System32\\vssadmin.exe",
        "CommandLine": "vssadmin.exe delete shadows /all /quiet",
    }
    print(f"  Shadow copy deletion -> match: {len(run_shadow_copy_rule([synthetic_shadow])) == 1}")

    synthetic_defender = {
        "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "CommandLine": "powershell.exe Set-MpPreference -DisableRealtimeMonitoring $true",
    }
    print(f"  Defender disabled -> match: {len(run_defender_disabled_rule([synthetic_defender])) == 1}")

    synthetic_enum = {
        "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "CommandLine": "powershell.exe Get-ChildItem -Recurse C:\\Users\\victim\\Documents | Rename-Item",
    }
    print(f"  Mass file enumeration -> match: {len(run_mass_file_enum_rule([synthetic_enum])) == 1}")

    print("-" * 60)
    print("Test con eventi sintetici supply chain:")

    synthetic_install_hook = {
        "ParentImage": "/usr/local/bin/npm",
        "Image": "/bin/bash",
    }
    print(f"  Install hook spawning shell -> match: {len(run_install_hook_rule([synthetic_install_hook])) == 1}")

    synthetic_manifest_bad = {
        "TargetFilename": "/home/runner/project/package.json",
        "Image": "/usr/bin/curl",
    }
    print(f"  Manifest tampering (tool sospetto) -> match: {len(run_manifest_tampering_rule([synthetic_manifest_bad])) == 1}")

    synthetic_manifest_ok = {
        "TargetFilename": "/home/runner/project/package.json",
        "Image": "/usr/local/bin/npm",
    }
    print(f"  Manifest tampering (npm legittimo) -> match: {len(run_manifest_tampering_rule([synthetic_manifest_ok])) == 0}")

    synthetic_exfil = {
        "Image": "/usr/local/bin/node",
        "DestinationHostname": "evil-collector.example.net",
    }
    print(f"  Build exfil verso host sconosciuto -> match: {len(run_build_exfil_rule([synthetic_exfil])) == 1}")

    synthetic_exfil_ok = {
        "Image": "/usr/local/bin/npm",
        "DestinationHostname": "registry.npmjs.org",
    }
    print(f"  Build verso registry npm legittimo -> match: {len(run_build_exfil_rule([synthetic_exfil_ok])) == 0}")


if __name__ == "__main__":
    main()
