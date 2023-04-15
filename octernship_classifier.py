from bs4 import BeautifulSoup
import requests
import time


# Define the criteria for an active contributor
num_contributions_threshold = [50, 20]
diversity_threshold = 3  # contributed to at least 3 different repositories


def is_valid_github_link(link):
    try:
        response = requests.get(link)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_profile_info(profile_url):
    # Retrieve repository and profile information
    profile_response = requests.get(profile_url)
    profile = profile_response.text
    soup = BeautifulSoup(profile, "html.parser")

    # Evaluate criteria
    num_contributions_str_element = soup.find(name="h2", class_="f4 text-normal mb-2")
    if num_contributions_str_element:
        num_contributions_str = num_contributions_str_element.text.split()[0]
        try:
            num_contributions = int(num_contributions_str.replace(",", ""))
        except (AttributeError, ValueError):
            num_contributions = int(num_contributions_str)
    else:
        num_contributions = 0

    num_repos_contributed_element = soup.find(name="span", class_="Counter")
    if num_repos_contributed_element:
        num_repos_contributed_str = int(num_repos_contributed_element.text)
        num_repos_contributed = int(num_repos_contributed_str)
    else:
        num_repos_contributed = 0

    return num_contributions, num_repos_contributed


def to_invite(profile_url):
    # Retrieve repository and profile information
    num_contributions, num_repos_contributed = get_profile_info(profile_url)

    # Determine if the user meets the active contributor criteria
    is_active_contributor = (
        num_contributions >= num_contributions_threshold[0]
        and num_repos_contributed >= diversity_threshold
    )

    # Print the results
    comments = f"Made {num_contributions} contributions in the past year across {num_repos_contributed} repositories."
    invite_status = "No"

    if is_active_contributor:
        invite_status = "Yes"
    else:
        if num_contributions >= num_contributions_threshold[1]:
            invite_status = "Maybe"
        else:
            invite_status = "No"

    return invite_status, comments


def clean_github_link(link):
    if not link.startswith("https://"):
        link = "https://" + link

    if link.startswith("https://github.com/"):
        parts = link.split("?")
        if len(parts) > 1:
            link = parts[0]

    return link


# Test
link = "https://github.com/skajose"
print(is_valid_github_link(link))
print(to_invite(link))
