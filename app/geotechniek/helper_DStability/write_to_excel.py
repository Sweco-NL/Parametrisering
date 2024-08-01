import pandas as pd
from app.geotechniek.helper_DStability import soil_collection, partialfactor


def dgeostability_to_excel(inputfile, inputfile_path, gamma_phi, gamma_c):
    with open(inputfile_path, "wb+") as writefile:
        writefile.write(inputfile["content"])

    content = inputfile_path.open().read()

    _soil_collection = soil_collection.SoilCollection(content)

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
        'Cv [m²/s]'
    ], index=[])

    #read parameter data from file and fill dataframe
    for i in range(_soil_collection.number_of_soils):
        # define soil parameters
        name = _soil_collection.soil_list[i].name
        gamma_wet = _soil_collection.soil_list[i].soil_gam_wet
        gamma_dry = _soil_collection.soil_list[i]._soil_gam_dry
        phi = _soil_collection.soil_list[i].soil_phi
        phi_k = partialfactor.partialfactor_phi(phi, gamma_phi)
        cohesion = _soil_collection.soil_list[i].soil_cohesion
        cohesion_k = partialfactor.partialfactor_cohesion(cohesion, gamma_c)
        dilatancy = _soil_collection.soil_list[i].soil_dilatancy
        dilatancy_k = partialfactor.partialfactor_phi(dilatancy, gamma_phi)

        # Append a new row to the DataFrame for each soil
        df = df._append({'Materiaal':                           name,
                        'γ [kN/m³]':                            gamma_dry,
                        'γ (sat) [kN/m³]':                      gamma_wet,
                        'φ [°]':                                phi_k,
                        'C [kPa]':                              cohesion_k,
                        'ψ [°]':                                dilatancy_k}, ignore_index=True)
    return df
