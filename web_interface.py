"""
FastAPI Web Interface for PDF Upload and Management
"""
import os
from pathlib import Path
from typing import List, Optional, Dict
import shutil
from dotenv import load_dotenv
import json
from datetime import datetime
import base64
import logging

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            .pdf-checkbox {
                margin: 8px 0;
                padding: 8px;
                background: white;
                border-radius: 4px;
                border: 1px solid #ddd;
            }
            .pdf-checkbox:hover {
                background: #f9f9f9;
            }
            .pdf-checkbox label {
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .pdf-checkbox input[type="checkbox"] {
                width: 18px;
                height: 18px;
                cursor: pointer;
            }
            .pdf-info {
                font-size: 12px;
                color: #666;
                margin-left: 28px;
            }
            .progress-bar {
                width: 100%;
                height: 25px;
                background-color: #f0f0f0;
                border-radius: 4px;
                overflow: hidden;
                margin: 10px 0;
            }
            .progress-fill {
                height: 100%;
                background-color: #4CAF50;
                transition: width 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            .process-result {
                margin: 10px 0;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 4px;
                border-left: 3px solid #4CAF50;
            }
            .process-error {
                border-left-color: #f44336;
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
            
            <details open>
                <summary>📄 Process Selected PDFs</summary>
                <div class="upload-section">
                    <h3>Select PDFs to Process</h3>
                    <button onclick="loadPDFList()" class="secondary">Refresh PDF List</button>
                    <div id="pdfList" style="margin-top: 15px;"></div>
                    <button onclick="processSelectedPDFs()" style="margin-top: 15px;">Process Selected PDFs</button>
                    <div id="processStatus"></div>
                    <div id="processProgress" style="margin-top: 15px;"></div>
                </div>
            </details>
            
            <details>
                <summary>💾 Export Results to GitHub</summary>
                <div class="config-section">
                    <h3>Save to GitHub</h3>
                    <p>Export your processed outputs (markdown files, database, and manifest) to GitHub.</p>
                    
                    <div style="margin-top: 20px;">
                        <label style="display: block; font-weight: bold; margin-bottom: 10px;">
                            <input type="radio" name="githubExportType" value="branch" checked> Create New Branch
                        </label>
                        <div id="branchOptions" style="margin-left: 25px; margin-bottom: 20px;">
                            <div style="margin: 10px 0;">
                                <label>Repository Owner:</label>
                                <input type="text" id="repoOwner" value="yaniber" style="width: 200px; padding: 5px;">
                            </div>
                            <div style="margin: 10px 0;">
                                <label>Repository Name:</label>
                                <input type="text" id="repoName" value="MFEGSN" style="width: 200px; padding: 5px;">
                            </div>
                            <div style="margin: 10px 0;">
                                <label>Branch Name:</label>
                                <input type="text" id="branchName" placeholder="e.g., colab-outputs-2024" style="width: 300px; padding: 5px;">
                            </div>
                        </div>
                        
                        <label style="display: block; font-weight: bold; margin-bottom: 10px;">
                            <input type="radio" name="githubExportType" value="repo"> Create New Repository
                        </label>
                        <div id="repoOptions" style="margin-left: 25px; display: none;">
                            <div style="margin: 10px 0;">
                                <label>Repository Name:</label>
                                <input type="text" id="newRepoName" placeholder="e.g., my-pdf-outputs" style="width: 300px; padding: 5px;">
                            </div>
                            <div style="margin: 10px 0;">
                                <label>Description:</label>
                                <input type="text" id="repoDescription" placeholder="Optional description" style="width: 400px; padding: 5px;">
                            </div>
                            <div style="margin: 10px 0;">
                                <label>
                                    <input type="checkbox" id="repoPrivate"> Make Private
                                </label>
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <label style="display: block; font-weight: bold; margin-bottom: 5px;">GitHub Personal Access Token (PAT):</label>
                        <input type="password" id="githubExportPat" placeholder="ghp_..." style="width: 100%; max-width: 500px; padding: 8px;">
                        <small style="display: block; color: #666; margin-top: 5px;">
                            Token will not be stored. Required scopes: <code>repo</code>
                        </small>
                    </div>
                    
                    <button onclick="exportToGitHub()" class="secondary">Export to GitHub</button>
                    <div id="githubExportStatus"></div>
                </div>
            </details>
            
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
            
            // PDF List and Processing
            async function loadPDFList() {
                const listDiv = document.getElementById('pdfList');
                listDiv.innerHTML = '<div>Loading...</div>';
                
                try {
                    const response = await fetch('/api/pdfs');
                    const result = await response.json();
                    
                    if (result.pdfs.length === 0) {
                        listDiv.innerHTML = '<div class="status">No PDF files found. Upload some PDFs first.</div>';
                        return;
                    }
                    
                    let html = '<div style="margin-bottom: 10px;">';
                    html += '<label style="font-weight: bold;"><input type="checkbox" id="selectAllPDFs" onchange="toggleSelectAll()"> Select All</label>';
                    html += '</div>';
                    
                    result.pdfs.forEach(pdf => {
                        html += `
                            <div class="pdf-checkbox">
                                <label>
                                    <input type="checkbox" class="pdf-select" value="${pdf.name}">
                                    <span><strong>${pdf.name}</strong></span>
                                </label>
                                <div class="pdf-info">Size: ${pdf.size_mb} MB | Modified: ${new Date(pdf.modified).toLocaleString()}</div>
                            </div>
                        `;
                    });
                    
                    listDiv.innerHTML = html;
                } catch (error) {
                    listDiv.innerHTML = `<div class="status error">Error loading PDFs: ${error.message}</div>`;
                }
            }
            
            function toggleSelectAll() {
                const selectAll = document.getElementById('selectAllPDFs');
                const checkboxes = document.querySelectorAll('.pdf-select');
                checkboxes.forEach(cb => cb.checked = selectAll.checked);
            }
            
            async function processSelectedPDFs() {
                const checkboxes = document.querySelectorAll('.pdf-select:checked');
                const selectedPDFs = Array.from(checkboxes).map(cb => cb.value);
                
                if (selectedPDFs.length === 0) {
                    document.getElementById('processStatus').innerHTML = 
                        '<div class="status error">Please select at least one PDF</div>';
                    return;
                }
                
                const statusDiv = document.getElementById('processStatus');
                const progressDiv = document.getElementById('processProgress');
                
                statusDiv.innerHTML = '<div class="status">Starting processing...</div>';
                progressDiv.innerHTML = '';
                
                try {
                    const formData = new FormData();
                    formData.append('pdf_names', JSON.stringify(selectedPDFs));
                    
                    const response = await fetch('/api/process-pdfs', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        const taskId = result.task_id;
                        statusDiv.innerHTML = `<div class="status success">Processing started (Task ID: ${taskId})</div>`;
                        
                        // Poll for status
                        pollProcessingStatus(taskId);
                    } else {
                        statusDiv.innerHTML = `<div class="status error">Error: ${result.detail}</div>`;
                    }
                } catch (error) {
                    statusDiv.innerHTML = `<div class="status error">Error: ${error.message}</div>`;
                }
            }
            
            async function pollProcessingStatus(taskId) {
                const progressDiv = document.getElementById('processProgress');
                const statusDiv = document.getElementById('processStatus');
                
                const pollInterval = setInterval(async () => {
                    try {
                        const response = await fetch(`/api/process-status/${taskId}`);
                        const status = await response.json();
                        
                        const progress = (status.processed / status.total * 100).toFixed(0);
                        
                        let html = `
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${progress}%">
                                    ${progress}% (${status.processed}/${status.total})
                                </div>
                            </div>
                        `;
                        
                        if (status.current) {
                            html += `<p>Currently processing: <strong>${status.current}</strong></p>`;
                        }
                        
                        if (status.results.length > 0) {
                            html += '<h4>Processed PDFs:</h4>';
                            status.results.forEach(result => {
                                html += `
                                    <div class="process-result">
                                        <strong>${result.pdf}</strong><br>
                                        Document ID: ${result.doc_id}<br>
                                        Markdown: ${result.markdown_path}<br>
                                        Size: ${(result.size / (1024 * 1024)).toFixed(2)} MB
                                    </div>
                                `;
                            });
                        }
                        
                        if (status.errors.length > 0) {
                            html += '<h4>Errors:</h4>';
                            status.errors.forEach(error => {
                                html += `
                                    <div class="process-result process-error">
                                        <strong>${error.pdf}</strong>: ${error.error}
                                    </div>
                                `;
                            });
                        }
                        
                        progressDiv.innerHTML = html;
                        
                        if (status.status === 'completed') {
                            clearInterval(pollInterval);
                            statusDiv.innerHTML = '<div class="status success">✓ Processing completed!</div>';
                        }
                    } catch (error) {
                        clearInterval(pollInterval);
                        progressDiv.innerHTML = `<div class="status error">Error checking status: ${error.message}</div>`;
                    }
                }, 1000); // Poll every second
            }
            
            // GitHub Export
            document.querySelectorAll('input[name="githubExportType"]').forEach(radio => {
                radio.addEventListener('change', function() {
                    document.getElementById('branchOptions').style.display = 
                        this.value === 'branch' ? 'block' : 'none';
                    document.getElementById('repoOptions').style.display = 
                        this.value === 'repo' ? 'block' : 'none';
                });
            });
            
            async function exportToGitHub() {
                const statusDiv = document.getElementById('githubExportStatus');
                const pat = document.getElementById('githubExportPat').value;
                
                if (!pat) {
                    statusDiv.innerHTML = '<div class="status error">GitHub PAT is required</div>';
                    return;
                }
                
                const exportType = document.querySelector('input[name="githubExportType"]:checked').value;
                statusDiv.innerHTML = '<div class="status">Exporting to GitHub...</div>';
                
                try {
                    const formData = new FormData();
                    formData.append('github_pat', pat);
                    
                    let endpoint;
                    if (exportType === 'branch') {
                        const branchName = document.getElementById('branchName').value;
                        if (!branchName) {
                            statusDiv.innerHTML = '<div class="status error">Branch name is required</div>';
                            return;
                        }
                        
                        formData.append('branch_name', branchName);
                        formData.append('repo_owner', document.getElementById('repoOwner').value);
                        formData.append('repo_name', document.getElementById('repoName').value);
                        endpoint = '/api/github/branch';
                    } else {
                        const repoName = document.getElementById('newRepoName').value;
                        if (!repoName) {
                            statusDiv.innerHTML = '<div class="status error">Repository name is required</div>';
                            return;
                        }
                        
                        formData.append('repo_name', repoName);
                        formData.append('repo_description', document.getElementById('repoDescription').value);
                        formData.append('private', document.getElementById('repoPrivate').checked);
                        endpoint = '/api/github/repo';
                    }
                    
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        let html = `<div class="status success">${result.message}</div>`;
                        if (result.branch_url) {
                            html += `<p><a href="${result.branch_url}" target="_blank">View Branch</a></p>`;
                            html += `<p><a href="${result.create_pr_url}" target="_blank">Create Pull Request</a></p>`;
                        }
                        if (result.repo_url) {
                            html += `<p><a href="${result.repo_url}" target="_blank">View Repository</a></p>`;
                        }
                        statusDiv.innerHTML = html;
                        
                        // Clear PAT
                        document.getElementById('githubExportPat').value = '';
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


@app.get("/api/pdfs")
async def list_pdfs():
    """List all PDF files in the pdfs directory"""
    pdf_dir = Path("pdfs")
    if not pdf_dir.exists():
        return {"pdfs": []}
    
    pdfs = []
    for pdf_file in pdf_dir.glob("*.pdf"):
        stat = pdf_file.stat()
        pdfs.append({
            "name": pdf_file.name,
            "size": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        })
    
    return {"pdfs": sorted(pdfs, key=lambda x: x["name"])}


# Global variable to track processing status
processing_status = {}
processing_status_lock = __import__('threading').Lock()

# Constants for GitHub operations
MAX_FILES_PER_GITHUB_COMMIT = 50  # GitHub API limit for files per request


@app.post("/api/process-pdfs")
async def process_selected_pdfs(
    background_tasks: BackgroundTasks,
    pdf_names: str = Form(...)
):
    """Process selected PDF files"""
    import uuid
    
    task_id = str(uuid.uuid4())
    pdf_list = json.loads(pdf_names)
    
    if not pdf_list:
        raise HTTPException(status_code=400, detail="No PDFs selected")
    
    # Initialize processing status (thread-safe)
    with processing_status_lock:
        processing_status[task_id] = {
            "status": "starting",
            "total": len(pdf_list),
            "processed": 0,
            "current": None,
            "results": [],
            "errors": []
        }
    
    # Start background processing
    background_tasks.add_task(process_pdfs_background, task_id, pdf_list)
    
    return {"task_id": task_id, "message": "Processing started"}


def process_pdfs_background(task_id: str, pdf_names: List[str]):
    """Background task to process PDFs"""
    import logging
    
    logger = logging.getLogger(__name__)
    
    with processing_status_lock:
        processing_status[task_id]["status"] = "processing"
    
    for idx, pdf_name in enumerate(pdf_names):
        try:
            with processing_status_lock:
                processing_status[task_id]["current"] = pdf_name
            
            pdf_path = Path("pdfs") / pdf_name
            if not pdf_path.exists():
                error_info = {"pdf": pdf_name, "error": "File not found"}
                logger.error(f"PDF not found: {pdf_name}")
                with processing_status_lock:
                    processing_status[task_id]["errors"].append(error_info)
                continue
            
            # Extract PDF content
            result = pdf_extractor.extract_pdf(str(pdf_path))
            
            # Index in RAG database
            doc_id = pdf_path.stem
            rag_indexer.index_document(
                doc_id=doc_id,
                content=result["markdown"],
                metadata={
                    "source": str(pdf_path),
                    "markdown_path": result["markdown_path"]
                }
            )
            
            # Get page count (rough estimate from markdown)
            page_count = result.get("pages", "N/A")
            
            result_info = {
                "pdf": pdf_name,
                "doc_id": doc_id,
                "markdown_path": result["markdown_path"],
                "pages": page_count,
                "size": pdf_path.stat().st_size
            }
            with processing_status_lock:
                processing_status[task_id]["results"].append(result_info)
            
        except Exception as e:
            error_info = {"pdf": pdf_name, "error": str(e)}
            logger.error(f"Error processing {pdf_name}: {e}", exc_info=True)
            with processing_status_lock:
                processing_status[task_id]["errors"].append(error_info)
        
        with processing_status_lock:
            processing_status[task_id]["processed"] = idx + 1
    
    with processing_status_lock:
        processing_status[task_id]["status"] = "completed"
        processing_status[task_id]["current"] = None


@app.get("/api/process-status/{task_id}")
async def get_processing_status(task_id: str):
    """Get the status of a PDF processing task"""
    if task_id not in processing_status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return processing_status[task_id]


def create_manifest():
    """Create a manifest.json file with metadata about processed PDFs"""
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "pdfs": [],
        "markdown_files": [],
        "database_info": {}
    }
    
    # List PDFs
    pdf_dir = Path("pdfs")
    if pdf_dir.exists():
        for pdf_file in pdf_dir.glob("*.pdf"):
            stat = pdf_file.stat()
            manifest["pdfs"].append({
                "name": pdf_file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    # List markdown files
    md_dir = Path("markdown_outputs")
    if md_dir.exists():
        for md_file in md_dir.glob("*.md"):
            stat = md_file.stat()
            manifest["markdown_files"].append({
                "name": md_file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    # Database stats
    try:
        stats = rag_indexer.get_collection_stats()
        manifest["database_info"] = stats
    except Exception:
        manifest["database_info"] = {"error": "Could not retrieve stats"}
    
    # Write manifest
    manifest_path = Path("manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    return manifest


@app.post("/api/github/branch")
async def export_to_github_branch(
    github_pat: str = Form(...),
    branch_name: str = Form(...),
    repo_owner: str = Form("yaniber"),
    repo_name: str = Form("MFEGSN")
):
    """Export results to a new GitHub branch"""
    if not github_pat:
        raise HTTPException(status_code=400, detail="GitHub PAT is required")
    
    if not branch_name:
        raise HTTPException(status_code=400, detail="Branch name is required")
    
    try:
        from github import Github, GithubException
        
        # Create manifest
        manifest = create_manifest()
        
        # Initialize GitHub client
        g = Github(github_pat)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        
        # Get default branch
        default_branch = repo.default_branch
        source_branch = repo.get_branch(default_branch)
        
        # Create new branch
        try:
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source_branch.commit.sha
            )
        except GithubException as e:
            if e.status == 422:
                raise HTTPException(status_code=400, detail=f"Branch '{branch_name}' already exists")
            raise
        
        # Prepare files to commit
        files_to_commit = []
        
        # Add manifest
        files_to_commit.append({
            "path": "manifest.json",
            "content": json.dumps(manifest, indent=2)
        })
        
        # Add markdown files
        md_dir = Path("markdown_outputs")
        if md_dir.exists():
            for md_file in md_dir.glob("*.md"):
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                files_to_commit.append({
                    "path": f"markdown_outputs/{md_file.name}",
                    "content": content
                })
        
        # Add ChromaDB files (as base64 for binary files)
        db_dir = Path("chroma_db")
        if db_dir.exists():
            for db_file in db_dir.rglob("*"):
                if db_file.is_file():
                    try:
                        with open(db_file, "rb") as f:
                            content = base64.b64encode(f.read()).decode()
                        rel_path = str(db_file.relative_to(Path(".")))
                        files_to_commit.append({
                            "path": rel_path,
                            "content": content,
                            "encoding": "base64"
                        })
                    except Exception as e:
                        logger.warning(f"Could not read ChromaDB file {db_file}: {e}")
        
        # Commit files (GitHub API has limits, so we'll do this in batches)
        commit_message = f"Add processed outputs from Colab - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Track failed files for reporting
        failed_files = []
        successful_files = 0
        
        # Limit to avoid API rate limits
        for file_info in files_to_commit[:MAX_FILES_PER_GITHUB_COMMIT]:
            try:
                path = file_info["path"]
                content = file_info["content"]
                encoding = file_info.get("encoding", "utf-8")
                
                # Try to get existing file
                try:
                    existing_file = repo.get_contents(path, ref=branch_name)
                    repo.update_file(
                        path=path,
                        message=commit_message,
                        content=content,
                        sha=existing_file.sha,
                        branch=branch_name
                    )
                except GithubException:
                    # File doesn't exist, create it
                    repo.create_file(
                        path=path,
                        message=commit_message,
                        content=content,
                        branch=branch_name
                    )
                successful_files += 1
                successful_files += 1
            except Exception as e:
                logger.error(f"Failed to upload file {path} to GitHub: {e}")
                failed_files.append(path)
        
        branch_url = f"https://github.com/{repo_owner}/{repo_name}/tree/{branch_name}"
        pr_url = f"https://github.com/{repo_owner}/{repo_name}/compare/{branch_name}"
        
        message = f"Successfully created branch '{branch_name}' and pushed {successful_files} file(s)"
        if failed_files:
            message += f". {len(failed_files)} file(s) failed to upload."
        
        return {
            "status": "success",
            "message": message,
            "branch_url": branch_url,
            "create_pr_url": pr_url,
            "successful_files": successful_files,
            "failed_files": failed_files if failed_files else None
        }
        
    except ImportError:
        raise HTTPException(status_code=500, detail="PyGithub not installed. Install with: pip install PyGithub")
    except GithubException as e:
        raise HTTPException(status_code=400, detail=f"GitHub API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/github/repo")
async def export_to_new_github_repo(
    github_pat: str = Form(...),
    repo_name: str = Form(...),
    repo_description: str = Form(""),
    private: bool = Form(False)
):
    """Export results to a new GitHub repository"""
    if not github_pat:
        raise HTTPException(status_code=400, detail="GitHub PAT is required")
    
    if not repo_name:
        raise HTTPException(status_code=400, detail="Repository name is required")
    
    try:
        from github import Github, GithubException
        
        # Create manifest
        manifest = create_manifest()
        
        # Initialize GitHub client
        g = Github(github_pat)
        user = g.get_user()
        
        # Create new repository
        try:
            repo = user.create_repo(
                name=repo_name,
                description=repo_description or "Processed PDF outputs from MFEGSN",
                private=private,
                auto_init=True
            )
        except GithubException as e:
            if e.status == 422:
                raise HTTPException(status_code=400, detail=f"Repository '{repo_name}' already exists")
            raise
        
        # Prepare files to commit
        files_to_commit = []
        
        # Add manifest
        files_to_commit.append({
            "path": "manifest.json",
            "content": json.dumps(manifest, indent=2)
        })
        
        # Add README
        readme_content = f"""# {repo_name}

Processed PDF outputs from MFEGSN

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Contents

- `markdown_outputs/`: Extracted PDF content in Markdown format
- `chroma_db/`: Vector database for semantic search
- `manifest.json`: Metadata about processed files

## Statistics

- Total PDFs: {len(manifest['pdfs'])}
- Total Markdown files: {len(manifest['markdown_files'])}
- Database: {manifest['database_info'].get('total_documents', 'N/A')} documents, {manifest['database_info'].get('total_chunks', 'N/A')} chunks
"""
        files_to_commit.append({
            "path": "README.md",
            "content": readme_content
        })
        
        # Add markdown files
        md_dir = Path("markdown_outputs")
        if md_dir.exists():
            for md_file in md_dir.glob("*.md"):
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                files_to_commit.append({
                    "path": f"markdown_outputs/{md_file.name}",
                    "content": content
                })
        
        # Commit files
        commit_message = f"Initial commit with processed outputs"
        
        # Track failed files for reporting
        failed_files = []
        successful_files = 0
        
        for file_info in files_to_commit[:MAX_FILES_PER_GITHUB_COMMIT]:
            try:
                path = file_info["path"]
                content = file_info["content"]
                
                repo.create_file(
                    path=path,
                    message=commit_message,
                    content=content
                )
                successful_files += 1
            except Exception as e:
                logger.error(f"Failed to upload file {path} to GitHub: {e}")
                failed_files.append(path)
        
        repo_url = repo.html_url
        
        message = f"Successfully created repository '{repo_name}' with {successful_files} file(s)"
        if failed_files:
            message += f". {len(failed_files)} file(s) failed to upload."
        
        return {
            "status": "success",
            "message": message,
            "repo_url": repo_url,
            "successful_files": successful_files,
            "failed_files": failed_files if failed_files else None
        }
        
    except ImportError:
        raise HTTPException(status_code=500, detail="PyGithub not installed. Install with: pip install PyGithub")
    except GithubException as e:
        raise HTTPException(status_code=400, detail=f"GitHub API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


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
