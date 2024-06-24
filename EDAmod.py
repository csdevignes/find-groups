'''
Modules used for EDA in streamlit
'''

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import numpy as np
from kmodes.kmodes import KModes
import streamlit as st

# Treatment
def treatment(df):
    nivnum = {"cap" : 3,
              "bep" : 3,
              "bac" : 4,
              "bac +2" : 5,
              "bac +3" : 6,
              "bac +5" : 7,
              "doctorat" : 8}
    cat_col = df.columns[2:]
    for column in cat_col:
        df[column] = df[column].str.lower()
        df[column] = df[column].astype('category')
    df["NivNum diplome"] = df["Niveau de diplôme"].apply(lambda x: nivnum[x]).astype('int64')
    df["NivNum parent1"] = df["Parent 1"].apply(lambda x: nivnum[x]).astype('int64')
    df["NivNum parent2"] = df["Parent 2"].apply(lambda x: nivnum[x]).astype('int64')
    df["Parents Somme"] = df.loc[:, ["NivNum parent1", "NivNum parent2"]].agg(func='sum', axis=1)
    df["Parents Max"] = df.loc[:, ["NivNum parent1", "NivNum parent2"]].agg(func='max', axis=1)
    df["Parents Moyenne"] = df.loc[:, ["NivNum parent1", "NivNum parent2"]].agg(func='mean', axis=1)
    return df

# Visualisation

def distri_plot(data, select_col, hue):
    fig, ax = plt.subplots()
    sns.histplot(data, y=select_col, ax=ax, hue=hue,
                 multiple='stack')
    ax.set_xlabel("Effectif")
    ax.set_ylabel(select_col)
    ax.tick_params(axis='x', labelrotation=90)
    return fig

def joint_plot(data_plot):
    fig, ax = plt.subplots()
    sns.scatterplot(data_plot, x=data_plot.columns[0], y=data_plot.columns[1])
    ax.tick_params(axis='x', labelrotation=90)
    return fig

def corr_plot(data_plot, annot):
    fig, ax = plt.subplots()
    corr = cat_corr(data_plot)
    sns.heatmap(corr, annot = annot, xticklabels=True, yticklabels=True)
    return fig

def cat_corr(df):
    '''
    Function used to calculate correlation between categorical variables
    :param df: Dataframe containing variable to calculate correlation for
    :return: dataframe containing correlation scores
    '''
    def cramers_V(var1, var2):
        '''
        Compute Cramers V for 2 series of data
        :param var1: serie 1 of data
        :param var2: serie 2 of data
        :return: float, cramer_V score
        '''
        crosstab = np.array(pd.crosstab(var1, var2))
        stats = chi2_contingency(crosstab)[0]
        cram_V = stats / (np.sum(crosstab) * (min(crosstab.shape) - 1))
        return cram_V

    def cramers_col(column_name):
        '''
        For each column of the dataframe, creates a serie with rows corresponding to all column in the dataframe.
        Then for each row (= other column), calls cramers_V with data from the column (column_name) and data from
        this other column. This returns a single score value.
        :param column_name: string, name of the column treated
        :return: dataframe with score values for every column vs given column
        '''
        col = pd.Series(np.empty(df.columns.shape), index=df.columns, name=column_name)
        for row in df:
            cram = cramers_V(df[column_name], df[row])
            col[row] = round(cram, 2)
        return col
    res = df.apply(lambda column: cramers_col(column.name))
    return res
@st.cache_data
def kmode_group(df):
    km = KModes(n_clusters=5, init='Huang', n_init=50, verbose=1, random_state=42)
    clusters = km.fit_predict(df)
    return km

def filter_df(df, groups):
    mask = df["Group"].isin(groups)
    df = df.loc[mask]
    return df