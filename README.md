# MFEGSN - PDF RAG System with MCP Server

Système complet pour l'extraction de contenu PDF et recherche sémantique (RAG) avec serveur MCP.

## 🚀 Fonctionnalités

- **Upload de PDFs** : Interface web pour télécharger des fichiers PDF
- **Extraction structurée** : Utilise Marker pour extraire texte, figures et références
- **Conversion Markdown** : Convertit automatiquement les PDFs en format Markdown
- **RAG (Retrieval-Augmented Generation)** : Indexation vectorielle avec ChromaDB
- **Serveur MCP** : Serveur Model Context Protocol pour intégration VSCode
- **Recherche sémantique** : Requêtes intelligentes sur les documents indexés

## 📋 Prérequis

### Option 1 : Docker (Recommandé)
- Docker
- Docker Compose

### Option 2 : Installation locale
- Python 3.8+
- pip

## 🔧 Installation

### 🐳 Option 1 : Avec Docker (Démarrage Rapide)

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

### 💻 Option 2 : Installation locale

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

### Interface Web

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

1. Lancer le serveur MCP :
```bash
python mcp_server/server.py
```

2. Configuration VSCode :

Ajouter dans votre configuration MCP VSCode (`.vscode/mcp_config.json` ou settings) :

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