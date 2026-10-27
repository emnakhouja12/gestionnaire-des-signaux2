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
from scipy.signal import butter, filtfilt
st.set_page_config(
    page_icon="📡",
    layout="wide"
)

st.markdown("""
<style>

/* ===== Signal Analyzer - Premium UI ===== */

/* Background */
.stApp {
    background: #f7f7fd;
}

.block-container {
    padding: 2.5rem 3rem 3rem;
    max-width: 1450px;
}

/* Dashboard cards */
.stat-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 15px 18px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    min-height: 90px;
}

.stat-title {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 8px;
}

.stat-value {
    font-size: 28px;
    font-weight: bold;
    color: #111827;
}

/* Titles */
h1 {
    color: #292746 !important;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    margin-bottom: 0.4rem;
}

h2, h3 {
    color: #38345e !important;
    font-weight: 700 !important;
}

.stApp h5 {
    color: #9B7EBD !important;
    font-size: 20px !important;
    font-weight: 800 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #eeecff;
    border-right: 1px solid #e2dffc;
}

/* Widget labels */
.stApp div[data-testid="stWidgetLabel"] p,
.stApp .stRadio > label,
.stApp .stTextInput > label,
.stApp .stNumberInput > label {
    color: #9B7EBD !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
}

/* Markdown labels */
.stApp div[data-testid="stMarkdownContainer"] p {
    color: #9B7EBD;
    font-weight: 700;
}

/* Inputs and select boxes */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #ffffff !important;
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

div[data-baseweb="input"] input {
    color: #34304F !important;
}

/* Radio buttons */
div[role="radiogroup"] {
    gap: 22px;
}

.stApp div[role="radiogroup"] label p {
    color: #000000 !important;
    font-weight: 600 !important;
}

.stApp div[role="radiogroup"] input {
    accent-color: #493366 !important;
}

/* Buttons */
.stButton > button {
    background: #493366 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px;
    font-weight: 700;
    min-height: 46px;
    box-shadow: none !important;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #35234D !important;
    color: #ffffff !important;
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

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Data table */
div[data-testid="stDataFrame"] {
    border: 1px solid #e6e3f2;
    border-radius: 12px;
    overflow: hidden;
}

/* Metric values */
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricValue"] *,
.stApp [data-testid="stMetricValue"] p {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* ===== SNR Slider ===== */

/* Slider track */
.stApp div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background-color: #E8DCEC !important;
}

/* Active track: target the filled section */
.stApp div[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div {
    background-color: #493366 !important;
}

/* Slider thumb */
.stApp div[data-testid="stSlider"] [role="slider"] {
    background-color: #493366 !important;
    border: 2px solid #493366 !important;
    box-shadow: none !important;
}

/* Slider value */
.stApp div[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #493366 !important;
    font-weight: 700 !important;
}

/* ===== SNR slider: mauve ===== */

/* Barre active */
.stApp [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderTrack"] > div {
    background-color: #493366 !important;
}

/* Autre structure possible de la barre active */
.stApp [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div {
    background-color: #493366 !important;
}

/* Curseur rond */
.stApp [data-testid="stSlider"] [role="slider"] {
    background-color: #493366 !important;
    border-color: #493366 !important;
    box-shadow: 0 0 0 2px #f7f7fd !important;
}

/* Valeur au-dessus du curseur */
.stApp [data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #493366 !important;
}

/* Boutons SNR : état normal */
.stApp [class*="snr_buttons"] div[data-testid="stButton"] button {
    min-height: 105px;
    border-radius: 16px;
    border: 1px solid #D9C9EA !important;
    background: #FFFFFF !important;
    color: #493366 !important;
    font-size: 1.2rem;
    font-weight: 700;
    white-space: pre-line;
    transition: all 0.2s ease;
}

/* Au survol : violet foncé */
.stApp [class*="snr_buttons"] div[data-testid="stButton"] button:hover {
    background: #493366 !important;
    color: #FFFFFF !important;
    border-color: #493366 !important;
}

/* Au clic ou au focus : garder le fond blanc */
.stApp div[data-testid="stButton"] button:focus:not(:hover) {
    background: #FFFFFF !important;
    color: #493366 !important;
    border-color: #D9C9EA !important;
    box-shadow: none !important;
}



</style>
""", unsafe_allow_html=True)



def analyser_signal(valeurs):
    amplitude_max = np.max(np.abs(valeurs))
    valeur_moyenne = np.mean(valeurs)
    valeur_rms = np.sqrt(np.mean(valeurs ** 2))
    puissance_moyenne = np.mean(valeurs ** 2)
    return amplitude_max, valeur_moyenne, valeur_rms, puissance_moyenne

        
def gener_signal(type_signal, amplitude, frequence, duree):
    t = np.linspace(0, duree, 500, endpoint=False)
    if type_signal == "carré": 
       valeurs=amplitude*np.sign(np.sin(2*np.pi*frequence*t))
    elif type_signal == "sinusoïdal":
       valeurs=amplitude*np.sin(2*np.pi*frequence*t)
    elif type_signal == "triangulaire":
        valeurs = (2 * amplitude / np.pi)* np.arcsin( np.sin(2 * np.pi * frequence * t))
    elif type_signal == "dent de scie":
        valeurs = 2 * amplitude * (frequence * t - np.floor(frequence * t + 0.5))
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
 
         
def afficher_comparaison_snr(temps, signal_original, signal_bruite):
    st.subheader("📈 Comparaison des signaux")
    st.caption("Axe X : temps (s) | Axe Y : amplitude")
    donnees = pd.DataFrame({"Signal original":signal_original,"Signal bruité":signal_bruite },index=temps)
    st.line_chart(donnees)
         

def ajouter_bruit(valeurs, snr_db):
    puissance_signal = np.mean(valeurs ** 2)
    if puissance_signal == 0:
        st.error("La puissance du signal doit être positive.")
        #arret de la fonction si la puissnace est égale à 0
        return None, None
    puissance_bruit = puissance_signal/(10 **(snr_db /10))
    bruit = np.random.normal(0,np.sqrt(puissance_bruit),len(valeurs))
    signal_bruite = valeurs + bruit
    return signal_bruite, bruit

# Calcul du SNR
def calculer_snr(signal, bruit):
    puissance_signal = np.mean(signal ** 2)
    puissance_bruit = np.mean(bruit ** 2)
    if puissance_bruit == 0:
        return float("infini")
    return 10 * np.log10(puissance_signal / puissance_bruit)
        
         

def afficher_comparaison_snr(temps, signal_original, signal_bruite):
    st.subheader("📈 Comparaison des signaux")
    st.caption("Axe X : temps (s) | Axe Y : amplitude")
    donnees = pd.DataFrame({"Signal original": signal_original,"Signal bruité": signal_bruite}, index=temps)
    st.line_chart(donnees)
         


def afficher_comparaison_fft(temps, signal_original, signal_bruite):
    N = len(signal_original)
    dt = temps[1] - temps[0]
    # FFT du signal original
    fft_original = np.fft.fft(signal_original)
    frequences = np.fft.fftfreq(N, dt)
    amplitude_original = np.abs(fft_original) / N
    # FFT du signal bruité
    fft_bruite = np.fft.fft(signal_bruite)
    amplitude_bruitee = np.abs(fft_bruite) / N
    # Garder les fréquences positives
    masque = frequences >= 0
    frequences = frequences[masque]
    amplitude_original = amplitude_original[masque]
    amplitude_bruitee = amplitude_bruitee[masque]
    # Corriger l'amplitude du spectre positif
    amplitude_original[1:] *= 2
    amplitude_bruitee[1:] *= 2
    st.subheader("📊 Comparaison des spectres FFT")
    st.caption("Axe X : fréquence (Hz) | Axe Y : amplitude")
    donnees =pd.DataFrame({"Signal original": amplitude_original,"Signal bruité":amplitude_bruitee},index=frequences)
    st.line_chart(donnees)


def filtrer_signal(signal, frequence_coupure, frequence_echantillonnage):
    frequence_nyquist = frequence_echantillonnage / 2
    if frequence_coupure <= 0 or frequence_coupure >= frequence_nyquist:
        st.error("La fréquence de coupure doit être comprise entre 0 et la fréquence de Nyquist.")
        return None
    ordre = 4
    numerateur,denominateur=butter(ordre,frequence_coupure/frequence_nyquist, btype="low")
    signal_filtre=filtfilt(numerateur,denominateur,signal)
    return signal_filtre
        
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
    st.session_state["page_navigation"] = st.session_state.pop(
        "nouvelle_page"
    )
page = st.sidebar.radio( "Navigation",["🏠 Dashboard", "🗂️ Gestion des signaux","📈 Analyse des signaux", "🔬 Fibre optique","🔊 Bruit et SNR"], key="page_navigation") 
if page == "🏠 Dashboard":
    st.title("📡 Tableau de bord")
    st.caption("Bienvenue dans Signal Analyzer — Gérez vos signaux et analysez leurs caractéristiques.") 
    st.divider()
    # Calcul des statistiques réelles
    total = len(st.session_state.l)
    sinus = sum( 1 for s in st.session_state.l if s["type"] == "sinusoïdal")
    carres = sum( 1 for s in st.session_state.l if s["type"] == "carré")
    triangulaire=sum( 1 for s in st.session_state.l if s["type"] == "triangulaire")
    dent_de_scie=sum( 1 for s in st.session_state.l if s["type"] == "dent de scie")
    # Cartes statistiques
    col1, col2, col3 ,col4,col5= st.columns(5,border=True)
    with col1:
        col1.metric("📡 Total des signaux", total)
    with col2:
        st.metric("〰️ Signaux sinusoïdaux", sinus)
    with col3:
        st.metric("⬜ Signaux carrés", carres)
    with col4:
        st.metric("Signaux triangulaires", triangulaire)
    with col5:
        st.metric("Signaux dent de scie", dent_de_scie)        
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
                "Amplitude": s["amplitude"]})  
        st.dataframe( derniers,use_container_width=True,hide_index=True)
    else:
        st.info( "Aucun signal enregistré.Ajoutez votre premier signal dans Gestion des signaux.")
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
    tab1, tab2, tab3 = st.tabs(["➕ Ajouter", "✏ Modifier","🗑️ Supprimer"])
    with tab1:
        st.markdown("## ➕ Ajouter un signal")
        st.caption( "Configurez les paramètres de votre signal " "pour l'ajouter à votre bibliothèque.")
        st.divider()
        st.markdown('<p style="color: #000000; font-weight: 700; ''font-size: 0.95rem; margin-bottom: 0.5rem;">' 'Paramètres du signal</p>',unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")
        with col1:
            nom = st.text_input("Nom du signal",placeholder="Ex. : Signal_1") 
            frequence = st.number_input("Fréquence (Hz)",min_value=0.0,value=0.0)
            st.markdown("Type de signal")
            type_signal = st.radio("Sélectionnez une forme d'onde", ["sinusoïdal", "carré","triangulaire", "dent de scie"], horizontal=True, index=None,label_visibility="collapsed")
        with col2:
            amplitude = st.number_input("Amplitude", min_value=0.0, value=0.0,step=0.5)
            offset=st.number_input("Composante continue",value=0.0,step=0.5)
            duree = st.number_input( "Durée (s)",min_value=0.0,value=0.0,step=0.5)
        st.divider()
        st.markdown( "<p style='color:#77738f;font-size:13px;'>" "💡 Vérifiez les paramètres avant d'ajouter le signal." "</p>", unsafe_allow_html=True)
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
   
            

elif page == "📈 Analyse des signaux":
    st.title("📈 Analyse temporelle et FFT")
    st.write(
        "Visualisez vos signaux dans les domaines temporel et fréquentiel ")
    st.divider()
    if not st.session_state.l:
        st.info(
            "📭 Aucun signal disponible, veuillez ajouter un signal dans la page Gestion des signaux » pour commencer l'analyse.")
    else:
        col1, col2 = st.columns(2, gap="large")
        noms = [x["nom"] for x in st.session_state.l]
        with col1:
            st.subheader("📡 Signal à analyser")
            signal = st.radio("Choisir un signal :",noms, index=None,key="signal_analyse")
        with col2:
            st.subheader("📊 Type d'affichage")
            choix = st.radio( "Choisir la visualisation :",["Signal temporel", "Spectre FFT", "Les deux"],index=None, key="type_affichage")
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
            # Nouvelle section : mesures du signal
            st.divider()
            with st.expander("📐 Mesures du signal", expanded=True):
                valeurs = np.array(choisi[0]["valeur"])
                amplitude_max, valeur_moyenne, valeur_rms, puissance_moyenne = analyser_signal(valeurs)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(  "Amplitude maximale",str(round(amplitude_max, 3)) +" V")
                    st.metric( "Valeur moyenne",str(round(valeur_moyenne, 3))+" V")
                with col2:
                    st.metric("Valeur efficace (RMS)",str(round(valeur_rms, 3))+" V")
                    st.metric("Puissance moyenne (charge de 1 Ω)",str(round(puissance_moyenne, 3))+" W")
        else:
            st.info("👆 Sélectionnez un signal et un type d'affichage pour visualiser le graphique.")
                
            
elif page == "🔬 Fibre optique":
    st.title("🔬 Analyse de la fibre optique")
    st.caption(
        "Calculez la puissance reçue et vérifiez la qualité de votre liaison optique.")
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


elif page == "🔊 Bruit et SNR":
    st.title("🔊 Bruit et rapport signal sur bruit (SNR)")
    st.write( "Ajoutez du bruit à un signal et analysez la qualité du signal obtenu.")
    st.divider()
    if not st.session_state.l:
        st.info("Aucun signal disponible.Veuillez d'abord ajouter un signal dans la page Gestion des signaux .")
    else:
        noms =[s["nom"] for s in st.session_state.l]
        signal_choisi = st.selectbox("Choisir un signal",noms)
        st.markdown("### Rapport signal sur bruit souhaité (dB)")
        if "snr_db" not in st.session_state:
            st.session_state.snr_db = 15
        with st.container(key="snr_buttons"):
            col1, col2, col3, col4 = st.columns(4, gap="small")
            with col1:
                if st.button("5 dB", key="snr_5",use_container_width=True):
                    st.session_state.snr_db = 5
            with col2:
                if st.button("15 dB", key="snr_15",use_container_width=True):
                    st.session_state.snr_db = 15
            with col3:
                if st.button("25 dB", key="snr_25",use_container_width=True):
                    st.session_state.snr_db = 25
            with col4:
                if st.button("35 dB", key="snr_35",use_container_width=True):
                    st.session_state.snr_db = 35
        snr_db = st.session_state.snr_db
        st.divider()
        if st.button("🔊 Générer le signal bruité",key="generer_signal_bruite"):
            #Rechercher le signal sélectionné
            choisi = []
            for s in st.session_state.l:
                if s["nom"] ==signal_choisi:
                    choisi.append(s)
            signal_original=np.array(choisi[0]["valeur"])
            # Ajouter le bruit
            resultat=ajouter_bruit(signal_original,snr_db)
            if resultat[0] is not None:
                signal_bruite, bruit =resultat
                # Calculer le SNR réellement obtenu
                snr_mesure=calculer_snr(signal_original,bruit)
                # Sauvegarder les résultats
                st.session_state.signal_original=signal_original
                st.session_state.signal_bruite=signal_bruite
                st.session_state.bruit=bruit
                st.session_state.snr_mesure=snr_mesure
                st.session_state.temps_snr=np.array(choisi[0]["temps"])
                st.success("Signal bruité généré avec succès !")
        if "snr_mesure" in st.session_state:
           st.divider()
           st.subheader("📊 Résultats du rapport signal sur bruit")
           col1, col2 = st.columns(2)
           with col1:
               st.metric("SNR souhaité", f"{snr_db} dB")
           with col2: 
                st.metric("SNR mesuré",f"{st.session_state.snr_mesure:.2f} dB")
        if "signal_bruite" in st.session_state:
            afficher_comparaison_snr(st.session_state.temps_snr, st.session_state.signal_original,st.session_state.signal_bruite)
        if "signal_bruite" in st.session_state:
            afficher_comparaison_fft( st.session_state.temps_snr,st.session_state.signal_original,st.session_state.signal_bruite)
        st.divider()
        st.subheader("🎚️ Filtrage du signal bruité")
        if "signal_bruite" not in st.session_state:
            st.info("Générez d'abord un signal bruité pour pouvoir appliquer le filtre passe-bas.")
        else:
            frequence_coupure =st.number_input("Fréquence de coupure (Hz)",min_value=1.0,value=10.0,step=1.0,key="frequence_coupure", disabled=False)
            if st.button("Appliquer le filtre passe-bas"):
                signal_bruite=np.array(st.session_state.signal_bruite)
                signal_original =np.array(st.session_state.signal_original)
                temps = np.array(st.session_state.temps_snr)
                pas = temps[1] - temps[0]
                frequence_echantillonnage = 1 / pas
                signal_filtre =filtrer_signal(signal_bruite,frequence_coupure,frequence_echantillonnage) 
                if signal_filtre is not None:
                    st.session_state.signal_filtre =signal_filtre
                    erreur_avant = signal_original - signal_bruite
                    erreur_apres = signal_original - signal_filtre
                    puissance_signal = np.mean(signal_original ** 2)
                    puissance_bruit_avant = np.mean(erreur_avant ** 2)
                    puissance_bruit_apres = np.mean(erreur_apres ** 2)
                    st.success("Le filtre passe-bas a été appliqué !")
                    if puissance_signal > 0 and puissance_bruit_avant > 0:
                        snr_avant = 10 * np.log10( puissance_signal / puissance_bruit_avant)
                        st.metric("SNR avant filtrage", f"{snr_avant:.2f} dB")
                    else:
                        snr_avant = None
                    if puissance_signal > 0 and puissance_bruit_apres > 0:
                        snr_apres = 10 * np.log10( puissance_signal / puissance_bruit_apres)
                    else:
                        snr_apres = None
                    if snr_avant is not None and snr_apres is not None:
                        amelioration = snr_apres - snr_avant
                        st.metric("Amélioration du SNR",f"{amelioration:.2f} dB")
            if "signal_filtre" in st.session_state:
                st.caption("Axe X : temps (s) | Axe Y : amplitude")
                donnees = pd.DataFrame({"Signal original":np.array(st.session_state.signal_original),
                "Signal bruité": np.array(st.session_state.signal_bruite),"Signal filtré":np.array(st.session_state.signal_filtre)},index=np.array(st.session_state.temps_snr))
                st.line_chart(donnees)




