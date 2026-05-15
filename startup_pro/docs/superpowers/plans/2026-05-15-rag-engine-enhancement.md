# Advanced RAG Engine Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enhance the deterministic Vaidya.ai RAG retrieval pipeline by integrating BM25-style document length normalization, bi-gram semantic concept preservation, and optional automated deep-research synthesis routing.

**Architecture:** We extend the current custom TF-IDF matrix generation by applying document length scaling to prevent long chunks from disproportionately outweighing dense, compact classical sutras. Additionally, we update the tokenizer to preserve multi-word Ayurvedic concepts (e.g., 'vyana vata') as unified bi-gram tokens, and expose an optional research routing flag to leverage Gemini Deep Research for cross-disciplinary clinical mechanism syntheses.

**Tech Stack:** Python 3.10+, NumPy, pypdf, httpx (for Deep Research API integrations)

---

### Task 1: Advanced Term Tokenization and BM25-Style Normalization

**Files:**
- Modify: `backend/rag_engine.py:61-75`
- Modify: `tests/test_pdf_ingestion.py:1-40`

- [ ] **Step 1: Write the failing test**

Modify `tests/test_pdf_ingestion.py` to assert that bi-gram phrases are successfully tokenized and scored correctly under length normalization.

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: FAIL due to missing `test_advanced_tokenization_and_scoring` bi-gram tokens in the base tokenizer implementation.

- [ ] **Step 3: Write minimal implementation**

Update `backend/rag_engine.py` to extract consecutive unigram pairs as bi-grams and scale TF-IDF vectors by document length averages.

```python
    def _tokenize(self, text: str) -> List[str]:
        """Enhanced tokenization capturing unigrams and consecutive bi-gram classical concepts."""
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        return words + bigrams

    def _build_tfidf_index(self):
        """Constructs an enhanced TF-IDF matrix scaled by document length normalization."""
        self.vocab = {}
        if not self.chunks:
            self.tf_idf_matrix = np.array([])
            return

        # Map complete vocabulary set
        for chunk in self.chunks:
            tokens = self._tokenize(chunk["text"])
            for t in tokens:
                if t not in self.vocab:
                    self.vocab[t] = len(self.vocab)

        num_docs = len(self.chunks)
        vocab_size = len(self.vocab)
        tf_matrix = np.zeros((num_docs, vocab_size))
        doc_lengths = np.zeros(num_docs)

        # Compute raw term frequencies and document lengths
        for idx, chunk in enumerate(self.chunks):
            tokens = self._tokenize(chunk["text"])
            doc_lengths[idx] = len(tokens)
            for t in tokens:
                if t in self.vocab:
                    tf_matrix[idx, self.vocab[t]] += 1

        # Calculate average document length for BM25-style scaling
        avg_doc_len = np.mean(doc_lengths) if num_docs > 0 and np.sum(doc_lengths) > 0 else 1.0
        
        # Calculate Inverse Document Frequency (IDF) smoothly
        doc_freq = np.sum(tf_matrix > 0, axis=0)
        self.idf = np.log((1 + num_docs) / (1 + doc_freq)) + 1

        # Apply term frequency scaling normalized by document length ratio (b=0.75 scaling factor)
        b = 0.75
        length_penalty = 1.0 - b + b * (doc_lengths / avg_doc_len)
        length_penalty = np.maximum(length_penalty, 0.1)[:, np.newaxis]
        
        normalized_tf = tf_matrix / length_penalty
        self.tf_idf_matrix = normalized_tf * self.idf
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: PASS cleanly across all tokenization and vectorization steps.

- [ ] **Step 5: Commit**

```bash
git add backend/rag_engine.py tests/test_pdf_ingestion.py
git commit -m "feat: implement bi-gram terminology tokenization and BM25 document length normalization"
```

---

### Task 2: Deep Research Hook & Metadata Source Pre-Filtering

**Files:**
- Modify: `backend/rag_engine.py:100-140`
- Modify: `backend/main.py:40-80`

- [ ] **Step 1: Write the failing test**

Add verification for source filtering and research stub payload handling.

```python
def test_source_filtering_and_research_hook(tmp_path):
    sample_txt = tmp_path / "sample_charaka.txt"
    sample_txt.write_text("[CHUNK 1: Specific Sutra]\nTreat inflammation with standardized herbs.")
    
    engine = RagEngine(data_path=str(tmp_path))
    
    # Assert targeting specific non-existent source yields empty list
    empty_res = engine.query("inflammation", target_source="Nonexistent Source")
    assert len(empty_res) == 0
    
    # Assert query execution correctly passes research triggers
    res = engine.query("deep research mechanism of turmeric", top_k=1)
    assert len(res) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: FAIL due to missing `target_source` keyword parameter in `RagEngine.query`.

- [ ] **Step 3: Write minimal implementation**

Update `query()` method in `backend/rag_engine.py` to support pre-filtering by source string matching and trigger optional Deep Research summary structures.

```python
    def query(self, query_str: str, top_k: int = 3, target_source: str = None) -> List[Dict[str, Any]]:
        """Retrieves top semantic matches using cosine similarity against the normalized TF-IDF matrix."""
        if not self.chunks or not self.vocab:
            return []

        query_tokens = self._tokenize(query_str)
        query_vector = np.zeros(len(self.vocab))
        for t in query_tokens:
            if t in self.vocab:
                query_vector[self.vocab[t]] += 1

        # Apply IDF weights to query vector
        query_vector = query_vector * self.idf
        norm_q = np.linalg.norm(query_vector)
        if norm_q == 0:
            return []

        scores = []
        for idx in range(len(self.chunks)):
            # Filter by target source string prefix/substring if specified
            if target_source and target_source.lower() not in self.chunks[idx]["source"].lower():
                scores.append(-1.0)
                continue
                
            doc_vector = self.tf_idf_matrix[idx]
            norm_d = np.linalg.norm(doc_vector)
            if norm_d == 0:
                scores.append(0.0)
            else:
                sim = np.dot(query_vector, doc_vector) / (norm_q * norm_d)
                scores.append(float(sim))

        top_indices = np.argsort(scores)[::-1]
        results = []
        for idx in top_indices:
            if scores[idx] <= 0.05 or len(results) >= top_k:
                break
                
            chunk_copy = self.chunks[idx].copy()
            chunk_copy["confidence_score"] = scores[idx]
            
            # Embed Deep Research mechanism metadata reference if triggered
            if "deep research" in query_str.lower() or "mechanism" in query_str.lower():
                chunk_copy["research_synthesis_available"] = True
                chunk_copy["research_trigger_command"] = f"python3 scripts/research.py --query 'Clinical biomolecular mechanism correlation for: {chunk_copy['title']}' --json"
            else:
                chunk_copy["research_synthesis_available"] = False
                
            results.append(chunk_copy)

        return results
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_pdf_ingestion.py -v`
Expected: PASS successfully validating source constraint filters and metadata generation.

- [ ] **Step 5: Commit**

```bash
git add backend/rag_engine.py
git commit -m "feat: enable query targeting by source indexing and map autonomous deep research triggers"
```
