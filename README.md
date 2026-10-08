#  Web Scraping & Data Engineering Pipeline

Ce dépôt présente un double volet : d'une part, la réponse aux **briefs de formation Data Engineer (Simplon)** axés sur les fondamentaux du web scraping et l'éthique de la collecte ; d'autre part, un projet personnel et opérationnel de veille automatisée (**Nexus Pipeline — Data Radar**).

---

##  1. Le Brief Simplon : Collecter des données via web scraping

### Objectifs pédagogiques
* **Maîtriser les techniques fondamentales** du crawling et du scraping avec Python (`requests`, `BeautifulSoup`, `pandas`).
* **Comprendre et respecter l'éthique du web** : analyse des codes de réponse HTTP (403, 429), gestion des en-têtes et intégration d'un `User-Agent` explicite avec moyen de contact.
* **Interpréter les fichiers `robots.txt`** pour identifier les zones autorisées et interdire l'accès aux espaces restreints.
* **Industrialiser la collecte** sur des sites structurés (pagination, fiches de détail, relations entre entités et normalisation des données).

### Réalisations et Notebooks associés
* **`1-scraping-classique.ipynb`** : Crawling de 1 000 livres sur *Books to Scrape*, extraction des prix, notes et catégories, et génération d'un dataset propre (`livres.csv`).
* **`2-user-agent-et-robots.ipynb`** : Expérimentation sur le blocage des requêtes anonymes (comparaison Wikipedia / livres) et intégration d'une fonction de requête polie avec temporisation (`time.sleep`) pour éviter la surcharge des serveurs.
* **`3-mission-adaptation.ipynb`** : Adaptation autonome sur *Quotes to Scrape* (extraction de citations et association relationnelle avec les fiches biographiques des auteurs sans redondance de requêtes, calcul des tops auteurs et tags).

---

##  2. Projet Avancé : Nexus Pipeline — Data Radar (Hellowork)

### Objectifs et Contexte
Construire un pipeline de données automatisé et industrialisé pour collecter, analyser et restituer les offres d'emploi de **Data Engineer à Toulouse** (`l=Toulouse+31000`) publiées sur **Hellowork**.

### Fonctionnalités Clés
* **Scraping intelligent & résilient** : Extraction granulaire des fiches d'offres incluant les salaires, les badges de métadonnées (type de contrat, expérience) et les technologies officielles recherchées (« À noter sur ce job »).
* **Dashboard Interactif (`offres_toulouse.html`)** : Restitution visuelle moderne aux couleurs Tech / Data, dotée d'un **mode sombre / clair interactif** en JavaScript et de liens directs vers les annonces d'origine.
* **Orchestration avec Apache Airflow** :
  * Déploiement local conteneurisé via Docker Compose (`apache/airflow:2.8.1-python3.10` avec `LocalExecutor` et backend PostgreSQL).
  * Automatisation des exécutions (planification `@daily`) et écriture des rapports dynamiques dans un volume partagé.

---

##  Structure du Dépôt

```text
├── dags/                          # Fichiers DAGs pour Apache Airflow
│   └── hellowork_dag.py           # Pipeline orchestré de veille Hellowork
├── notebooks/                     # Notebooks Jupyter des briefs et ateliers Simplon
│   ├── 1-scraping-classique.ipynb 
│   ├── 2-user-agent-et-robots.ipynb 
│   └── 3-mission-adaptation.ipynb 
├── docker-compose.yaml            # Infrastructure Docker (Airflow + PostgreSQL)
├── hellowork.py                   # Script de scraping autonome (Hellowork)
├── offres_toulouse.html           # Tableau de bord interactif généré (Dark/Light)
└── .gitignore                     # Règles d'exclusion Git (venv, logs, csv)
```

## Lancement rapide

### Cloner le repo
```
git clone [https://github.com/GregoryElBajoury/web-scrapping.git](https://github.com/GregoryElBajoury/web-scrapping.git)
cd web-scrapping
```

### Lancer l'orchestrateur Airflow :


```
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up -d
```

### Interface Airflow : http://localhost:8080 (Identifiants : airflow / airflow)

Auteur
Grégory El Bajoury — Data Engineer | Devops Engineer
Nexus DevOps





