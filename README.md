# MFEGSN - PDF RAG System with MCP Server

Système complet pour l'extraction de contenu PDF et recherche sémantique (RAG) avec serveur MCP.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yaniber/MFEGSN/blob/main/MFEGSN_Colab.ipynb)

## 🚀 Fonctionnalités

- **Upload de PDFs** : Interface web pour télécharger des fichiers PDF
- **Import Google Drive** : Importez vos PDFs directement depuis Google Drive via Google Colab
- **Extraction structurée** : Utilise Marker pour extraire texte, figures et références
- **Conversion Markdown** : Convertit automatiquement les PDFs en format Markdown
- **RAG (Retrieval-Augmented Generation)** : Indexation vectorielle avec ChromaDB
- **Serveur MCP** : Serveur Model Context Protocol pour intégration VSCode
- **Recherche sémantique** : Requêtes intelligentes sur les documents indexés
- **Google Colab** : Exécutez l'application dans le cloud sans installation locale

## 📋 Prérequis

### Option 1 : Google Colab (Le plus simple !)
- Un compte Google (gratuit)
- Aucune installation nécessaire

### Option 2 : Docker (Recommandé pour usage local)
- Docker
- Docker Compose

### Option 3 : Installation locale
- Python 3.8+
- pip

## 🔧 Installation

### ☁️ Option 1 : Google Colab (Démarrage Instantané)

**La méthode la plus rapide !** Aucune installation, exécution dans le cloud.

1. Cliquez sur le badge ci-dessus ou visitez :
   https://colab.research.google.com/github/yaniber/MFEGSN/blob/main/MFEGSN_Colab.ipynb

2. Suivez les instructions dans le notebook pour :
   - 📤 Uploader des PDFs ou les importer depuis Google Drive
   - 🔍 Extraire et indexer vos documents
   - 🔎 Effectuer des recherches sémantiques
   - 💾 Sauvegarder les résultats vers Google Drive ou GitHub

**Avantages :**
- ✅ Aucune installation locale nécessaire
- ✅ Import direct depuis Google Drive
- ✅ GPU gratuit pour un traitement plus rapide
- ✅ Sauvegarde facile vers Drive ou GitHub
- ✅ Partage facile avec d'autres utilisateurs

### 🐳 Option 2 : Avec Docker (Démarrage Rapide Local)

**C'est la méthode la plus simple !** Tout est configuré automatiquement avec persistance des données.

1. Cloner le repository :
```bash
git clone https://github.com/yaniber/MFEGSN.git
cd MFEGSN
```

2. Lancer l'application avec le script de démarrage rapide :
```bash
chmod +x start.sh
./start.sh
```

C'est tout ! L'application sera accessible sur http://localhost:8000

**Le script lance automatiquement deux services Docker :**
- 🌐 **Interface Web** : http://localhost:8000 (upload de PDFs, recherche)
- 🔧 **Serveur MCP** : Tourne en arrière-plan pour intégration VSCode/Roo Code

**Avantages :**
- ✅ Aucune installation de dépendances Python nécessaire
- ✅ Persistance automatique des données (bind mounts)
- ✅ Les données sont sauvegardées dans le repository (git push)
- ✅ Environnement isolé et reproductible

**Commandes utiles :**
```bash
./start.sh                        # Démarrer l'application
./stop.sh                         # Arrêter l'application
docker compose logs               # Voir les logs (ou docker-compose logs)
```

📖 **[Guide complet Docker](DOCKER.md)** pour plus de détails sur la configuration Docker, la persistance des données, et le dépannage.

**Note** : Le script `start.sh` détecte automatiquement si vous utilisez Docker Compose v1 (`docker-compose`) ou v2 (`docker compose`).

### 💻 Option 3 : Installation locale

1. Cloner le repository :
```bash
git clone https://github.com/yaniber/MFEGSN.git
cd MFEGSN
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Copier le fichier de configuration :
```bash
cp .env.example .env
```

## 🎯 Utilisation

### ☁️ Utilisation avec Google Colab

**Le moyen le plus simple pour commencer !**

1. **Ouvrir le notebook** : Cliquez sur le badge "Open in Colab" en haut de ce README

2. **Importer des PDFs** :
   - **Option A** : Montez Google Drive et importez depuis vos dossiers
   - **Option B** : Uploadez directement depuis votre ordinateur

3. **Traiter les documents** : Exécutez les cellules pour extraire et indexer

4. **Effectuer des recherches** : Interrogez vos documents avec des requêtes sémantiques

5. **Sauvegarder les résultats** :
   
   #### Sauvegarder vers Google Drive
   ```python
   # Dans le notebook Colab
   GDRIVE_OUTPUT_FOLDER = "/content/drive/MyDrive/MFEGSN_Outputs"
   # Exécutez la cellule de sauvegarde Drive
   ```
   
   #### Sauvegarder vers GitHub (nouvelle branche)
   ```python
   # Dans le notebook Colab
   # 1. Configurez Git avec vos informations
   # 2. Créez une nouvelle branche automatiquement
   # 3. Commitez vos outputs (PDFs, Markdown, base de données)
   # 4. Poussez vers GitHub avec un Personal Access Token
   ```
   
   **Instructions détaillées dans le notebook Colab** pour :
   - Créer un Personal Access Token GitHub
   - Pousser vers une nouvelle branche
   - Créer une Pull Request pour merger vos données

### 🌐 Interface Web

Lancer l'interface web pour uploader et gérer les PDFs :

```bash
python web_interface.py
```

Accéder à l'interface : http://localhost:8000

Fonctionnalités de l'interface :
- Upload de fichiers PDF (simple ou multiple)
- Extraction automatique et indexation
- Recherche sémantique dans les documents
- Statistiques de la collection

### Serveur MCP

Le serveur MCP permet l'intégration avec VSCode Copilot et Roo Code.

**Avec Docker (Recommandé)** : Le serveur MCP est **automatiquement lancé** en arrière-plan quand vous utilisez `./start.sh`. Aucune action supplémentaire nécessaire !

**Sans Docker (Installation locale)** :
1. Lancer le serveur MCP manuellement :
```bash
python mcp_server/server.py
```

#### Configuration VSCode

**Pour utiliser le serveur MCP avec VSCode**, vous avez deux options :

##### Option 1 : Avec Docker (Recommandé)
Le serveur MCP tourne déjà dans Docker ! Pour l'utiliser avec VSCode :

1. Assurez-vous que les containers Docker sont démarrés (`./start.sh`)
2. Ajoutez dans votre fichier `.vscode/mcp.json` :
   ```json
   {
     "mcpServers": {
       "pdf-rag-server": {
         "command": "docker",
         "args": ["exec", "-i", "pdf-rag-mcp", "python", "mcp_server/server.py"]
       }
     }
   }
   ```
   *Note: Le nom `pdf-rag-mcp` correspond au `container_name` défini dans docker-compose.yml. Si vous modifiez le nom du container, mettez à jour cette configuration. Vérifiez avec `docker compose ps`.*

3. **Alternative** : Accéder aux outils via l'interface web (http://localhost:8000)

##### Option 2 : Installation locale (sans Docker)
Ajouter dans votre fichier `.vscode/mcp.json` :

```json
{
  "mcpServers": {
    "pdf-rag-server": {
      "command": "python",
      "args": ["/chemin/vers/MFEGSN/mcp_server/server.py"]
    }
  }
}
```

### Outils MCP Disponibles

Le serveur MCP expose les outils suivants :

- **extract_pdf** : Extraire le contenu d'un PDF et convertir en Markdown
- **index_document** : Indexer un document dans la base RAG
- **query_documents** : Rechercher dans les documents indexés
- **update_document** : Mettre à jour un document existant
- **delete_document** : Supprimer un document
- **list_documents** : Lister tous les documents indexés
- **get_collection_stats** : Obtenir les statistiques de la collection
- **extract_all_pdfs** : Extraire et indexer tous les PDFs du dossier

### Utilisation Programmatique

```python
from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer

# Extraction PDF
extractor = PDFExtractor()
result = extractor.extract_pdf("pdfs/document.pdf")
print(f"Markdown saved to: {result['markdown_path']}")

# Indexation RAG
indexer = RAGIndexer()
indexer.index_document(
    doc_id="document",
    content=result["markdown"],
    metadata={"source": "document.pdf"}
)

# Recherche
results = indexer.query("What is the main topic?", n_results=5)
for doc, metadata in zip(results['results'], results['metadatas']):
    print(f"Document: {metadata['doc_id']}")
    print(f"Content: {doc[:200]}")
```

## 📁 Structure du Projet

```
MFEGSN/
├── pdfs/                    # Dossier pour les PDFs uploadés
├── markdown_outputs/        # Fichiers Markdown générés
├── chroma_db/              # Base de données vectorielle
├── src/
│   ├── pdf_extractor/      # Module d'extraction PDF
│   │   ├── __init__.py
│   │   └── extractor.py
│   └── rag_indexer/        # Module d'indexation RAG
│       ├── __init__.py
│       └── indexer.py
├── mcp_server/
│   └── server.py           # Serveur MCP
├── web_interface.py        # Interface web FastAPI
├── requirements.txt        # Dépendances Python
├── mcp_config.json        # Configuration MCP
└── README.md
```

## 🔍 API Endpoints (Interface Web)

- `GET /` - Page d'accueil avec interface upload
- `POST /upload` - Upload et traitement de PDFs
- `GET /query?q={query}&n={n}` - Recherche dans les documents
- `GET /documents` - Liste des documents indexés
- `GET /stats` - Statistiques de la collection
- `DELETE /documents/{doc_id}` - Suppression d'un document

## 🛠️ Technologies Utilisées

- **Marker** : Extraction de contenu PDF de haute qualité
- **PyMuPDF** : Fallback pour l'extraction PDF
- **ChromaDB** : Base de données vectorielle
- **Sentence Transformers** : Embeddings pour la recherche sémantique
- **FastAPI** : Interface web moderne
- **MCP (Model Context Protocol)** : Intégration avec les éditeurs de code

## 📝 Exemples

### Exemple 1 : Upload via l'interface web

1. Ouvrir http://localhost:8000
2. Cliquer sur "Choose File" et sélectionner un PDF
3. Cliquer sur "Upload & Extract"
4. Le document est automatiquement extrait et indexé

### Exemple 2 : Requête via l'interface

1. Entrer une question dans le champ de recherche
2. Cliquer sur "Search"
3. Les résultats pertinents s'affichent avec leur score de pertinence

### Exemple 3 : Utilisation avec VSCode Copilot

Une fois le serveur MCP configuré, vous pouvez interroger vos documents directement depuis VSCode :

```
@pdf-rag-server query_documents {"query": "Explain the methodology section"}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

Ce projet est open source.

## 🐛 Dépannage

### Problème : Marker n'est pas disponible
Si Marker ne peut pas être installé, le système utilisera PyMuPDF comme fallback.

### Problème : Port 8000 déjà utilisé
Modifier le port dans `web_interface.py` :
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Problème : Erreur d'import des modules
Assurez-vous d'être dans le bon environnement virtuel et que toutes les dépendances sont installées :
```bash
pip install -r requirements.txt
```