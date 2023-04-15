from pprint import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from octernship_classifier import to_invite, is_valid_github_link
import os
import pandas as pd
import numpy as np

# Set up the Google Sheets API client
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# Load the spreadsheet and select the appropriate worksheet
sheet = client.open(
    'Copy of GitHub Octernship Event Registration (Responses)').worksheet('formResponses1')

# Load the data into a Pandas DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data).set_index("id")


def categoise_user(row):
    # get the GitHub profile link from the current row
    row_id = row.name
    github_link = row['addYourGitHubProfileLinkBelow']
    if row['invite'] == "":

        if not github_link.startswith("https://"):
            github_link = "https://" + github_link

        if is_valid_github_link(github_link):
            invite_decision, comments = to_invite(github_link)
        else:
            invite_decision = "No"
            comments = ""

        # Update the invite and comments columns for this row in the Google Sheet
        sheet.update_cell(row_id + 1, 18, invite_decision)
        sheet.update_cell(row_id + 1, 19, comments)
        print(f"Row {row_id} completed without errors!")


df.apply(categoise_user, axis=1)
