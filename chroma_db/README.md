# ChromaDB Vector Database Directory

This directory contains the ChromaDB vector database used for semantic search and RAG (Retrieval-Augmented Generation).

## What is stored here?

- Vector embeddings of document chunks
- Document metadata
- Index structures for fast similarity search

## Data Persistence

When using Docker (via `start.sh`), this directory is mounted as a bind mount, ensuring:
- Data persists between container restarts
- All indexed documents are preserved
- You can backup data by committing to git (if desired)

## Structure

The directory structure is managed by ChromaDB and includes:
- Collection metadata
- Vector indices
- Document storage

## Notes

- This directory is created automatically on first run
- The contents are typically ignored by git (see `.gitignore`)
- To backup the database, you can modify `.gitignore` to include the database files
- The database is compatible across Docker and local installations
