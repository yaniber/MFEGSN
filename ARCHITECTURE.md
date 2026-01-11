# MFEGSN - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Web Interface  │  MCP Server     │  CLI / Python API       │
│  (FastAPI)      │  (stdio)        │  (Direct Import)        │
└────────┬────────┴────────┬────────┴────────┬────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │      Application Layer             │
         ├────────────────┬──────────────────┤
         │ PDF Extractor  │  RAG Indexer     │
         │ (Marker)       │  (ChromaDB)      │
         └────────┬───────┴────────┬─────────┘
                  │                │
         ┌────────┴────────────────┴─────────┐
         │         Data Layer               │
         ├──────────────────────────────────┤
         │  PDFs  │ Markdown │ Vector DB    │
         │ Folder │  Folder  │ (ChromaDB)   │
         └──────────────────────────────────┘
```

## Components

### 1. PDF Extractor (`src/pdf_extractor/`)

**Purpose**: Extract structured content from PDF files

**Technologies**:
- Primary: Marker (high-quality PDF extraction)
- Fallback: PyMuPDF (if Marker unavailable)

**Features**:
- Text extraction
- Figure detection
- Reference parsing
- Metadata extraction
- Markdown conversion

**Key Methods**:
```python
extract_pdf(pdf_path) -> Dict
extract_all_pdfs() -> List[Dict]
```

### 2. RAG Indexer (`src/rag_indexer/`)

**Purpose**: Vector database for semantic search

**Technologies**:
- ChromaDB (vector database)
- Sentence Transformers (embeddings)

**Features**:
- Document chunking (with overlap)
- Vector embeddings
- Semantic search
- CRUD operations on documents
- Collection statistics

**Key Methods**:
```python
index_document(doc_id, content, metadata)
query(query_text, n_results)
update_document(doc_id, content)
delete_document(doc_id)
list_documents()
```

### 3. MCP Server (`mcp_server/`)

**Purpose**: Model Context Protocol server for VSCode integration

**Protocol**: MCP (Model Context Protocol)
**Communication**: stdio

**Available Tools**:
1. `extract_pdf` - Extract and optionally index a PDF
2. `index_document` - Index arbitrary text content
3. `query_documents` - Semantic search across indexed docs
4. `update_document` - Update existing document
5. `delete_document` - Remove document from index
6. `list_documents` - List all indexed documents
7. `get_collection_stats` - Get database statistics
8. `extract_all_pdfs` - Batch process all PDFs

**Usage in VSCode**:
```
@pdf-rag-server extract_pdf {"pdf_path": "pdfs/paper.pdf"}
@pdf-rag-server query_documents {"query": "methodology"}
```

### 4. Web Interface (`web_interface.py`)

**Purpose**: Browser-based UI for PDF upload and querying

**Technology**: FastAPI + HTML/JavaScript

**Endpoints**:
- `GET /` - Home page with upload form
- `POST /upload` - Upload and process PDFs
- `GET /query` - Search documents
- `GET /documents` - List indexed documents
- `GET /stats` - Collection statistics
- `DELETE /documents/{doc_id}` - Delete document

**Features**:
- Multi-file upload
- Real-time search
- Results with relevance scores
- Collection management

## Data Flow

### PDF Upload Flow
```
1. User uploads PDF
   ↓
2. Save to pdfs/ directory
   ↓
3. PDFExtractor processes file
   ↓
4. Convert to Markdown
   ↓
5. Save to markdown_outputs/
   ↓
6. RAGIndexer chunks content
   ↓
7. Generate embeddings
   ↓
8. Store in ChromaDB
```

### Query Flow
```
1. User submits query
   ↓
2. Query converted to embedding
   ↓
3. Vector similarity search
   ↓
4. ChromaDB returns top-k results
   ↓
5. Results with relevance scores
   ↓
6. Display to user
```

## Directory Structure

```
MFEGSN/
├── src/
│   ├── pdf_extractor/          # PDF processing module
│   │   ├── __init__.py
│   │   └── extractor.py        # PDFExtractor class
│   └── rag_indexer/            # RAG/vector DB module
│       ├── __init__.py
│       └── indexer.py          # RAGIndexer class
├── mcp_server/
│   └── server.py               # MCP protocol server
├── pdfs/                       # PDF storage (uploads)
├── markdown_outputs/           # Extracted markdown files
├── chroma_db/                  # Vector database (persistent)
├── .vscode/
│   └── mcp.json               # VSCode MCP config
├── web_interface.py           # FastAPI web app
├── example_usage.py           # Example Python script
├── test_system.py             # Test suite
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image
├── docker-compose.yml         # Docker Compose config
├── setup.sh / setup.bat       # Setup scripts
├── README.md                  # Full documentation
└── QUICKSTART.md             # Quick start guide
```

## Configuration

### Environment Variables

Create a `.env` file:
```bash
PDF_DIR=pdfs
MARKDOWN_OUTPUT_DIR=markdown_outputs
CHROMA_DB_DIR=./chroma_db
WEB_PORT=8000
```

### VSCode MCP Configuration

`.vscode/mcp.json`:
```json
{
  "mcpServers": {
    "pdf-rag-server": {
      "command": "python",
      "args": ["${workspaceFolder}/mcp_server/server.py"]
    }
  }
}
```

## Deployment Options

### 1. Local Development
```bash
python web_interface.py
```

### 2. Docker
```bash
docker-compose up
```

### 3. MCP Server (VSCode)
Configure in VSCode settings and restart

## Security Considerations

1. **Input Validation**: PDF files are validated before processing
2. **Path Traversal**: File paths are sanitized
3. **Resource Limits**: Consider adding limits for large PDFs
4. **Authentication**: Add authentication for production use
5. **CORS**: Configure CORS for web interface in production

## Performance Optimization

1. **Chunking Strategy**: Configurable chunk size and overlap
2. **Batch Processing**: Process multiple PDFs in parallel
3. **Caching**: ChromaDB provides built-in caching
4. **Async Operations**: FastAPI handles concurrent requests

## Extensibility

### Adding New Extractors
Extend `PDFExtractor` class:
```python
def extract_with_custom_tool(self, pdf_file):
    # Custom extraction logic
    pass
```

### Custom Embeddings
Modify `RAGIndexer` to use different embedding models:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('your-model')
```

### Additional MCP Tools
Add new tools to `mcp_server/server.py`:
```python
@server.list_tools()
async def list_tools():
    return [
        # ... existing tools
        Tool(name="your_tool", ...)
    ]
```

## Troubleshooting

### Common Issues

1. **Marker Installation Fails**: System falls back to PyMuPDF
2. **Port Already in Use**: Change port in `web_interface.py`
3. **Import Errors**: Ensure virtual environment is activated
4. **Database Locked**: Check ChromaDB directory permissions

### Logs

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

Potential improvements:
- [ ] Support for more document formats (DOCX, HTML, etc.)
- [ ] Advanced filtering and faceted search
- [ ] User authentication and multi-tenancy
- [ ] Real-time PDF streaming
- [ ] OCR for scanned PDFs
- [ ] Automatic language detection
- [ ] Export to various formats
- [ ] API rate limiting
- [ ] Background job processing
- [ ] Admin dashboard

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python test_system.py`
5. Submit a pull request

## License

Open source - see LICENSE file for details.
