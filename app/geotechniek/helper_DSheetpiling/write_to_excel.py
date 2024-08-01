from app.geotechniek.helper_DSheetpiling import soil_collection
import pandas as pd

def dsheetpiling_to_excel(inputfile, inputfile_path):
    with open(inputfile_path, "wb+") as writefile:
        writefile.write(inputfile["content"])

    content = inputfile_path.open().read()

    _soil_collection = soil_collection.SoilCollection(content)
    print(_soil_collection.number_of_soils)

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
        cohesion = _soil_collection.soil_list[i].soil_cohesion
        k1 = _soil_collection.soil_list[i].soil_cur_kb1
        k2 = _soil_collection.soil_list[i].soil_cur_kb2
        k3 = _soil_collection.soil_list[i].soil_cur_kb3

        # Append a new row to the DataFrame for each soil
        df = df._append({'Materiaal':                           name,
                        'γ [kN/m³]':                            gamma_dry,
                        'γ (sat) [kN/m³]':                      gamma_wet,
                        'C [kPa]':                              cohesion,
                        'φ [°]':                                phi,
                        'k1 [kN/m³]':                           k1,
                        'k2 [kN/m³]':                           k2,
                        'k3 [kN/m³]':                           k3}, ignore_index=True)


    #write df data to excel file
    #df.to_excel(r"C:\Users\NL1B4D\Documents\Python\output_shi.xlsx", engine='xlsxwriter', index=False)
    return df