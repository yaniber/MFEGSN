"""
RAG Indexer for document vectorization and retrieval
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class RAGIndexer:
    """Index and query documents using vector embeddings"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.collection_name = "pdf_documents"
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the vector database"""
        import chromadb
        from chromadb.config import Settings
        
        self.client = chromadb.Client(Settings(
            persist_directory=self.persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "PDF documents collection"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def index_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None):
        """
        Index a document in the vector database
        
        Args:
            doc_id: Unique identifier for the document
            content: Text content to index
            metadata: Optional metadata dictionary
        """
        if metadata is None:
            metadata = {}
        
        # Split content into chunks
        chunks = self._split_text(content)
        
        # Add documents to collection
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{**metadata, "chunk_id": i, "doc_id": doc_id} for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        
        logger.info(f"Indexed document {doc_id} with {len(chunks)} chunks")
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_len:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]  # Filter empty chunks
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        Query the vector database
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            
        Returns:
            Dictionary with results including documents, metadatas, and distances
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return {
            "query": query_text,
            "results": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else []
        }
    
    def update_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None):
        """Update an existing document"""
        # Delete old chunks
        self.delete_document(doc_id)
        # Add new content
        self.index_document(doc_id, content, metadata)
        logger.info(f"Updated document {doc_id}")
    
    def delete_document(self, doc_id: str):
        """Delete a document from the index"""
        # Get all chunk IDs for this document
        results = self.collection.get(
            where={"doc_id": doc_id}
        )
        
        if results and results["ids"]:
            self.collection.delete(ids=results["ids"])
            logger.info(f"Deleted document {doc_id}")
    
    def list_documents(self) -> List[str]:
        """List all indexed document IDs"""
        results = self.collection.get()
        doc_ids = set()
        
        if results and results["metadatas"]:
            for metadata in results["metadatas"]:
                if "doc_id" in metadata:
                    doc_ids.add(metadata["doc_id"])
        
        return list(doc_ids)
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        doc_ids = self.list_documents()
        
        return {
            "total_chunks": count,
            "total_documents": len(doc_ids),
            "documents": doc_ids
        }
