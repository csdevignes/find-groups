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
    raw = pd.read_excel(uploaded_file, index_col=0)

# Treatment
p = EDAmod.Pretreatment(raw)
data = p.df

with st.sidebar:
    if st.checkbox("Détection des groupes", key='group-on'):
        all_variables = [col for col in data.columns[1:]]
        default_opt = ['Age', 'Genre', 'Orientation', 'militantisme', 'Socio pro', 'Zone', 'Ecole', 'Diplôme en cours', 'e_Niveau de diplôme', 'Précaire (Seuil de pauvreté 1158)', 'Autres dicscriminations', 'Parents Max']
        variables = st.multiselect(
            "Variables à conserver :",
            all_variables, default_opt, key='k-variables')

def filterrow_options(pt):
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("Grouper les orientations"):
            pt.group_orientation()
    with col2:
        if st.checkbox("Filtrer orientation pas définie"):
            pt.remove_nd()
    return pt

# Visualisation of distributions and correlations
if not st.session_state['group-on']:
    st.write("Cliquer sur l'en-tête d'une colonne pour commencer à visualiser les données. Sélectionner 1, 2 colonnes ou plus.")
    p = filterrow_options(p)
    data = p.df
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
    p = filterrow_options(p)
    p.encode_all(variables)
    data = p.df
    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("PCA", key="PCA-on")
        st.checkbox("Afficher les ID", key="show-id")
    with col2:
        st.selectbox("Détection des groupes", options=["kmodes", "kmeans"], index=1, key="cluster-method")
    with col3:
        st.number_input("Nombre de groupes", min_value=1, max_value=len(data), value=5, step=1,
                        key="cluster-number")
    if st.session_state["cluster-method"] == "kmodes":
        kmode_g = EDAmod.kmode_group(data[variables], ncluster = st.session_state["cluster-number"])
        data["Group"] = kmode_g.labels_
        st.write(f"Métrique : coût {kmode_g.cost_}")
    if st.session_state["cluster-method"] == "kmeans":
        kmean_g = EDAmod.kmeans_group(data, variables, ncluster = st.session_state["cluster-number"])
        data["Group"] = kmean_g.labels_
        st.write(f"Métrique : inertie {kmean_g.inertia_}")
    if st.session_state["PCA-on"]:
        st.pyplot(EDAmod.run_pca(data, variables, data["Group"], annot_id=st.session_state["show-id"]))
    if "Group" in data:
        all_groups = sorted([g for g in data["Group"].unique()])
        st.multiselect("Sélectionner les groupes à afficher", all_groups, default=all_groups, key="show-groups")
        data_f = EDAmod.filter_df(data, st.session_state["show-groups"], variables)
        data_f["Group"] = data_f["Group"].astype('category')
        new_col = []
        for col in data.columns:
            if col not in data_f.columns and not str(col).startswith('e_'):
                new_col.append(col)
        data_f = data_f.join(data[new_col], how='left')
        order_col = ['Prénom', 'Group'] + [col for col in data_f.columns if col not in ['Prénom', 'Group']]
        data_f = data_f[order_col]
        select_dict = st.dataframe(data_f, on_select="rerun", selection_mode="single-column")
        select_col = select_dict["selection"]["columns"]
        if len(select_col) >= 1:
            st.pyplot(EDAmod.distri_plot(data_f, select_col[0], "Group"))




