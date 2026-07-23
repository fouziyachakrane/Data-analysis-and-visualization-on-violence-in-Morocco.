import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
data = pd.read_csv('dataset.csv')

# Configurer le style général
sns.set(style="whitegrid")

# 1. Lieux & Type d'activité (diagramme en barres empilé)
plt.figure(figsize=(4, 3))
sns.countplot(data=data, x='Lieu', hue='Type_activite', palette='Set2')
plt.title("Distribution des types d'activité selon les lieux", fontsize=14)
plt.xlabel("Lieu", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.legend(title="Type d'activité")
plt.tight_layout()
plt.show()

# 2. Contexte & Type de violence
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Contexte', hue='Type_violence', palette='Set3')
plt.title("Type de violence selon le contexte", fontsize=14)
plt.xlabel("Contexte", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.legend(title="Type de violence")
plt.tight_layout()
plt.show()

# 3. Niveau scolaire & Type d'activité
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Niveau_scolaire', hue='Type_activite', palette='coolwarm')
plt.title("Type d'activité selon le niveau scolaire", fontsize=14)
plt.xlabel("Niveau scolaire", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.legend(title="Type d'activité", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 4. Age & Type de violence
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Age', hue='Type_violence', palette='viridis')
plt.title("Type de violence selon l'âge", fontsize=14)
plt.xlabel("Tranche d'âge", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.legend(title="Type de violence")
plt.tight_layout()
plt.show()

# 5. État & Contexte
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Etat', hue='Contexte', palette='pastel')
plt.title("Contexte selon l'état civil", fontsize=14)
plt.xlabel("État civil", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.legend(title="Contexte", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 6. Proportion des lieux (circulaire)
lieu_counts = data['Lieu'].value_counts()
plt.figure(figsize=(8, 8))
plt.bar(lieu_counts.index, lieu_counts.values, color=sns.color_palette("Set2"))
plt.title("Proportion des lieux (barres)", fontsize=14)
plt.xlabel("Lieu", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.tight_layout()
plt.show()

# 7. Proportion des cas selon les régions (circulaire)
region_counts = data['Region'].value_counts()
plt.figure(figsize=(8, 8))
region_counts.plot.pie(autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel"))
plt.title("Proportion des cas selon les régions", fontsize=14)
plt.ylabel("")
plt.tight_layout()
plt.show()

# 8. Distribution des types de violence (histogramme)
violence_counts = data['Type_violence'].value_counts()
plt.figure(figsize=(8, 6))
plt.bar(violence_counts.index, violence_counts.values, color=sns.color_palette("coolwarm"))
plt.title("Distribution des types de violence (barres)", fontsize=14)
plt.xlabel("Type de violence", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.tight_layout()
plt.show()

# Suggestions pour le meilleur type de graphe :
# - Barres empilées pour visualiser les distributions par catégorie.
# - Utiliser des couleurs contrastées pour une meilleure lisibilité.
