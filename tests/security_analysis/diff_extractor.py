import argparse
import csv
import json
import os
import re
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import requests

from pydriller import Repository

# ---------------------------------------------------------------------------
# 1) CVE API Endpoint (NVD 2.0)
# ---------------------------------------------------------------------------
CVE_API_URL_V2 = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# ---------------------------------------------------------------------------
# 2) OWASP Classification Mapping
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
    "security fix": "Low",
    "patch": "Low",
    "mitigation": "Low"
}

# ---------------------------------------------------------------------------
# 3) Security Keywords -> Severity (excluding CVE, which is handled separately)
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
    "mitigation": "Low"
}

# ---------------------------------------------------------------------------
# 4) Regex to detect CVE IDs (e.g., CVE-2023-1234)
# ---------------------------------------------------------------------------
CVE_REGEX = re.compile(r'\bCVE-\d{4}-\d{4,}\b', re.IGNORECASE)


def fetch_cve_details_v2(cve_id: str) -> str:
    """
    Fetches CVE details from the NVD 2.0 API for a given CVE ID.
    Returns a short description or an error message.
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
    Extracts and returns a list of CVE IDs found in a commit message.
    """
    return CVE_REGEX.findall(commit_msg)


def classify_owasp(commit_msg: str) -> str:
    """
    Classifies the commit based on OWASP mapping.
    Returns the first matching OWASP category or 'Unknown Category'.
    """
    msg_lower = commit_msg.lower()
    for keyword, category in OWASP_MAPPING.items():
        if keyword in msg_lower:
            return category
    return "Unknown Category"


def classify_severity(commit_msg: str) -> str:
    """
    Determines the severity based on security keywords found in the commit message.
    Returns the first matching severity or 'Low' as fallback.
    """
    msg_lower = commit_msg.lower()
    for keyword, severity in SECURITY_KEYWORDS.items():
        if keyword in msg_lower:
            return severity
    return "Low"


def extract_security_diffs_and_store(repo_url, since=None, to=None, continuous=False, interval=300, max_workers=4):
    """
    Main function to:
    - Scan the repository for security-related commits (using keywords and CVE extraction)
    - Classify commits based on severity and OWASP categories
    - Generate CLI alerts for high-risk commits
    - Store diff files in 'patches/' and create summary reports (CSV, JSON, Markdown)
    - Support continuous scanning mode with interval-based execution
    - Return a separate list of flagged security commits when scanning completes (if continuous is False)

    :param repo_url: Repository path or URL.
    :param since: Optional start date (YYYY-MM-DD).
    :param to: Optional end date (YYYY-MM-DD).
    :param continuous: If True, runs in continuous scanning mode.
    :param interval: Interval in seconds between scans in continuous mode.
    :param max_workers: Number of threads for parallel processing.
    :return: List of flagged security commits (if continuous mode is disabled).
    """
    last_checked_commit = None  # For continuous mode to avoid reprocessing

    while True:
        repo_args = {"since": since, "to": to} if (since or to) else {}
        flagged_commits = []

        # Use multi-threading to process commits faster
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for commit in Repository(repo_url, **repo_args).traverse_commits():
                # If continuous scanning is enabled, stop at the last processed commit
                if last_checked_commit and commit.hash == last_checked_commit:
                    break
                executor.submit(process_commit, commit, flagged_commits)

        if flagged_commits:
            # Save results: write diff files and generate summary reports
            save_results(flagged_commits)
            # For continuous mode, update the last processed commit
            if not continuous:
                # In non-continuous mode, return the list of flagged commits for further use
                return flagged_commits
            last_checked_commit = flagged_commits[0][0].hash
        else:
            print("[!] No new security-related commits found.")

        if not continuous:
            break

        print(f"[INFO] Sleeping for {interval} seconds before the next scan...")
        time.sleep(interval)


def process_commit(commit, flagged_commits):
    """
    Processes a commit to:
    - Extract CVE IDs and fetch their details.
    - Classify severity based on security keywords.
    - Classify the commit under an OWASP category.
    - Generate an alert for high-risk commits.
    - Append the commit info to the flagged_commits list.

    :param commit: A PyDriller commit object.
    :param flagged_commits: Shared list to store flagged commits.
    """
    commit_msg = commit.msg
    cve_ids = extract_cve_ids_from_msg(commit_msg)
    cve_info = None
    if cve_ids:
        # Process only the first found CVE for simplicity
        first_cve = cve_ids[0]
        cve_info = f"{first_cve}: {fetch_cve_details_v2(first_cve)}"

    severity = classify_severity(commit_msg)
    owasp_category = classify_owasp(commit_msg)

    # If the commit has a high or critical severity, or contains CVE references, flag it
    if severity in ["Critical", "High"] or cve_ids:
        flagged_commits.append((commit, severity, cve_info if cve_info else "No CVE found", owasp_category))
        if severity in ["Critical", "High"]:
            print(
                f"\n[ALERT] High-risk commit detected!\n"
                f"Commit: {commit.hash}\n"
                f"Severity: {severity}\n"
                f"OWASP Category: {owasp_category}\n"
                f"CVE Info: {cve_info if cve_info else 'None'}\n"
            )


def save_results(flagged_commits):
    """
    Saves diff files for each flagged commit and generates summary reports in CSV, JSON, and Markdown.

    :param flagged_commits: List of tuples (commit, severity, cve_info, owasp_category)
    """
    security_data = []
    os.makedirs("patches", exist_ok=True)

    # For trend analysis: count commits per month
    monthly_counts = {}

    for (commit, severity, cve_info, owasp_category) in flagged_commits:
        commit_month = commit.author_date.strftime("%Y-%m")
        monthly_counts[commit_month] = monthly_counts.get(commit_month, 0) + 1

        for mod in commit.modified_files:
            full_diff = mod.diff or ""
            if not full_diff.strip():
                continue

            label_patches_with_commit_hash(commit.hash, mod.filename, full_diff)
            entry = {
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "severity": severity,
                "cve_details": cve_info if cve_info else "N/A",
                "owasp_category": owasp_category,
                "filename": mod.filename,
                "diff_preview": full_diff[:100]
            }
            security_data.append(entry)

    save_patches_in_csv(security_data, "report.csv")
    save_patches_in_json(security_data, "report.json")
    save_patches_in_markdown(security_data, "report.md")

    print("[OK] Finished saving patch files in 'patches/' folder.")
    print("[OK] Summary reports saved in 'report.csv', 'report.json', and 'report.md'.")

    print("\n=== Trend Analysis ===")
    for month in sorted(monthly_counts.keys()):
        print(f"{month}: {monthly_counts[month]} commits")


def label_patches_with_commit_hash(commit_hash, filename, diff_text):
    """
    Creates a .diff file in the 'patches' folder labeled with the commit hash and filename.

    :param commit_hash: SHA of the commit.
    :param filename: Name of the modified file.
    :param diff_text: The diff content.
    """
    short_hash = commit_hash[:7]
    sanitized_filename = filename.replace("/", "_")
    outfile = f"patches/{short_hash}_{sanitized_filename}.diff"
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(diff_text)
    print(f"[+] Wrote patch file: {outfile}")


def save_patches_in_csv(data, csv_filename):
    """Saves the list of security commit dictionaries to a CSV file."""
    if not data:
        print("[!] No security data to write to CSV.")
        return
    headers = list(data[0].keys())
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"[+] CSV created: {csv_filename}")


def save_patches_in_json(data, json_filename):
    """Saves the list of security commit dictionaries to a JSON file."""
    if not data:
        print("[!] No security data to write to JSON.")
        return
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] JSON created: {json_filename}")


def save_patches_in_markdown(data, md_filename):
    """Saves the list of security commit dictionaries to a Markdown table."""
    if not data:
        print("[!] No security data to write to Markdown.")
        return
    headers = list(data[0].keys())
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in data:
            row_values = [str(row[h]) for h in headers]
            f.write("| " + " | ".join(row_values) + " |\n")
    print(f"[+] Markdown created: {md_filename}")


def main():
    """Parses command-line arguments and starts the extraction process."""
    parser = argparse.ArgumentParser(
        description="Extract diffs from security-related commits with CVE detection, OWASP classification, "
                    "and trend analysis. Supports continuous scanning."
    )
    parser.add_argument("--repo", required=True, help="Path or URL to the Git repository.")
    parser.add_argument("--since", help="Start date (YYYY-MM-DD) to limit commit history.", default=None)
    parser.add_argument("--to", help="End date (YYYY-MM-DD) to limit commit history.", default=None)
    parser.add_argument("--continuous", action="store_true", help="Enable continuous scanning mode.")
    parser.add_argument("--interval", type=int, default=300, help="Seconds between scans if continuous.")
    args = parser.parse_args()

    since_date = datetime.strptime(args.since, "%Y-%m-%d") if args.since else None
    to_date = datetime.strptime(args.to, "%Y-%m-%d") if args.to else None

    flagged_commits = extract_security_diffs_and_store(
        repo_url=args.repo,
        since=since_date,
        to=to_date,
        continuous=args.continuous,
        interval=args.interval
    )
    # If not in continuous mode, flagged_commits is returned for further processing if needed.
    if flagged_commits:
        print(f"[INFO] Total flagged commits returned: {len(flagged_commits)}")


if __name__ == "__main__":
    main()
