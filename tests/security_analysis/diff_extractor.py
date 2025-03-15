import argparse
import csv
import json
import os
import time
import requests
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pydriller import Repository

# CVE API Endpoint
CVE_API_URL = "https://services.nvd.nist.gov/rest/json/cves/1.0"

# OWASP Classification (Improved Mapping with regex handling)
OWASP_MAPPING = {
    r"\binjection\b": "A03:2021 - Injection",
    r"\bsql injection\b": "A03:2021 - Injection",
    r"\bcross site scripting\b": "A07:2021 - Identification & Authentication Failures",
    r"\bxss\b": "A07:2021 - Identification & Authentication Failures",
    r"\bbuffer overflow\b": "A05:2021 - Security Misconfiguration",
    r"\bprivilege escalation\b": "A06:2021 - Vulnerable & Outdated Components",
    r"\bunauthorized access\b": "A01:2021 - Broken Access Control",
    r"\bdenial of service\b": "A09:2021 - Security Logging & Monitoring Failures",
}

# Security Keywords + Severity Level (No Changes Here)
SECURITY_KEYWORDS = {
    "cve": "Critical",
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
    "mitigation": "Low"
}

import re

def extract_cve_id(commit_message):
    """
    Extracts CVE ID (if any) from the commit message.
    """
    match = re.search(r'CVE-\d{4}-\d+', commit_message, re.IGNORECASE)
    return match.group(0) if match else None


def fetch_cve_details(cve_id):
    try:
        response = requests.get(f"{CVE_API_URL}?cveId={cve_id}")
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "CVE_Items" in data["result"]:
                return data["result"]["CVE_Items"][0]["cve"]["description"]["description_data"][0]["value"]
        return "No CVE details found."
    except Exception as e:
        return f"Error fetching CVE details: {str(e)}"


def classify_owasp(commit_message):
    """
    Classifies a commit under an OWASP category using regex matching.
    """
    commit_message = commit_message.lower()

    for pattern, category in OWASP_MAPPING.items():
        if re.search(pattern, commit_message):
            return category

    return "Unknown Category"

def extract_security_diffs_and_store(repo_url, since=None, to=None, continuous=False, interval=300):
    """
    Scans the repository for security-related commits.
    Fetches CVE details & assigns OWASP category.
    Supports continuous monitoring.
    """
    while True:
        repo_args = {"since": since, "to": to} if (since or to) else {}

        flagged_commits = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            for commit in Repository(repo_url, **repo_args).traverse_commits():
                executor.submit(process_commit, commit, flagged_commits)

        if not flagged_commits:
            print("[!] No security-related commits found. Sleeping...")
        else:
            save_results(flagged_commits)

        if not continuous:
            break

        time.sleep(interval)  # Wait before the next scan

def process_commit(commit, flagged_commits):
    """
    Processes a commit to check for security-related keywords.
    Extracts real CVE ID.
    Fetches CVE details if found.
    Assigns OWASP category using improved regex matching.
    """
    for keyword, severity in SECURITY_KEYWORDS.items():
        if keyword in commit.msg.lower():
            cve_id = extract_cve_id(commit.msg)
            cve_details = fetch_cve_details(cve_id)
            owasp_category = classify_owasp(commit.msg)
            flagged_commits.append((commit, severity, cve_details, owasp_category))
            break

def save_results(flagged_commits):
    """
    Saves results to CSV, JSON, and Markdown.
    """
    security_data = []
    os.makedirs("patches", exist_ok=True)

    for commit, severity, cve_details, owasp_category in flagged_commits:
        for mod in commit.modified_files:
            if not mod.diff:
                continue
            save_patch(commit.hash, mod.filename, mod.diff)

            entry = {
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "severity": severity,
                "cve_details": cve_details,
                "owasp_category": owasp_category,
                "filename": mod.filename,
                "diff_preview": mod.diff[:100]
            }
            security_data.append(entry)

    save_csv(security_data, "report.csv")
    save_json(security_data, "report.json")
    save_markdown(security_data, "report.md")

def save_patch(commit_hash, filename, diff_text):
    """
    Saves the diff content to a labeled patch file.
    """
    short_hash = commit_hash[:7]
    sanitized_filename = filename.replace("/", "_")
    patch_path = f"patches/{short_hash}_{sanitized_filename}.diff"

    with open(patch_path, "w", encoding="utf-8") as f:
        f.write(diff_text)

    print(f"[+] Saved patch: {patch_path}")

def save_csv(data, filename):
    """Saves extracted data to a CSV file."""
    if not data:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"[+] CSV created: {filename}")

def save_json(data, filename):
    """Saves extracted data to a JSON file."""
    if not data:
        return
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] JSON created: {filename}")

def save_markdown(data, filename):
    """Saves extracted data to a Markdown table."""
    if not data:
        return
    headers = list(data[0].keys())
    with open(filename, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in data:
            f.write("| " + " | ".join(str(row[h]) for h in headers) + " |\n")
    print(f"[+] Markdown created: {filename}")

def main():
    """
    Parses arguments and starts the extraction process.
    """
    parser = argparse.ArgumentParser(
        description="Extract security-related commit diffs with CVE & OWASP classification."
    )
    parser.add_argument("--repo", required=True, help="Path or URL of the repository.")
    parser.add_argument("--since", help="Start date (YYYY-MM-DD)", default=None)
    parser.add_argument("--to", help="End date (YYYY-MM-DD)", default=None)
    parser.add_argument("--continuous", action="store_true", help="Enable continuous monitoring.")
    parser.add_argument("--interval", type=int, default=300, help="Time between scans (seconds).")
    args = parser.parse_args()

    since_date = datetime.strptime(args.since, "%Y-%m-%d") if args.since else None
    to_date = datetime.strptime(args.to, "%Y-%m-%d") if args.to else None

    extract_security_diffs_and_store(args.repo, since=since_date, to=to_date, continuous=args.continuous, interval=args.interval)

if __name__ == "__main__":
    main()
