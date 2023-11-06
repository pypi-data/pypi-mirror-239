import subprocess
import json

# Function to get the URL of the remote repository
def get_remote_url():
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(e)

# Function to get the latest commit date
def get_latest_commit_date():
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

# Function to check if the repository is active
# For this example, "active" is arbitrarily defined as having a commit in the last 90 days
def is_repo_active():
    from datetime import datetime, timedelta
    latest_commit_date = get_latest_commit_date()
    if latest_commit_date:
        last_commit_datetime = datetime.strptime(latest_commit_date, '%a %b %d %H:%M:%S %Y %z')
        return (datetime.now(last_commit_datetime.tzinfo) - last_commit_datetime) < timedelta(days=90)
    else:
        return False

# Use the functions
def repo_main():
    remote_url = get_remote_url()
    if remote_url:
        print(f"Remote URL: {remote_url}")
        if is_repo_active():
            print("The repository is active.")
            return remote_url
            
        else:
            print("The repository is not active.")
    else:
        print("No remote repository found for this directory.")
