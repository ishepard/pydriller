SECURITY_KEYWORDS = ["security", "CVE", "buffer overflow", "exploit"]

def filter_security_commits(repo_url):
    from pydriller import Repository
    flagged_commits = []
    for commit in Repository(repo_url).traverse_commits():
        # If commit message or diff lines contain security terms
        if any(kw in commit.msg.lower() for kw in SECURITY_KEYWORDS):
            flagged_commits.append(commit)
    return flagged_commits
