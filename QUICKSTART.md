# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Docker (Recommandé - Plus Rapide!)

**Avec Docker, l'application web ET le serveur MCP sont lancés automatiquement !**

#### 1. Prérequis
- Docker installé ([Installation Docker](https://docs.docker.com/get-docker/))
- Docker Compose installé ([Installation Docker Compose](https://docs.docker.com/compose/install/))

#### 2. Lancement

```bash
# Clone the repository
git clone https://github.com/yaniber/MFEGSN.git
cd MFEGSN

# Start with Docker
chmod +x start.sh
./start.sh
```

Ouvrez votre navigateur : **http://localhost:8000**

**✅ Deux services Docker sont maintenant en cours d'exécution :**
- 🌐 **Interface Web** : http://localhost:8000 (upload, recherche de documents)
- 🔧 **Serveur MCP** : Arrière-plan (intégration VSCode Copilot/Roo Code)

#### 3. Arrêter l'application

```bash
./stop.sh
```

#### 4. Persistance des données

Toutes les données sont automatiquement sauvegardées dans votre repository grâce aux bind mounts :
- `./pdfs` - Vos fichiers PDF uploadés
- `./markdown_outputs` - Les fichiers Markdown générés
- `./chroma_db` - La base de données vectorielle

Pour sauvegarder vos données :
```bash
git add pdfs markdown_outputs chroma_db
git commit -m "Mise à jour des données"
git push
```

**Note :** Tous les fichiers de données (PDFs, Markdown, base de données vectorielle) sont suivis par git. Cela permet de sauvegarder l'intégralité de vos données et documents traités.

---

### Option 2: Installation Locale

#### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yaniber/MFEGSN.git
cd MFEGSN

# Run the setup script (Linux/Mac)
chmod +x setup.sh
./setup.sh

# Or on Windows
setup.bat
```

### 2. Start the Web Interface

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Start the web server
python web_interface.py
```

Open your browser to: **http://localhost:8000**

### 3. Upload Your First PDF

1. Click "Choose File" on the web interface
2. Select a PDF file
3. Click "Upload & Extract"
4. Wait for the extraction to complete

### 4. Query Your Documents

1. Enter a question in the search box
2. Click "Search"
3. View the relevant results with similarity scores

## 🔌 VSCode Integration with MCP

### Setup MCP in VSCode (Docker Version)

If you're using the Docker setup (recommended), the MCP server is already running!

1. Install the MCP extension in VSCode
2. Add the following to your VSCode MCP configuration file (`.vscode/mcp.json`):

**Option A - Via Docker exec (Recommended for Docker setup):**
```json
{
  "mcpServers": {
    "pdf-rag-server": {
      "command": "docker",
      "args": ["exec", "-i", "pdf-rag-mcp", "python", "mcp_server/server.py"],
      "env": {}
    }
  }
}
```
*Note: Le container `pdf-rag-mcp` doit être en cours d'exécution. Lancez `./start.sh` avant de démarrer VSCode. Vérifiez avec `docker compose ps`.*

**Option B - Direct Python (for local installation):**
```json
{
  "mcpServers": {
    "pdf-rag-server": {
      "command": "python",
      "args": ["/absolute/path/to/MFEGSN/mcp_server/server.py"],
      "env": {}
    }
  }
}
```

3. Restart VSCode
4. The MCP tools will now be available in Copilot Chat

### Using MCP Tools in VSCode

Open Copilot Chat and use commands like:

```
@pdf-rag-server extract_pdf {"pdf_path": "pdfs/document.pdf"}
@pdf-rag-server query_documents {"query": "What is the main topic?"}
@pdf-rag-server list_documents
```

## 📝 Common Tasks

### Extract All PDFs in a Directory

```python
python example_usage.py
```

### Query from Command Line

```python
from src.rag_indexer.indexer import RAGIndexer

indexer = RAGIndexer()
results = indexer.query("your question here", n_results=5)

for doc in results['results']:
    print(doc)
```

### Update an Indexed Document

```python
from src.rag_indexer.indexer import RAGIndexer

indexer = RAGIndexer()
indexer.update_document("doc_id", "new content")
```

## 🛠️ Troubleshooting

### Dependencies Not Installed

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

Change the port in `web_interface.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

### Marker Installation Issues

If Marker fails to install, the system will automatically fall back to PyMuPDF. You'll see a warning in the logs, but extraction will continue to work.

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [example_usage.py](example_usage.py) script for more examples
- Check the API documentation at http://localhost:8000/docs when the web server is running
