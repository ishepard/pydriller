"""
patch_labeler.py
----------------
Contains a function to write out the entire patch (diff) for a given commit/file pair
to a .diff file labeled with the commit hash and filename.
"""

import os

def label_patches_with_commit_hash(commit_hash, filename, diff_text):
    """
    Creates a .diff file named '<commit_hash>_<filename>.diff' in the 'patches' folder.
    This step effectively 'labels' each patch with the commit hash for easy reference.
    """
    # Optionally shorten to first 7 chars if you prefer:
    short_hash = commit_hash[:7]

    # If the filename has slashes, replace them to avoid directory-creation issues
    sanitized_filename = filename.replace("/", "_")

    # Ensure 'patches' directory exists
    os.makedirs("patches", exist_ok=True)

    # Build final output path
    outfile = f"patches/{short_hash}_{sanitized_filename}.diff"

    # Write the full patch diff to the file
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(diff_text or "")  # or "" in case diff_text is None
    print(f"[+] Wrote patch file: {outfile}")
