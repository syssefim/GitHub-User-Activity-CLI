import sys
import requests








def main():
    # Check if a username argument was provided
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    print(f"Fetching activity for {username}...")

    events = fetch_github_activity(username)
    
    if events:
        display_activity(events)



def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        headers = {'User-Agent': 'python-cli-app'}
        response = requests.get(url, headers=headers)

        # Check for specific HTTP status codes
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Error: User '{username}' not found.")
            return None
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        # This catches network errors (DNS, connection refused, etc.)
        print(f"Network error: {e}")
        return None



def display_activity(events):
    if not events:
        print("No recent activity found.")
        return

    # Iterate through the fetched events
    print("Output:")
    for event in events:
        event_type = event.get('type')
        repo_name = event.get('repo', {}).get('name', 'unknown repo')
        payload = event.get('payload', {})

        action_text = ""

        # Handle specific event types based on the requirements
        if event_type == 'PushEvent':
            commits = payload.get('commits', [])
            count = len(commits)
            action_text = f"Pushed {count} commit{'s' if count != 1 else ''} to {repo_name}"
            
        elif event_type == 'IssuesEvent':
            action = payload.get('action', 'interacted with')
            action_text = f"{action.capitalize()} an issue in {repo_name}"
            
        elif event_type == 'WatchEvent':
            # 'Watch' in GitHub API usually corresponds to 'Starring' a repo
            action_text = f"Starred {repo_name}"
            
        elif event_type == 'ForkEvent':
            action_text = f"Forked {repo_name}"
            
        elif event_type == 'CreateEvent':
            ref_type = payload.get('ref_type', 'item')
            action_text = f"Created {ref_type} in {repo_name}"

        elif event_type == 'PullRequestEvent':
            action = payload.get('action', 'interacted with')
            action_text = f"{action.capitalize()} a pull request in {repo_name}"

        # Print the formatted output if we recognized the event
        if action_text:
            print(f"- {action_text}")






if __name__ == "__main__":
    main()