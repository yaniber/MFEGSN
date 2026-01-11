"""
FastAPI Web Interface for PDF Upload and Management
"""
import os
from pathlib import Path
from typing import List
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer

app = FastAPI(title="PDF RAG System", description="Upload, extract, and query PDFs")

# Initialize components
pdf_extractor = PDFExtractor()
rag_indexer = RAGIndexer()


@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with upload form"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PDF RAG System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
            .upload-section {
                margin: 20px 0;
                padding: 20px;
                border: 2px dashed #ccc;
                border-radius: 8px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
            .query-section {
                margin-top: 30px;
            }
            input[type="text"] {
                width: 70%;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .results {
                margin-top: 20px;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 4px;
            }
            .result-item {
                margin: 10px 0;
                padding: 10px;
                background: white;
                border-left: 3px solid #4CAF50;
            }
            .status {
                margin: 10px 0;
                padding: 10px;
                border-radius: 4px;
            }
            .success {
                background-color: #d4edda;
                color: #155724;
            }
            .error {
                background-color: #f8d7da;
                color: #721c24;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 PDF RAG System</h1>
            <p>Upload PDFs, extract content, and query using semantic search</p>
            
            <div class="upload-section">
                <h2>Upload PDF</h2>
                <form id="uploadForm" enctype="multipart/form-data">
                    <input type="file" id="fileInput" accept=".pdf" multiple>
                    <button type="submit">Upload & Extract</button>
                </form>
                <div id="uploadStatus"></div>
            </div>
            
            <div class="query-section">
                <h2>Query Documents</h2>
                <input type="text" id="queryInput" placeholder="Enter your query...">
                <button onclick="queryDocuments()">Search</button>
                <div id="queryResults" class="results"></div>
            </div>
            
            <div style="margin-top: 30px;">
                <button onclick="listDocuments()">List All Documents</button>
                <button onclick="getStats()">Get Statistics</button>
                <div id="infoResults" class="results"></div>
            </div>
        </div>
        
        <script>
            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const fileInput = document.getElementById('fileInput');
                const statusDiv = document.getElementById('uploadStatus');
                
                if (!fileInput.files.length) {
                    statusDiv.innerHTML = '<div class="status error">Please select a file</div>';
                    return;
                }
                
                const formData = new FormData();
                for (let file of fileInput.files) {
                    formData.append('files', file);
                }
                
                statusDiv.innerHTML = '<div class="status">Uploading and processing...</div>';
                
                try {
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        statusDiv.innerHTML = `<div class="status success">
                            Successfully uploaded ${result.processed} file(s)<br>
                            ${result.details.map(d => `- ${d.filename}: ${d.status}`).join('<br>')}
                        </div>`;
                    } else {
                        statusDiv.innerHTML = `<div class="status error">Error: ${result.detail}</div>`;
                    }
                } catch (error) {
                    statusDiv.innerHTML = `<div class="status error">Error: ${error.message}</div>`;
                }
            });
            
            async function queryDocuments() {
                const query = document.getElementById('queryInput').value;
                const resultsDiv = document.getElementById('queryResults');
                
                if (!query) {
                    resultsDiv.innerHTML = '<div class="status error">Please enter a query</div>';
                    return;
                }
                
                resultsDiv.innerHTML = '<div>Searching...</div>';
                
                try {
                    const response = await fetch(`/query?q=${encodeURIComponent(query)}`);
                    const result = await response.json();
                    
                    if (result.results.length === 0) {
                        resultsDiv.innerHTML = '<div>No results found</div>';
                        return;
                    }
                    
                    let html = `<h3>Results for: "${query}"</h3>`;
                    result.results.forEach((doc, idx) => {
                        const metadata = result.metadatas[idx];
                        const relevance = (1 - result.distances[idx]).toFixed(3);
                        html += `
                            <div class="result-item">
                                <strong>Document: ${metadata.doc_id}</strong> (Relevance: ${relevance})<br>
                                <small>Chunk ${metadata.chunk_id}</small><br>
                                ${doc.substring(0, 300)}...
                            </div>
                        `;
                    });
                    resultsDiv.innerHTML = html;
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="status error">Error: ${error.message}</div>`;
                }
            }
            
            async function listDocuments() {
                const resultsDiv = document.getElementById('infoResults');
                resultsDiv.innerHTML = '<div>Loading...</div>';
                
                try {
                    const response = await fetch('/documents');
                    const result = await response.json();
                    
                    let html = `<h3>Indexed Documents (${result.documents.length})</h3>`;
                    html += '<ul>';
                    result.documents.forEach(doc => {
                        html += `<li>${doc}</li>`;
                    });
                    html += '</ul>';
                    resultsDiv.innerHTML = html;
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="status error">Error: ${error.message}</div>`;
                }
            }
            
            async function getStats() {
                const resultsDiv = document.getElementById('infoResults');
                resultsDiv.innerHTML = '<div>Loading...</div>';
                
                try {
                    const response = await fetch('/stats');
                    const result = await response.json();
                    
                    resultsDiv.innerHTML = `
                        <h3>Collection Statistics</h3>
                        <p>Total Documents: ${result.total_documents}</p>
                        <p>Total Chunks: ${result.total_chunks}</p>
                    `;
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="status error">Error: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    """Upload and process PDF files"""
    results = []
    
    for file in files:
        if not file.filename.endswith('.pdf'):
            results.append({
                "filename": file.filename,
                "status": "skipped (not a PDF)"
            })
            continue
        
        try:
            # Save uploaded file
            pdf_path = Path("pdfs") / file.filename
            with open(pdf_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Extract content
            result = pdf_extractor.extract_pdf(str(pdf_path))
            
            # Index in RAG
            doc_id = pdf_path.stem
            rag_indexer.index_document(
                doc_id=doc_id,
                content=result["markdown"],
                metadata={
                    "source": str(pdf_path),
                    "markdown_path": result["markdown_path"]
                }
            )
            
            results.append({
                "filename": file.filename,
                "status": "success",
                "doc_id": doc_id,
                "markdown_path": result["markdown_path"]
            })
        
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": f"error: {str(e)}"
            })
    
    return {
        "processed": len(results),
        "details": results
    }


@app.get("/query")
async def query_documents(q: str, n: int = 5):
    """Query the RAG database"""
    results = rag_indexer.query(q, n)
    return results


@app.get("/documents")
async def list_documents():
    """List all indexed documents"""
    docs = rag_indexer.list_documents()
    return {"documents": docs}


@app.get("/stats")
async def get_stats():
    """Get collection statistics"""
    stats = rag_indexer.get_collection_stats()
    return stats


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from the index"""
    try:
        rag_indexer.delete_document(doc_id)
        return {"status": "success", "message": f"Deleted document {doc_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
