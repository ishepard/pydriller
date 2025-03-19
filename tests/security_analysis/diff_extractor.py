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
    """
    Fetch CVE details from NVD 2.0 API given a CVE ID.
    If found, return a short description. Otherwise 'No CVE details found.'
    """
    try:
        url = f"{CVE_API_URL_V2}?cveId={cve_id}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            vulnerabilities = data.get("vulnerabilities", [])
            if vulnerabilities:
                cve_obj = vulnerabilities[0]
                cve_desc = cve_obj["cve"]["descriptions"][0]["value"]
                return cve_desc
        return "No CVE details found."
    except Exception as exc:
        return f"Error fetching CVE details: {str(exc)}"


def extract_cve_ids_from_msg(commit_msg: str):
    """
    Return a list of CVE IDs found in the commit message using regex.
    """
    return CVE_REGEX.findall(commit_msg)


def classify_owasp(commit_message: str) -> str:
    """
    Classify the commit under an OWASP category based on known keywords.
    """
    msg_lower = commit_message.lower()
    for keyword, category in OWASP_MAPPING.items():
        if keyword in msg_lower:
            return category
    return "Unknown Category"


def classify_severity(commit_message: str) -> str:
    """
    Assign severity if a known keyword is found. Default 'Low' if none found.
    """
    msg_lower = commit_message.lower()
    for keyword, severity in SECURITY_KEYWORDS.items():
        if keyword in msg_lower:
            return severity
    return "Low"


def extract_security_diffs_and_store(repo_url, since=None, to=None,
                                     continuous=False, interval=300):
    """
    Main scanning:
      - Traverse commits
      - Use regex to find CVEs
      - Classify severity/OWASP
      - Save results to CSV/JSON/Markdown
      - If continuous=True, re-scan after 'interval' seconds
    """
    last_checked_commit = None

    while True:
        repo_args = {"since": since, "to": to} if (since or to) else {}
        flagged_commits = []

        # concurrently process each commit
        with ThreadPoolExecutor(max_workers=4) as executor:
            for commit in Repository(repo_url, **repo_args).traverse_commits():
                if commit.hash == last_checked_commit:
                    break
                executor.submit(process_commit, commit, flagged_commits)

        if flagged_commits:
            save_results(flagged_commits)
            # store the latest commit's hash
            last_checked_commit = flagged_commits[0][0].hash

        if not continuous:
            break

        print(f"[ℹ️] Sleeping for {interval} seconds before the next scan...")
        time.sleep(interval)


def process_commit(commit, flagged_commits):
    """
    For each commit:
      - check CVEs
      - check severity & OWASP
      - store flagged commits
      - alert on high risk
    """
    commit_msg_lower = commit.msg.lower()
    found_cves = extract_cve_ids_from_msg(commit.msg)
    severity = classify_severity(commit_msg_lower)
    owasp_category = classify_owasp(commit_msg_lower)

    if severity in ["Critical", "High"] or found_cves:
        cve_text = "No CVE found"
        if found_cves:
            first_cve = found_cves[0]
            details = fetch_cve_details_v2(first_cve)
            cve_text = f"{first_cve}: {details}"

        flagged_commits.append((commit, severity, cve_text, owasp_category))

        # CLI alert
        print(f"\n[⚠️ ALERT] High-risk security commit detected!\n"
              f"Commit Hash: {commit.hash}\n"
              f"Severity Level: {severity}\n"
              f"CVE Details: {cve_text}\n"
              f"OWASP Category: {owasp_category}\n")


def save_results(flagged_commits):
    from tests.security_analysis.patch_labeler import label_patches_with_commit_hash
    security_data = []
    os.makedirs("patches", exist_ok=True)

    for (commit, severity, cve_details, owasp_category) in flagged_commits:
        for mod in commit.modified_files:
            diff_text = mod.diff or ""
            if not diff_text.strip():
                continue

            label_patches_with_commit_hash(commit.hash, mod.filename, diff_text)
            row = {
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "severity": severity,
                "cve_details": cve_details,
                "owasp_category": owasp_category,
                "filename": mod.filename,
                "diff_preview": diff_text[:100]
            }
            security_data.append(row)

    save_patches_in_csv(security_data, "report.csv")
    save_patches_in_json(security_data, "report.json")
    save_patches_in_markdown(security_data, "report.md")


def save_patches_in_csv(data, filename):
    import csv
    if not data:
        print(f"[!] No data to write to {filename}")
        return
    headers = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"[+] CSV created -> {filename}")


def save_patches_in_json(data, filename):
    import json
    if not data:
        print(f"[!] No data to write to {filename}")
        return
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] JSON created -> {filename}")


def save_patches_in_markdown(data, filename):
    if not data:
        print(f"[!] No data to write to {filename}")
        return
    headers = list(data[0].keys())
    with open(filename, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in data:
            line = "| " + " | ".join(str(row[h]) for h in headers) + " |\n"
            f.write(line)
    print(f"[+] Markdown created -> {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract diffs from security-related commits using regex-based CVE detection and OWASP classification."
    )
    parser.add_argument("--repo", required=True, help="Path or URL to the Git repository.")
    parser.add_argument("--since", help="Start date (YYYY-MM-DD)", default=None)
    parser.add_argument("--to", help="End date (YYYY-MM-DD)", default=None)
    parser.add_argument("--continuous", action="store_true", help="Enable continuous scanning.")
    parser.add_argument("--interval", type=int, default=300, help="Seconds between scans if continuous.")
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
