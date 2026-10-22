# Analyseur de signaux — Analyse temporelle et fréquentielle

## Description du projet

**Analyseur de signaux** est une application développée en Python avec Streamlit permettant de créer, gérer, visualiser et analyser des signaux dans les domaines temporel et fréquentiel.

L'application dispose d'une interface interactive qui permet de manipuler les paramètres des signaux et de visualiser leurs caractéristiques, notamment grâce à la transformée de Fourier rapide (FFT).

Ce projet a été réalisé dans le cadre de mon apprentissage du **traitement du signal et du multimédia**.

## Fonctionnalités

### Gestion des signaux

- Ajouter un signal en précisant son nom, son type, son amplitude, sa fréquence et sa durée.
- Modifier les paramètres d'un signal existant.
- Supprimer un signal.
- Afficher les signaux enregistrés dans un tableau.

### Analyse des signaux

- Visualiser les signaux dans le domaine temporel.
- Analyser le contenu fréquentiel à l'aide de la FFT.
- Afficher le signal temporel, le spectre fréquentiel ou les deux simultanément.

### Gestion des données

- Enregistrer les informations des signaux dans une base de données.
- Consulter et gérer les signaux à partir de l'interface de l'application.

## Technologies utilisées

- **Python** : développement de l'application et traitement des données.
- **Streamlit** : création de l'interface interactive.
- **NumPy** : calculs numériques et traitement des signaux.
- **Matplotlib** : visualisation graphique des signaux.
- **FFT** : analyse fréquentielle.
- **SQLite** : stockage des données.

*Remarque : vérifie que les bibliothèques mentionnées correspondent bien à celles utilisées dans ton code.*

## Installation et exécution

### 1. Cloner le dépôt

```bash
git clone URL_DE_VOTRE_DEPOT
```

### 2. Accéder au dossier du projet

```bash
cd Signal-Analyser
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira dans le navigateur.

## Utilisation

1. Lancer l'application.
2. Accéder à la section de gestion des signaux.
3. Ajouter un signal en renseignant ses paramètres.
4. Consulter, modifier ou supprimer les signaux enregistrés.
5. Accéder à la page d'analyse des signaux.
6. Choisir le mode de visualisation souhaité :
   - **Signal temporel** : visualisation de l'évolution du signal en fonction du temps.
   - **Spectre FFT** : représentation des composantes fréquentielles du signal.
   - **Les deux** : affichage des deux représentations.

## Objectifs pédagogiques

Ce projet a pour objectifs de :

- Mettre en pratique la programmation Python.
- Comprendre la représentation des signaux dans les domaines temporel et fréquentiel.
- Découvrir l'utilisation de la FFT pour l'analyse fréquentielle.
- Développer une application interactive avec Streamlit.
- Manipuler une base de données pour enregistrer et gérer des informations.

## Auteur

**Emna Khouja**

Étudiante en Technologies de l'Information et de la Communication (TIC) à la Faculté des Sciences de Tunis (FST).

---

*Projet académique — Traitement du signal et multimédia.*
