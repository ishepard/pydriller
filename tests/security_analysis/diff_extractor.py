import argparse
import csv
from commit_filter import filter_security_commits

def extract_security_diffs(repo_url, output_csv=None):
    """
    Extract diffs from security-related commits in the specified repository.

    :param repo_url: Path or URL to the Git repository.
    :param output_csv: Optional CSV filename. If provided, diffs will be saved to this file
                       instead of being printed to the console.
    """
    # Call the filter function to get commits flagged as security-related
    flagged_commits = filter_security_commits(repo_url)

    if output_csv:
        # If the user specified a CSV filename, write the results to that file
        with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # Write header row
            writer.writerow(["Commit Hash", "File Path", "Diff"])

            for commit in flagged_commits:
                for mod in commit.modified_files:
                    # Determine file path (prefer new_path, fallback to old_path)
                    file_path = mod.new_path or mod.old_path
                    diff_text = mod.diff or ""

                    writer.writerow([
                        commit.hash,
                        file_path,
                        diff_text
                    ])

        print(f"[+] Security diffs have been saved to: {output_csv}")
    else:
        # If no CSV filename is specified, print the diffs to the console
        for commit in flagged_commits:
            print("=" * 60)
            print(f"Commit: {commit.hash}")
            for mod in commit.modified_files:
                file_path = mod.new_path or mod.old_path
                diff_text = mod.diff or ""

                print(f"\nModified File: {file_path}")
                print("Diff:\n", diff_text)


def main():
    """
    Entry point for running this script from the command line.

    Usage examples:
        python diff_extractor.py --repo <path_or_url_to_repo>
        python diff_extractor.py --repo <path_or_url_to_repo> --csv results.csv
    """
    parser = argparse.ArgumentParser(description="Extract diffs from commits flagged as security-related.")
    parser.add_argument("--repo", required=True,
                        help="Path or URL to the Git repository to analyze.")
    parser.add_argument("--csv", required=False,
                        help="Optional CSV filename to save results. If not provided, diffs will be printed.")
    args = parser.parse_args()

    extract_security_diffs(args.repo, args.csv)


if __name__ == "__main__":
    main()