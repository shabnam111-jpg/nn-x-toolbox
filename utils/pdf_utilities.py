"""
PDF Processing Utilities for Palm Reading Knowledge Base
Extracts and processes palm reading information from PDFs.
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

# ═════════════════════════════════════════════════════════════════════════════
# OPTIONAL IMPORTS - GRACEFUL FALLBACK
# ═════════════════════════════════════════════════════════════════════════════

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    logger.warning("PyPDF2 not installed. PDF text extraction will be limited.")

try:
    from pdf2image import convert_from_path
    HAS_PDF2IMAGE = True
except ImportError:
    HAS_PDF2IMAGE = False
    logger.warning("pdf2image not installed. Image extraction from PDFs will be disabled.")

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False
    logger.warning("PyMuPDF not installed. Advanced PDF processing will be limited.")

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

PDF_EXTRACT_DIR = Path(__file__).parent.parent / "assets" / "extracted"

# ═════════════════════════════════════════════════════════════════════════════
# CORE PDF FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def check_pdf_valid(pdf_path: str) -> Dict[str, any]:
    """
    Check if a PDF file is valid and readable.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Dictionary with validation results
    """
    pdf_file = Path(pdf_path)
    
    result = {
        'valid': False,
        'exists': pdf_file.exists(),
        'readable': False,
        'pages': 0,
        'size_mb': 0,
        'message': '',
    }
    
    if not result['exists']:
        result['message'] = f"PDF file not found: {pdf_path}"
        return result
    
    try:
        result['size_mb'] = round(pdf_file.stat().st_size / (1024 * 1024), 2)
        
        if HAS_PYPDF2:
            try:
                with open(pdf_file, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    result['pages'] = len(reader.pages)
                    result['readable'] = True
                    result['valid'] = True
                    result['message'] = f"✓ Valid PDF with {result['pages']} pages"
            except Exception as e:
                result['message'] = f"PyPDF2 Error: {str(e)}"
        
        elif HAS_FITZ:
            try:
                doc = fitz.open(pdf_file)
                result['pages'] = len(doc)
                result['readable'] = True
                result['valid'] = True
                result['message'] = f"✓ Valid PDF with {result['pages']} pages"
                doc.close()
            except Exception as e:
                result['message'] = f"PyMuPDF Error: {str(e)}"
        else:
            result['message'] = "No PDF library available"
    
    except Exception as e:
        result['message'] = f"Error checking PDF: {str(e)}"
    
    return result

def extract_text_from_pdf(pdf_path: str, max_pages: Optional[int] = None) -> Optional[str]:
    """
    Extract all text from a PDF file.
    
    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum number of pages to extract (None = all)
    
    Returns:
        Extracted text or None
    """
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        logger.error(f"PDF not found: {pdf_path}")
        return None
    
    extracted_text = ""
    
    # Try PyPDF2 first (most compatible)
    if HAS_PYPDF2:
        try:
            with open(pdf_file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages_to_extract = min(len(reader.pages), max_pages or len(reader.pages))
                
                for page_num in range(pages_to_extract):
                    page = reader.pages[page_num]
                    extracted_text += f"\n--- Page {page_num + 1} ---\n"
                    extracted_text += page.extract_text()
            
            logger.info(f"✓ Extracted text from {pages_to_extract} pages")
            return extracted_text
        
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
    
    # Fallback to PyMuPDF
    if HAS_FITZ and not extracted_text:
        try:
            doc = fitz.open(pdf_file)
            pages_to_extract = min(len(doc), max_pages or len(doc))
            
            for page_num in range(pages_to_extract):
                page = doc[page_num]
                extracted_text += f"\n--- Page {page_num + 1} ---\n"
                extracted_text += page.get_text()
            
            doc.close()
            logger.info(f"✓ Extracted text from {pages_to_extract} pages using PyMuPDF")
            return extracted_text
        
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
    
    if not extracted_text:
        logger.warning("Could not extract text - no PDF library available")
    
    return extracted_text if extracted_text else None

def extract_images_from_pdf(pdf_path: str, output_dir: Optional[str] = None) -> List[str]:
    """
    Extract images from a PDF file.
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save extracted images (uses default if None)
    
    Returns:
        List of paths to extracted images
    """
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        logger.error(f"PDF not found: {pdf_path}")
        return []
    
    output_dir = Path(output_dir or PDF_EXTRACT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    extracted_images = []
    
    # Try pdf2image first
    if HAS_PDF2IMAGE:
        try:
            images = convert_from_path(pdf_file)
            for idx, image in enumerate(images):
                image_path = output_dir / f"page_{idx+1}.png"
                image.save(image_path, 'PNG')
                extracted_images.append(str(image_path))
            
            logger.info(f"✓ Extracted {len(extracted_images)} images using pdf2image")
            return extracted_images
        
        except Exception as e:
            logger.error(f"pdf2image extraction failed: {e}")
    
    # Fallback to PyMuPDF
    if HAS_FITZ and not extracted_images:
        try:
            doc = fitz.open(pdf_file)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_idx, img in enumerate(image_list):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    image_path = output_dir / f"page_{page_num+1}_img_{img_idx+1}.png"
                    pix.save(image_path)
                    extracted_images.append(str(image_path))
            
            doc.close()
            logger.info(f"✓ Extracted {len(extracted_images)} images using PyMuPDF")
            return extracted_images
        
        except Exception as e:
            logger.error(f"PyMuPDF image extraction failed: {e}")
    
    if not extracted_images:
        logger.warning("Could not extract images - no PDF library available")
    
    return extracted_images

# ═════════════════════════════════════════════════════════════════════════════
# HIGH-LEVEL PROCESSING FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def process_palm_reading_pdf(pdf_path: str) -> Dict:
    """
    Process a palm reading PDF comprehensively.
    Extracts text, images, and validates content.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Dictionary with processing results
    """
    logger.info(f"Processing palm reading PDF: {pdf_path}")
    
    result = {
        'success': False,
        'pdf_path': pdf_path,
        'validation': None,
        'text': None,
        'images': [],
        'error': None,
    }
    
    # Validate PDF
    result['validation'] = check_pdf_valid(pdf_path)
    if not result['validation']['valid']:
        result['error'] = result['validation']['message']
        return result
    
    # Extract text
    text_content = extract_text_from_pdf(pdf_path)
    if text_content:
        result['text'] = text_content
        logger.info(f"✓ Successfully extracted text content")
    
    # Extract images
    images = extract_images_from_pdf(pdf_path)
    if images:
        result['images'] = images
        logger.info(f"✓ Successfully extracted {len(images)} images")
    
    result['success'] = True
    logger.info("✓ PDF processing completed successfully")
    
    return result

def parse_palmistry_knowledge(text_content: str) -> Dict[str, List[str]]:
    """
    Parse extracted text for palmistry knowledge patterns.
    
    Args:
        text_content: Raw text extracted from PDF
    
    Returns:
        Dictionary with categorized knowledge
    """
    knowledge = {
        'lines': [],
        'mounts': [],
        'meanings': [],
        'health_indicators': [],
        'personality': [],
    }
    
    if not text_content:
        return knowledge
    
    lines = text_content.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        
        # Detect line readings
        if any(x in line_lower for x in ['life line', 'head line', 'heart line', 'fate line', 'mercury line']):
            knowledge['lines'].append(line.strip())
        
        # Detect mount readings
        if any(x in line_lower for x in ['mount of', 'jupiter', 'saturn', 'apollo', 'mercury', 'venus', 'luna', 'mars']):
            knowledge['mounts'].append(line.strip())
        
        # Detect meanings/interpretations
        if any(x in line_lower for x in ['means', 'indicates', 'represents', 'suggests', 'shows']):
            knowledge['meanings'].append(line.strip())
        
        # Detect health information
        if any(x in line_lower for x in ['health', 'disease', 'illness', 'medical', 'physical']):
            knowledge['health_indicators'].append(line.strip())
        
        # Detect personality info
        if any(x in line_lower for x in ['personality', 'character', 'trait', 'temperament', 'nature']):
            knowledge['personality'].append(line.strip())
    
    logger.info(f"✓ Parsed knowledge: {len(knowledge['lines'])} lines, {len(knowledge['mounts'])} mounts")
    return knowledge

# ═════════════════════════════════════════════════════════════════════════════
# STATUS & DIAGNOSTICS
# ═════════════════════════════════════════════════════════════════════════════

def get_pdf_utilities_status() -> Dict:
    """Get status of PDF processing utilities."""
    return {
        'module': 'PDF Utilities',
        'version': '1.0.0',
        'pypdf2_available': HAS_PYPDF2,
        'pdf2image_available': HAS_PDF2IMAGE,
        'fitz_available': HAS_FITZ,
        'extract_dir': str(PDF_EXTRACT_DIR),
    }
