# Tâches : Enrichissement des Données Emploi

Objectif : Passer d'une liste simple d'offres à une base de données riche (Compétences, Expérience, Outils) pour analyse Power BI.

- [ ] **Phase 1 : Amélioration des Scrapers (Récupération du Contenu)**
    - [ ] Modifier `scraper_apec.py` pour appeler l'API "détail" pour chaque offre. <!-- id: 0 -->
    - [ ] Modifier `scraper_wttj.py` pour visiter chaque page d'offre et extraire la description. <!-- id: 1 -->
    - [ ] Tester les scrapers sur un petit échantillon (5-10 offres) pour valider. <!-- id: 2 -->
    - [ ] Lancer le scraping complet (avec délais pour éviter le blocage). <!-- id: 3 -->

- [ ] **Phase 2 : Extraction d'Intelligence (NLP/Regex)**
    - [ ] Créer `scripts/extract_skills.py`. <!-- id: 4 -->
    - [ ] Définir les dictionnaires de compétences (Langages, Outils, Soft Skills, Diplômes). <!-- id: 5 -->
    - [ ] Implémenter l'extraction des années d'expérience (Regex). <!-- id: 6 -->
    - [ ] Générer `data/offres_enriched.csv` (Offres + colonnes compétences). <!-- id: 7 -->
    - [ ] Générer `data/skills_long.csv` (Format "Un skill par ligne" pour Power BI). <!-- id: 8 -->

- [ ] **Phase 3 : Validation & Nettoyage Final**
    - [ ] Vérifier la qualité des extractions (Faux positifs ?). <!-- id: 9 -->
    - [ ] Fusionner avec le nettoyage existant (Villes, Contrats). <!-- id: 10 -->
    - [ ] Produire le jeu de données final pour Power BI. <!-- id: 11 -->
