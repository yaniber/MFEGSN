#!/usr/bin/env python3
"""
Test script to validate the PDF RAG system functionality
"""
import sys
from pathlib import Path
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.pdf_extractor.extractor import PDFExtractor
from src.rag_indexer.indexer import RAGIndexer


def create_sample_pdf():
    """Create a simple test PDF using reportlab if available"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        pdf_path = "pdfs/test_document.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Test Document for PDF RAG System")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, "This is a test document created for validation purposes.")
        c.drawString(100, 700, "")
        c.drawString(100, 680, "Introduction")
        c.drawString(100, 660, "This document contains sample text to test PDF extraction.")
        c.drawString(100, 640, "")
        c.drawString(100, 620, "Methodology")
        c.drawString(100, 600, "We use marker-pdf or PyMuPDF for extraction.")
        c.drawString(100, 580, "")
        c.drawString(100, 560, "References")
        c.drawString(100, 540, "[1] Smith, J. (2023). PDF Processing.")
        c.drawString(100, 520, "[2] Jones, A. (2024). RAG Systems.")
        
        c.save()
        print(f"✓ Created test PDF: {pdf_path}")
        return pdf_path
    except ImportError:
        print("⚠ reportlab not available, skipping PDF creation")
        return None


def test_pdf_extractor():
    """Test PDF extraction functionality"""
    print("\n=== Testing PDF Extractor ===")
    
    try:
        extractor = PDFExtractor()
        print("✓ PDFExtractor initialized")
        
        # Check if test PDF exists or create it
        test_pdf = "pdfs/test_document.pdf"
        if not Path(test_pdf).exists():
            test_pdf = create_sample_pdf()
        
        if test_pdf and Path(test_pdf).exists():
            result = extractor.extract_pdf(test_pdf)
            print(f"✓ PDF extracted successfully")
            print(f"  - Markdown path: {result['markdown_path']}")
            print(f"  - References found: {len(result.get('references', []))}")
            return True
        else:
            print("⚠ No test PDF available, skipping extraction test")
            return None
            
    except Exception as e:
        print(f"✗ Error testing PDF extractor: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_indexer():
    """Test RAG indexing functionality"""
    print("\n=== Testing RAG Indexer ===")
    
    try:
        # Use temporary directory for test database
        with tempfile.TemporaryDirectory() as tmpdir:
            indexer = RAGIndexer(persist_directory=tmpdir)
            print("✓ RAGIndexer initialized")
            
            # Test indexing
            test_content = """
            This is a test document about machine learning.
            Machine learning is a subset of artificial intelligence.
            It focuses on training algorithms to learn patterns from data.
            """
            
            indexer.index_document("test_doc", test_content, {"type": "test"})
            print("✓ Document indexed")
            
            # Test querying
            results = indexer.query("What is machine learning?", n_results=2)
            print(f"✓ Query executed, found {len(results['results'])} results")
            
            # Test listing
            docs = indexer.list_documents()
            assert "test_doc" in docs, "Test document not found in list"
            print(f"✓ Document listing works, found {len(docs)} document(s)")
            
            # Test stats
            stats = indexer.get_collection_stats()
            print(f"✓ Stats retrieved: {stats['total_chunks']} chunks, {stats['total_documents']} docs")
            
            # Test update
            indexer.update_document("test_doc", "Updated content", {"type": "test_updated"})
            print("✓ Document updated")
            
            # Test delete
            indexer.delete_document("test_doc")
            print("✓ Document deleted")
            
            docs_after = indexer.list_documents()
            assert "test_doc" not in docs_after, "Test document still in list after deletion"
            print("✓ Deletion verified")
            
            return True
            
    except Exception as e:
        print(f"✗ Error testing RAG indexer: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test integration of PDF extraction and RAG indexing"""
    print("\n=== Testing Integration ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            extractor = PDFExtractor()
            indexer = RAGIndexer(persist_directory=tmpdir)
            
            test_pdf = "pdfs/test_document.pdf"
            if not Path(test_pdf).exists():
                test_pdf = create_sample_pdf()
            
            if test_pdf and Path(test_pdf).exists():
                # Extract
                result = extractor.extract_pdf(test_pdf)
                print("✓ PDF extracted")
                
                # Index
                doc_id = Path(test_pdf).stem
                indexer.index_document(
                    doc_id=doc_id,
                    content=result["markdown"],
                    metadata={"source": test_pdf}
                )
                print("✓ Content indexed")
                
                # Query
                results = indexer.query("test document", n_results=3)
                print(f"✓ Query successful, found {len(results['results'])} results")
                
                if results['results']:
                    print(f"  - Top result preview: {results['results'][0][:100]}...")
                
                return True
            else:
                print("⚠ No test PDF available, skipping integration test")
                return None
                
    except Exception as e:
        print(f"✗ Error in integration test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_imports():
    """Test that all modules can be imported"""
    print("\n=== Testing Imports ===")
    
    tests = []
    
    try:
        from src.pdf_extractor.extractor import PDFExtractor
        print("✓ PDFExtractor imported")
        tests.append(True)
    except Exception as e:
        print(f"✗ Failed to import PDFExtractor: {e}")
        tests.append(False)
    
    try:
        from src.rag_indexer.indexer import RAGIndexer
        print("✓ RAGIndexer imported")
        tests.append(True)
    except Exception as e:
        print(f"✗ Failed to import RAGIndexer: {e}")
        tests.append(False)
    
    return all(tests)


def main():
    """Run all tests"""
    print("=" * 60)
    print("PDF RAG System Test Suite")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "PDF Extractor": test_pdf_extractor(),
        "RAG Indexer": test_rag_indexer(),
        "Integration": test_integration()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        if result is True:
            status = "✓ PASSED"
        elif result is False:
            status = "✗ FAILED"
        else:
            status = "⚠ SKIPPED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed > 0:
        print("\n⚠ Some tests failed. Please check the errors above.")
        return 1
    else:
        print("\n✓ All tests passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
