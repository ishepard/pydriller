# security_analysis/diff_extractor.py

import argparse
import csv
import json
import os
import re
import time
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pydriller import Repository

# ---------------------------------------------------------------------------
# CVE API Endpoint (NVD 2.0)
# ---------------------------------------------------------------------------
CVE_API_URL_V2 = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# ---------------------------------------------------------------------------
# OWASP Classification Mapping
# ---------------------------------------------------------------------------
OWASP_MAPPING = {
    "injection": "A03:2021 - Injection",
    "sql injection": "A03:2021 - Injection",
    "sqli": "A03:2021 - Injection",
    "command injection": "A03:2021 - Injection",
    "xpath injection": "A03:2021 - Injection",
    "ldap injection": "A03:2021 - Injection",

    "cross site scripting": "A07:2021 - Identification & Authentication Failures",
    "xss": "A07:2021 - Identification & Authentication Failures",

    "buffer overflow": "A05:2021 - Security Misconfiguration",
    "directory traversal": "A05:2021 - Security Misconfiguration",
    "security misconfiguration": "A05:2021 - Security Misconfiguration",

    "privilege escalation": "A06:2021 - Vulnerable & Outdated Components",
    "insecure deserialization": "A08:2021 - Insecure Deserialization",
    "broken access control": "A01:2021 - Broken Access Control",
    "unauthorized access": "A01:2021 - Broken Access Control",

    "denial of service": "A09:2021 - Security Logging & Monitoring Failures",
    "dos": "A09:2021 - Security Logging & Monitoring Failures",

    "insufficient logging": "A09:2021 - Security Logging & Monitoring Failures",
    "inadequate logging": "A09:2021 - Security Logging & Monitoring Failures",

    "insecure communication": "A10:2021 - Server-Side Request Forgery",
    "server side request forgery": "A10:2021 - Server-Side Request Forgery",

    "broken authentication": "A07:2021 - Identification & Authentication Failures",
    "session fixation": "A07:2021 - Identification & Authentication Failures",
    "cross-site request forgery": "A07:2021 - Identification & Authentication Failures",
    "csrf": "A07:2021 - Identification & Authentication Failures",

    # If you have any "security fix", "patch", "mitigation" that
    # appear in commit messages, they might have 'Low' severity by default.
    "security fix": "Low",
    "patch": "Low",
    "mitigation": "Low"
}

# ---------------------------------------------------------------------------
# Security Keywords -> Severity
# ---------------------------------------------------------------------------
SECURITY_KEYWORDS = {
    "remote code execution": "Critical",
    "rce": "Critical",
    "sql injection": "Critical",
    "sqli": "Critical",
    "cross site scripting": "High",
    "xss": "High",
    "privilege escalation": "High",
    "buffer overflow": "High",
    "command injection": "High",
    "directory traversal": "Medium",
    "zero day": "Medium",
    "unauthorized access": "Medium",
    "denial of service": "Low",
    "dos": "Low",
    "security fix": "Low",
    "patch": "Low",
    "mitigation": "Low",
}

# Regex to detect CVE-YYYY-NNNNN
CVE_REGEX = re.compile(r'\bCVE-\d{4}-\d{4,}\b', re.IGNORECASE)

def fetch_cve_details_v2(cve_id: str) -> str:
    try:
        url = f"{CVE_API_URL_V2}?cveId={cve_id}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            vulnerabilities = data.get("vulnerabilities", [])
            if vulnerabilities:
                cve_obj = vulnerabilities[0]
                return cve_obj["cve"]["descriptions"][0]["value"]
        return "No CVE details found."
    except Exception as exc:
        return f"Error fetching CVE details: {str(exc)}"

def extract_cve_ids_from_msg(commit_msg: str):
    return CVE_REGEX.findall(commit_msg)

def classify_owasp(commit_message: str) -> str:
    msg_lower = commit_message.lower()
    for keyword, category in OWASP_MAPPING.items():
        if keyword in msg_lower:
            return category
    return "Unknown Category"

def classify_severity(commit_message: str) -> str:
    msg_lower = commit_message.lower()
    for keyword, severity in SECURITY_KEYWORDS.items():
        if keyword in msg_lower:
            return severity
    return "Low"

def extract_security_diffs_and_store(repo_url, since=None, to=None,
                                     continuous=False, interval=300):
    last_checked_commit = None
    while True:
        repo_args = {"since": since, "to": to} if (since or to) else {}
        flagged_commits = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            for commit in Repository(repo_url, **repo_args).traverse_commits():
                if commit.hash == last_checked_commit:
                    break
                executor.submit(process_commit, commit, flagged_commits)

        # Always call save_results, even if flagged_commits is empty
        save_results(flagged_commits)

        # If there are flagged commits, store the latest one
        if flagged_commits:
            last_checked_commit = flagged_commits[0][0].hash

        if not continuous:
            break

        print(f"[ℹ️] Sleeping for {interval} seconds before the next scan...")
        time.sleep(interval)

def process_commit(commit, flagged_commits):
    commit_msg_lower = commit.msg.lower()
    found_cves = extract_cve_ids_from_msg(commit.msg)
    severity = classify_severity(commit_msg_lower)
    owasp_category = classify_owasp(commit_msg_lower)

    # Flag if severity is "Critical"/"High" or a CVE is found
    if severity in ["Critical", "High"] or found_cves:
        cve_text = "No CVE found"
        if found_cves:
            cve_text = f"{found_cves[0]}: {fetch_cve_details_v2(found_cves[0])}"

        flagged_commits.append((commit, severity, cve_text, owasp_category))
        print(f"\n[⚠️ ALERT] High-risk security commit detected!\n"
              f"Commit Hash: {commit.hash}\n"
              f"Severity Level: {severity}\n"
              f"CVE Details: {cve_text}\n"
              f"OWASP Category: {owasp_category}\n")

def save_results(flagged_commits):
    # Let’s put the reports in the same folder as THIS script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    patches_dir = os.path.join(script_dir, "patches")
    os.makedirs(patches_dir, exist_ok=True)

    security_data = []

    from .patch_labeler import label_patches_with_commit_hash

    for commit, severity, cve_details, owasp_category in flagged_commits:
        for mod in commit.modified_files:
            diff_text = mod.diff or ""
            if not diff_text.strip():
                continue

            label_patches_with_commit_hash(commit.hash, mod.filename, diff_text, patches_dir)
            security_data.append({
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "severity": severity,
                "cve_details": cve_details,
                "owasp_category": owasp_category,
                "filename": mod.filename,
                "diff_preview": diff_text[:100]
            })

    # Even if security_data is empty, create empty files
    csv_path = os.path.join(script_dir, "report.csv")
    json_path = os.path.join(script_dir, "report.json")
    md_path = os.path.join(script_dir, "report.md")

    save_patches_in_csv(security_data, csv_path)
    save_patches_in_json(security_data, json_path)
    save_patches_in_markdown(security_data, md_path)

def save_patches_in_csv(data, filename):
    headers = [
        "commit_hash", "author", "date", "severity",
        "cve_details", "owasp_category", "filename", "diff_preview"
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"[+] CSV created -> {filename}")

def save_patches_in_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] JSON created -> {filename}")

def save_patches_in_markdown(data, filename):
    headers = [
        "commit_hash", "author", "date", "severity",
        "cve_details", "owasp_category", "filename", "diff_preview"
    ]
    with open(filename, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in data:
            line = "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |\n"
            f.write(line)
    print(f"[+] Markdown created -> {filename}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--since", default=None)
    parser.add_argument("--to", default=None)
    parser.add_argument("--continuous", action="store_true")
    parser.add_argument("--interval", type=int, default=300)
    args = parser.parse_args()

    since_date = datetime.strptime(args.since, "%Y-%m-%d") if args.since else None
    to_date = datetime.strptime(args.to, "%Y-%m-%d") if args.to else None

    extract_security_diffs_and_store(
        repo_url=args.repo,
        since=since_date,
        to=to_date,
        continuous=args.continuous,
        interval=args.interval
    )

if __name__ == "__main__":
    main()