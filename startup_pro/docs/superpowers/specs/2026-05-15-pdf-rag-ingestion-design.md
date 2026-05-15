# Specification: PDF Ingestion and Rolling Chunking Pipeline for Offline RAG Engine

## 1. Overview
This specification details the design and data flow for enabling pure-Python PDF document extraction, rolling chunking, and unified vector ingestion inside the Vaidya.ai custom offline RAG engine. By extending the existing dataset scanning mechanics, the platform will seamlessly parse and query traditional medical texts supplied in standard PDF formats alongside pre-processed text archives.

## 2. Architecture & Pipeline Integration

### 2.1 Dependencies
- **Library**: `pypdf` (Pure Python library selected to eliminate native C-extension compilation risks and guarantee maximum portability across host environments).

### 2.2 Ingestion & Processing Flow
- **File Discovery**: The `RagEngine.load_and_process_data()` method scans the target `data/` path to detect all valid files ending with either `.txt` or `.pdf`.
- **Source Naming Resolution**: Derives professional, domain-aware source headers from PDF basenames mirroring the text index logic:
  - References containing "Charaka" map to "Charaka Samhita — Sutrasthana".
  - References containing "Sushruta" map to "Sushruta Samhita — Core Archives".
  - References containing "Ayush" map to "Ministry of AYUSH — Standard Treatment Guidelines".
  - References containing "Nia" or "Bams" map to "National Institute of Ayurveda — Academic Curriculum".
  - General files map to `Vaidya.ai Source Index ({basename})`.

### 2.3 Extraction & Rolling Chunking Mechanics
- **Reader Initialization**: Opens detected `.pdf` files in binary read mode (`'rb'`) via `pypdf.PdfReader`.
- **Text Accumulation**: Iterates sequentially over all document pages, accumulating extracted plain text strings while cleaning non-standard inline line breaks and extra whitespace.
- **Rolling Window Logic**: 
  - Tokenizes the cleaned continuous text string into sequential individual words.
  - Generates rolling context chunks of exactly **150 words** each.
  - Applies a **20-word rolling overlap** step back between consecutive chunks. This guarantees that semantic concepts spanning chunk boundaries are preserved intact for accurate vector similarity recall.
- **Schema Mapping**: Appends each generated block directly into the internal `self.chunks` list formatted as:
  ```json
  {
    "id": "CHUNK_XXX",
    "title": "Document Excerpt (Page/Section Context)",
    "text": "<extracted rolling word block>",
    "source": "<resolved source name>"
  }
  ```
- **Vectorization Compatibility**: The existing downstream TF-IDF analyzer (`_build_tfidf_index()`) seamlessly indexes these populated dictionary records without requiring schema adjustments.

## 3. Error Handling & Edge Cases
- **Corrupted/Encrypted Documents**: Wraps individual PDF extraction blocks in a `try...except` block. Exceptions log descriptive console warnings without throwing uncaught runtime errors, allowing valid documents to initialize successfully.
- **Image-Only/Scanned PDFs**: Pages yielding empty strings or pure whitespace strings are safely bypassed to maintain matrix density.

## 4. Verification & Testing Strategy
- **Ingestion Audit**: Confirm that processing a PDF file correctly outputs uniform, continuous, overlapping dictionaries inside `self.chunks`.
- **Retrieval Integrity**: Execute search queries using highly localized terms embedded inside uploaded PDF documents to verify retrieval ranking accuracy, score calculations, and verbatim source pin displays.
