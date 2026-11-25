# Gestion des incidents informatiques

Application web (Flask + SQLite) permettant de signaler et suivre les incidents
informatiques d'un établissement : ajout, liste, détails, changement de statut et suppression.
Le projet met en place une chaîne DevOps complète : Git/GitHub, Docker, Docker Compose,
GitHub Actions (CI/CD) et publication d'image dans GHCR.

## Auteurs
- PRENOM NOM 1 (@github-1)
- PRENOM NOM 2 (@github-2)

## Structure du projet
```
gestion-incidents/
├── app/                    # Application Flask (routes, base SQLite, templates HTML)
├── tests/                  # Tests automatisés (pytest)
├── Dockerfile              # Construction de l'image
├── compose.yaml            # Lancement local (build + volume)
├── compose.deploy.yaml     # Déploiement depuis l'image GHCR
├── requirements.txt
└── .github/workflows/
    ├── ci.yml              # Intégration continue
    └── cd.yml              # Publication de l'image dans GHCR
```

## Lancer l'application en local (sans Docker)
```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Ouvrir http://localhost:5000

## Lancer les tests
```bash
pytest -v
```

## Lancer avec Docker Compose
```bash
docker compose up -d --build
docker compose ps
docker compose logs
docker compose down        # ajouter -v pour supprimer aussi les données
```
Les incidents sont conservés dans le volume `incidents_data`.

## Pipelines GitHub Actions
- **CI (`ci.yml`)** : déclenché sur push et Pull Request vers `main`. Installe les
  dépendances, exécute les tests, vérifie `compose.yaml` et construit l'image.
- **CD (`cd.yml`)** : déclenché sur push vers `main`. Exécute les tests, puis (si OK) publie
  l'image dans GHCR avec les tags `latest` et le SHA du commit.

## Déploiement à partir de l'image publiée
Remplacer `VOTRE_UTILISATEUR` dans `compose.deploy.yaml`, puis :
```bash
docker compose -f compose.deploy.yaml pull
docker compose -f compose.deploy.yaml up -d
docker compose -f compose.deploy.yaml logs
```
Mise à jour après un nouveau push : refaire `pull` puis `up -d`.

## Routes principales
| Route | Méthode | Rôle |
|---|---|---|
| `/` | GET | Liste des incidents |
| `/incidents/nouveau` | GET, POST | Ajouter un incident |
| `/incidents/<id>` | GET | Détails d'un incident |
| `/incidents/<id>/statut` | POST | Modifier le statut |
| `/incidents/<id>/supprimer` | POST | Supprimer l'incident |
| `/health` | GET | Vérification de l'état |
