# PDF RAG Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement pure-Python PDF text extraction, priority source repository mapping, and rolling word chunking to seamlessly ingest PDF documents into the local hybrid TF-IDF vector matrix.

**Architecture:** Update `RagEngine.load_and_process_data()` to identify both `.txt` and `.pdf` files. Extract clean continuous text across PDF pages using `pypdf.PdfReader`, resolve advanced source titles using priority domain keywords, and split accumulated words into rolling chunks of 150 words with a 20-word overlap for high retrieval recall.

**Tech Stack:** Python 3.10+, `pypdf`, `pytest`, `unittest.mock`

---

### Task 1: Core PDF Ingestion Engine and Priority Source Mappings

**Files:**
- Create: `tests/test_pdf_ingestion.py`
- Modify: `backend/rag_engine.py:1-6`
- Modify: `backend/rag_engine.py:16-60`
- Test: `tests/test_pdf_ingestion.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: FAIL with `assert len(engine.chunks) == 2` failing because `len(engine.chunks)` evaluates to `0` (PDFs currently ignored).

- [ ] **Step 3: Write minimal implementation**

Modify `backend/rag_engine.py` lines 1-6 to include `pypdf`:
```python
import os
import re
import math
import numpy as np
from typing import List, Dict, Any
import pypdf
```

Modify `backend/rag_engine.py` lines 16-60 to implement PDF scanning, priority source routing, and rolling chunking:
```python
    def load_and_process_data(self):
        """Loads dataset files and splits them into semantic multi-document blocks."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Target path not found at {self.data_path}")

        files_to_process = []
        if os.path.isdir(self.data_path):
            for filename in sorted(os.listdir(self.data_path)):
                if filename.endswith(".txt") or filename.endswith(".pdf"):
                    files_to_process.append(os.path.join(self.data_path, filename))
        else:
            files_to_process.append(self.data_path)

        self.chunks = []
        for file_path in files_to_process:
            is_pdf = file_path.endswith(".pdf")
            basename = os.path.basename(file_path).replace(".txt", "").replace(".pdf", "").replace("_", " ").title()

            # Determine source baseline name mapping explicit user priority sources
            if "Ccras" in basename or "Niimh" in basename or "Amar" in basename or "Manuscript" in basename or "Rare" in basename:
                source_name = "CCRAS/NIIMH AMAR Repository — Rare Manuscripts & Archives"
            elif "Apta" in basename:
                source_name = "APTA Digital Library — Classical Archives"
            elif "Charaka" in basename:
                if "Online" in basename or "Culture" in basename or "Ebook" in basename or "E-Book" in basename:
                    source_name = "Charaka Samhita Online / Indian Culture Authoritative e-Books"
                else:
                    source_name = "Charaka Samhita — Sutrasthana"
            elif "Sushruta" in basename:
                source_name = "Sushruta Samhita — Core Archives"
            elif "Ayush" in basename:
                source_name = "Ministry of AYUSH — Standard Treatment Guidelines"
            elif "Nia" in basename or "Bams" in basename:
                source_name = "National Institute of Ayurveda — Academic Curriculum"
            elif "Archive" in basename or "Dli" in basename or "Scanned" in basename:
                source_name = "Internet Archive / Digital Library of India Scanned Archives"
            else:
                source_name = f"Vaidya.ai Source Index ({basename})"

            if is_pdf:
                reader = pypdf.PdfReader(file_path)
                full_text = []
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        full_text.append(extracted)
                combined_text = " ".join(full_text)
                combined_text = re.sub(r'\s+', ' ', combined_text).strip()
                
                words = combined_text.split()
                chunk_size = 150
                overlap = 20
                step = chunk_size - overlap
                
                if words:
                    for idx in range(0, len(words), step):
                        chunk_words = words[idx:idx + chunk_size]
                        chunk_text = " ".join(chunk_words)
                        if len(chunk_words) >= 10 or idx == 0:
                            self.chunks.append({
                                "id": f"CHUNK_{len(self.chunks)+1:03d}",
                                "title": f"{basename} (Excerpt {idx//step + 1})",
                                "text": chunk_text,
                                "source": source_name
                            })
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                raw_chunks = re.split(r'\[CHUNK \d+: ([^\]]+)\]', content)
                for i in range(1, len(raw_chunks), 2):
                    title = raw_chunks[i].strip()
                    text = raw_chunks[i+1].strip() if i+1 < len(raw_chunks) else ""
                    if text:
                        self.chunks.append({
                            "id": f"CHUNK_{len(self.chunks)+1:03d}",
                            "title": title,
                            "text": text,
                            "source": source_name
                        })

        self._build_tfidf_index()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_pdf_ingestion.py backend/rag_engine.py
git commit -m "feat: implement PDF document ingestion and priority source mappings"
```

---

### Task 2: Edge Case Resilience and Empty Page Handling

**Files:**
- Modify: `tests/test_pdf_ingestion.py`
- Modify: `backend/rag_engine.py:53-70`
- Test: `tests/test_pdf_ingestion.py`

- [ ] **Step 1: Write the failing test**

Append the following test case to `tests/test_pdf_ingestion.py` to verify graceful exception handling for broken PDFs and skipped empty pages:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: FAIL due to unhandled exceptions when processing corrupted PDF paths without a `try...except` block.

- [ ] **Step 3: Write minimal implementation**

Update the PDF processing block in `backend/rag_engine.py` to wrap `pypdf.PdfReader` initialization in a `try...except` block:
```python
            if is_pdf:
                try:
                    reader = pypdf.PdfReader(file_path)
                    full_text = []
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted and extracted.strip():
                            full_text.append(extracted.strip())
                    
                    if not full_text:
                        continue
                        
                    combined_text = " ".join(full_text)
                    combined_text = re.sub(r'\s+', ' ', combined_text).strip()
                    
                    words = combined_text.split()
                    chunk_size = 150
                    overlap = 20
                    step = chunk_size - overlap
                    
                    if words:
                        for idx in range(0, len(words), step):
                            chunk_words = words[idx:idx + chunk_size]
                            chunk_text = " ".join(chunk_words)
                            if len(chunk_words) >= 10 or idx == 0:
                                self.chunks.append({
                                    "id": f"CHUNK_{len(self.chunks)+1:03d}",
                                    "title": f"{basename} (Excerpt {idx//step + 1})",
                                    "text": chunk_text,
                                    "source": source_name
                                })
                except Exception as e:
                    print(f"Warning: Intercepted PDF parsing failure for {file_path}: {e}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_pdf_ingestion.py backend/rag_engine.py
git commit -m "fix: add robust try-except error resilience and empty PDF page skipping"
```
