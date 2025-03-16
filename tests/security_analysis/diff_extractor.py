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
    Main scanning function:
      - Scans the repository for commits
      - Looks for CVE references via regex
      - Classifies severity via known keywords
      - Classifies OWASP category
      - Writes results to CSV/JSON/Markdown
      - Optionally runs continuously
    """
    while True:
        # Build PyDriller arguments
        repo_args = {"since": since, "to": to} if (since or to) else {}

        flagged_commits = []
        # Use concurrency for performance if needed
        with ThreadPoolExecutor(max_workers=4) as executor:
            for commit in Repository(repo_url, **repo_args).traverse_commits():
                executor.submit(process_commit, commit, flagged_commits)

        if flagged_commits:
            save_results(flagged_commits)
        else:
            print("[!] No security-related commits found in this scan.")

        if not continuous:
            break
        print(f"[i] Sleeping for {interval} seconds before next scan...")
        time.sleep(interval)


def process_commit(commit, flagged_commits):
    """
    Checks the commit message for:
      - CVE references (using regex)
      - Security keywords for severity
      - OWASP category based on keywords
    If the commit is security-related (non-"Low" severity or containing a CVE), it is added to flagged_commits.
    """
    # Convert commit message to lower-case for consistent matching.
    commit_msg_lower = commit.msg.lower()

    # 1) Extract CVE identifiers (if any) using regex.
    found_cves = extract_cve_ids_from_msg(commit.msg)

    # 2) Determine severity from security keywords (defaults to "Low" if no match).
    severity = classify_severity(commit_msg_lower)

    # 3) Determine the OWASP category from the commit message.
    owasp_category = classify_owasp(commit_msg_lower)

    # 4) Decide if the commit should be flagged:
    #    If the severity is not "Low" or if any CVE IDs were found.
    if severity != "Low" or found_cves:
        # Prepare a string to hold CVE details.
        cve_text = "No CVE found"
        if found_cves:
            # For simplicity, fetch details for the first CVE found.
            first_cve = found_cves[0]
            cve_details = fetch_cve_details_v2(first_cve)
            cve_text = f"{first_cve}: {cve_details}"

        flagged_commits.append((commit, severity, cve_text, owasp_category))


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
