import logging
import os.path
import sys

import openpyxl
import pandas as pd
import random



_deja_hasard = set()
def hasard(a = 0, b = 100):
    '''
    Randomly pick an integer (by default between 0 and 100)
    :param: a: lower value
    :param: b: upper value
    :return: unique integer (not drawn yet)
    '''
    res = random.randint(a,b)
    while res in _deja_hasard:
        res = random.randint(a,b)
    _deja_hasard.add(res)
    return res
def affecter_ids(ensemble):
    '''
    Create a dictionnary from an ensemble of value which associates to each value a randomly picked unique number.
    :param ensemble: set of value to replace (user names, etc.)
    :return: dict name => random ID
    '''
    res = {}
    for nom in ensemble:
        res[nom] = hasard()
    return res

# Anonymize dataset
def replace_name(name) :
    if name in key_table:
        anon_ID = key_table[name]
    return anon_ID

if __name__ == "__main__":
    if len(sys.argv) == 2:
        excelpath = sys.argv[1]
    else:
        logging.error(f"Usage : python anonymisation.py [<path to excel to anonymize.xlsx>]")
        sys.exit()

    data = pd.read_excel(excelpath)
    idcol = input(f'File {excelpath} loaded. Enter name of column to anonymize : ')
    # Creates random IDs
    noms = data[idcol].values.tolist()
    key_table = affecter_ids(noms)

    # Saves key table with names and random IDs
    key_df = pd.DataFrame.from_dict(data=key_table, orient='index', columns=["ID"])
    path_h, path_t = os.path.split(excelpath)
    file_name = path_t.split('.')[0]
    key_df.to_excel(f"{path_h}/{file_name}_anon_key.xlsx")

    data[idcol] = data[idcol].apply(replace_name)

    data.to_excel(f"{path_h}/{file_name}_anon.xlsx")
    print("Anonymized file saved. Preview")
    print(data.head())
