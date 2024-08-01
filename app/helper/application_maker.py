"""
Create ap
"""
from typing import List

from flask import Flask
from pywebio.platform.flask import webio_view


def application_maker(_app: Flask,
                      full_app_name: str,
                      pywebio_application,
                      methods: List[str] = ["GET",
                                            "POST",
                                            "OPTIONS"]):
    """
    Add application to app.

    Parameters
    ----------
    full_app_name: Name of the app
    pywebio_application: Pywebio function
    methods: Method for the app. Usually "GET", "POST", "OPTIONS"

    Returns
    -------
    Returns true if all went well.
    """
    _app.add_url_rule(f"/{full_app_name}", f"{full_app_name}", webio_view(pywebio_application), methods=methods)
    return True
