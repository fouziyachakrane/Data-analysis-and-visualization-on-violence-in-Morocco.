<div align="center">

# 🇲🇦 GRB-10

### Analyse & Visualisation des Données de Violence Basée sur le Genre au Maroc

*Une application desktop pour explorer, cartographier et visualiser des données sensibles à travers une interface moderne et interactive.*

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-Cartographie-77B829?style=for-the-badge&logo=leaflet&logoColor=white)
![License](https://img.shields.io/badge/License-Académique-lightgrey?style=for-the-badge)

</div>

---

## ✨ Aperçu

**GRB-10** est une application de bureau construite avec **PySide6** qui transforme un jeu de données brut sur la violence basée sur le genre au Maroc en une expérience visuelle claire et exploitable : carte interactive des régions, tableaux de bord statistiques et générateur de graphiques à la demande.

<div align="center">

| 🗺️ Carte interactive | 📊 Graphiques statistiques | 🎛️ Visualisation dynamique |
|:---:|:---:|:---:|
| Statistiques par région, code couleur, popups détaillés | 8 analyses croisées prêtes à l'emploi | Choisissez vos variables, générez à la volée |

</div>


---

## 🚀 Fonctionnalités

- 🗺️ **Carte interactive du Maroc** (Folium + GeoPandas) — intensité de violence par région, thème sombre, popups riches (urbain/rural, types de violence)
- 📈 **8 graphiques statistiques** (Seaborn/Matplotlib) — lieu, contexte, âge, niveau scolaire, état civil… avec navigation détaillée
- 🎛️ **Générateur interactif** — combinez variable principale, filtre et catégorie pour créer barres ou camemberts à la demande
- 🖤 **Interface moderne** — fenêtre sans bordure, thème sombre, menu latéral rétractable

---

## 🗂️ Structure du projet

```
grb-10/
├── main.py                        # Point d'entrée — fenêtre principale
├── ui_interface.py                # Interface Qt Designer (PySide6)
├── ressources_rc.py               # Ressources compilées (icônes, images)
├── more.py                        # Modélisation orientée objet du dataset
├── graphe.py                      # Script de graphiques statiques
├── dataset.csv                    # Données VBG
├── maroc.geojson                  # Géométries des régions du Maroc
├── style.json                     # Style de la carte
├── requirements.txt               # Dépendances Python
├── Rapport_des_Taches_Projet.pdf  # Rapport du projet
└── RAPPORT_PYTHON[1].docx         # Rapport détaillé (Word)
```

---

## 📋 Jeu de données

| Colonne | Description |
|---|---|
| `Lieu` | Urbain / Rurale |
| `Region` | Région administrative du Maroc |
| `Age` | Tranche d'âge |
| `Etat` | État civil |
| `Type_activite` | Type d'activité professionnelle |
| `Contexte` | Contexte de l'incident (ex. conjugal) |
| `Type_violence` | Type de violence (physique, psychologique…) |
| `Niveau_scolaire` | Niveau d'éducation |

---

## ⚙️ Installation

```bash
# 1. Cloner le repo
git clone https://github.com/<votre-utilisateur>/grb-10.git
cd grb-10

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

**Prérequis** : Python 3.11+

---

## ▶️ Utilisation

```bash
python main.py
```

L'application démarre sur la **carte du Maroc**. Utilisez le menu latéral (☰) pour naviguer entre :

1. 🗺️ **Carte** — vue géographique des statistiques par région
2. 📊 **Graphes** — 8 visualisations statistiques prédéfinies
3. 🎛️ **Visualisation interactive** — graphiques personnalisés

---

## 🛠️ Stack technique

<div align="center">

| Domaine | Outils |
|---|---|
| Interface graphique | PySide6 |
| Cartographie | Folium, GeoPandas |
| Traitement de données | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |

</div>

---

## 👥 Auteurs

Projet réalisé dans le cadre d'un travail académique.

## 📄 Licence

Ce projet est destiné à un usage académique.

<div align="center">

⭐ *N'hésitez pas à mettre une étoile si ce projet vous a été utile !*

</div>
