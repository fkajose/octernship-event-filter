from octernship_classifier import (
    to_invite,
    is_valid_github_link,
    clean_github_link,
    get_profile_info,
)
import pandas as pd

# Read the excel file and store it in a pandas dataframe
df = pd.read_excel(
    "GitHub Octernship Event Registration (Responses).xlsx",
    sheet_name="Form responses 1",
)


def process_row(row):
    """
    Process a single row of the dataframe and return a dictionary with the invite and comments.

    Parameters:
    row (pandas.Series): A single row of the dataframe.

    Returns:
    dict: A dictionary with the keys "Invite" and "Comments".
    """
    github_link = clean_github_link(str(row["Add your GitHub profile link below"]))
    attending_virtually = row["How will you attend this event?"] == "Virtually"
    is_student = row["Are you a student?"] == "Yes"
    invite, comments = (
        to_invite(github_link)
        if is_valid_github_link(github_link)
        else ("No", "Invalid Link. Manually Review.")
    )
    if not is_student:
        invite = "No"
        comments += " Not a student."
    if attending_virtually:
        invite = "Maybe"
        comments += " Wants to attend virtually."
    return {"Invite": invite, "Comments": comments}


# Apply process_row function to each row of the dataframe and save the results to a new dataframe
processed_df = df.apply(process_row, axis=1, result_type="expand")


def get_info(row):
    """
    Get the contributions and number of public repos for a single row of the dataframe.

    Parameters:
    row (pandas.Series): A single row of the dataframe.

    Returns:
    dict: A dictionary with the keys "Contributions" and "Public Repos".
    """
    github_link = clean_github_link(str(row["Add your GitHub profile link below"]))
    contributions, repos = (
        get_profile_info(github_link) if is_valid_github_link(github_link) else (0, 0)
    )
    return {"Contributions": contributions, "Public Repos": repos}


# Apply get_info function to each row of the dataframe and save the results to new columns
df[["Contributions", "Public Repos"]] = df.apply(get_info, axis=1, result_type="expand")

# Print a message indicating that all rows were processed without errors and save the dataframe to a new excel file
print("All rows processed without errors!")
processed_df.to_excel(
    "GitHub Octernship Event Registration (Responses) Processed.xlsx",
    index=False,
    sheet_name="Form responses 1",
)
