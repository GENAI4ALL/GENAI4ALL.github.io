import requests
import json
import time
import re
from bs4 import BeautifulSoup


def extract_repos_from_html(html_file):
    """Extract all GitHub repositories from the toolsData object in resources.html"""
    with open(html_file, "r") as f:
        content = f.read()

    # Find the toolsData object
    match = re.search(r"const toolsData = ({.*?});", content, re.DOTALL)
    if not match:
        raise ValueError("Could not find toolsData in the HTML file")

    # Extract all repo values
    repos = set()
    for line in content.split("\n"):
        if "repo:" in line:
            # Extract the repo value between quotes
            repo_match = re.search(r'repo:\s*[\'"]([^\'"]+)[\'"]', line)
            if repo_match:
                repos.add(repo_match.group(1))

    return sorted(list(repos))


def get_star_count(repo):
    """Get the star count for a repository"""
    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["stargazers_count"]
    print(f"Warning: Could not get stars for {repo} (Status: {response.status_code})")
    return 0


def update_stars():
    """Update the stars.json file with current star counts"""
    # Extract repos from HTML
    repos = extract_repos_from_html("resources.html")
    print(f"Found {len(repos)} repositories in resources.html")

    # Read existing stars.json if it exists
    try:
        with open("stars.json", "r") as f:
            stars_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stars_data = {}

    # Update each repo's star count
    for repo in repos:
        if (
            repo not in stars_data
            or time.time() - stars_data.get("_last_updated", 0) > 86400
        ):  # Update if older than 24h
            stars = get_star_count(repo)
            stars_data[repo] = stars
            print(f"Updated {repo}: {stars} stars")
            time.sleep(1)  # Rate limiting

    # Add timestamp
    stars_data["_last_updated"] = time.time()

    # Write back to stars.json
    with open("stars.json", "w") as f:
        json.dump(stars_data, f, indent=4)

    print(f"Successfully updated stars.json with {len(repos)} repositories")


if __name__ == "__main__":
    try:
        update_stars()
    except Exception as e:
        print(f"Error: {str(e)}")
