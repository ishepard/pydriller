from pydriller import Repository

# Extended list of security-related keywords mapped to severity levels
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
    "heap overflow": "High",
    "stack overflow": "High",
    "command injection": "High",
    "race condition": "Medium",
    "arbitrary file upload": "Medium",
    "directory traversal": "Medium",
    "zero day": "Medium",
    "unauthorized access": "Medium",
    "denial of service": "Low",
    "dos": "Low",
    "ddos": "Low",
    "cryptographic weakness": "Low",
    "authentication bypass": "Low",
    "patch": "Low",
    "security fix": "Low",
    "mitigation": "Low"
}

def filter_security_commits(repo_url):
    """
    Traverses the repository and filters commits that contain security-related keywords.

    :param repo_url: URL or local path to the Git repository.
    :return: List of security-related commits with severity classification.
    """
    flagged_commits = []

    for commit in Repository(repo_url).traverse_commits():
        # Check commit message for security-related keywords
        for keyword, severity in SECURITY_KEYWORDS.items():
            if keyword in commit.msg.lower():
                flagged_commits.append({
                    "commit_hash": commit.hash,
                    "author": commit.author.name,
                    "date": commit.author_date,
                    "message": commit.msg,
                    "severity": severity  # Assign severity level based on keyword
                })
                break  # Stop checking after the first match to avoid duplicates

    return flagged_commits