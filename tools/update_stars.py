"""
Update GitHub star counts for repos listed in resources.html

Usage (PowerShell/CMD):
  python tools/update_stars.py

Optional:
  Set GITHUB_TOKEN env var to increase API rate limits.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "resources.html"
STARS_JSON_PATH = ROOT / "stars.json"


def extract_repos_from_html(html_path: Path) -> list[str]:
    """Extract GitHub repos from the toolsData object in resources.html.

    Looks for lines like: repo: "owner/name"
    """
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Narrow to toolsData block if present (best-effort)
    m = re.search(r"const\\s+toolsData\\s*=\\s*({.*?});", content, re.DOTALL)
    search_area = m.group(1) if m else content

    repos: set[str] = set()
    for line in search_area.splitlines():
        if "repo:" in line:
            repo_match = re.search(r"repo:\s*[\'\"]([^\'\"]+)[\'\"]", line)
            if repo_match:
                repos.add(repo_match.group(1).strip())

    if not repos:
        raise ValueError("Could not find any repo entries in resources.html")

    return sorted(repos)


def get_star_count(repo: str) -> int:
    """Get star count for a repo using GitHub REST API."""
    url = f"https://api.github.com/repos/{repo}"
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(url, headers=headers, timeout=20)
    if resp.status_code == 200:
        try:
            return int(resp.json().get("stargazers_count", 0))
        except Exception:
            return 0

    # Helpful diagnostics
    remaining = resp.headers.get("X-RateLimit-Remaining")
    reset = resp.headers.get("X-RateLimit-Reset")
    msg = f"Warning: {repo} status={resp.status_code} remaining={remaining} reset={reset}"
    print(msg)
    return 0


def update_stars() -> None:
    repos = extract_repos_from_html(HTML_PATH)
    print(f"Found {len(repos)} repositories in {HTML_PATH.name}")

    # Load previous data
    try:
        with open(STARS_JSON_PATH, "r", encoding="utf-8") as f:
            stars_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stars_data = {}

    last_updated = stars_data.get("_last_updated", 0)
    needs_refresh = (time.time() - last_updated) > 86400  # 24h

    for repo in repos:
        if needs_refresh or repo not in stars_data:
            stars = get_star_count(repo)
            stars_data[repo] = stars
            print(f"Updated {repo}: {stars} stars")
            time.sleep(0.3)  # small delay for politeness

    stars_data["_last_updated"] = time.time()

    with open(STARS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(stars_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated {STARS_JSON_PATH.name} with {len(repos)} repositories")


if __name__ == "__main__":
    try:
        update_stars()
    except Exception as e:
        print(f"Error: {e}")