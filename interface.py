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
    data_path = 'collected_data_4.csv'
    data = pd.read_csv(data_path)
    return data


def liste_item(data):
    '''renvoie la liste des items '''
    return data['product name'].unique()

def camembert(data, valeurs, noms ):
    '''renvoie un camembert : propotion des valeurs selon les noms '''
    fig = px.pie(data, values = valeurs, names = noms, title='Population of European continent')
    st.plotly_chart(fig, use_container_width=True)

def info_generale_replica(data_item):
    nb_replicas = data_item.shape[0]
    replica_green_moy = data_item['replica is_green_website'].mean()
    affluence_moy = data_item['rank'].mean()
    prix_moyen = data_item['replica price'].mean() 
    return df

def boolean_string(oui_ou_non):
    if(oui_ou_non == 1):
        return 'Oui'
    else : 
        return 'Non'
    
def affichage_image(data_item):
    try:
        product_image = data_item['product image'].values[0]
        return st.image(product_image, width = 200)
    except:
        pass
    
def affichage_prix(data_item):
    try:
        product_prix = str(data_item['product price'].values[0])
        return st.markdown('- Prix : ' + product_prix +' euros' )
    except:
        pass

def affichage_site(data_item):
    try:
        product_web_site  = data_item['product domain'].values[0]
        return st.markdown('- Site web : ' + product_web_site)
    except:
        pass
        
def affichage_anciennete(data_item):
    try:
        product_age_months = str(data_item['product website_age_in_months']\
                                 .values[0])
        age = '- Anciennet√© du site : '+  product_age_months + ' mois'
        return st.markdown(age)
    except:
        pass

def affichage_shopify(data_item):
    try:
        product_shopify = data_item['product is_shopify'].values[0]
        return st.markdown('- Shopify : ' + boolean_string(product_shopify))
    except:
        pass
    
def affichage_green(data_item):
    try:
        product_green = data_item['product is_green_website'].values[0]
        return st.markdown('- Fiable : ' + boolean_string(product_green))
    except:
        pass

def affichage_classe(data_item):
    try:
        product_class = data_item['product class'].values[0]
        return st.markdown('- Classe de produit : ' + product_class)
    except:
        pass

#%% Analyse ANOVA globale
@st.cache
def classe_anova_replica(data):
    
    ''' Pour tous les produits nous voulons faires des analyses de
    corr√©lation entre le label final (product class) avec les propri√©t√©s des 
    r√©plicas : prix des r√©plicas, proportion de sites Green, proportion de 
    site shopify'''
       
    liste_item = data['product name'].unique() # liste des produits
    
    def ecart_moy_prix_replica(nom_produit, data):
        '''Pour chaque produit nous voulons avoir le prix des r√©plicas,
        en particulier l'√©cart moyen avec le prix original. Nous divisons cette 
        diff√©rence par le prix original pour avoir des valeurs homog√®nes '''
        
        data_item = data[data['product name'] == nom_produit]
        prix_item = data_item['product price'].values[0]
        liste_ecarts_prix = data_item['replica price']
              
        return (liste_ecarts_prix - prix_item).mean()/prix_item
    
    def moy_site_green_replica(nom_produit, data):
        '''Proportion de site green dans les r√©plicas d'un produit'''
        data_item = data[data['product name'] == nom_produit]
        return data_item['replica is_green_website'].mean()
    
    def moy_shopyfi_replica(nom_produit, data):
        '''Proportion de site shopyfi dans les r√©plicas d'un produit'''
        data_item = data[data['product name'] == nom_produit]
        return data_item['replica is_shopify'].mean()

    def classe_item(nom_produit, data):
        data_item = data[data['product name'] == nom_produit]
        return data_item['product class'].values[0]
    
    # Construction d'un data frame avec toutes les infos 
    # 1 - valeurs des colonnes : 
    prix_moyen = [ecart_moy_prix_replica(nom,data) for nom in liste_item]
    green_moyen = [moy_site_green_replica(nom,data) for nom in liste_item]
    shopify_moyen = [moy_shopyfi_replica(nom,data) for nom in liste_item]
    label_item = [classe_item(nom, data) for nom in liste_item]
   
    df = pd.DataFrame({'Nom_item':liste_item,
                           'Ecart prix relatif': prix_moyen,
                           'Proportion Green Web Site': green_moyen, 
                           'Porportion Shopify': shopify_moyen,
                           'Classe du produit' : label_item
                           })
    
    # fig = px.box(df, x="Classe du produit", y="Porportion Shopify",color = "Classe du produit")
    # fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    # st.plotly_chart(fig, use_container_width=True)
    
    return df
        
    



#%% TEST
def interface():  
    
    #st.title('Visualisation du data frame')
    data = load_data()
    #st.write(data)
    
    #st.sidebar.checkbox("Pr√©sentation")
    # S√©lection du type d'analyse g√©n√©rale √† effectuer
    #types_analyse = {"Mots cl√©s g√©n√©riques": data[dossiers_source[0]],
    #"Destinations Fran√ßaises": data[dossiers_source[1]],
    #"Destinations Fran√ßaises et Europ√©ennes": data[dossiers_source[2]]}
    #txt = "Types d'analyses: " 
    #noms_types = list(types_analyse.keys())
    
    
    #liste_items = liste_item(data)
    #mode = st.sidebar.selectbox('Liste des items',liste_items )
    # Barre de texte  : texte input
    #recherche = st.text_input("un test text_input")
    
    
    if st.sidebar.checkbox("Analyse par item"):
        liste_items = liste_item(data)
        mode = st.sidebar.selectbox('Liste des items', liste_items)
        #mode = st.sidebar.selectbox('Liste des items',np.insert(liste_items,0," "))

        
        data_item = data[data['product name'] == mode]
        
        #st.title('Visualisation des r√©plicas '+str(mode))
        #st.write(data_item)
        st.title(str(mode))
        affichage_classe(data_item)
        #product_image = data_item['product image'][0]
        #product_web_site  = data_item['product domain'][0]
        #product_prix = str(data_item['product price'][0])
        #product_shopify = data_item['product is_shopify'][0]
        #product_age_months = str(data_item['product website_age_in_months'][0]) 
        
        #product_lien_url = '['+product_web_site+']' + '('+product_web_site+')'
        #st.image(product_image, width = 200)
        #try :
            #st.markdown(product_lien_url)
        #except :
            #pass
        
        affichage_image(data_item)
        affichage_prix(data_item)
        affichage_site(data_item)
        affichage_green(data_item)
        affichage_anciennete(data_item)
        affichage_shopify(data_item)

        
        
        st.markdown('## Information r√©plicas ')
        st.markdown('- Nombe de r√©plicas : ' +  str(round(data_item.shape[0],2)))
        st.markdown('- Prix moyen : ' +  str(round(data_item['replica price'].mean(),2)) )
        st.markdown('- Green site web (%) : '  + 
                    str(round(data_item['replica is_green_website'].mean() * 100,2)))
        st.markdown('- Affluence moyenne : ' +  str(round(data_item['rank'].mean(),2)))
        
        
        genre = st.radio("Informations compl√©mentaires sur les r√©plicas",('Domaines', 'Affluence', 'Images'))
 
        if genre == 'Domaines':
            nb_domaine_replica = data_item["replica domain"].value_counts().reset_index()            
            #camembert(nb_domaine_replica,'index','replica domain')
            fig = px.pie(nb_domaine_replica, values = 'replica domain', names = 'index', title= 'Domaine des r√©plicas')
            st.plotly_chart(fig, use_container_width=True)
        if genre == 'Images':
            liste_images_url = data_item['replica image'].tolist()
            st.image(liste_images_url, width = 100)
            
        if genre == 'Affluence':
            fig = px.scatter(data_item, x="replica price", y="replica website_age_in_months",\
                             size="rank", color="replica is_green_website",\
                             hover_name="product domain", log_x=True, size_max=40)
            st.plotly_chart(fig, use_container_width=True)
            
            
                
    if st.sidebar.checkbox("Analyse r√©plica par Classe"):
        data_classe = classe_anova_replica(data)
        mode = st.sidebar.selectbox("Type d'analyse", ['Ecart prix relatif',
                                                        'Proportion Green Web Site',
                                                        'Porportion Shopify'])
        
        fig = px.box(data_classe, x="Classe du produit", y= mode ,color = "Classe du produit")
        fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        st.plotly_chart(fig, use_container_width=True)
            
        
        
    
        
        
        



#%%
### VII - PROGRAMME PRINCIPAL
interface()
