#!/usr/bin/env python3
"""
Example script demonstrating PDF extraction and RAG indexing
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer


def main():
    """Main function demonstrating the workflow"""
    
    # Initialize components
    print("Initializing PDF Extractor and RAG Indexer...")
    extractor = PDFExtractor()
    indexer = RAGIndexer()
    
    # Example 1: Extract a single PDF
    print("\n=== Example 1: Extract Single PDF ===")
    pdf_path = "pdfs/example.pdf"
    
    if Path(pdf_path).exists():
        result = extractor.extract_pdf(pdf_path)
        print(f"✓ Extracted to: {result['markdown_path']}")
        print(f"✓ Found {len(result.get('references', []))} references")
        
        # Index the document
        doc_id = Path(pdf_path).stem
        indexer.index_document(
            doc_id=doc_id,
            content=result["markdown"],
            metadata={
                "source": pdf_path,
                "markdown_path": result["markdown_path"]
            }
        )
        print(f"✓ Indexed document: {doc_id}")
    else:
        print(f"⚠ PDF not found: {pdf_path}")
        print(f"  Place a PDF file in the 'pdfs' directory to test extraction")
    
    # Example 2: Extract all PDFs
    print("\n=== Example 2: Extract All PDFs ===")
    pdf_files = list(Path("pdfs").glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF(s)")
    
    for pdf_file in pdf_files:
        try:
            result = extractor.extract_pdf(str(pdf_file))
            doc_id = pdf_file.stem
            
            indexer.index_document(
                doc_id=doc_id,
                content=result["markdown"],
                metadata={"source": str(pdf_file)}
            )
            print(f"✓ Processed: {pdf_file.name}")
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")
    
    # Example 3: Query the indexed documents
    print("\n=== Example 3: Query Documents ===")
    
    # Get collection stats
    stats = indexer.get_collection_stats()
    print(f"Total documents: {stats['total_documents']}")
    print(f"Total chunks: {stats['total_chunks']}")
    
    if stats['total_documents'] > 0:
        # Example queries
        queries = [
            "What is the main topic?",
            "Explain the methodology",
            "What are the key findings?"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            results = indexer.query(query, n_results=3)
            
            if results['results']:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['results'],
                    results['metadatas'],
                    results['distances']
                ), 1):
                    relevance = 1 - distance
                    print(f"\n  Result {i} (relevance: {relevance:.3f}):")
                    print(f"    Document: {metadata.get('doc_id', 'unknown')}")
                    print(f"    Preview: {doc[:150]}...")
            else:
                print("  No results found")
    else:
        print("No documents indexed yet. Add PDFs to the 'pdfs' directory and run this script again.")
    
    # Example 4: List all documents
    print("\n=== Example 4: List All Documents ===")
    documents = indexer.list_documents()
    if documents:
        for doc in documents:
            print(f"  - {doc}")
    else:
        print("  No documents indexed")


if __name__ == "__main__":
    main()
