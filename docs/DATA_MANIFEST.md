# Manifeste des Données (Power BI Ready)

## Fichiers Livrés

### 1. `data/offres_enriched.csv` (Table Principale)
- **Volume** : ~1780 offres.
- **Contenu** : Fusion de 3 sources (APEC Détails, APEC Listings, WTTJ).
- **Nettoyage** : Sauts de ligne supprimés pour garantir le chargement Power BI.

### 2. `data/skills_powerbi.csv` (Table Compétences)
- **Volume** : ~750 compétences détectées.
- **Usage** : À utiliser pour filtrer la table principale par compétence.

## ⚠️ Point d'Attention sur la Qualité des Données

Vous avez un volume "conséquent" d'offres (1780), mais elles n'ont pas toutes le même niveau de détail :

| Source | Nombre d'offres | Description présente ? | Analyse possible |
|--------|-----------------|------------------------|------------------|
| **APEC (Détails)** | ~370 | ✅ OUI | **Tout** (Compétences, Expérience, Salaire) |
| **WTTJ** | ~630 | ❌ NON (Titres seuls) | **Partielle** (Localisation, Entreprise, Titre) |
| **APEC (Listings)** | ~770 | ❌ NON (Titres seuls) | **Partielle** (Localisation, Entreprise, Titre) |

**Explication** : Les sources WTTJ et listings APEC n'ont récupéré que les titres et liens, sans le texte de l'annonce.
**Conséquence dans Power BI** : 
- Si vous faites un graphique par **Localisation**, vous aurez ~1780 données.
- Si vous filtrez par **Compétence "Python"**, vous ne verrez que les offres issues du lot "APEC Détails" (~370 offres max).

## Recommandation Power BI
Pour ne pas fausser vos analyses de compétences :
- Créez un filtre visuel ou une mesure pour exclure les offres où `description` est vide si vous analysez les technos.
- Gardez toutes les offres pour analyser la **répartition géographique** ou les **entreprises qui recrutent**.
