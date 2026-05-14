import os
from unittest.mock import MagicMock, patch
import pytest
from backend.rag_engine import RagEngine

def test_pdf_ingestion_and_rolling_chunking(tmp_path):
    # Create a fake PDF file path inside tmp_path matching CCRAS priority source keywords
    pdf_file = tmp_path / "ccras_rare_manuscript_guidelines.pdf"
    pdf_file.write_text("fake binary content")
    
    # Mock pypdf.PdfReader to return mock pages
    mock_page1 = MagicMock()
    # Generate exactly 200 words to test rolling chunking (chunk size 150, overlap 20, step 130)
    # First chunk: words 0 to 150. Second chunk: words 130 to 200 (length 70 words)
    words = [f"word{i}" for i in range(200)]
    mock_page1.extract_text.return_value = " ".join(words[:110])
    
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = " ".join(words[110:])
    
    mock_reader_instance = MagicMock()
    mock_reader_instance.pages = [mock_page1, mock_page2]
    
    with patch("pypdf.PdfReader", return_value=mock_reader_instance):
        engine = RagEngine(data_path=str(tmp_path))
        
        # Verify chunks are created successfully
        assert len(engine.chunks) == 2
        
        # Verify Priority Source mapping resolution
        assert engine.chunks[0]["source"] == "CCRAS/NIIMH AMAR Repository — Rare Manuscripts & Archives"
        assert engine.chunks[1]["source"] == "CCRAS/NIIMH AMAR Repository — Rare Manuscripts & Archives"
        
        # Verify chunking logic word count boundaries
        assert engine.chunks[0]["id"] == "CHUNK_001"
        assert len(engine.chunks[0]["text"].split()) == 150
        assert len(engine.chunks[1]["text"].split()) == 70

def test_empty_and_corrupted_pdf_handling(tmp_path):
    # Test handling of an unreadable/corrupted PDF file
    broken_pdf = tmp_path / "corrupted_archive.pdf"
    broken_pdf.write_text("invalid pdf headers")
    
    # Test handling of an empty/scanned PDF page yielding no text
    empty_pdf = tmp_path / "scanned_image_only.pdf"
    empty_pdf.write_text("fake binary content")
    
    mock_empty_page = MagicMock()
    mock_empty_page.extract_text.return_value = "   " # Pure whitespace
    
    mock_reader_instance = MagicMock()
    mock_reader_instance.pages = [mock_empty_page]
    
    # Simulate pypdf throwing an exception for the broken PDF, but parsing the empty one safely
    def side_effect(path):
        if "corrupted" in str(path):
            raise Exception("File format error")
        return mock_reader_instance

    with patch("pypdf.PdfReader", side_effect=side_effect):
        engine = RagEngine(data_path=str(tmp_path))
        # Complete execution should succeed without crashing, resulting in zero chunks added
        assert len(engine.chunks) == 0

def test_advanced_tokenization_and_scoring(tmp_path):
    # Verify bi-gram retention and length penalty scoring
    sample_txt = tmp_path / "sample_sutra.txt"
    sample_txt.write_text("[CHUNK 1: Test Sutra]\nVyana Vata causes severe vascular resistance.")
    
    engine = RagEngine(data_path=str(tmp_path))
    tokens = engine._tokenize("Vyana Vata causes resistance")
    
    # Assert bi-gram terms are retained alongside unigrams
    assert "vyana vata" in tokens
    assert "vyana" in tokens
    
    # Verify retrieval returns high confidence scores adjusted for chunk density
    results = engine.query("Vyana Vata resistance", top_k=1)
    assert len(results) == 1
    assert results[0]["confidence_score"] > 0.0
