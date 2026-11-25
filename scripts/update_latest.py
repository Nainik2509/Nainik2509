"""Refresh the 'Latest Repositories' block in README.md from the GitHub API."""
import json, os, re, subprocess, sys

USER = os.environ.get("GH_USER", "Nainik2509")
README = "README.md"
START, END = "<!-- LATEST-REPOS:START -->", "<!-- LATEST-REPOS:END -->"

raw = subprocess.check_output(
    ["gh", "api", f"users/{USER}/repos?type=owner&sort=pushed&per_page=30"], text=True
)
repos = [r for r in json.loads(raw) if not r["fork"] and not r["archived"] and r["name"].lower() != USER.lower()][:5]

rows = ["| Repository | About | Language | Updated |", "| :-- | :-- | :-- | :-- |"]
for r in repos:
    about = (r["description"] or "-").replace("|", "/")
    if len(about) > 90:
        about = about[:87].rstrip() + "..."
    rows.append(f"| [**{r['name']}**]({r['html_url']}) | {about} | {r['language'] or '-'} | {r['pushed_at'][:10]} |")
block = "\n".join(rows)

text = open(README, encoding="utf-8").read()
pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
if not pattern.search(text):
    sys.exit("markers not found in README.md")
new = pattern.sub(f"{START}\n{block}\n{END}", text)
if new != text:
    open(README, "w", encoding="utf-8").write(new)
    print("README updated")
else:
    print("no change")
