# Guide d'intégration Power BI : Analyse des Offres d'Emploi

Ce guide explique comment importer les données et utiliser le script Python pour visualiser les compétences.

## 1. Importation des Données (Étape OBLIGATOIRE)

Vous avez deux fichiers CSV prêts à l'emploi. **Pour commencer, chargez uniquement le fichier principal.**

### Fichier Principal : `data/offres_enriched.csv`
C'est le fichier qui contient TOUTES les informations :
*   Titre, Entreprise, Contrat, Localisation
*   Colonnes pour chaque compétence (Python, SQL, etc.) avec 1 (oui) ou 0 (non).

**Procédure dans Power BI Desktop :**
1.  Cliquez sur **"Obtenir les données"** > **"Texte/CSV"**.
2.  Sélectionnez le fichier `data/offres_enriched.csv`.
3.  Cliquez sur **"Transformer les données"** pour vérifier que les colonnes sont bien détectées.
4.  Une fois chargé, vous pouvez créer vos graphiques (ex: diagramme en barres des Contrats).

---

## 2. (OPTIONNEL) Le Script Python pour le Nuage de Mots

**À quoi sert ce script ?**
Power BI ne propose pas de "Nuage de Mots" par défaut. Le fichier `scripts/powerbi_visuals.py` contient du code Python pour **générer ce graphique spécifique à l'intérieur de Power BI**.

**Si vous ne voulez pas de Nuage de Mots, IGNOREZ CETTE SECTION.**

**Comment l'utiliser ?**
1.  Dans Power BI, cliquez sur l'icône **Visuel Python** (symbole `Py`) dans le volet *Visualisations*.
2.  Glissez les champs (ex: `description`) dans la zone "Valeurs" du visuel.
3.  Un éditeur de script va s'ouvrir en bas de la fenêtre Power BI.
4.  **Copiez tout le contenu** du fichier `scripts/powerbi_visuals.py`.
5.  **Collez-le** dans l'éditeur de script Power BI.
6.  Cliquez sur la flèche "Exécuter" en haut de l'éditeur de script.
