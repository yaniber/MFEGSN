# PDF Upload Directory

Place your PDF files here for processing.

Files in this directory will be:
1. Extracted using Marker (or PyMuPDF as fallback)
2. Converted to Markdown
3. Indexed in the RAG vector database

## Usage

### Via Web Interface
1. Start the web server: `python web_interface.py`
2. Visit http://localhost:8000
3. Use the upload form to add PDFs

### Via Command Line
Simply copy PDF files to this directory and run:
```bash
python example_usage.py
```

### Via MCP Server
Use the MCP tools to extract PDFs:
```
extract_pdf(pdf_path="pdfs/your_document.pdf")
```

## Notes
- Supported format: PDF only
- PDFs are not deleted after processing
- Original PDFs are preserved
