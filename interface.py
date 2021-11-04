from datetime import timedelta
from pathlib import Path
from time import sleep

import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st

#%%
@st.cache
def load_data():
    '''Lecture du fichier csv'''
    data_path = 'Data/collected_data_4.csv'
    data = pd.read_csv(data_path)
    return data


def liste_item(data):
    '''renvoie la liste des items '''
    return data['product name'].unique()

def camembert(data, valeurs, noms ):
    '''renvoie un camembert : propotion des valeurs selon les noms '''
    fig = px.pie(data, values = valeurs, names = noms, title='Population of European continent')
    st.plotly_chart(fig, use_container_width=True)
    
    



#%% 
def interface():  
    
    #st.title('Visualisation du data frame')
    data = load_data()
    #st.write(data)
    
    #st.sidebar.checkbox("Présentation")
    # Sélection du type d'analyse générale à effectuer
    #types_analyse = {"Mots clés génériques": data[dossiers_source[0]],
    #"Destinations Françaises": data[dossiers_source[1]],
    #"Destinations Françaises et Européennes": data[dossiers_source[2]]}
    #txt = "Types d'analyses: " 
    #noms_types = list(types_analyse.keys())
    
    
    #liste_items = liste_item(data)
    #mode = st.sidebar.selectbox('Liste des items',liste_items )
    # Barre de texte  : texte input
    #recherche = st.text_input("un test text_input")
    
    
    if st.sidebar.checkbox("Analyse par item", value=True):
        liste_items = liste_item(data)
        mode = st.sidebar.selectbox('Liste des items',np.insert(liste_items,0," "))
        
        data_item = data[data['product name'] == mode]
        st.title('Visualisation du data frame '+str(mode))
        st.write(data_item)
        
        if st.sidebar.checkbox("Domaine des réplicas", value=True):
            nb_domaine_replica = data_item["replica domain"].value_counts().reset_index()            
            #camembert(nb_domaine_replica,'index','replica domain')
            fig = px.pie(nb_domaine_replica, values = 'replica domain', names = 'index', title='Population of European continent')
            st.plotly_chart(fig, use_container_width=True)
        
        
        
        



#%%
### VII - PROGRAMME PRINCIPAL
interface()