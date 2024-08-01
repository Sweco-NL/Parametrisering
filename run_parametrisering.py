"""
Run this module to create the app.
"""
from flask import Flask
from flask import send_file
from jinja2 import Template

from app.helper.application_maker import application_maker
from app.helper.download_pywebio import download_pywebio
from general.utilities import settings
from app.app_parameter import app_parameter

# Setup app
app = Flask(__name__)


def run_app(host="10.240.0.253", port=8040, debug=True):
    """
    Run this function to startup the server.
    Parameters
    ----------
    host : host for the webpage
    port : port for the webpage
    debug : allow debugging.

    Returns
    -------

    """
    # Create a list of tuples.
    applications_settings = tuple([f"{settings.path}_app", app_parameter,
                                   ["GET", "POST", "OPTIONS"]]), \
                            tuple([f"{settings.path}_download", download_pywebio,
                                   ["GET", "POST", "OPTIONS"]])

    @app.route("/")
    def main_app() -> str:
        """
        Create a template for all applications
        Returns
        -------
        Return a string with the template
        """
        template = Template("{% for path, _ , methods in applications_settings%}"
                            "<a href=\'{{path}}\'>{{path}}</a><br>"
                            "{% endfor %}").render(applications_settings=applications_settings)
        return template

    @app.route("/download_file/<file_date>")
    def download_file(file_date):
        """
        Download the file. Use the file_date as path to the zip file.
        Parameters
        ----------
        file_date : Date of the file to be downloaded. Format should be "yyyy_dd_mm_HH:MM"

        Returns
        -------
        Download the zip path.
        """
        zip_path = settings.app_folder / f"{file_date}" / f"{file_date}.zip"
        if zip_path.exists():
            return send_file(zip_path)
        else:
            return "File not found"

    # Create the applications
    for applications_setting in applications_settings:
        application_maker(app, *applications_setting)
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_app(host="10.240.0.253", port=8040, debug=True)
