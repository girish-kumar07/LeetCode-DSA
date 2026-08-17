import os
import base64
import requests
from pathlib import Path

# -----------------------------
# GitHub configuration
# -----------------------------

TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "girish-kumar07"
REPO = "LeetCode-DSA"

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN is not set.")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

# -----------------------------
# Get problem information
# -----------------------------

number = input("Problem number: ").strip()
title = input("Problem title: ").strip()
difficulty = input("Difficulty (Easy/Medium/Hard): ").strip().capitalize()
solution_path = input("Path to solution.py: ").strip()

if difficulty not in ["Easy", "Medium", "Hard"]:
    raise ValueError("Difficulty must be Easy, Medium, or Hard.")

# -----------------------------
# Read solution file
# -----------------------------

solution_file = Path(solution_path)

if not solution_file.exists():
    raise FileNotFoundError(f"Solution file not found: {solution_file}")

solution_content = solution_file.read_text(encoding="utf-8")

# -----------------------------
# Create GitHub path
# -----------------------------

folder_name = f"{int(number):04d}-{title.lower().replace(' ', '-')}"

github_path = f"{difficulty}/{folder_name}/solution.py"

# -----------------------------
# Encode solution
# -----------------------------

encoded_content = base64.b64encode(
    solution_content.encode("utf-8")
).decode("utf-8")

url = (
    f"https://api.github.com/repos/"
    f"{OWNER}/{REPO}/contents/{github_path}"
)

# -----------------------------
# Check whether file exists
# -----------------------------

response = requests.get(url, headers=HEADERS)

data = {
    "message": f"Add LeetCode #{number} - {title}",
    "content": encoded_content,
}

if response.status_code == 200:
    # File already exists → update it
    existing_file = response.json()
    data["sha"] = existing_file["sha"]

    response = requests.put(
        url,
        headers=HEADERS,
        json=data
    )

    action = "updated"

elif response.status_code == 404:
    # File doesn't exist → create it
    response = requests.put(
        url,
        headers=HEADERS,
        json=data
    )

    action = "uploaded"

else:
    print("GitHub API error:")
    print(response.status_code)
    print(response.text)
    raise SystemExit(1)

# -----------------------------
# Result
# -----------------------------

if response.status_code in (200, 201):
    print()
    print("SUCCESS!")
    print(f"Solution {action} successfully.")
    print(f"GitHub path: {github_path}")
else:
    print("Upload failed.")
    print(response.status_code)
    print(response.text)