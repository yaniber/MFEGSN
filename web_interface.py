"""
FastAPI Web Interface for PDF Upload and Management
"""
import os
from pathlib import Path
from typing import List, Optional
import shutil
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import sys

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer

app = FastAPI(title="PDF RAG System", description="Upload, extract, and query PDFs")

# Initialize components
pdf_extractor = PDFExtractor()
rag_indexer = RAGIndexer()

# Configuration
NGROK_AUTHTOKEN = os.getenv("NGROK_AUTHTOKEN", "")
GOOGLE_DRIVE_API_KEY = os.getenv("GOOGLE_DRIVE_API_KEY", "")
GITHUB_PAT = os.getenv("GITHUB_PAT", "")


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
            .header-buttons {
                margin: 20px 0;
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            .colab-button {
                display: inline-flex;
                align-items: center;
                background-color: #F9AB00;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                text-decoration: none;
                font-size: 14px;
                font-weight: bold;
            }
            .colab-button:hover {
                background-color: #E69500;
            }
            .colab-button img {
                height: 20px;
                margin-right: 8px;
            }
            .upload-section {
                margin: 20px 0;
                padding: 20px;
                border: 2px dashed #ccc;
                border-radius: 8px;
            }
            .gdrive-section {
                margin: 20px 0;
                padding: 20px;
                background-color: #f9f9f9;
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
            button.secondary {
                background-color: #2196F3;
            }
            button.secondary:hover {
                background-color: #0b7dda;
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
            .info-box {
                background-color: #e7f3ff;
                padding: 15px;
                border-radius: 4px;
                margin: 20px 0;
                border-left: 4px solid #2196F3;
            }
            .config-section {
                margin: 20px 0;
                padding: 20px;
                background-color: #fff9e6;
                border-radius: 8px;
                border-left: 4px solid #ffc107;
            }
            .config-item {
                margin: 15px 0;
            }
            .config-item label {
                display: block;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .config-item input[type="password"],
            .config-item input[type="text"] {
                width: 100%;
                max-width: 500px;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .config-item small {
                display: block;
                color: #666;
                margin-top: 3px;
            }
            .config-status {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 12px;
                margin-left: 10px;
            }
            .config-status.configured {
                background-color: #d4edda;
                color: #155724;
            }
            .config-status.not-configured {
                background-color: #f8d7da;
                color: #721c24;
            }
            details {
                margin: 20px 0;
            }
            summary {
                cursor: pointer;
                font-weight: bold;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 4px;
            }
            summary:hover {
                background-color: #e0e0e0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 PDF RAG System</h1>
            <p>Upload PDFs, extract content, and query using semantic search</p>
            
            <div class="header-buttons">
                <a href="https://colab.research.google.com/github/yaniber/MFEGSN/blob/main/MFEGSN_Colab.ipynb" 
                   class="colab-button" target="_blank">
                    <img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Colab">
                    Open in Google Colab
                </a>
            </div>
            
            <div class="info-box">
                <strong>🚀 New!</strong> You can now run this application on Google Colab and import PDFs from Google Drive!
                Click the button above to get started.
            </div>
            
            <details>
                <summary>⚙️ Configuration (Optional)</summary>
                <div class="config-section">
                    <p><strong>Configure API keys and tokens to enable additional features:</strong></p>
                    
                    <div class="config-item">
                        <label>
                            🌐 Ngrok Authtoken 
                            <span class="config-status" id="ngrokStatus">Not Configured</span>
                        </label>
                        <input type="password" id="ngrokAuthtoken" placeholder="Enter your ngrok authtoken">
                        <small>Get your token from <a href="https://dashboard.ngrok.com/get-started/your-authtoken" target="_blank">ngrok dashboard</a>. This allows public access to your local server.</small>
                    </div>
                    
                    <div class="config-item">
                        <label>
                            📁 Google Drive API Key 
                            <span class="config-status" id="gdriveStatus">Not Configured</span>
                        </label>
                        <input type="password" id="googleDriveApiKey" placeholder="Enter your Google Drive API key">
                        <small>Follow <a href="https://developers.google.com/drive/api/v3/quickstart/python" target="_blank">Google Drive API quickstart</a> to get your API key.</small>
                    </div>
                    
                    <div class="config-item">
                        <label>
                            🔑 GitHub Personal Access Token (PAT) 
                            <span class="config-status" id="githubStatus">Not Configured</span>
                        </label>
                        <input type="password" id="githubPat" placeholder="Enter your GitHub PAT">
                        <small>Create token at <a href="https://github.com/settings/tokens" target="_blank">GitHub settings</a>. Required scopes: <code>repo</code></small>
                    </div>
                    
                    <button onclick="saveConfiguration()" class="secondary">Save Configuration</button>
                    <button onclick="loadConfiguration()">Check Status</button>
                    <div id="configStatus"></div>
                    
                    <div style="margin-top: 15px; padding: 10px; background-color: #fff3cd; border-radius: 4px; border-left: 3px solid #ffc107;">
                        <strong>⚠️ Note:</strong> Configuration is stored in-memory only and will be lost when the server restarts. 
                        For persistent configuration, add these values to your <code>.env</code> file.
                    </div>
                </div>
            </details>
            
            <div class="upload-section">
                <h2>Upload PDF</h2>
                <form id="uploadForm" enctype="multipart/form-data">
                    <input type="file" id="fileInput" accept=".pdf" multiple>
                    <button type="submit">Upload & Extract</button>
                </form>
                <div id="uploadStatus"></div>
            </div>
            
            <div class="gdrive-section">
                <h2>📁 Import from Google Drive</h2>
                <p>To import PDFs from Google Drive, use the <strong>Google Colab notebook</strong> (button above).</p>
                <p>The notebook allows you to:</p>
                <ul>
                    <li>Mount your Google Drive</li>
                    <li>Import PDFs directly from your Drive folders</li>
                    <li>Process and index your documents</li>
                    <li>Save outputs back to Drive or push to GitHub</li>
                </ul>
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
            
            // Configuration management
            async function loadConfiguration() {
                try {
                    const response = await fetch('/api/config');
                    const config = await response.json();
                    
                    // Update status indicators
                    updateStatusIndicator('ngrokStatus', config.ngrok_configured);
                    updateStatusIndicator('gdriveStatus', config.google_drive_configured);
                    updateStatusIndicator('githubStatus', config.github_configured);
                    
                    document.getElementById('configStatus').innerHTML = 
                        '<div class="status success">Configuration status loaded</div>';
                } catch (error) {
                    document.getElementById('configStatus').innerHTML = 
                        `<div class="status error">Error loading config: ${error.message}</div>`;
                }
            }
            
            function updateStatusIndicator(elementId, isConfigured) {
                const element = document.getElementById(elementId);
                if (isConfigured) {
                    element.textContent = '✓ Configured';
                    element.className = 'config-status configured';
                } else {
                    element.textContent = '✗ Not Configured';
                    element.className = 'config-status not-configured';
                }
            }
            
            async function saveConfiguration() {
                const statusDiv = document.getElementById('configStatus');
                statusDiv.innerHTML = '<div class="status">Saving configuration...</div>';
                
                const formData = new FormData();
                
                const ngrokToken = document.getElementById('ngrokAuthtoken').value;
                const gdriveKey = document.getElementById('googleDriveApiKey').value;
                const githubPat = document.getElementById('githubPat').value;
                
                if (ngrokToken) formData.append('ngrok_authtoken', ngrokToken);
                if (gdriveKey) formData.append('google_drive_api_key', gdriveKey);
                if (githubPat) formData.append('github_pat', githubPat);
                
                try {
                    const response = await fetch('/api/config', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        statusDiv.innerHTML = `<div class="status success">${result.message}</div>`;
                        
                        // Update status indicators
                        updateStatusIndicator('ngrokStatus', result.config.ngrok_configured);
                        updateStatusIndicator('gdriveStatus', result.config.google_drive_configured);
                        updateStatusIndicator('githubStatus', result.config.github_configured);
                        
                        // Clear input fields
                        document.getElementById('ngrokAuthtoken').value = '';
                        document.getElementById('googleDriveApiKey').value = '';
                        document.getElementById('githubPat').value = '';
                    } else {
                        statusDiv.innerHTML = `<div class="status error">Error: ${result.detail}</div>`;
                    }
                } catch (error) {
                    statusDiv.innerHTML = `<div class="status error">Error: ${error.message}</div>`;
                }
            }
            
            // Load configuration on page load
            window.addEventListener('load', loadConfiguration);
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


@app.get("/api/config")
async def get_config():
    """Get current configuration status"""
    return {
        "ngrok_configured": bool(NGROK_AUTHTOKEN),
        "google_drive_configured": bool(GOOGLE_DRIVE_API_KEY),
        "github_configured": bool(GITHUB_PAT),
    }


@app.post("/api/config")
async def update_config(
    ngrok_authtoken: Optional[str] = Form(None),
    google_drive_api_key: Optional[str] = Form(None),
    github_pat: Optional[str] = Form(None)
):
    """Update configuration (in-memory only, not persisted)"""
    global NGROK_AUTHTOKEN, GOOGLE_DRIVE_API_KEY, GITHUB_PAT
    
    if ngrok_authtoken is not None and ngrok_authtoken.strip():
        NGROK_AUTHTOKEN = ngrok_authtoken.strip()
    if google_drive_api_key is not None and google_drive_api_key.strip():
        GOOGLE_DRIVE_API_KEY = google_drive_api_key.strip()
    if github_pat is not None and github_pat.strip():
        GITHUB_PAT = github_pat.strip()
    
    return {
        "status": "success",
        "message": "Configuration updated (in-memory only)",
        "config": {
            "ngrok_configured": bool(NGROK_AUTHTOKEN),
            "google_drive_configured": bool(GOOGLE_DRIVE_API_KEY),
            "github_configured": bool(GITHUB_PAT),
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Check if ngrok should be used
    use_ngrok = os.getenv("USE_NGROK", "false").lower() == "true" or NGROK_AUTHTOKEN
    ngrok_tunnel = None
    
    if use_ngrok and NGROK_AUTHTOKEN:
        try:
            from pyngrok import ngrok, conf
            
            # Set authtoken
            conf.get_default().auth_token = NGROK_AUTHTOKEN
            
            # Start ngrok tunnel
            port = int(os.getenv("WEB_PORT", "8000"))
            ngrok_tunnel = ngrok.connect(port, bind_tls=True)
            public_url = ngrok_tunnel.public_url
            
            print("\n" + "="*60)
            print("🌐 NGROK TUNNEL ACTIVE")
            print("="*60)
            print(f"Public URL: {public_url}")
            print(f"Local URL:  http://localhost:{port}")
            print("="*60 + "\n")
        except ImportError:
            print("⚠️  pyngrok not installed. Install with: pip install pyngrok")
            print("    Falling back to local mode only.\n")
        except Exception as e:
            print(f"⚠️  Failed to start ngrok tunnel: {e}")
            print("    Falling back to local mode only.\n")
    
    # Start uvicorn
    port = int(os.getenv("WEB_PORT", "8000"))
    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    finally:
        # Close ngrok tunnel on exit
        if ngrok_tunnel:
            try:
                ngrok.disconnect(ngrok_tunnel.public_url)
            except Exception:
                # Ignore errors during cleanup
                pass
