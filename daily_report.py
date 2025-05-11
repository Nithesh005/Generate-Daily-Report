from git import Repo
from datetime import datetime, timedelta

# Repo paths
repos = {
    "EZBILL-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\EZBILL-SERVICE'),
    "BBPS-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\BBPS-SERVICE'),
    "TYCHE-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\TYCHE-SERVICE'),
}

since = datetime.now() - timedelta(days=3)

# Collect commit messages
all_commits = []
for name, repo in repos.items():
    for commit in repo.iter_commits():
        commit_time = datetime.fromtimestamp(commit.committed_date)
        if commit_time > since:
            all_commits.append(f"[{name}] {commit.author.name}: {commit.summary}")

# Combine for AI input
raw_commit_text = "\n".join(all_commits)

print("🧠 Feed this into ChatGPT:\n")
print(raw_commit_text)