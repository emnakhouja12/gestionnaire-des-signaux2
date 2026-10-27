# Signal Analyzer - Analyse et traitement des signaux

Application interactive développée avec **Python et Streamlit** dans le cadre d'un projet académique en Traitement du signal et multimédia à la Faculté des Sciences de Tunis (FST).

## Présentation du projet

Signal Analyzer permet de générer, gérer, visualiser et analyser différents signaux, d'étudier le bruit et le SNR, de tester un filtre passe-bas et de calculer la puissance reçue dans une liaison à fibre optique.

## Objectifs

- Générer et analyser différents types de signaux.
- Étudier les domaines temporel et fréquentiel.
- Mesurer les caractéristiques des signaux.
- Évaluer l'effet du bruit et du filtrage.
- Étudier les pertes dans une liaison optique.
- Enregistrer les paramètres dans une base SQLite.

## Fonctionnalités

### 1. Tableau de bord

- Statistiques des signaux enregistrés par type.
- Affichage des derniers signaux ajoutés.
- Accès rapide aux principales fonctionnalités.

### 2. Gestion des signaux

Ajout, modification, suppression et affichage des signaux avec les paramètres suivants : nom, type, amplitude, fréquence et durée.

Types disponibles :
- Sinusoïdal.
- Carré.
- Triangulaire.
- Dent de scie.

### 3. Analyse temporelle et fréquentielle

- Visualisation temporelle des signaux.
- Calcul et affichage du spectre FFT.
- Estimation de la fréquence dominante.
- Avertissement lié à la condition de Nyquist-Shannon.
- Calcul de l'amplitude maximale, de la valeur moyenne, de la valeur efficace (RMS) et de la puissance moyenne.

### 4. Analyse de la fibre optique

Calcul de la puissance reçue à partir de la puissance d'émission, de la longueur de la fibre et de son coefficient d'atténuation. L'application prend également en compte les pertes des connecteurs et des épissures, puis compare le résultat à la sensibilité du récepteur.

Longueurs d'onde proposées : 850 nm, 1310 nm et 1550 nm.

### 5. Bruit et rapport signal sur bruit (SNR)

- Génération d'un bruit gaussien avec un SNR souhaité de 5, 15, 25 ou 35 dB.
- Comparaison temporelle des signaux original et bruité.
- Comparaison de leurs spectres FFT.
- Mesure du SNR obtenu.
- Filtrage passe-bas Butterworth d'ordre 4.
- Comparaison du SNR avant et après filtrage.

## Technologies utilisées

- **Python** : développement.
- **Streamlit** : interface interactive.
- **NumPy** : calcul et traitement des signaux.
- **Pandas** : organisation des données et graphiques.
- **SciPy** : filtrage numérique.
- **SQLite** : stockage des données.
- **Git et GitHub** : gestion de versions.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/emnakhouja12/gestionnaire-des-signaux2.git
cd gestionnaire-des-signaux2
```

### 2. Installer les dépendances

```bash
pip install streamlit numpy pandas scipy
```

### 3. Lancer l'application

```bash
streamlit run projet.py
```

## Base de données

L'application utilise SQLite (`signals2.db`) pour enregistrer les paramètres des signaux : type, nom, amplitude, fréquence et durée. La base de données est créée automatiquement si elle n'existe pas.

## Structure du projet

```text
Signal-Analyzer/
├── projet.py
├── signals2.db
└── README.md
```

- `projet.py` : code de l'application.
- `signals2.db` : base de données créée automatiquement.
- `README.md` : documentation du projet.

## Utilisation

1. Lancer l'application.
2. Ajouter des signaux dans la page de gestion.
3. Les modifier, les supprimer ou les consulter.
4. Analyser leur représentation temporelle et leur spectre FFT.
5. Étudier le bruit, le SNR et le filtrage.
6. Calculer la puissance reçue d'une liaison à fibre optique.

## Perspectives d'amélioration

- Ajouter de nouveaux types de signaux.
- Permettre l'exportation des résultats.
- Enrichir les outils d'analyse et de visualisation.

## Contexte académique

Projet réalisé dans le cadre des études en **Technologies de l'Information et de la Communication (TIC)** à la **Faculté des Sciences de Tunis (FST)**, autour du traitement du signal et des télécommunications.

## Auteur
Emna khouja.
