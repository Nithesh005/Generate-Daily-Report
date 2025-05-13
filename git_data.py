from flask import Flask, jsonify
from git import Repo
# from datetime import datetime, timedelta
from datetime import datetime, date, timedelta
from mail.send_mail import send_daily_report

app = Flask(__name__)
@app.route('/send-report', methods=['GET'])
def send_report():
    try:
        print("📊 Gathering Reports ... 📈")
        # Set time window
        n = 1
        # since = datetime.now() - timedelta(days=n)
        since = datetime.combine(date.today(), datetime.min.time())

        # Define repositories with labels
        repos = {
            "EZBILL-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\EZBILL-SERVICE'),
            "BBPS-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\BBPS-SERVICE'),
            "TYCHE-SERVICE": Repo(r'D:\Wowelse\Dream-Infinity\TYCHE-SERVICE')
        }

        report_sections = []
        commit_count = 0
        author_stats = {}

        # Collect and format commits
        for name, repo in repos.items():
            section = [f"\n📁 **{name}**\n" + "-"*30]
            for commit in repo.iter_commits():
                commit_time = datetime.fromtimestamp(commit.committed_date)
                if commit_time > since:
                    msg = commit.summary
                    author = commit.author.name
                    section.append(f"{msg}")
                    # section.append(f"📝 {msg} — _{author}_")
                    commit_count += 1

                    # Track author stats
                    author_stats[author] = author_stats.get(author, 0) + 1
            if len(section) > 1:
                report_sections.append("\n".join(section))
        # print("📂 Categorizing Reports 🗂️")
        # Highlights
        highlights = {
            "Features": [],
            "Bug Fixes": [],
            "Refactors": [],
            "Other Changes": []
        }

        keywords = {
            "Features": ["add", "feature", "implement", "create"],
            "Bug Fixes": ["fix", "resolve", "bug", "error"],
            "Refactors": ["refactor", "clean", "optimize", "structure"]
        }
        # print("⚙️ Generating Reports 📊")
        for section in report_sections:
            for line in section.splitlines():
                lower = line.lower()
                matched = False
                for category, keys in keywords.items():
                    if any(k in lower for k in keys):
                        highlights[category].append(line)
                        matched = True
                        break
                if not matched and line.strip().startswith("📝"):
                    highlights["Other Changes"].append(line)
        
        # print("✨ Highlights Reports 🌟")
        # Build final report
        # ==============================
        final_report = f"""
        Hi,\n
        🗓️ Daily Status Report ({datetime.now().strftime('%B %d, %Y')})
        Following are the current updates,
        """
        # ==============================
        # 🔢 Total Commits: {commit_count}
        # 👨‍💻 Contributors:
        # + "\n".join([f"- {author}: {count} commits" for author, count in author_stats.items()]) + "\n"


        # Append highlights
        # for title, items in highlights.items():
        #     import pdb; pdb.set_trace()
        #     if items:
        #         final_report += f"\n{title}\n" + "-"*len(title) + "\n" + "\n".join(items) + "\n"

        cleaned_items = []
        # import pdb; pdb.set_trace()

        for title, items in highlights.items():
            if items:
                # cleaned_items.append(f"\n{title}\n" + "-"*len(title))
                cleaned_items.append(f"\n{title} : \n")
                for item in items:
                    # Remove emoji at the start and trailing attribution
                    cleaned_item = item.lstrip("*").strip()
                    if "— _Nithi_'" in cleaned_item:
                        cleaned_item = cleaned_item.split("— _Nithi_'")[0].strip()
                    cleaned_items.append(f"- {cleaned_item}\n")

        footer_text = """
        Warm regards,
        Nithesh
        """
        final_report = final_report + "\n".join(cleaned_items)+"\n" + footer_text

        # Append repo-wise detailed commits
        # final_report += "\n\n📂 Repository Breakdown\n=======================" + "".join(report_sections)

        # Send the email with the report
        send_daily_report(final_report)

        return jsonify({"message": "✅ Report sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": f"❌ Failed to generate or send report: {e}"}), 500

if __name__ == '__main__':
    # with app.app_context():
    #     send_report()  # This now has access to Flask context
    app.run(debug=True)
