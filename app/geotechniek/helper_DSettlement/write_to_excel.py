from app.geotechniek.helper_DSettlement import soil_collection
import pandas as pd

def dsettlement_to_excel(inputfile, inputfile_path):
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
        cv = _soil_collection.soil_list[i].soil_cv
        RR = _soil_collection.soil_list[i].soil_RR
        CR = _soil_collection.soil_list[i].soil_CR
        Ca = _soil_collection.soil_list[i].soil_Ca

        # Append a new row to the DataFrame for each soil
        df = df._append({'Materiaal':                               name,
                        'γ [kN/m³]':                                gamma_dry,
                        'γ (sat) [kN/m³]':                          gamma_wet,
                        'Cv [m²/s]':                                cv,
                        'RR [-]':                                   RR,
                        'CR [-]':                                   CR,
                        'Ca [-]':                                   Ca}, ignore_index=True)


    #write df data to excel file
    #df.to_excel(r"C:\Users\NL1B4D\Documents\Python\output_sli.xlsx", engine='xlsxwriter', index=False)
    return(df)
