from pathlib import Path
from app.geotechniek.diff import diff
from pywebio.input import input_group, file_upload, input, FLOAT
from pywebio.output import put_link, put_text, put_file
from app.helper.app_header import general_app_header
from general.utilities import Current_date_time, settings, create_zip_file
from datetime import datetime
from app.geotechniek.helper_DSettlement.write_to_excel import dsettlement_to_excel
from app.geotechniek.helper_DStability.write_to_excel import dgeostability_to_excel
from app.geotechniek.helper_DSheetpiling.write_to_excel import dsheetpiling_to_excel
from app.geotechniek.helper_DFoundations.write_to_excel import dfoundations_to_excel
from app.geotechniek.helper_DStability.partialfactor import check_rc

def app_parameter():
    # TODO:  I would recommend switching the code below so
    #  that it uses dSweco instead of the current setup.
    # General header
    # Create the header which is used in every app. This should be a separate repository which is
    # shared among apps.
    general_app_header(settings.app_name,
                       float(settings.versie),
                       settings.omschrijving,
                       validated=False)

    # Add a link to the download page
    put_link(f"Parameter download pagina", f"/parameter_download")
    # Upload form

    raw_data = input_group("Basic info", [
        file_upload('Deltares bestanden',
                    name='uploaded_files',
                    required=True,
                    accept=".shi, .sli, .foi",
                    multiple=True),
        input('Partiële factor voor hoek van inwendige wrijving (alleen bij D-Geo Stability)',
              name='gamma_phi',
              type=FLOAT),
        input('Partiële factor voor hoek van cohesie (alleen bij D-Geo Stability)',
              name='gamma_c',
              type=FLOAT)])

    main_folder = Path(r"F:\webapp_data\parameter_app")

    # Save the input data
    put_text("Opslaan input data")
    
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    current_time_path = main_folder / current_time_str
    current_time_path.mkdir()

    uploaded_files = raw_data['uploaded_files']
    gamma_phi = raw_data['gamma_phi']
    gamma_c = raw_data['gamma_c']

    #Run script
    list = []
    for input_file in uploaded_files:
        input_file_path = current_time_path / input_file["filename"]
        suffix = input_file_path.suffix
        if suffix == '.sli':
            list.append(dsettlement_to_excel(input_file, input_file_path))
        elif suffix == '.foi':
            list.append(dfoundations_to_excel(input_file, input_file_path))
        elif suffix == '.sti':
            list.append(dgeostability_to_excel(input_file, input_file_path, gamma_phi, gamma_c))
            print('-')
        elif suffix == '.shi':
            list.append(dsheetpiling_to_excel(input_file, input_file_path))
        else:
            put_text("Het opgegegeven bestand wordt niet ondersteund")
    diff(list)
