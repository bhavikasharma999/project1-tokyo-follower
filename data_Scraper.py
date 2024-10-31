import requests
import csv
import os
from google.colab import files  # Use `from IPython.display import files` if using Jupyter Notebook locally

# GitHub API Token and Base URL
TOKEN = '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'  # Make sure to keep this token secure
BASE_URL = 'https://api.github.com'
HEADERS = {"Authorization": f"token {TOKEN}"}

# Directory for saving files
SAVE_DIR = 'project1-tokyo-follower'

# Create directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_users_in_tokyo():
    """Fetches GitHub users located in Tokyo with over 200 followers."""
    users = []
    query = "location:Tokyo+followers:>200"
    page = 1
    per_page = 100

    while True:
        url = f"{BASE_URL}/search/users?q={query}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        print(f"Fetching page {page}...")

        if response.status_code != 200:
            print("Error fetching data:", response.json())
            break

        data = response.json()
        users.extend(data['items'])

        if len(data['items']) < per_page:
            break

        page += 1

    detailed_users = []
    for user in users:
        user_info = get_user_details(user['login'])
        detailed_users.append(user_info)

    return detailed_users

def get_user_details(username):
    """Fetches detailed information for a specific GitHub user."""
    user_url = f"{BASE_URL}/users/{username}"
    user_data = requests.get(user_url, headers=HEADERS).json()

    return {
        'login': user_data.get('login'),
        'name': user_data.get('name'),
        'company': clean_company_name(user_data.get('company')),
        'location': user_data.get('location'),
        'email': user_data.get('email'),
        'hireable': user_data.get('hireable'),
        'bio': user_data.get('bio'),
        'public_repos': user_data.get('public_repos'),
        'followers': user_data.get('followers'),
        'following': user_data.get('following'),
        'created_at': user_data.get('created_at'),
    }

def clean_company_name(company):
    """Cleans up and formats the company name."""
    if company:
        company = company.strip().upper()
        if company.startswith('@'):
            company = company[1:]
    return company

def get_user_repos(username):
    """Fetches repository information for a specific GitHub user."""
    repos_url = f"{BASE_URL}/users/{username}/repos?per_page=100"
    response = requests.get(repos_url, headers=HEADERS)
    repos_data = response.json()

    repos = []
    for repo in repos_data:
        repos.append({
            'login': username,
            'full_name': repo.get('full_name'),
            'created_at': repo.get('created_at'),
            'stargazers_count': repo.get('stargazers_count'),
            'watchers_count': repo.get('watchers_count'),
            'language': repo.get('language'),
            'has_projects': repo.get('has_projects'),
            'has_wiki': repo.get('has_wiki'),
            'license_name': repo['license']['key'] if repo.get('license') else None,
        })

    return repos

def save_users_to_csv(users):
    """Saves user data to a CSV file."""
    file_path = os.path.join(SAVE_DIR, 'users.csv')
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        writer.writeheader()
        writer.writerows(users)
    print(f"Saved user data to {file_path}")

def save_repos_to_csv(repos):
    """Saves repository data to a CSV file."""
    file_path = os.path.join(SAVE_DIR, 'repositories.csv')
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])
        writer.writeheader()
        writer.writerows(repos)
    print(f"Saved repository data to {file_path}")

if __name__ == "__main__":
    # Fetch users in Tokyo with more than 200 followers
    users = get_users_in_tokyo()
    save_users_to_csv(users)

    # Fetch each user's repositories and save to CSV
    all_repos = []
    for user in users:
        repos = get_user_repos(user['login'])
        all_repos.extend(repos)
    save_repos_to_csv(all_repos)

    # Download the files (works for Google Colab; replace with local Jupyter download if needed)
    files.download(os.path.join(SAVE_DIR, 'users.csv'))
    files.download(os.path.join(SAVE_DIR, 'repositories.csv'))

    print("Data fetching and file download completed.")
