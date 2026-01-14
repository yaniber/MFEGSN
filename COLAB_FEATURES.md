# Google Colab Enhanced Features

This document describes the enhanced features added to the MFEGSN Google Colab notebook.

## Overview

The enhanced Colab notebook now supports:
- 🌐 Public URL access via Ngrok
- ✅ Selective PDF processing
- 📊 Real-time progress tracking
- 💾 One-click GitHub export

## New Features

### 1. Ngrok Integration for Public Access

The notebook now includes Ngrok integration, allowing you to access the web interface from anywhere with a public URL.

#### Setup:
1. Get your Ngrok authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
2. Run the "Configure API Keys" cell and enter your token
3. Run the "Launch Web Interface with Ngrok" cell
4. Copy the public URL displayed and open it in your browser

#### Security Notes:
- The Ngrok token is stored only in memory for the session
- Never share your Ngrok public URL with untrusted parties
- The tunnel is automatically closed when you stop the server

### 2. Enhanced Web Interface

The web interface has been significantly enhanced with new capabilities:

#### Select and Process Specific PDFs
- View all PDFs in the `pdfs/` directory
- Select specific PDFs using checkboxes
- Process only the selected PDFs instead of all PDFs at once
- View file size and modification date for each PDF

#### Real-time Progress Tracking
- Live progress bar showing processing status
- See which PDF is currently being processed
- View results as they complete
- See errors for any PDFs that fail to process
- Summary of processed PDFs with metadata

#### GitHub Export (One-Click)
Choose between two export options:

**Option 1: Create New Branch**
- Exports to an existing repository
- Creates a new branch with your outputs
- Provides link to create a Pull Request
- Default repository: yaniber/MFEGSN

**Option 2: Create New Repository**
- Creates a brand new repository under your account
- Can be public or private
- Includes a README with statistics
- All outputs are committed automatically

#### Exported Files:
- `manifest.json` - Metadata about processed files
- `markdown_outputs/` - All extracted Markdown files
- `chroma_db/` - Vector database files (for text files)
- `README.md` - Auto-generated summary (new repo only)

### 3. Improved Error Handling

The notebook now includes better error handling:
- Dependency conflicts with Google Colab are filtered out
- Better error messages when initialization fails
- Automatic directory creation for required folders
- Graceful degradation when optional features are unavailable

### 4. Server Management

New cells for managing the web server:
- **Launch Web Interface**: Starts the server with Ngrok
- **View Server Logs**: Troubleshooting helper
- **Stop Web Server**: Cleanly shuts down the server and tunnel

## Usage Examples

### Basic Workflow

```python
# 1. Install dependencies
# Run the installation cell

# 2. Import PDFs from Google Drive
# Run the Google Drive import cells

# 3. Configure Ngrok (optional)
# Run the API keys cell and enter your Ngrok token

# 4. Launch web interface
# Run the "Launch Web Interface" cell

# 5. Open the public URL in your browser

# 6. In the web interface:
#    - Click "Refresh PDF List" to see available PDFs
#    - Select the PDFs you want to process
#    - Click "Process Selected PDFs"
#    - Watch the progress in real-time

# 7. Export to GitHub:
#    - Scroll to "Export Results to GitHub"
#    - Choose "Create New Branch" or "Create New Repository"
#    - Enter your GitHub PAT (required)
#    - Fill in the required fields
#    - Click "Export to GitHub"
#    - Follow the links to view your branch/repo

# 8. When done, stop the server
# Run the "Stop Web Server" cell
```

### Processing PDFs Selectively

This is useful when you have many PDFs but only want to process a few:

1. Upload or import your PDFs
2. Launch the web interface
3. Click "Refresh PDF List"
4. Check only the PDFs you want to process
5. Click "Process Selected PDFs"
6. Monitor progress in real-time

### Exporting to GitHub

#### To a New Branch:
1. Make sure you have processed some PDFs
2. Get a GitHub Personal Access Token with `repo` scope
3. In the web interface, scroll to "Export Results to GitHub"
4. Select "Create New Branch"
5. Enter branch name (e.g., `colab-outputs-2024`)
6. Enter your GitHub PAT
7. Click "Export to GitHub"
8. Click the "Create Pull Request" link to merge your changes

#### To a New Repository:
1. Make sure you have processed some PDFs
2. Get a GitHub Personal Access Token with `repo` scope
3. In the web interface, scroll to "Export Results to GitHub"
4. Select "Create New Repository"
5. Enter repository name (e.g., `my-pdf-outputs`)
6. Optionally add a description
7. Choose public or private
8. Enter your GitHub PAT
9. Click "Export to GitHub"
10. Click the repository link to view your new repo

## Security Considerations

### Tokens and Credentials

All tokens and credentials are:
- Never displayed in plain text in the interface
- Stored only in memory for the session
- Not persisted to disk
- Not included in any logs or outputs
- Cleared from form fields after use

### Best Practices

1. **Ngrok Token**: Keep it private, don't share your public URL
2. **GitHub PAT**: Use fine-grained tokens with minimal scopes
3. **Public URLs**: Close the Ngrok tunnel when not in use
4. **Sensitive Data**: Don't process PDFs with sensitive information on public infrastructure

## Troubleshooting

### Dependency Conflicts

You may see warnings about dependency conflicts with Google Colab packages:
```
google-colab 1.0.0 requires requests==2.32.4, but you have requests 2.32.5
```

**Solution**: These warnings are normal and can be safely ignored. The application will work correctly.

### Server Not Starting

If the server doesn't start:
1. Check the server logs using the "View Server Logs" cell
2. Make sure you're in the MFEGSN directory
3. Try stopping and restarting the server
4. Verify all dependencies are installed

### Ngrok Tunnel Not Working

If you can't access the public URL:
1. Verify your Ngrok token is configured correctly
2. Check that the token has not expired
3. View server logs for Ngrok errors
4. Try restarting the server

### GitHub Export Failing

If GitHub export fails:
1. Verify your PAT is valid and has `repo` scope
2. Check that the branch/repo name doesn't already exist
3. Ensure you have network connectivity
4. Check for error messages in the interface

### PDFs Not Processing

If PDFs fail to process:
1. Check that the PDFs are valid and not corrupted
2. Ensure the PDFs are in the `pdfs/` directory
3. Look for error messages in the processing status
4. Try processing one PDF at a time to isolate the issue

## API Endpoints

The enhanced web interface exposes these new API endpoints:

### GET /api/pdfs
List all PDF files in the pdfs directory with metadata.

**Response:**
```json
{
  "pdfs": [
    {
      "name": "document.pdf",
      "size": 1048576,
      "size_mb": 1.0,
      "modified": "2024-01-01T12:00:00"
    }
  ]
}
```

### POST /api/process-pdfs
Start processing selected PDFs in the background.

**Parameters:**
- `pdf_names`: JSON array of PDF filenames

**Response:**
```json
{
  "task_id": "uuid-string",
  "message": "Processing started"
}
```

### GET /api/process-status/{task_id}
Get the status of a processing task.

**Response:**
```json
{
  "status": "processing",
  "total": 5,
  "processed": 2,
  "current": "document.pdf",
  "results": [...],
  "errors": [...]
}
```

### POST /api/github/branch
Export results to a new branch in an existing repository.

**Parameters:**
- `github_pat`: GitHub Personal Access Token
- `branch_name`: Name for the new branch
- `repo_owner`: Repository owner (default: yaniber)
- `repo_name`: Repository name (default: MFEGSN)

**Response:**
```json
{
  "status": "success",
  "message": "Successfully created branch...",
  "branch_url": "https://github.com/...",
  "create_pr_url": "https://github.com/.../compare/..."
}
```

### POST /api/github/repo
Export results to a new GitHub repository.

**Parameters:**
- `github_pat`: GitHub Personal Access Token
- `repo_name`: Name for the new repository
- `repo_description`: Optional description
- `private`: Boolean, whether repo should be private

**Response:**
```json
{
  "status": "success",
  "message": "Successfully created repository...",
  "repo_url": "https://github.com/..."
}
```

## System Requirements

### Google Colab
- Free tier is sufficient for most use cases
- Pro/Pro+ recommended for large PDF batches
- GPU not required

### Dependencies
All dependencies are automatically installed via `requirements.txt`:
- pyngrok >= 7.0.0
- PyGithub >= 2.1.0
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- (and all standard MFEGSN dependencies)

### Browser Compatibility
The web interface works with:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Limitations

- GitHub API has rate limits (60 requests/hour unauthenticated, 5000/hour with PAT)
- Maximum file size for GitHub is 100MB per file
- Ngrok free tier has connection limits (check ngrok.com for details)
- Processing time depends on PDF size and complexity

## Support

For issues or questions:
1. Check this documentation first
2. View the troubleshooting section
3. Open an issue on GitHub: https://github.com/yaniber/MFEGSN/issues

## License

This project is licensed under the same license as MFEGSN.
