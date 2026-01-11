# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Installation

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

### Setup MCP in VSCode

1. Install the MCP extension in VSCode
2. Add the following to your VSCode settings (`.vscode/settings.json`):

```json
{
  "mcp.servers": {
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
