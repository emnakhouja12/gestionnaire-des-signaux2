# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 15:13:11 2026

@author: Emna
"""

#creation d'un menu

import streamlit as st
import sqlite3
import numpy as np
import pandas as pd

st.set_page_config(
    page_icon="📡",
    layout="wide"
)


st.markdown("""
<style>
/* Background */

/* ===== Signal Analyzer - Premium UI ===== */

.stApp {
    background: #f7f7fd;
}

.block-container {
    padding: 2.5rem 3rem 3rem;
    max-width: 1450px;
}

/* Main title */
h1 {
    color: #292746 !important;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    margin-bottom: 0.4rem;
}

/* Section titles */
h2, h3 {
    color: #38345e !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #eeecff;
    border-right: 1px solid #e2dffc;
}

/* Form labels */
div[data-testid="stWidgetLabel"] p {
    color: #595477 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}

/* Inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: white !important;
    border: 1px solid #e4e1f2 !important;
    border-radius: 12px !important;
    min-height: 46px;
    transition: border-color 0.2s;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #8175ed !important;
    box-shadow: 0 0 0 3px rgba(129, 117, 237, 0.12);
}

/* Radio options */
div[role="radiogroup"] {
    gap: 22px;
}

div[role="radiogroup"] label p {
    color: #403b5c !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #8275f5, #6758e8);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.5rem;
    font-weight: 650;
    min-height: 46px;
    box-shadow: 0 4px 10px rgba(103, 88, 232, 0.16);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #7164e9, #5545d4);
    box-shadow: 0 6px 15px rgba(103, 88, 232, 0.24);
    transform: translateY(-1px);
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600;
    padding: 13px 19px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #6858e8 !important;
}

/* Dividers */
hr {
    border-color: #e7e5f2;
}

/* Success and error messages */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Data table */
div[data-testid="stDataFrame"] {
    border: 1px solid #e6e3f2;
    border-radius: 12px;
    overflow: hidden;
}

/* Mauve labels for all form fields */
.stApp div[data-testid="stWidgetLabel"] p,
.stApp label[data-testid="stWidgetLabel"] p,
.stApp .stRadio > label,
.stApp .stTextInput > label,
.stApp .stNumberInput > label {
    color: #9B7EBD !important;
    font-weight: 700 !important;
}

/* Mauve text for radio option labels */
.stApp div[role="radiogroup"] label p {
    color: #9B7EBD !important;
    font-weight: 600 !important;
}

/* Keep input text dark and readable */
.stApp div[data-baseweb="input"] input {
    color: #34304F !important;
}
.stApp h5 {
    font-weight: 800 !important;
    color: #9B7EBD !important;
    font-size: 20px !important;
}

/* Make field labels bold too */
.stApp div[data-testid="stWidgetLabel"] p {
    font-weight: 700 !important;
    color: #9B7EBD !important;}
    
/* Radio button circle */
.stApp div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
    color: #000000 !important;
}

/* Radio button selected circle */
.stApp div[role="radiogroup"] input {
    accent-color: #000000 !important;
}

/* Radio button text */
.stApp div[role="radiogroup"] label p {
    color: #000000 !important;
}


""", unsafe_allow_html=True)

def gener_signal(type_signal, amplitude, frequence, duree):
    t = np.linspace(0, duree, 500, endpoint=False)
    if type_signal == "carré": 
       valeurs=amplitude*np.sign(np.sin(2*np.pi*frequence*t))
    else:
       valeurs=amplitude*np.sin(2*np.pi*frequence*t)
    return t, valeurs
def afficher_signal(l):
     for x in l:
         st.subheader('Signal temporel de '+x['nom']) 
         st.caption("Axe X : temps (s) | Axe Y : amplitude")
         st.line_chart(pd.DataFrame({"amplitude": x['valeur']}, index=x['temps']))

def fft_signal(l): 
    for x in l:
         valeurs = x['valeur']
         temps = x['temps']
         N = len(valeurs)
         dt = temps[1] - temps[0]
         fft_valeurs = np.fft.fft(valeurs)
         frequences = np.fft.fftfreq(N, dt)
         amplitude_fft = np.abs(fft_valeurs) / N
         masque = frequences >= 0
         amplitude_fft[masque] *= 2
         amplitude_fft[frequences == 0] /= 2
         i = np.argmax(amplitude_fft[masque][1:])+ 1
         st.write("Fréquence dominante :", frequences[masque][i], "Hz")
         fs = 1 / dt
         #fmax=x['frequence'] 
         if x['frequence'] > fs / 2:
             st.warning("Shannon non respecté : le pic affiché est faux")
         st.subheader("Spectre de " + x['nom'])
         st.caption("Axe X : fréquence (Hz) | Axe Y : amplitude")
         st.line_chart(pd.DataFrame({"amplitude": amplitude_fft[masque]}, index=frequences[masque]))
#=====================
# BASE DE  DONNÉES
conn = sqlite3.connect("signals2.db")
conn.execute("create table if not exists signals2(type text, nom text, amplitude real, frequence real, duree real)")
conn.commit()
st.sidebar.title("📡 Signal Analyzer")
if 'l' not in st.session_state:
    st.session_state.l = []
    rows=conn.execute('select type, nom, amplitude, frequence, duree from signals2').fetchall()
    for x in rows:
        t = np.linspace(0, x[3], 500, endpoint=False)
        t, valeurs = gener_signal(x[0], x[2], x[3], x[4])
        dic = {'type':x[0],'nom': x[1], 'amplitude': x[2], 'frequence': x[3],
               'duree': x[4],'valeur': valeurs, 'temps': t}
        st.session_state.l.append(dic)
if "page_navigation" not in st.session_state:
    st.session_state["page_navigation"] = "🏠 Dashboard"

if "nouvelle_page" in st.session_state:
    st.session_state["page_navigation"] = st.session_state.pop( "nouvelle_page")
page = st.sidebar.radio( "Navigation",["🏠 Dashboard", "🗂️ Gestion des signaux","📈 Analyse des signaux", "🔬 Fibre optique"], key="page_navigation") 
if page == "🏠 Dashboard":

    st.title("📡 Tableau de bord")
    st.caption(
        "Bienvenue dans Signal Analyzer — "
        "Gérez vos signaux et analysez leurs caractéristiques.")
    st.divider()
    # Calcul des statistiques réelles
    total = len(st.session_state.l)
    sinus = sum( 1 for s in st.session_state.l if s["type"] == "sinusoïdal")
    carres = sum( 1 for s in st.session_state.l if s["type"] == "carré")
    # Cartes statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📡 Total des signaux", total)
    with col2:
        st.metric("〰️ Signaux sinusoïdaux", sinus)
    with col3:
        st.metric("⬜ Signaux carrés", carres)
    st.divider()
    # Derniers signaux
    st.subheader("📋 Derniers signaux ajoutés")
    if total > 0:
        derniers = []
        for s in st.session_state.l[-5:][::-1]:
            derniers.append({
                "Nom": s["nom"],
                "Type": s["type"],
                "Fréquence (Hz)": s["frequence"],
                "Amplitude": s["amplitude"]
            })
        st.dataframe( derniers,use_container_width=True,hide_index=True)
    else:
        st.info(
            "Aucun signal enregistré. "
            "Ajoutez votre premier signal dans "
            "Gestion des signaux." )
    st.divider()
    st.subheader("🚀 Accès rapide")
    st.write("Que souhaitez-vous faire ?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗂️ Gérer les signaux", use_container_width=True):
            st.session_state["onglet_gestion"] = "➕ Ajouter"
            st.session_state["nouvelle_page"] = "🗂️ Gestion des signaux"
            st.rerun()
    with col2:
        if st.button("📈 Analyser les signaux",use_container_width=True):
            st.session_state["nouvelle_page"] = ( "📈 Analyse des signaux" )
            st.rerun()

elif page == "🗂️ Gestion des signaux":
    st.title("🗂️ Gestion des signaux")
    tab1, tab2, tab3,tab4 = st.tabs(["➕ Ajouter", "✏ Modifier","🗑️ Supprimer","📡 Affichage"])
    with tab1:
        st.markdown("## ➕ Ajouter un signal")
        st.caption( "Configurez les paramètres de votre signal " "pour l'ajouter à votre bibliothèque.")
        st.divider()
        st.markdown("Type de signal")
        type_signal = st.radio("Sélectionnez une forme d'onde", ["sinusoïdal", "carré"], horizontal=True, index=None,label_visibility="collapsed")
        st.markdown("Paramètres du signal")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            nom = st.text_input("Nom du signal",placeholder="Ex. : Signal_1") 
            frequence = st.number_input("Fréquence (Hz)",min_value=0.0,value=0.0,)
        with col2:
            amplitude = st.number_input("Amplitude", min_value=0.0, value=0.0,step=0.5)
            duree = st.number_input( "Durée (s)",min_value=0.0,value=0.0,step=0.5)
        st.divider()
        st.markdown(
        "<p style='color:#77738f;font-size:13px;'>"
        "💡 Vérifiez les paramètres avant d'ajouter le signal."
        "</p>",
        unsafe_allow_html=True )
        message = st.empty()
        ajouter = st.button("＋  Ajouter le signal", use_container_width=False)
        if ajouter:
            if not nom:
                st.error("Donner un nom au signal")
            elif type_signal is None:
                st.error("Choisir le type de signal")
            elif amplitude <= 0 or frequence <= 0 or duree <= 0:
                st.error("Vérifier votre signal")
            else:
                t, valeurs = gener_signal(type_signal, amplitude, frequence, duree)
                conn.execute('INSERT INTO signals2 VALUES (?,?,?,?,?)',(type_signal, nom, amplitude, frequence, duree))
                conn.commit()
                dic = {
                    'type': type_signal,
                    'nom': nom,
                    'amplitude': amplitude,
                    'frequence': frequence,
                    'duree': duree,
                    'valeur': valeurs,
                    'temps': t
                    }
                st.session_state.l.append(dic)
                message.success("✅ Signal ajouté avec succès !")
    with tab2:
        st.subheader("✏️ Modifier un signal")
        if len(st.session_state.l) > 0:
            noms = [s['nom'] for s in st.session_state.l]
            nom_choisi = st.selectbox("Choisir le signal à modifier",noms)
            signal = next(s for s in st.session_state.l if s['nom'] == nom_choisi)
            col1, col2 = st.columns(2, gap="large")
            with col1:
                nouveau_nom = st.text_input("Nom du signal",value=signal['nom'])
                nouvelle_frequence = st.number_input("Fréquence (Hz)",min_value=0.0,value=float(signal['frequence']))
            with col2:
                nouvelle_amplitude = st.number_input("Amplitude", min_value=0.0, value=float(signal['amplitude']))
                nouvelle_duree = st.number_input("Durée (s)",min_value=0.0,value=float(signal['duree']))
            if st.button("💾 Enregistrer les modifications"):
                t2,valeur2 = gener_signal(signal['type'], nouvelle_amplitude,nouvelle_frequence, nouvelle_duree)
                conn.execute(
                    "UPDATE signals2 SET nom=?, amplitude=?, frequence=?, duree=? WHERE nom=?",(nouveau_nom, nouvelle_amplitude, nouvelle_frequence, nouvelle_duree,  nom_choisi))
                conn.commit()
                signal["nom"] = nouveau_nom
                signal["amplitude"] = nouvelle_amplitude
                signal["frequence"] = nouvelle_frequence
                signal["duree"] =nouvelle_duree
                signal["valeur"] = valeur2
                signal["temps"] = t2
                st.success("✅ Signal modifié avec succès !")
                st.dataframe(st.session_state.l)
    with tab3: 
       st.subheader("🗑️ Supprimer un signal")
       if len(st.session_state.l) > 0:
           noms = [s['nom'] for s in st.session_state.l]
           nom_choisi = st.selectbox("Effacer un signal :",noms)
           signal = next(s for s in st.session_state.l if s['nom'] == nom_choisi)
           st.write("### 📊 Informations du signal")
           col1, col2 = st.columns(2)
           with col1: 
               st.write("**Type :**", signal['type'])
               st.write("**Fréquence :**", signal['frequence'], "Hz")
           with col2:
               st.write("**Amplitude :**", signal['amplitude'])
               st.write("**Durée :**", signal['duree'], "s")
           if st.button("🗑️ Supprimer ce signal"):
               conn.execute("DELETE FROM signals2 WHERE nom = ?",(nom_choisi,))
               conn.commit()
               st.session_state.l.remove(signal)
               st.success("Signal supprimé avec succès !")
               st.rerun()
       else: 
           st.info("Aucun signal disponible à supprimer.")
    with tab4:
        st.subheader("📡 Affichage des signaux")
        st.write("Consultez vos signaux.")
        if len(st.session_state.l) > 0:
            st.markdown("### 📋 Liste des signaux")
            tableau = []
            for s in st.session_state.l:
                tableau.append({"Type": s["type"],"Nom": s["nom"],"Amplitude": s["amplitude"],"Fréquence (Hz)": s["frequence"],
                   "Durée (s)": s.get("duree", s.get("dureé", 0))})          
            st.dataframe(tableau,use_container_width=True, hide_index=True)
            
elif page == "📈 Analyse des signaux":
    st.title("📈 Analyse temporelle et FFT")
    st.write(
        "Visualisez vos signaux dans les domaines "
        "temporel et fréquentiel.")
    st.divider()
    if not st.session_state.l:
        st.info(
            "📭 Aucun signal disponible. "
            "Veuillez ajouter un signal dans la page "
            "« Gestion des signaux » pour commencer l'analyse.")
    else:
        col1, col2 = st.columns(2, gap="large")
        noms = [x["nom"] for x in st.session_state.l]
        with col1:
            st.subheader("📡 Signal à analyser")
            signal = st.radio("Choisir un signal :",noms,index=None,key="signal_analyse")
        with col2:
            st.subheader("📊 Type d'affichage")
            choix = st.radio("Choisir la visualisation :", ["Signal temporel", "Spectre FFT", "Les deux"], index=None,    key="type_affichage")
        st.divider()
        st.subheader("📈 Visualisation du signal")
        if signal and choix:
            choisi = []
            for s in st.session_state.l:
                if s["nom"] == signal:
                    choisi.append(s)
            if choix == "Signal temporel":
                afficher_signal(choisi)
            elif choix == "Spectre FFT":
                fft_signal(choisi)
            elif choix == "Les deux":
                afficher_signal(choisi)
                fft_signal(choisi)
        else:
            st.info(
                "👆 Sélectionnez un signal et un type "
                "d'affichage pour visualiser le graphique.")
elif page == "🔬 Fibre optique":
    st.title("🔬 Analyse de la fibre optique")
    st.caption(
        "Calculez la puissance reçue et vérifiez "
        "la qualité de votre liaison optique.")
    st.divider()
    # Paramètres de transmission
    st.subheader("📡 Paramètres de la liaison")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        longeur_donde = st.selectbox("Longueur d'onde",["850 nm", "1310 nm", "1550 nm"],index=None, placeholder="Choisir une longueur d'onde")
        puiss = st.radio( "Unité de puissance émise",  ["dBm", "mW"], index=None,horizontal=True)
        puis_emise = st.number_input(  "Puissance d'émission", min_value=0.0,help="Valeur de la puissance à l'entrée de la fibre." )
    with col2:
        longeur = st.number_input( "Longueur de la fibre (km)", min_value=0.0)
        attenuation = st.number_input("Coefficient d'atténuation (dB/km)",min_value=0.0)
        sensibilite = st.number_input("Sensibilité du récepteur (dBm)", value=-20.0)
    st.divider()
    # Pertes supplémentaires
    st.subheader("⚙️ Pertes supplémentaires")
    ajouter_pertes = st.checkbox("Prendre en compte les connecteurs et les épissures")
    nbre_connecteur = 0
    perte_connecteur = 0.0
    nbre_epissure = 0
    perte_eppisure = 0.0
    if ajouter_pertes:
        with st.expander("Configurer les pertes", expanded=True):
            col3, col4 = st.columns(2, gap="large")
            with col3:
                nbre_connecteur = st.number_input( "Nombre de connecteurs", min_value=0, step=1)
                perte_connecteur = st.number_input( "Perte par connecteur (dB)",min_value=0.0)
            with col4:
                nbre_epissure = st.number_input("Nombre d'épissures",min_value=0,step=1)
                perte_eppisure = st.number_input("Perte par épissure (dB)",min_value=0.0)
    st.divider()
    if st.button("Calculer la puissance récue "):
        if longeur:
            if longeur<=0:
                st.error("verifier la longeur")     
            elif puiss=='mW':
                puiss_emise2=10*np.log10(puis_emise)
                #if nbre_connecteur and perte_connecteur and nbre_epissure and  perte_eppisure: 
                precue=round(puiss_emise2-attenuation*longeur-nbre_connecteur*perte_connecteur-nbre_epissure*perte_eppisure,2)
                st.write("Precue=",precue,"dBm")   
            else:
                #if nbre_connecteur and nbre_epissure:  
                precue=round(puis_emise-attenuation*longeur-nbre_connecteur*perte_connecteur-nbre_epissure*perte_eppisure,2)
                st.write("Precue=",precue,"dBm")
                if precue>=sensibilite: 
                    st.success('Liaison acceptable')
                else:
                    st.error("Liaison inacceptable")
