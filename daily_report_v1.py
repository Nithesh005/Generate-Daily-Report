from openai import OpenAI
from git import Repo
from datetime import datetime, timedelta

# ==== SETUP ====
client = OpenAI(api_key="test")  # Updated for v1.x
since = datetime.now() - timedelta(days=10)

repos = {
    "EZBILL-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\EZBILL-SERVICE'),
    "BBPS-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\BBPS-SERVICE'),
    "TYCHE-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\TYCHE-SERVICE'),
}

# ==== COLLECT COMMITS ====
commit_logs = []
for name, repo in repos.items():
    for commit in repo.iter_commits():
        commit_time = datetime.fromtimestamp(commit.committed_date)
        if commit_time > since:
            commit_logs.append(f"[{name}] {commit.author.name}: {commit.summary}")

commit_text = "\n".join(commit_logs)

if not commit_text.strip():
    print("No recent commits found.")
    exit()

# ==== GPT PROMPT ====
prompt = f"""
Summarize the following git commit logs into a daily work report. Group by project, highlight key features, bug fixes, and improvements. Make it sound professional.

{commit_text}
"""

# ==== NEW OPENAI API CALL (v1.x) ====
response = client.chat.completions.create(
    # model="gpt-4",  # or "gpt-3.5-turbo"
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a technical assistant who creates professional work reports."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=500
)

summary = response.choices[0].message.content
print("==== Daily Work Summary ====\n")
print(summary)
