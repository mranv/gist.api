import requests
import random

# Function to fetch a new custom code from the GitHub Gist API
def fetch_custom_code():
    response = requests.get("https://api.github.com/gists/public")
    if response.status_code == 200:
        # Get all public gists
        gists = response.json()
        if gists:
            # Select a random gist
            selected_gist = random.choice(gists)
            # Get the description (title) and the raw URL of the gist content
            gist_title = selected_gist['description'] or "No Description"
            raw_url = list(selected_gist['files'].values())[0]['raw_url']
            code_response = requests.get(raw_url)
            if code_response.status_code == 200:
                return gist_title, code_response.text
            else:
                raise Exception("Failed to fetch gist content")
        else:
            raise Exception("No gists available in the response")
    else:
        raise Exception("Failed to fetch gists from API")

try:
    # Read the current status from the file
    with open("status.md", "r") as f:
        text = f.readline()
        num = [int(x) for x in text.split() if x.isdigit()][0]
        num += 1  # Increment the pull request count

    # Fetch a new custom code
    gist_title, custom_code = fetch_custom_code()

    # Update the status.md file
    with open("status.md", "w") as f:
        f.write(f"{num} pull requests merged<br>")
        f.write("Currently:<br>")
        f.write(f"Title: {gist_title}<br>")
        f.write(f"Custom Code:<br><pre>{custom_code}</pre>")

except FileNotFoundError:
    # Handle the case where status.md doesn't exist
    gist_title, custom_code = fetch_custom_code()
    with open("status.md", "w") as f:
        f.write("1 pull request merged<br>")
        f.write("Currently:<br>")
        f.write(f"Title: {gist_title}<br>")
        f.write(f"Custom Code:<br><pre>{custom_code}</pre>")

except Exception as e:
    print(f"An error occurred: {e}")

# Output the gist title for the GitHub Actions workflow
print(f"::set-output name=gist_title::{gist_title}")
