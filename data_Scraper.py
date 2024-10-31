import requests
import pandas as pd

# GitHub API token and base URL
TOKEN = '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'
BASE_URL = 'https://api.github.com'

# Define headers for authentication
headers = {
    'Authorization': f'token {TOKEN}'
}

# Fetch users in Tokyo with over 200 followers
def fetch_users():
    url = f'{BASE_URL}/search/users?q=location:Tokyo+followers:>200'
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching users: {response.status_code} {response.text}")
        return []

    users_data = response.json().get('items', [])
    users = []

    for user in users_data:
        users.append({
            'login': user.get('login', ''),
            'name': user.get('name', '') or '',
            'company': user.get('company', '').strip('@').strip().upper() if user.get('company') else '',
            'location': user.get('location', '') or '',
            'email': user.get('email', '') or '',
            'hireable': user.get('hireable', '') if user.get('hireable') is not None else '',
            'bio': user.get('bio', '') or '',
            'public_repos': user.get('public_repos', 0),
            'followers': user.get('followers', 0),
            'following': user.get('following', 0),
            'created_at': user.get('created_at', '')
        })
    
    return users

# Main execution
if __name__ == "__main__":
    users = fetch_users()
    
    # Sort users by followers in descending order and get top 5
    top_users = sorted(users, key=lambda x: x['followers'], reverse=True)[:5]

    # Extract their logins
    top_user_logins = [user['login'] for user in top_users]

    # Print logins comma-separated
    print(', '.join(top_user_logins))
