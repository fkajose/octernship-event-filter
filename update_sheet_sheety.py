from pprint import pprint
from octernship_classifier import to_invite, is_valid_github_link
import requests
import os
import pandas as pd

# Get SHEETY_TOKEN and SHEETY_OCTERNSHIP from environment variables
TOKEN = os.environ.get("SHEETY_TOKEN")
sheety_endpoint = os.environ.get("SHEETY_OCTERNSHIP")

# Set authorization header for requests to Sheety API
headers = {
    "Authorization": f"Bearer {TOKEN}",
}

# Get the data from the Sheety API and store it in a pandas dataframe
response = requests.get(sheety_endpoint, headers=headers)
data = response.json()["formResponses1"]
df = pd.DataFrame(data).set_index("id")

# Initialize an empty dictionary to hold the new data to be sent to the Sheety API
payload = {"formResponses1": []}


def process_row(row):
    """Process a single row of the dataframe, and add the new data to the payload dictionary."""
    row_id = row.name
    github_link = row["addYourGitHubProfileLinkBelow"]

    # If the GitHub link doesn't start with "https://", add it to the beginning of the link
    if not github_link.startswith("https://"):
        github_link = "https://" + github_link

    # Determine whether to invite the participant based on their GitHub profile link
    if is_valid_github_link(github_link):
        invite_decision, comments = to_invite(github_link)
    else:
        invite_decision = "No"
        comments = ""

    # Add the new data to the payload dictionary
    payload["formResponses1"].append(
        {"id": row_id, "invite": row["invite"], "comments": row["comments"]}
    )

    # Return a dictionary with the invite decision and comments for the current row
    return {"invite": invite_decision, "comments": comments}


# Apply the process_row function to each row of the dataframe and save the results to new columns
df[["invite", "comments"]] = df.apply(process_row, axis=1, result_type="expand")

# Send the new data to the Sheety API using a PUT request
response = requests.put(sheety_endpoint, json=payload, headers=headers)
response.raise_for_status()

# Print a message indicating that all rows were processed without errors, and display the updated dataframe and payload
print(f"All rows processed without errors!")
pprint(df)
pprint(payload)
