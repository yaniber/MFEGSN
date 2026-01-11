"""
PDF Extractor using Marker
Extracts text, figures, and references from PDFs and converts to Markdown
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract content from PDFs using Marker and convert to Markdown"""
    
    def __init__(self, pdf_dir: str = "pdfs", output_dir: str = "markdown_outputs"):
        self.pdf_dir = Path(pdf_dir)
        self.output_dir = Path(output_dir)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract content from a PDF file and convert to Markdown
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing:
                - markdown: The extracted content in Markdown format
                - figures: List of extracted figures
                - references: Extracted references
                - metadata: PDF metadata
        """
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting content from {pdf_file.name}")
        
        try:
            # Import marker modules
            from marker.convert import convert_single_pdf
            from marker.models import load_all_models
            
            # Load models
            model_lst = load_all_models()
            
            # Convert PDF to Markdown
            full_text, images, out_meta = convert_single_pdf(
                str(pdf_file),
                model_lst,
                max_pages=None
            )
            
            # Save markdown output
            output_path = self.output_dir / f"{pdf_file.stem}.md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            # Extract references (simple heuristic - look for References section)
            references = self._extract_references(full_text)
            
            result = {
                "markdown": full_text,
                "markdown_path": str(output_path),
                "figures": images,
                "references": references,
                "metadata": out_meta,
                "source_pdf": str(pdf_file)
            }
            
            logger.info(f"Successfully extracted content to {output_path}")
            return result
            
        except ImportError:
            # Fallback to PyMuPDF if marker is not available
            logger.warning("Marker not available, using PyMuPDF fallback")
            return self._extract_with_pymupdf(pdf_file)
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            raise
    
    def _extract_with_pymupdf(self, pdf_file: Path) -> Dict[str, any]:
        """Fallback extraction using PyMuPDF"""
        if not PYMUPDF_AVAILABLE:
            raise ImportError("PyMuPDF is not installed. Install it with: pip install PyMuPDF")
        
        doc = fitz.open(pdf_file)
        full_text = ""
        
        for page_num, page in enumerate(doc):
            text = page.get_text()
            full_text += f"\n\n## Page {page_num + 1}\n\n{text}"
        
        # Save markdown output
        output_path = self.output_dir / f"{pdf_file.stem}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        references = self._extract_references(full_text)
        
        return {
            "markdown": full_text,
            "markdown_path": str(output_path),
            "figures": [],
            "references": references,
            "metadata": {"pages": len(doc)},
            "source_pdf": str(pdf_file)
        }
    
    def _extract_references(self, text: str) -> List[str]:
        """Extract references from text (simple heuristic)"""
        references = []
        lines = text.split("\n")
        
        in_references = False
        for line in lines:
            line_lower = line.lower().strip()
            if "references" in line_lower or "bibliography" in line_lower:
                in_references = True
                continue
            
            if in_references and line.strip():
                # Simple check: references often start with [1], [2] or numbers
                if line.strip()[0].isdigit() or line.strip().startswith("["):
                    references.append(line.strip())
        
        return references
    
    def extract_all_pdfs(self) -> List[Dict[str, any]]:
        """Extract all PDFs in the pdf directory"""
        results = []
        for pdf_file in self.pdf_dir.glob("*.pdf"):
            try:
                result = self.extract_pdf(str(pdf_file))
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to extract {pdf_file}: {e}")
        
        return results
