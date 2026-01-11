# Docker Quick Start - Guide de Démarrage Rapide

Ce document explique comment utiliser Docker pour lancer rapidement l'application MFEGSN avec persistance des données.

## 🎯 Avantages de l'utilisation de Docker

- **Installation Simplifiée** : Pas besoin d'installer Python ou les dépendances manuellement
- **Isolation** : L'application fonctionne dans un environnement isolé
- **Reproductibilité** : Fonctionne de manière identique sur tous les systèmes
- **Persistance des Données** : Toutes les données sont sauvegardées dans le repository via bind mounts

## 📦 Prérequis

- Docker (version 20.10+)
- Docker Compose (version 2.0+ ou 1.27+)

**Note sur Docker Compose** : Ce guide utilise la syntaxe moderne `docker compose` (v2), mais le script `start.sh` est compatible avec les deux versions :
- Docker Compose v2 : `docker compose` (intégré à Docker Desktop)
- Docker Compose v1 : `docker-compose` (installation séparée)

Les commandes peuvent être utilisées de manière interchangeable selon votre installation.

### Installation de Docker

- **Linux** : `curl -fsSL https://get.docker.com | sh`
- **macOS** : [Docker Desktop pour Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Windows** : [Docker Desktop pour Windows](https://docs.docker.com/desktop/install/windows-install/)

## 🚀 Démarrage Rapide

### Lancer l'application

```bash
# Cloner le repository
git clone https://github.com/yaniber/MFEGSN.git
cd MFEGSN

# Lancer l'application avec un seul script
chmod +x start.sh
./start.sh
```

Le script `start.sh` va automatiquement :
1. ✓ Vérifier que Docker et Docker Compose sont installés
2. ✓ Créer les dossiers nécessaires (pdfs, markdown_outputs, chroma_db)
3. ✓ Créer le fichier .env si nécessaire
4. ✓ Construire les images Docker
5. ✓ Démarrer les containers

### Accéder à l'application

Une fois démarrée, l'application est accessible sur :
- **Interface Web** : http://localhost:8000
- **MCP Server** : Tourne en arrière-plan pour l'intégration VSCode

### Arrêter l'application

```bash
./stop.sh
```

## 💾 Persistance des Données

### Bind Mounts

Les dossiers suivants du repository sont montés dans les containers Docker :

| Dossier Local | Dossier Container | Description |
|---------------|-------------------|-------------|
| `./pdfs` | `/app/pdfs` | Fichiers PDF uploadés |
| `./markdown_outputs` | `/app/markdown_outputs` | Fichiers Markdown générés |
| `./chroma_db` | `/app/chroma_db` | Base de données vectorielle |

### Sauvegarde avec Git

Grâce aux bind mounts, **toutes les modifications sont immédiatement reflétées dans votre repository local**. Pour sauvegarder vos données :

```bash
# Ajouter les fichiers (selon votre .gitignore)
git add pdfs markdown_outputs chroma_db

# Commiter les changements
git commit -m "Mise à jour des données"

# Pousser vers GitHub
git push
```

**Note** : Par défaut, le `.gitignore` ignore les fichiers PDF et Markdown individuels pour éviter de gros commits. Si vous souhaitez les inclure, modifiez le `.gitignore`.

## 🔧 Commandes Utiles

**Note** : Remplacez `docker compose` par `docker-compose` si vous utilisez Docker Compose v1.

### Voir les logs

```bash
# Tous les containers
docker compose logs

# Suivi en temps réel
docker compose logs -f

# Un container spécifique
docker compose logs pdf-rag-web
docker compose logs pdf-rag-mcp
```

### Vérifier l'état des containers

```bash
docker compose ps
```

### Redémarrer les services

```bash
docker compose restart
```

### Reconstruire les images

```bash
docker compose up -d --build
```

### Accéder à un container

```bash
# Shell interactif dans le container web
docker compose exec pdf-rag-web bash

# Shell interactif dans le container MCP
docker compose exec pdf-rag-mcp bash
```

### Nettoyer les données

```bash
# Arrêter et supprimer les containers
docker compose down

# Supprimer aussi les volumes (ATTENTION : perte de données si non sauvegardées)
docker compose down -v

# Supprimer les images
docker compose down --rmi all
```

## 🏗️ Architecture Docker

### Services

Le fichier `docker-compose.yml` définit deux services :

1. **pdf-rag-web** : Interface web FastAPI (port 8000)
2. **pdf-rag-mcp** : Serveur MCP pour l'intégration VSCode

### Image Docker

L'image est construite à partir du `Dockerfile` qui :
- Utilise Python 3.11-slim comme base
- Installe gcc et g++ pour les dépendances C
- Installe toutes les dépendances Python
- Configure le répertoire de travail `/app`
- Expose le port 8000

## 🔍 Résolution de Problèmes

### Le script start.sh échoue

**Problème** : "Docker is not installed"
```bash
# Vérifier l'installation de Docker
docker --version
docker compose version
```

**Problème** : "Docker daemon is not running"
```bash
# Démarrer le daemon Docker (Linux)
sudo systemctl start docker

# Ou lancer Docker Desktop (Mac/Windows)
```

### Les containers ne démarrent pas

```bash
# Voir les erreurs
docker compose logs

# Reconstruire complètement
docker compose down
docker compose up -d --build
```

### Port 8000 déjà utilisé

Modifier le fichier `docker-compose.yml` :
```yaml
services:
  pdf-rag-web:
    ports:
      - "8001:8000"  # Changez 8000 par un autre port
```

### Problèmes de permissions

Sur Linux, si vous avez des problèmes de permissions avec les fichiers créés par Docker :

```bash
# Changer le propriétaire des fichiers
sudo chown -R $USER:$USER pdfs markdown_outputs chroma_db
```

## 📚 Ressources Supplémentaires

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [README principal](README.md)
- [Guide Quick Start](QUICKSTART.md)

## 🤝 Contribution

Si vous rencontrez des problèmes ou avez des suggestions pour améliorer le démarrage Docker, n'hésitez pas à ouvrir une issue sur GitHub.
