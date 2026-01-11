# Markdown Outputs Directory

This directory contains the Markdown files generated from PDF extraction.

## Structure

Each PDF file in the `pdfs` directory is converted to a corresponding `.md` file here:
- `document.pdf` → `document.md`
- `research_paper.pdf` → `research_paper.md`

## Format

The Markdown files contain:
- Structured text content
- Headings and formatting
- References (when detected)
- Metadata about the original PDF

## Notes
- Files are automatically created during PDF extraction
- These files are used for indexing in the RAG system
- You can manually edit these files if needed
- The RAG indexer uses these files as the source for vector embeddings
