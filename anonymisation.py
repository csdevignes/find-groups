'''

@Usage:
python anonyme.py [<fichier csv>]

'''


import logging
import sys

import openpyxl
import pandas as pd
import random



_deja_hasard = set()
def hasard(a = 0, b = 100):
    '''
    Choisir au hasard un entier unique (par défaut entre 0 et 1000)
    :param: a: borne inf
    :param: b: borne sup
    :return: un entier unique (non encore tiré)
    '''
    res = random.randint(a,b)
    while res in _deja_hasard:
        res = random.randint(a,b)
    _deja_hasard.add(res)
    return res
def affecter_ids(ensemble):
    '''
    Créer un dict à partir de ensemble qui associe à chaque nom un numéro unique affecté au hasard.
    :param ensemble: ensemble des noms d'utilisateurs, un set
    :return: un dict <nom> => <ID>
    '''
    res = {}
    for nom in ensemble:
        res[nom] = hasard()
    return res

data = pd.read_excel('tableur ideìaux types.xlsx')

# Creates random IDs
noms = data["Prénom"].values.tolist()
key_table = affecter_ids(noms)

# Saves key table with names and random IDs
key_df = pd.DataFrame.from_dict(data=key_table, orient='index', columns=["ID"])
key_df.to_excel("tableau_key.xlsx")

# Anonymize dataset
def replace_name(name) :
    if name in key_table:
        anon_ID = key_table[name]
    return anon_ID

data["Prénom"] = data["Prénom"].apply(replace_name)

data.to_excel("tableur_anonyme.xlsx")

