import logging
import sys

import openpyxl
import pandas as pd

def dummy_column(serie):
    '''
    Create a dummy column (serie) containing data generated from randomly picking from values
    present in the original serie. Frequencies are passed as weights to have a similar value representation.
    :param serie: pandas serie
    :return: pandas serie
    '''
    number = len(serie)
    frequencies = serie.value_counts(normalize=True)
    values = pd.Series(frequencies.index)
    weights = pd.Series(frequencies.values)
    dummy_serie = values.sample(n = number, replace=True, weights=weights, ignore_index=True)
    return dummy_serie

def dummy_dataset(dataset) :
    '''
    Create a dummy dataset by picking randomly from original dataset, with the same columns and row number
    :param dataset: pandas dataframe, original dataset
    :return: pandas dataframe, dummy dataset
    '''
    dummy = dataset.apply(dummy_column, axis=0)
    return dummy


if __name__ == "__main__":
    if len(sys.argv) == 2:
        excelpath = sys.argv[1]
    else:
        logging.error(f"Usage : python dummy_file.py [<path to anonymized excel to use as template.xlsx>]")
        sys.exit()

    data = pd.read_excel(excelpath, index_col=0)
    print(data.describe(include='all'))
    dummy_data = dummy_dataset(data)
    print(dummy_data.describe(include='all'))
