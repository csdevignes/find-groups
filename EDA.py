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
p = EDAmod.Pretreatment(data)
data = p.df

with st.sidebar:
    if st.checkbox("Détection des groupes", key='group-on'):
        all_variables = [col for col in data.columns[1:]]
        default_opt = ['Age', 'Genre', 'Orientation', 'militantisme', 'Socio pro', 'Zone', 'Ecole', 'Diplôme en cours', 'Niveau de diplôme', 'Précaire (Seuil de pauvreté 1158)', 'Autres dicscriminations', 'NivNum diplome', 'Parents Somme', 'Parents Max', 'Parents Moyenne']
        variables = st.multiselect(
            "Variables à conserver :",
            all_variables, default_opt, key='k-variables')

# Visualisation of distributions and correlations
if not st.session_state['group-on']:
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

    if len(st.session_state["select-col"]) == 0:
        st.write("Cliquer sur au moins une colonne pour charger une visualisation.")
    elif len(st.session_state["select-col"]) == 1:
        select_col = st.session_state["select-col"][0]
        st.pyplot(EDAmod.distri_plot(data, select_col, None))
    elif len(st.session_state["select-col"]) == 2:
        select_data = data[st.session_state["select-col"]]
        st.pyplot(EDAmod.joint_plot(select_data))
    else:
        select_data = data[st.session_state["select-col"]]
        annot_on = st.checkbox("Afficher score de corrélation")
        st.pyplot(EDAmod.corr_plot(select_data, annot_on))

# Searching for groups

if st.session_state['group-on']:
    p.encode_all(variables)
    data = p.df
    kmode_g = EDAmod.kmode_group(data[variables])
    data["Group"] = kmode_g.labels_
    # data["Group"] = data["Group"].astype('category')
    # data = EDAmod.filter_df(data, variables)
    st.dataframe(data)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("PCA", key="PCA-on")
    with col2:
        st.selectbox("Détection des groupes", options=["kmodes", "kmeans"], key="cluster-method")
    with col3:
        st.checkbox("Afficher les ID", key="show-id")
    if st.session_state["PCA-on"]:
        st.pyplot(EDAmod.run_pca(data, variables, data["Group"], annot_id=st.session_state["show-id"]))




