# Complete Usage Examples

## Table of Contents
1. [Basic PDF Extraction](#basic-pdf-extraction)
2. [RAG Indexing and Querying](#rag-indexing-and-querying)
3. [Web Interface](#web-interface)
4. [MCP Server](#mcp-server)
5. [Advanced Usage](#advanced-usage)

---

## Basic PDF Extraction

### Extract a Single PDF

```python
from src.pdf_extractor.extractor import PDFExtractor

# Initialize extractor
extractor = PDFExtractor()

# Extract PDF
result = extractor.extract_pdf("pdfs/research_paper.pdf")

print(f"Markdown: {result['markdown_path']}")
print(f"Figures: {len(result['figures'])}")
print(f"References: {len(result['references'])}")
print(f"Content preview: {result['markdown'][:200]}...")
```

### Extract All PDFs in Directory

```python
from src.pdf_extractor.extractor import PDFExtractor

extractor = PDFExtractor()
results = extractor.extract_all_pdfs()

for result in results:
    print(f"Processed: {result['source_pdf']}")
    print(f"  → {result['markdown_path']}")
```

---

## RAG Indexing and Querying

### Index Documents

```python
from src.rag_indexer.indexer import RAGIndexer

# Initialize indexer
indexer = RAGIndexer()

# Index a document
content = """
Your document content here.
This can be the extracted markdown from a PDF.
"""

indexer.index_document(
    doc_id="my_document",
    content=content,
    metadata={
        "author": "John Doe",
        "year": 2024,
        "topic": "AI"
    }
)
```

### Query Documents

```python
from src.rag_indexer.indexer import RAGIndexer

indexer = RAGIndexer()

# Simple query
results = indexer.query("What is machine learning?", n_results=5)

for i, (doc, metadata, distance) in enumerate(zip(
    results['results'],
    results['metadatas'],
    results['distances']
)):
    relevance = 1 - distance
    print(f"Result {i+1} (relevance: {relevance:.3f})")
    print(f"Document: {metadata['doc_id']}")
    print(f"Content: {doc[:200]}...")
    print()
```

### Update a Document

```python
indexer.update_document(
    doc_id="my_document",
    content="Updated content here",
    metadata={"updated": True}
)
```

### Delete a Document

```python
indexer.delete_document("my_document")
```

### List All Documents

```python
docs = indexer.list_documents()
print(f"Indexed documents: {docs}")
```

### Get Collection Statistics

```python
stats = indexer.get_collection_stats()
print(f"Total documents: {stats['total_documents']}")
print(f"Total chunks: {stats['total_chunks']}")
```

---

## Web Interface

### Start the Server

```bash
python web_interface.py
```

### Using the API

#### Upload a PDF

```python
import requests

files = {'files': open('document.pdf', 'rb')}
response = requests.post('http://localhost:8000/upload', files=files)
print(response.json())
```

#### Query Documents

```python
import requests

response = requests.get(
    'http://localhost:8000/query',
    params={'q': 'machine learning', 'n': 5}
)
results = response.json()
print(results)
```

#### List Documents

```python
import requests

response = requests.get('http://localhost:8000/documents')
print(response.json())
```

#### Get Statistics

```python
import requests

response = requests.get('http://localhost:8000/stats')
print(response.json())
```

#### Delete a Document

```python
import requests

response = requests.delete('http://localhost:8000/documents/my_doc')
print(response.json())
```

---

## MCP Server

### Start the MCP Server

```bash
python mcp_server/server.py
```

### Configure in VSCode

Add to `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "pdf-rag-server": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server/server.py"]
    }
  }
}
```

### Using MCP Tools in VSCode

```
# Extract a PDF
@pdf-rag-server extract_pdf {"pdf_path": "pdfs/paper.pdf", "index": true}

# Query documents
@pdf-rag-server query_documents {"query": "What is the methodology?", "n_results": 5}

# List documents
@pdf-rag-server list_documents

# Get statistics
@pdf-rag-server get_collection_stats

# Update a document
@pdf-rag-server update_document {"doc_id": "paper", "content": "new content"}

# Delete a document
@pdf-rag-server delete_document {"doc_id": "paper"}

# Extract all PDFs
@pdf-rag-server extract_all_pdfs {"index": true}
```

---

## Advanced Usage

### Complete Workflow: PDF to Queryable Database

```python
from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer
from pathlib import Path

# Initialize
extractor = PDFExtractor()
indexer = RAGIndexer()

# Step 1: Extract PDF
pdf_path = "pdfs/research_paper.pdf"
result = extractor.extract_pdf(pdf_path)

print(f"✓ Extracted {Path(pdf_path).name}")
print(f"  Pages: {result['metadata'].get('pages', 'N/A')}")
print(f"  References: {len(result['references'])}")

# Step 2: Index the content
doc_id = Path(pdf_path).stem
indexer.index_document(
    doc_id=doc_id,
    content=result["markdown"],
    metadata={
        "source": pdf_path,
        "markdown_path": result["markdown_path"],
        "num_references": len(result["references"])
    }
)

print(f"✓ Indexed as {doc_id}")

# Step 3: Query the document
queries = [
    "What is the main contribution of this paper?",
    "Describe the methodology used",
    "What are the key findings?"
]

for query in queries:
    print(f"\nQuery: {query}")
    results = indexer.query(query, n_results=3)
    
    if results['results']:
        top_result = results['results'][0]
        relevance = 1 - results['distances'][0]
        print(f"Top result (relevance: {relevance:.3f}):")
        print(f"{top_result[:300]}...")
```

### Batch Processing Multiple PDFs

```python
from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer
from pathlib import Path
import glob

extractor = PDFExtractor()
indexer = RAGIndexer()

# Process all PDFs
pdf_files = glob.glob("pdfs/*.pdf")
print(f"Found {len(pdf_files)} PDF files")

for pdf_path in pdf_files:
    try:
        # Extract
        result = extractor.extract_pdf(pdf_path)
        
        # Index
        doc_id = Path(pdf_path).stem
        indexer.index_document(
            doc_id=doc_id,
            content=result["markdown"],
            metadata={"source": pdf_path}
        )
        
        print(f"✓ {Path(pdf_path).name}")
    except Exception as e:
        print(f"✗ {Path(pdf_path).name}: {e}")

# Query across all documents
results = indexer.query("artificial intelligence", n_results=10)
print(f"\nFound {len(results['results'])} relevant passages across all documents")
```

### Custom Chunking Strategy

```python
from src.rag_indexer.indexer import RAGIndexer

# Create custom indexer with different chunk size
indexer = RAGIndexer()

# Override chunk size for specific use case
def custom_chunking(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Use in indexing
content = "Your long document content..."
chunks = custom_chunking(content, chunk_size=500, overlap=100)

for i, chunk in enumerate(chunks):
    indexer.index_document(
        doc_id=f"doc_chunk_{i}",
        content=chunk,
        metadata={"chunk_index": i}
    )
```

### Integration with FastAPI

```python
from fastapi import FastAPI, BackgroundTasks
from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer

app = FastAPI()
extractor = PDFExtractor()
indexer = RAGIndexer()

def process_pdf_background(pdf_path: str, doc_id: str):
    """Background task for PDF processing"""
    result = extractor.extract_pdf(pdf_path)
    indexer.index_document(
        doc_id=doc_id,
        content=result["markdown"],
        metadata={"source": pdf_path}
    )

@app.post("/process")
async def process_pdf(pdf_path: str, background_tasks: BackgroundTasks):
    doc_id = Path(pdf_path).stem
    background_tasks.add_task(process_pdf_background, pdf_path, doc_id)
    return {"status": "processing", "doc_id": doc_id}
```

### Error Handling Best Practices

```python
from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_process_pdf(pdf_path: str):
    """Process PDF with comprehensive error handling"""
    try:
        extractor = PDFExtractor()
        indexer = RAGIndexer()
        
        # Extract
        result = extractor.extract_pdf(pdf_path)
        logger.info(f"Extracted {pdf_path}")
        
        # Index
        doc_id = Path(pdf_path).stem
        indexer.index_document(
            doc_id=doc_id,
            content=result["markdown"]
        )
        logger.info(f"Indexed {doc_id}")
        
        return {"status": "success", "doc_id": doc_id}
        
    except FileNotFoundError:
        logger.error(f"PDF not found: {pdf_path}")
        return {"status": "error", "message": "File not found"}
        
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return {"status": "error", "message": "Dependencies not installed"}
        
    except Exception as e:
        logger.exception(f"Unexpected error processing {pdf_path}")
        return {"status": "error", "message": str(e)}
```

---

## Docker Usage

### Build and Run with Docker

```bash
# Build the image
docker build -t pdf-rag-system .

# Run web interface
docker run -p 8000:8000 -v $(pwd)/pdfs:/app/pdfs pdf-rag-system

# Run with docker-compose
docker-compose up
```

### Docker Compose with Volumes

```yaml
# docker-compose.yml
version: '3.8'
services:
  pdf-rag:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./pdfs:/app/pdfs
      - ./markdown_outputs:/app/markdown_outputs
      - ./chroma_db:/app/chroma_db
```

---

## Troubleshooting

### Check if ChromaDB is Working

```python
try:
    from src.rag_indexer.indexer import RAGIndexer
    indexer = RAGIndexer()
    print("✓ ChromaDB is working")
except ImportError:
    print("✗ ChromaDB not installed: pip install chromadb")
```

### Verify PDF Extraction

```python
from src.pdf_extractor.extractor import PDFExtractor
import logging

logging.basicConfig(level=logging.DEBUG)

extractor = PDFExtractor()
result = extractor.extract_pdf("pdfs/test.pdf")
print(f"Extraction successful: {len(result['markdown'])} characters")
```

---

## Performance Tips

1. **Batch Processing**: Process multiple PDFs in parallel
2. **Chunk Size**: Adjust based on document type (500-1000 for articles, 200-500 for chat)
3. **Query Optimization**: Use specific queries for better results
4. **Caching**: ChromaDB caches embeddings automatically
5. **Resource Limits**: Monitor memory usage with large PDFs

---

For more information, see:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
