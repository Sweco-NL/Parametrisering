# DONE
import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import List

import numpy as np

"""
class SettingsDFoundations:
    settings_data = json.load(open(r"C:\WebApplicatiesGeotechniek\app_parametrisering\general\settings.json"))
    foi_folder = Path(settings_data["foi_folder"])
    test_file = foi_folder / settings_data["test_file"]
    latest_version = tuple(map(int, settings_data["latest_version"].split(".")))


def dfoundations_calc(folder: Path,
                      dfoundations_path: str = r"C:\Program Files (x86)\Deltares\D-Foundations 22.1.1\DFoundations.exe"):
    # Use dFoundations for batch calculation
    os.system(
        fr'cmd /c ""{dfoundations_path}" /b '
        fr'{str(folder.absolute())}"')
"""

def cleanup_output_folder(output_folder):
    # Iterate over folders
    for i in output_folder.glob("*"):
        # Iterate over files in folders
        for result in i.glob("*.*"):
            # Create output path
            output_path = output_folder / result.name
            # Move file to output folder
            shutil.move(result, output_path)
    # Remove all folders
    [shutil.rmtree(i) for i in output_folder.glob("*") if i.is_dir()]


def create_linear_list(start: float, end: float, stepsize: float, reverse=False):
    """ Create a list of floats starting at start, up to end with stepsize. The list can be reversed using the reverse statement.
    :param start: The start of the list
    :param end: The end of the list
    :param stepsize: The size of the steps
    :param reverse: Reverse the list
    :return:
    """

    _start = max([start, end])
    _end = min([start, end])

    diff = (_start - _end)
    num = diff / stepsize
    return sorted(np.linspace(start, end, round(num) + 1).tolist(), reverse=reverse)


def make_float(value: str) -> List[float]:
    """
    Turns a input string into a list of floats. Used to convert input from pywebio. Converts comma's with dots and
    splits entries by enter.
    Parameters
    ----------
    value

    Returns
    -------
    A list of floats.
    """
    # Replace the comma's in the input with dots.
    value = value.replace(",", ".")
    # Splits the string on linebreaks and then tries to convert the values to string.
    try:
        return sorted([float(item) for item in value.strip().split("\n") if item.split()])
    except ValueError:
        raise ValueError("One of the given values could not be converted to float.")


def check_if_float(value):
    m_float = make_float(value)
    if isinstance(m_float, list) and len(m_float) and isinstance(m_float[0], float):
        return None
    return f"Waarde {value} van type : {type(value)} kon niet geconverteerd worden naar decimaal."


def create_settings(
        omschrijving_html_path: Path = r"C:\WebApplicatiesGeotechniek\app_parametrisering\general\omschrijving.html",
        settings_json_path: Path = r"C:\WebApplicatiesGeotechniek\app_parametrisering\general\settings.json",
        tools_folder: Path = Path("F:/webapp_data")):
    """
    :param omschrijving_html_path: Path to the omschrijving setup as html : str
    :param settings_json_path: Path to the settings json : str
    :return: SimpleNamespace with :
        - app_name : str
        - versie : str
        - path : str
        - gevalideerd : bool
        - omschrijving : str
    """
    # Extract html with description
    omschrijving = Path(omschrijving_html_path).open().read()
    # Extract json file with settings
    json_data = json.load(Path(settings_json_path).open())
    # Combine data into class
    _settings = SimpleNamespace(**dict(**json_data, **dict(omschrijving=omschrijving)))
    # Add app_folder
    _settings.app_folder = tools_folder / f"{_settings.path}_app"
    # Add download_folder
    _settings.download_folder = _settings.app_folder / "download"
    return _settings


settings = create_settings()


class Current_date_time:
    def __init__(self, settings=settings, set_date=None):
        self.settings = settings
        if set_date is None:
            self._datetime_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        else:
            self._datetime_string = set_date
        self.uploaded_file_paths = set()

        self._output_folder = self.datetime_folder / "output_folder"
        self._input_folder = self.datetime_folder / "input_folder"

        if not self.datetime_folder.exists():
            self.datetime_folder.mkdir(parents=True, exist_ok=True)

    @property
    def datetime_string(self) -> str:
        return self._datetime_string

    @datetime_string.setter
    def datetime_string(self, datetime_string: str):
        self._datetime_string = datetime_string

    @property
    def datetime_folder(self) -> Path:
        return settings.app_folder / self.datetime_string

    @property
    def input_folder(self):
        input_folder = self.datetime_folder / "input_folder"
        if input_folder.exists() is False:
            os.mkdir(str(input_folder))
        return input_folder

    @property
    def output_folder(self):
        if self._output_folder.exists() is False:
            os.mkdir(str(self._output_folder))
        return self._output_folder

    @property
    def datetime_json(self):
        return self.settings.app_folder / self.datetime_string / "input.json"

    @property
    def datetime_zip(self):
        return self.datetime_folder / f"{self.datetime_string}.zip"

    def save_input_data(self, input_data : dict):
        with self.datetime_json.open("w+") as writefile:
            input_data = {key: value for key, value in input_data.items() if
                          isinstance(value, tuple([float, int, str, bool]))}
            json.dump(input_data, writefile,indent=4)

    def save_input_files(self, input_files: list):
        """
        A list with dictionaries with filename and content.
        [{content:bytes, filename:str}, {}, ...]
        :param input_files: list
        :return:
        """
        output = []

        # Iterate over input_data and save to file
        for nr, input_file in enumerate(input_files):
            # Get the filename
            filename = input_file["filename"]
            # Get the content
            content = input_file["content"]
            # Get the input_path
            input_folder = self.datetime_folder / "input_folder" / f"{nr}"
            # Create input_folder
            input_folder.mkdir(parents=True, exist_ok=True)
            # Create the path to the input file
            input_path = input_folder / filename
            # Save the file on the server
            with input_path.open("wb+") as writefile:
                writefile.write(content)
            output.append(input_path)
            self.uploaded_file_paths.add(input_path)
        return output


def create_zip_file(path, zip_path=None):
    if zip_path is None:
        zip_path = path / path.with_suffix(".zip").name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

        for p in path.rglob("*.*"):
            if p.suffix != ".zip":
                zipf.write(p, arcname=p.relative_to(path))


if __name__ == "__main__":
    print(settings.app_folder)
