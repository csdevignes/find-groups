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
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Treatment
class Pretreatment():
    '''
    Pretreatment of data. Conversion of text variables into categories.
    Encoding of diploma into numeric values
    :param df: dataframe containing original data
    '''
    def __init__(self, df):
        self.df = df
        self.replace_diploma_name()
        self.pool_categories()
        self.make_categories()
        self.compute_diploma()
    def replace_diploma_name(self):
        def select_first_letters(text):
            fl = text.split(' ')
            return fl[0]
        self.df["Diplôme en cours"] = self.df["Diplôme en cours"].apply(select_first_letters)
    def pool_categories(self):
        self.df.loc[self.df["Orientation"] == "Hétéro (en questionnement)", "Orientation"] = "hétérosexuelle"
        self.df.loc[self.df["Genre"].str.contains('trans'), "Genre"] = "trans"
    def make_categories(self):
        cat_col = self.df.columns[2:]
        for column in cat_col:
            if self.df[column].dtype == 'object':
                self.df[column] = self.df[column].str.lower()
                self.df[column] = self.df[column].astype('category')
    def compute_diploma(self):
        nivnum = {"cap": 3,
                  "bep": 3,
                  "bac": 4,
                  "bac +2": 5,
                  "bac +3": 6,
                  "bac +5": 7,
                  "doctorat": 8}
        for col in ["Niveau de diplôme", "Parent 1", "Parent 2"] :
            self.df[f'e_{col}'] = self.df[col].apply(lambda x: nivnum[x]).astype('int64')
        self.df["Parents Somme"] = self.df.loc[:, ["e_Parent 1", "e_Parent 2"]].agg(func='sum', axis=1)
        self.df["Parents Max"] = self.df.loc[:, ["e_Parent 1", "e_Parent 2"]].agg(func='max', axis=1)
        self.df["Parents Moyenne"] = self.df.loc[:, ["e_Parent 1", "e_Parent 2"]].agg(func='mean', axis=1)
    def remove_nd(self):
        self.df = self.df[self.df["Orientation"] != 'pas définie']
    def group_orientation(self):
        self.df["Orientation"] = self.df["Orientation"].astype('string')
        self.df.loc[self.df["Orientation"].isin(['omnisexuelle', 'pan']), "Orientation"] = 'omni/pan'
        self.df["Orientation"] = self.df["Orientation"].astype('category')
    def encode_all(self, variables):
        for column in variables :
            if self.df[column].dtype == 'category':
                enc = OrdinalEncoder(min_frequency=1)
                if f'e_{column}' not in self.df:
                    self.df[f"e_{column}"] = enc.fit_transform(self.df[column].to_numpy().reshape(-1, 1))
# Visualisation
def distri_plot(data, select_col, hue):
    '''
    Plot the distribution of a single variable, colored or not with group information
    :param data: dataframe containing variable to plot and hue column
    :param select_col: string, name of column to plot
    :param hue: string, name of column containing group information
    :return: fig object containing the plot
    '''
    fig, ax = plt.subplots()
    sns.histplot(data, y=select_col, ax=ax, hue=hue,
                 multiple='stack')
    ax.set_xlabel("Effectif")
    ax.set_ylabel(select_col)
    ax.tick_params(axis='x', labelrotation=90)
    return fig

def joint_plot(data_plot):
    '''
    Plot two variables, one in x and one in y, useful to visualize pairwise correlations
    :param data_plot: dataframe containing the 2 variables to plot (and only them)
    :return: fig object containing the plot
    '''
    fig, ax = plt.subplots()
    sns.scatterplot(data_plot, x=data_plot.columns[0], y=data_plot.columns[1])
    ax.tick_params(axis='x', labelrotation=90)
    return fig

def corr_plot(data_plot, annot):
    '''
    Plot the correlation matrix between multiple variables
    :param data_plot: dataframe containing all the variables to plot
    :param annot: boolean, state if correlation score values should be displayed on the plot
    :return: fig object containing the plot
    '''
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

# Grouping

@st.cache_data
def run_pca(df, variables, groups, annot_id=False):
    df_pca = pd.DataFrame()
    for var in variables:
        if df[var].dtype == 'category':
            df_pca[var] = df[f"e_{var}"]
        else:
            df_pca[var] = df[var]
    scaler = StandardScaler()
    pca = PCA(n_components=2, random_state=42)
    df_a = pd.DataFrame(scaler.fit_transform(df_pca), columns=df_pca.columns)
    X = pca.fit_transform(df_a)
    pca_res = pd.DataFrame({"variables" : pca.feature_names_in_,
               "pca0": pca.components_[0],
               "pca1": pca.components_[1]})
    print(pca_res)
    X = pd.DataFrame(X, columns=["PCA1", "PCA2"])
    X["Group"] = groups.astype('category')
    X["ID"] = df["Prénom"]
    fig,ax = plt.subplots()
    sns.scatterplot(X, x="PCA1", y="PCA2", hue="Group")
    for i in range(len(X)):
        if annot_id:
            ax.annotate(X.loc[i, "ID"], (X.loc[i, "PCA1"], X.loc[i, "PCA2"]))
        else:
            ax.annotate(i, (X.loc[i, "PCA1"], X.loc[i, "PCA2"]))
    return fig

@st.cache_data
def kmode_group(df, ncluster):
    km = KModes(n_clusters=ncluster, init='Huang', n_init=50, verbose=1, random_state=42)
    clusters = km.fit_predict(df)
    print(f"Kmode run with variables {df.info()}")
    return km
@st.cache_data
def kmeans_group(df, variables, ncluster):
    df_km = pd.DataFrame()
    for var in variables:
        if df[var].dtype == 'category':
            df_km[var] = df[f"e_{var}"]
        else:
            df_km[var] = df[var]
    scaler = StandardScaler()
    df_a = scaler.fit_transform(df_km)
    km = KMeans(n_clusters=ncluster, random_state=42)
    print(f"KMeans run with variables {df_km.info()}")
    labels = km.fit_predict(df_a)
    return km

def filter_df(df, groups, variables):
    mask = df["Group"].isin(groups)
    df = df.loc[mask]
    df_f = pd.DataFrame()
    for var in variables:
        df_f[var] = df[var]
    df_f["Group"] = df["Group"]
    return df_f