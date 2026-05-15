import os
import sys
from io import BytesIO

# Add project root to sys.path for direct imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pdf_generator import generate_analysis_pdf

def test_pdf_generation_integrity():
    """Verifies that the PDF generator produces a non-empty buffer for standard data."""
    test_data = {
        "answer": "Essential hypertension manage with Sarpagandha.",
        "confidence_tier": "HIGH",
        "corroborating_chunks": 3,
        "source_text": "Ministry of AYUSH",
        "source_line": "Sarpagandha root powder is indicated.",
        "modern_parallel": "Reserpine depletes catecholamines.",
        "extracted_entities": [
            {"term": "Sarpagandha", "definition": "Rauwolfia serpentina root."}
        ]
    }
    
    print("Testing PDF generation...")
    try:
        buffer = generate_analysis_pdf(test_data)
        assert isinstance(buffer, BytesIO)
        content = buffer.getvalue()
        assert len(content) > 1000 # Minimum size for a basic ReportLab PDF
        assert b"%PDF" in content # PDF Header check
        print(f"SUCCESS: PDF generated successfully ({len(content)} bytes).")
    except Exception as e:
        print(f"FAILED: PDF generation crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_pdf_generation_integrity()
