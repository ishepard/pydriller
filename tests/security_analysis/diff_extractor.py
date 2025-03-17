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
# 3) Security Keywords -> Severity
# ---------------------------------------------------------------------------
SECURITY_KEYWORDS = {
    # Typically "CVE" is not enough; we do a separate CVE extraction
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

# ---------------------------------------------------------------------------
# 4) Regex to detect CVE-YYYY-NNNNN
# ---------------------------------------------------------------------------
CVE_REGEX = re.compile(r'\bCVE-\d{4}-\d{4,}\b', re.IGNORECASE)


def fetch_cve_details_v2(cve_id: str) -> str:
    """
    Fetch CVE details from the NVD 2.0 API given a CVE ID.
    If found, return a short description. Otherwise return "No CVE details found."
    """
    try:
        # Example: GET https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-XXXX-XXXX
        url = f"{CVE_API_URL_V2}?cveId={cve_id}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # "vulnerabilities" is typically an array in the 2.0 data
            vulnerabilities = data.get("vulnerabilities", [])
            if vulnerabilities:
                # Usually the first item
                cve_obj = vulnerabilities[0]
                cve_desc = cve_obj["cve"]["descriptions"][0]["value"]
                return cve_desc
        return "No CVE details found."
    except Exception as exc:
        return f"Error fetching CVE details: {str(exc)}"


def extract_cve_ids_from_msg(commit_msg: str):
    """
    Return a list of CVE IDs found in the commit message using regex.
    e.g. ["CVE-2023-1234", "CVE-2019-0001"]
    """
    return CVE_REGEX.findall(commit_msg)


def classify_owasp(commit_message: str) -> str:
    """
    Classifies a commit under an OWASP category based on known keywords.
    Returns the FIRST matching category or 'Unknown Category'.
    """
    msg_lower = commit_message.lower()
    for keyword, category in OWASP_MAPPING.items():
        if keyword in msg_lower:
            return category
    return "Unknown Category"


def classify_severity(commit_message: str) -> str:
    """
    Assign a severity level if a known keyword is found.
    Return the FIRST match's severity or 'Low' if none found.
    (You can default to 'None' or 'Low' if no match.)
    """
    msg_lower = commit_message.lower()
    for keyword, severity in SECURITY_KEYWORDS.items():
        if keyword in msg_lower:
            return severity
    return "Low"  # fallback if no known keywords found

def extract_security_diffs_and_store(repo_url, since=None, to=None, continuous=False, interval=300):
    """
    Main function to:
    - Scan the repository for security-related commits
    - Use regex to extract CVE references
    - Classify security risks based on severity & OWASP
    - Store results in CSV, JSON, and Markdown
    - Support continuous scanning mode with interval-based execution

    :param repo_url: The target repository URL or path
    :param since: Start date for commit scanning
    :param to: End date for commit scanning
    :param continuous: Boolean flag to enable continuous mode
    :param interval: Time interval (in seconds) between continuous scans
    """
    last_checked_commit = None  # Track the last scanned commit to avoid reprocessing

    while True:
        repo_args = {"since": since, "to": to} if (since or to) else {}
        flagged_commits = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            for commit in Repository(repo_url, **repo_args).traverse_commits():
                if commit.hash == last_checked_commit:
                    break  # Stop processing if we reach the last known commit
                executor.submit(process_commit, commit, flagged_commits)

        if flagged_commits:
            save_results(flagged_commits)
            last_checked_commit = flagged_commits[0][0].hash  # Store latest scanned commit hash

        if not continuous:
            break

        # Log the scanning interval for user feedback
        print(f"[ℹ️] Sleeping for {interval} seconds before the next scan...")
        time.sleep(interval)  # Pause before re-scanning


def process_commit(commit, flagged_commits):
    """
    Processes each commit to:
    - Check for CVE references (using regex)
    - Identify security severity using predefined keywords
    - Classify the commit based on OWASP categories
    - Generate CLI alerts for high-risk security commits

    :param commit: PyDriller commit object
    :param flagged_commits: List to store flagged security commits
    """
    commit_msg_lower = commit.msg.lower()

    # Extract CVE IDs from the commit message
    found_cves = extract_cve_ids_from_msg(commit.msg)

    # Identify severity level (defaulting to "Low" if no keyword is found)
    severity = classify_severity(commit_msg_lower)

    # Classify the commit based on OWASP Top 10 categories
    owasp_category = classify_owasp(commit_msg_lower)

    # If a commit is classified as "High" or "Critical", or if it references a CVE, flag it
    if severity in ["Critical", "High"] or found_cves:
        cve_text = "No CVE found"
        if found_cves:
            first_cve = found_cves[0] # Process only the first CVE found
            cve_details = fetch_cve_details_v2(first_cve)
            cve_text = f"{first_cve}: {cve_details}"

        # Store the flagged commit for report generation
        flagged_commits.append((commit, severity, cve_text, owasp_category))

        # 🔴 CLI Alert for High-Risk Commits
        print(f"\n[⚠️ ALERT] High-risk security commit detected!\n"
              f"Commit Hash: {commit.hash}\n"
              f"Severity Level: {severity}\n"
              f"CVE Details: {cve_text}\n"
              f"OWASP Category: {owasp_category}\n")


def save_results(flagged_commits):
    """
    After scanning, gather the commit data and store in patches + CSV/JSON/Markdown.
    """
    security_data = []
    os.makedirs("patches", exist_ok=True)

    for (commit, severity, cve_details, owasp_category) in flagged_commits:
        for mod in commit.modified_files:
            full_diff = mod.diff or ""
            if not full_diff.strip():
                # skip empty diffs
                continue

            # Write out the patch
            label_patches_with_commit_hash(commit.hash, mod.filename, full_diff)

            # Build the dictionary entry
            entry = {
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "severity": severity,
                "cve_details": cve_details,
                "owasp_category": owasp_category,
                "filename": mod.filename,
                "diff_preview": full_diff[:100]
            }
            security_data.append(entry)

    # Save data to CSV/JSON/Markdown
    save_patches_in_csv(security_data, "report.csv")
    save_patches_in_json(security_data, "report.json")
    save_patches_in_markdown(security_data, "report.md")


def label_patches_with_commit_hash(commit_hash, filename, diff_text):
    """
    Creates a .diff file named '<commit_hash>_<filename>.diff' in the 'patches' folder.
    """
    short_hash = commit_hash[:7]
    sanitized_filename = filename.replace("/", "_")
    outfile = f"patches/{short_hash}_{sanitized_filename}.diff"
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(diff_text)
    print(f"[+] Wrote patch file: {outfile}")


def save_patches_in_csv(data, csv_filename):
    if not data:
        print("[!] No security data to write to CSV.")
        return
    headers = list(data[0].keys())
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"[+] CSV created -> {csv_filename}")


def save_patches_in_json(data, json_filename):
    if not data:
        print("[!] No security data to write to JSON.")
        return
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] JSON created -> {json_filename}")


def save_patches_in_markdown(data, md_filename):
    if not data:
        print("[!] No security data to write to Markdown.")
        return
    headers = list(data[0].keys())
    with open(md_filename, "w", encoding="utf-8") as f:
        # Write header
        f.write("| " + " | ".join(headers) + " |\n")
        # Write separator
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        # Write rows
        for row in data:
            row_values = [str(row[h]) for h in headers]
            line = "| " + " | ".join(row_values) + " |\n"
            f.write(line)
    print(f"[+] Markdown created -> {md_filename}")


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
