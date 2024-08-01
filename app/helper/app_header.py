from typing import Optional

from pywebio.output import *


def general_app_header(app_name: str,
                       version: float,
                       app_description: str = Optional[None],
                       sweco_logo_img_path: str = 'https://www.swecogroup.com/wp-content/uploads/sites/2/2021/03/sweco_black.png',
                       validated: bool = False
                       ):
    """
    Add a standardised header to the app with an image, app name and app version.
    Parameters
    ----------
    app_name : Name of the app
    version : Version of the app
    app_description : Description of the app
    sweco_logo_img_path :
    validated

    Returns
    -------

    """
    put_image(src=sweco_logo_img_path)
    put_html(f"<h1>{app_name}</h1>")
    if validated:
        put_html(f"<p style='color:#00FF00'>Gevalideerd</p>")
    else:
        put_html(f"<p style='color:#FF0000'>Niet gevalideerd</p>")
    put_html(f"<p>Versie {version}</p>")
    if app_description is not None:
        put_html(app_description)
