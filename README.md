# Octernship Project

This repository contains code I wrote for the GitHub Octernship Event. This project aims to filter out applicants for the Octernship Event Registration and update their status on a sheet. The project has been cleaned of private information and has several components, including:

## Files

- `selection_filter.ipynb`: a Jupyter Notebook file used to filter applicants and make lists of their emails for mailing. It also checks for duplicates and people whose names shouldn't be there but were.
- `update_sheet_offline.py`: a Python script that updates the sheet offline (without using API requests) with the processed data.
- `update_sheet_sheety.py`: a Python script that updates the sheet using the Sheety API.
- `update_sheet_gspread.py`: a Python script that updates the sheet using the Google Sheets API.
- `octernship_classifier.py`: a Python module that provides functions to classify applicants into "Yes", "Maybe", or "No" for the Octernship event.
- `README.md`: this file.

## Dependencies

- `pandas`: a Python library used for data manipulation and analysis.
- `numpy`: a Python library used for numerical operations.
- `requests`: a Python library used for making HTTP requests.
- `gspread`: a Python library used for accessing Google Sheets.
- `oauth2client`: a Python library used for authentication with Google APIs.
- `os`: a Python library used for loading environment variables.
- `bs4`: a Python library used for web scraping.

## Requirements

To run the code in this repository, you will need the following:

- Python 3
- Jupyter Notebook (for running `selection_filter.ipynb`)
- pandas, requests, and gspread libraries (for running the Python scripts)

## Usage

To use the code in this repository, follow these steps:

1. Clone the repository to your local machine.
2. Install the required libraries.
3. Update the necessary variables in the Python scripts (`update_sheet_offline.py`, `update_sheet_sheety.py`, and `update_sheet_gspread.py`) with your own values.
4. Run the Python scripts to update the desired destination with the data from the Excel file.
5. Open the `selection_filter.ipynb` notebook in Jupyter Notebook and follow the instructions to filter applicants and create lists of their emails for mailing.
