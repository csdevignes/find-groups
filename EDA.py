'''
Streamlit app to visualize data
'''

import streamlit as st
import pandas as pd
import openpyxl

import EDAmod

with st.sidebar:
    uploaded_file = st.file_uploader("Upload fichier Excel", type=['xlsx'],
                                     help="Ce fichier contient les information des répondeurs, anonymisés ou non")




if uploaded_file is None:
    st.write("Uploader le fichier Excel dans la barre de gauche")
else:
    data = pd.read_excel(uploaded_file, index_col=0)

# Treatment
data = EDAmod.treatment(data)

with st.sidebar:
    if st.checkbox("Lancer la PCA et le k-means", key='k-on'):
        all_variables = [col for col in data.columns[1:]]
        variables = st.multiselect(
            "Variables à conserver :",
            all_variables,
            ['Age', 'Genre', 'Orientation', 'militantisme', 'Socio pro', 'Zone', 'Ecole', 'Diplôme en cours', 'Niveau de diplôme', 'Précaire (Seuil de pauvreté 1158)', 'Autres dicscriminations', 'NivNum diplome', 'Parents Somme', 'Parents Max', 'Parents Moyenne'],
            key='k-variables')

if st.session_state['k-on']:
    groups = EDAmod.kmode_group(data[variables])
    data["Group"] = groups.labels_
    data["Group"] = data["Group"].astype('category')

# Visualisation
st.write("Cliquer sur l'en-tête d'une colonne pour commencer à visualiser les données. Sélectionner 1, 2 colonnes ou plus.")
select_dict = st.dataframe(data, on_select="rerun", selection_mode="multi-column", key='df-select')
if "select-col" not in st.session_state :
    st.session_state["select-col"] = select_dict["selection"]["columns"]
elif len(st.session_state["select-col"]) < len(data.columns[1:]) :
    st.session_state["select-col"] = select_dict["selection"]["columns"]

if st.button("Selectionner tout") :
    for col in data.columns[1:]:
        if col not in select_dict["selection"]["columns"]:
            select_dict["selection"]["columns"].append(col)
    st.session_state["select-col"] = select_dict["selection"]["columns"]

if st.button("Déselectionner tout") :
    st.session_state["select-col"] = []
    st.session_state["df-select"]["selection"]["columns"] = []

if st.session_state['k-on']:
    vis_group = st.multiselect("Groupes à visualiser :",
            data["Group"].unique().tolist(),
            data["Group"].unique().tolist(), key='vis-group')
    data = EDAmod.filter_df(data, vis_group)

if len(st.session_state["select-col"]) == 0:
    st.write("Cliquer sur au moins une colonne pour charger une visualisation.")
elif len(st.session_state["select-col"]) == 1:
    select_col = st.session_state["select-col"][0]
    if st.session_state['k-on']:
        st.pyplot(EDAmod.distri_plot(data, select_col, "Group"))
    else:
        st.pyplot(EDAmod.distri_plot(data, select_col, None))
elif len(st.session_state["select-col"]) == 2:
    select_data = data[st.session_state["select-col"]]
    st.pyplot(EDAmod.joint_plot(select_data))
else:
    select_data = data[st.session_state["select-col"]]
    annot_on = st.checkbox("Afficher score de corrélation")

    st.pyplot(EDAmod.corr_plot(select_data, annot_on))





