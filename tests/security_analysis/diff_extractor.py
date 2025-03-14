import argparse
import csv
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pydriller import Repository

# 🔍 Security keywords mapped to severity levels
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

def extract_security_diffs_and_store(repo_url, since=None, to=None, max_workers=4):
    """
    ✅ Scans the repository for security-related commits.
    ✅ Filters commits using `since` and `to` for performance optimization.
    ✅ Extracts only relevant diffs, reducing memory and CPU usage.
    ✅ Uses multi-threading for faster processing.

    :param repo_url: Path or URL of the repository.
    :param since: Date from which to start scanning commits.
    :param to: Date until which to scan commits.
    :param max_workers: Number of parallel threads for faster execution.
    """
    repo_args = {"since": since, "to": to} if (since or to) else {}

    # 🔹 Use multithreading for better performance
    flagged_commits = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for commit in Repository(repo_url, **repo_args).traverse_commits():
            executor.submit(process_commit, commit, flagged_commits)

    if not flagged_commits:
        print("[!] No security-related commits found. Exiting.")
        return

    security_data = []
    os.makedirs("patches", exist_ok=True)  # Ensure 'patches' directory exists

    for commit, severity in flagged_commits:
        for mod in commit.modified_files:
            if not mod.diff:
                continue  # Skip files without meaningful changes

            # 🔹 Save diff to a labeled patch file
            save_patch(commit.hash, mod.filename, mod.diff)

            # 🔹 Store essential commit data for reports
            entry = {
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "severity": severity,
                "filename": mod.filename,
                "diff_preview": mod.diff[:100]  # Store only the first 100 characters for preview
            }
            security_data.append(entry)

    # 🔹 Generate output reports
    save_csv(security_data, "report.csv")
    save_json(security_data, "report.json")
    save_markdown(security_data, "report.md")

    print("[✅] Done. Check 'patches/' for diff files.")
    print("[✅] Summary stored in 'report.csv', 'report.json', and 'report.md'.")

def process_commit(commit, flagged_commits):
    """
    Processes a commit to check for security-related keywords.

    :param commit: A commit object from PyDriller.
    :param flagged_commits: Shared list to store flagged commits.
    """
    for keyword, severity in SECURITY_KEYWORDS.items():
        if keyword in commit.msg.lower():
            flagged_commits.append((commit, severity))
            break  # Stop checking after the first match

def save_patch(commit_hash, filename, diff_text):
    """
    Saves the diff content to a labeled patch file.

    :param commit_hash: SHA hash of the commit.
    :param filename: Name of the modified file.
    :param diff_text: The diff content.
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
        print("[!] No data to write to CSV.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"[+] CSV created: {filename}")

def save_json(data, filename):
    """Saves extracted data to a JSON file."""
    if not data:
        print("[!] No data to write to JSON.")
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[+] JSON created: {filename}")

def save_markdown(data, filename):
    """Saves extracted data to a Markdown table."""
    if not data:
        print("[!] No data to write to Markdown.")
        return

    headers = list(data[0].keys())
    with open(filename, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in data:
            f.write("| " + " | ".join(str(row[h]) for h in headers) + " |\n")

    print(f"[+] Markdown created: {filename}")

def main():
    """Parses arguments and starts the extraction process."""
    parser = argparse.ArgumentParser(
        description="Extract security-related commit diffs with optimized performance."
    )
    parser.add_argument("--repo", required=True, help="Path or URL of the repository.")
    parser.add_argument("--since", help="Start date (YYYY-MM-DD)", default=None)
    parser.add_argument("--to", help="End date (YYYY-MM-DD)", default=None)
    args = parser.parse_args()

    # Convert dates if provided
    since_date = datetime.strptime(args.since, "%Y-%m-%d") if args.since else None
    to_date = datetime.strptime(args.to, "%Y-%m-%d") if args.to else None

    extract_security_diffs_and_store(args.repo, since=since_date, to=to_date)

if __name__ == "__main__":
    main()