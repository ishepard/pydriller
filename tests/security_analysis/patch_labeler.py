import os

def label_patches_with_commit_hash(commit_hash, filename, diff_text, output_dir):
    """
    Creates a .diff file named '<commit_hash>_<filename>.diff' in the provided output_dir.
    """
    short_hash = commit_hash[:7]
    sanitized_filename = filename.replace("/", "_")
    outfile = os.path.join(output_dir, f"{short_hash}_{sanitized_filename}.diff")
    os.makedirs(output_dir, exist_ok=True)
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(diff_text or "")
    print(f"[+] Wrote patch file: {outfile}")
