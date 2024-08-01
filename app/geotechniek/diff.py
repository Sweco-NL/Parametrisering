from pywebio.output import put_text
from pywebio.output import put_link, put_text, put_file

def diff(data):
    #Lijst met unieke grondsoorten
    unique_soils = set()

    for dataframe in range(len(data)):
        for rows in range(data[dataframe].shape[0]):
            unique_soils.add(data[dataframe].iloc[rows, 0])
    
    list_unique_soils = list(unique_soils)

    columns = data[0].shape[1]
    counter = 0

    for col in range(1, columns-1):
        for soil in list_unique_soils:
            unique_values = set()
            values = []

            for dataframe in range(len(data)):
                soilrow = data[dataframe].loc[data[dataframe]['Materiaal'] == soil]
                if not soilrow.empty:
                    soilID = soilrow.index[0]
                    value = data[dataframe].iloc[soilID, col]
                    unique_values.add(value)
                    values.append(value)

        if len(unique_values) != 1:
            put_text('Verschillen gevonden voor materiaal', soil,', parameter',data[dataframe].columns[col])
            put_text('de volgende waardes zijn gevonden:', values)
            counter += 1

    if counter == 0:
        put_text('Geen verschillen gevonden tussen de grondparameters van de opgegeven bestanden.')