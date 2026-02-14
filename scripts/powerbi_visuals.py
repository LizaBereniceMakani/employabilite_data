# Script pour Visual Python dans Power BI
# Ce script permet de générer un Nuage de Mots (WordCloud) des compétences et titres

# Pré-requis :
# 1. Installer python et les librairies : pip install pandas matplotlib wordcloud
# 2. Dans Power BI : Fichier > Options > Script Python > Définir le répertoire d'installation Python

# COPIER-COLLER CE CODE DANS L'ÉDITEUR DE SCRIPT PYTHON DE L'ÉLÉMENT VISUEL

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 'dataset' contient les données d'entrée du visuel Power BI
# Assurez-vous d'avoir glissé les champs 'Competence' ou 'titre' dans le visual
df = dataset

# Concaténer tout le texte
text = " ".join(desc for desc in df['Competence'].astype(str))

# Générer le nuage
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Afficher
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
