#Testbestand voor Nathan

from app.helper.utils import DeltaresReader
import re
from app.geotechniek.helper_DFoundations import profiles
from app.geotechniek.helper_DFoundations import soil_collection
from pathlib import Path
import pandas as pd
from pywebio.output import put_link, put_text, put_file

def dfoundations_to_excel(inputfile, inputfile_path):
    with open(inputfile_path, "wb+") as writefile:
        writefile.write(inputfile["content"])

    content = inputfile_path.open().read()

    profile = profiles.Profiles(content)
    CPTS = profiles.CPTs(profile._content)

    unique_soils_used = set()

    for CPT in range(profile.number_CPTs):
        sonderinginfo = profile.CPT_list[CPT].content
        title = profile.CPT_list[CPT].name

        for layer in range(profile.CPT_list[CPT].number_of_layers):
            material = CPTS.soil_list[layer].material
            unique_soils_used.add(material)

    list_unique_soils = list(unique_soils_used)

    _soil_collection = soil_collection.SoilCollection(content)
    soillist = []
    number_of_soils = _soil_collection.number_of_soils

    for i in range(number_of_soils):
        soillist.append(_soil_collection.soil_list[i].name)

    # declare a dataframe with desired soil parameter columns (in dutch)
    df = pd.DataFrame(columns=[
    'Materiaal',
    'γ [kN/m³]',
    'γ (sat) [kN/m³]',
    'φ [°]',
    'ψ [°]',
    'C [kPa]',
    'Cu [kPa]',
    'k1 [kN/m³]',
    'k2 [kN/m³]',
    'k3 [kN/m³]',
    'RR [-]',
    'CR [-]',
    'Ca [-]',
    'Cv [m²/s]'], index=[])

    #read parameter data from file and fill dataframe
    for soil in list_unique_soils:
        soilID = soillist.index(soil)
        name = _soil_collection.soil_list[soilID].name
        gamma_wet = _soil_collection.soil_list[soilID].soil_gam_wet
        gamma_dry = _soil_collection.soil_list[soilID]._soil_gam_dry
        phi = _soil_collection.soil_list[soilID].soil_phi
        cohesion = _soil_collection.soil_list[soilID].soil_cohesion

    # Append a new row to the DataFrame for each soil
        df = df._append({'Materiaal': name,
        'γ [kN/m³]': gamma_dry,
        'γ (sat) [kN/m³]': gamma_wet,
        'φ [°]': phi,
        'C [kPa]': cohesion}, ignore_index=True)

    return df








