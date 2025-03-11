import argparse
import csv
import json
import os
from pydriller import Repository

########################################################################
# 1) Define the security keywords and their associated severity levels
########################################################################
SECURITY_KEYWORDS = {
    "cve": "Critical",
    "buffer overflow": "High",
    "exploit": "High",
    "vulnerability": "Medium",
    "security fix": "Medium",
    "patch": "Low",
    "mitigation": "Low"
}


def extract_security_diffs_and_store(repo_url):
    """
    Main function:
      - Scans the repository for security-related commits by matching keywords (with severity).
      - For each flagged commit, writes a .diff file labeled by commit hash.
      - Stores a snippet of the commit data (including severity) in CSV, JSON, and Markdown.
    """

    ########################################################################
    # 2) Filter commits based on the SECURITY_KEYWORDS dictionary
    ########################################################################
    flagged_commits = []
    for commit in Repository(repo_url).traverse_commits():
        matched_severity = None
        for keyword, severity in SECURITY_KEYWORDS.items():
            if keyword in commit.msg.lower():
                matched_severity = severity
                break  # only use the first match to assign severity
        if matched_severity:
            flagged_commits.append((commit, matched_severity))

    if not flagged_commits:
        print("[!] No security-related commits were found. Exiting.")
        return

    # We'll store data (commit info, severity, diff snippet) for CSV/JSON/Markdown
    security_data = []

    # Ensure we have a folder for storing .diff files
    os.makedirs("patches", exist_ok=True)

    ########################################################################
    # 3) For each flagged commit, label patches with commit hash & store data
    ########################################################################
    for commit, severity in flagged_commits:
        for mod in commit.modified_files:
            full_diff = mod.diff or ""

            # A) Write out the full patch to a .diff file labeled by commit hash + filename
            label_patches_with_commit_hash(commit.hash, mod.filename, full_diff)

            # B) Build dictionary containing info for CSV/JSON/Markdown
            entry = {
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "severity": severity,  # from the matched keyword
                "filename": mod.filename,
                # We'll only store a partial snippet to keep the table short
                "diff_preview": full_diff[:100]
            }
            security_data.append(entry)

    ########################################################################
    # 4) Write summary data to CSV, JSON, and Markdown
    ########################################################################
    store_patches_in_csv(security_data, "report.csv")
    store_patches_in_json(security_data, "report.json")
    store_patches_in_markdown(security_data, "report.md")

    print("[+] Done. Labeled .diff files in 'patches/' folder.")
    print("[+] Summary stored in 'report.csv', 'report.json', and 'report.md'.")


def label_patches_with_commit_hash(commit_hash, filename, diff_text):
    """
    Creates a .diff file named '<commitHash>_<filename>.diff' in the 'patches' folder,
    labeling each patch with the commit hash for easy reference.
    """
    short_hash = commit_hash[:7]  # optional: shorten commit hash
    sanitized_filename = filename.replace("/", "_")
    outfile = f"patches/{short_hash}_{sanitized_filename}.diff"

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(diff_text)
    print(f"[+] Wrote patch file -> {outfile}")


def store_patches_in_csv(data, csv_filename):
    """
    Writes the list of dictionaries to a CSV file, including severity and commit hash.
    """
    if not data:
        print("[!] No security data to write to CSV.")
        return

    headers = list(data[0].keys())
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"[+] CSV created -> {csv_filename}")


def store_patches_in_json(data, json_filename):
    """
    Writes the list of dictionaries to a JSON file, including severity and commit hash.
    """
    if not data:
        print("[!] No security data to write to JSON.")
        return

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[+] JSON created -> {json_filename}")


def store_patches_in_markdown(data, md_filename):
    """
    Writes the list of dictionaries to a Markdown table, including severity and commit hash.
    """
    if not data:
        print("[!] No security data to write to Markdown.")
        return

    headers = list(data[0].keys())
    with open(md_filename, "w", encoding="utf-8") as f:
        # Header row
        header_row = "| " + " | ".join(headers) + " |\n"
        f.write(header_row)

        # Separator row
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |\n"
        f.write(separator_row)

        # Data rows
        for row in data:
            row_values = [str(row[h]) for h in headers]
            line = "| " + " | ".join(row_values) + " |\n"
            f.write(line)

    print(f"[+] Markdown created -> {md_filename}")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Extract diffs from security-related commits using severity-based keywords."
    )
    parser.add_argument("--repo", required=True,
                        help="Path or URL to the Git repository to analyze.")
    args = parser.parse_args()

    extract_security_diffs_and_store(args.repo)


if __name__ == "__main__":
    main()
