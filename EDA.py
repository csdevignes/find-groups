'''

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

# Visualisation
select_dict = st.dataframe(data, on_select="rerun", selection_mode="multi-column", key='df-select')
if len(st.session_state["select-col"]) < len(data.columns[1:]) :
    st.session_state["select-col"] = select_dict["selection"]["columns"]

if st.button("Selectionner tout") :
    for col in data.columns[1:]:
        if col not in select_dict["selection"]["columns"]:
            select_dict["selection"]["columns"].append(col)
    st.session_state["select-col"] = select_dict["selection"]["columns"]
    print(len(st.session_state["select-col"]))
    print(len(data.columns[1:]))

if st.button("Déselectionner tout") :
    st.session_state["select-col"] = []
    st.session_state["df-select"]["selection"]["columns"] = []



if len(st.session_state["select-col"]) == 0:
    st.write("Selectionner les colonnes a visualiser")
elif len(st.session_state["select-col"]) == 1:
    select_data = data[st.session_state["select-col"][0]]
    st.pyplot(EDAmod.distri_plot(select_data))
elif len(st.session_state["select-col"]) == 2:
    select_data = data[st.session_state["select-col"]]
    st.pyplot(EDAmod.joint_plot(select_data))
else:
    select_data = data[st.session_state["select-col"]]
    annot_on = st.checkbox("Afficher valeurs corrélation")
    st.pyplot(EDAmod.corr_plot(select_data, annot_on))




