# DONE
from pywebio.output import put_table, put_link, put_text
import re
from general.utilities import settings
import json


def download_pywebio():
    # Setup pattern for datetime folders
    datetime_folder_pattern = re.compile("\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}")

    # Create a list with the headers
    headers = ["Datum", "Input file(s)", "Omschrijving", "Download link"]

    # Create a list to save the data in
    data = []

    # Iterate over all folders
    
    for calc_folder in settings.app_folder.glob("*"):
        # Get the folder name
        folder_name = calc_folder.stem
        # Get the path to the input_file
        input_shi_file = [i.name for i in calc_folder.rglob("*.shi")]
        # Check if the folder has the pattern specified in datetime_folder_pattern
        if datetime_folder_pattern.search(folder_name):
            # Search the folder for zip files
            zip_files = [i for i in calc_folder.glob("*.zip")]

            # If the folder has zip_files in it and the input.json file exists
            if zip_files:
                input_file = ""
                omschrijving = " ".join(input_shi_file)

                # Append to the data list
                data.append([folder_name,
                               input_file,
                               omschrijving,
                               put_link(folder_name, f"/download_file/{folder_name}")])

    output = [headers] + list(reversed(data))
    # Create a table to display
    put_table(output)


if __name__ == "__main__":
    download_pywebio()
