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

    #print(events)



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










if __name__ == "__main__":
    main()