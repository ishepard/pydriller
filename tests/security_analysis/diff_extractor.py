import argparse
import csv
import json

# We import the security commit filter function from commit_filter.py
from commit_filter import filter_security_commits

def extract_security_diffs_and_store(repo_url):
    """
    1. Calls 'filter_security_commits(repo_url)' to obtain flagged (security-related) commits.
    2. For each flagged commit, collects relevant info (commit hash, author, date, file name, etc.).
    3. Stores the resulting data in CSV, JSON, and Markdown formats.
    """

    # Retrieve flagged commits from the separate commit_filter.py file
    flagged_commits = filter_security_commits(repo_url)
    security_data = []

    # Build a list of dictionaries containing information about each commit/file
    for commit in flagged_commits:
        for mod in commit.modified_files:
            # Construct a dictionary capturing basic info
            entry = {
                "commit_hash": commit.hash,
                "author": commit.author.name,
                "date": str(commit.author_date),
                "file_name": mod.filename,
                # Only a snippet of the diff to prevent storing huge outputs
                "diff_preview": (mod.diff or "")[:100]
            }
            security_data.append(entry)

    # Store the data in three different output formats
    store_patches_in_csv(security_data, "report.csv")
    store_patches_in_json(security_data, "report.json")
    store_patches_in_markdown(security_data, "report.md")

    print("[+] Security-related commit data has been saved as report.csv, report.json, and report.md.")

def store_patches_in_csv(data, csv_filename):
    """
    Writes the list of dictionaries (data) into a CSV file.
    Each dictionary's keys will correspond to column headers.
    """
    if not data:
        print("[!] No data found to store in CSV.")
        return

    # Extract column headers from the keys of the first dictionary entry
    headers = data[0].keys()

    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"[+] CSV file created -> {csv_filename}")

def store_patches_in_json(data, json_filename):
    """
    Writes the list of dictionaries (data) into a JSON file.
    """
    if not data:
        print("[!] No data found to store in JSON.")
        return

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[+] JSON file created -> {json_filename}")

def store_patches_in_markdown(data, md_filename):
    """
    Writes the list of dictionaries (data) into a simple Markdown table.
    Each dictionary key becomes a column in the table.
    """
    if not data:
        print("[!] No data found to store in Markdown.")
        return

    # Use the keys of the first dictionary to determine table headers
    headers = list(data[0].keys())

    with open(md_filename, "w", encoding="utf-8") as f:
        # 1) Write a Markdown header row
        header_row = "| " + " | ".join(headers) + " |\n"
        f.write(header_row)

        # 2) Write a separator row (--- for each column)
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |\n"
        f.write(separator_row)

        # 3) For each data entry, build a row containing the values
        for row in data:
            row_values = [str(row[h]) for h in headers]
            line = "| " + " | ".join(row_values) + " |\n"
            f.write(line)

    print(f"[+] Markdown file created -> {md_filename}")

def main():
    """
    The main entry point to run this script via command-line arguments.

    Usage example:
        python diff_extractor.py --repo /path/or/url/to/your/repository
    """
    parser = argparse.ArgumentParser(
        description="Extract security-related commits and store results in CSV, JSON, and Markdown."
    )
    parser.add_argument("--repo", required=True,
                        help="Path or URL to the Git repository to analyze.")
    args = parser.parse_args()

    # Call the main logic function
    extract_security_diffs_and_store(args.repo)

if __name__ == "__main__":
    main()