# Vaidya.ai: Intelligent Q&A Assistant for Ayurveda Knowledge

**AI Fusion Challenge Hackathon — Problem Statement 2 Submission**  
**Prototype Track**: Web Application Prototype  
**Design System**: "Sanskrit Premium" Glassmorphism UI  

---

## 1. Project Title and Problem Statement

**Project Title**: Vaidya.ai: Building an Intelligent Q&A Assistant for Ayurveda Knowledge  

**Problem Overview**:  
Ayurveda encompasses a vast body of traditional medical wisdom spanning scriptures, classical books, and botanical research documents. However, this foundational knowledge is often unstructured, highly fragmented, difficult to query, and inaccessible via modern semantic searches. Furthermore, generic Large Language Models frequently hallucinate classical definitions or provide unverified remedies when asked specialized health questions.

**The Challenge & Solution**:  
Our submission designs and implements an advanced AI-powered assistant capable of:
1. **Ingesting classical text blocks** directly from authentic sources (specifically referencing chapters from the *Charaka Samhita*).
2. **Understanding deep contextual attributes** using a dual-layered Hybrid Retrieval Engine.
3. **Answering natural language queries** while adhering strictly to a **zero-hallucination constraint**—synthesizing responses strictly from provided source texts **without relying on external internet lookups**.

---

## 2. Solution Overview & Key Differentiators

Vaidya.ai operates as an absolute domain-specific RAG (Retrieval-Augmented Generation) prototype ensuring utmost clinical safety and authentic verification.

### Core Features & Visual Excellence:
- **Confidence-Tiered Responses**: Automated calculation of high/moderate/low corroboration scores scaling from local distance vector thresholds.
- **Verbatim Source Pins**: Pinning the exact extracted classical reference text snippet directly under the summary so practitioners can independently audit answers.
- **Modern Clinical Parallels**: Translating ancient bio-energetic concepts into equivalent modern biomolecular or homeostatic correlations.
- **Interactive Sanskrit Entity Highlighting**: Automated continuous detection of foundational entities (*Vata*, *Pitta*, *Kapha*, *Haridra*, *Sattva*) to provide inline floating definition drawers.
- **Native Web Speech Integrations**: Voice input querying via microphone and native audio voice synthesis reading verified answers aloud.

---

## Product Screenshots

### Source-Grounded Search
![Vaidya.ai source-grounded search interface](docs/assets/screenshots/01-home-search.png)

### Roadmap Timeline
![Vaidya.ai phased roadmap timeline](docs/assets/screenshots/02-roadmap-timeline.png)

### Roadmap Deep-Dive
![Vaidya.ai roadmap bento detail cards](docs/assets/screenshots/03-roadmap-bento-detail.png)

### Mobile Layout
![Vaidya.ai mobile homepage layout](docs/assets/screenshots/04-mobile-home.png)

---

## 3. Technical Architecture

```
┌────────────────────────────────────────────────────────┐
│                   USER SEARCH QUERY                    │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│             HYBRID RETRIEVAL SEARCH ENGINE             │
│  Dense Vector Similarity Matrix + Sparse BM25 Overlap  │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│            DYNAMIC CONFIDENCE TIER SCORING             │
│  Corroboration Factor Verification (High/Moderate/Low) │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│           STRICT SCHEMA VALIDATION & ROUTING           │
│   Pre-cached Offline Bounds or LLM JSON Synthesis      │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│           GLASSMORPHIC PREMIUM WEB INTERFACE           │
│   Vanilla JS Fetch Layer + Native Speech APIs (TTS)    │
└────────────────────────────────────────────────────────┘
```

### Data Processing & Pipeline Flow:
1. **Ingestion Layer**: Custom chunking splitting domain files into localized 500-token semantic blocks with 50-token overlapping borders.
2. **Hybrid Vector Store**: Inline computation of normalized Term Frequency-Inverse Document Frequency (TF-IDF) float matrices optimized for real-time offline CPU matching, paired seamlessly with standard float vector models.
3. **API Bridge**: Asynchronous Python FastAPI backend exposing aggressive cross-origin routes alongside static front-end mounting.

---

## 4. APIs & Libraries Used

- **FastAPI & Uvicorn**: High-performance asynchronous API web framework serving endpoints and static web routing.
- **OpenAI Client API / OpenRouter Integration**: Used for remote completion parsing under `temperature=0.0` enforcement bounds.
- **Numpy**: Vector operations, cosine similarity array math, and high-speed ranking indices.
- **Pydantic**: Data model serialization and request payload typing.
- **Native Browser APIs**: `window.SpeechRecognition` (Voice-to-Text) and `window.speechSynthesis` (Text-to-Speech) modules.

---

## 5. Steps to Run & Test the Application Locally

### Prerequisites:
Ensure you have **Python 3.10+** installed on your target machine.

### Installation Instructions:
1. Clone the repository repository locally:
   ```bash
   git clone https://github.com/your-username/aivaidya.git
   cd aivaidya
   ```
2. Verify local dependency presence or install core packages:
   ```bash
   pip install fastapi uvicorn pydantic numpy python-dotenv openai
   ```
3. Set up configuration variables:
   Ensure your `.env` file exists at the root path containing:
   ```env
   OPENAI_API_KEY=sk-or-v1-your-key-here
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   LLM_MODEL=openai/gpt-4o-mini
   ```

### Running the Application Engine:
Execute the unified backend and frontend runner natively using Uvicorn:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing the Web Interface:
Open your preferred web browser and navigate directly to:
**`http://localhost:8000`**

---

## 6. Future Scope

- **Multi-Lingual Indic Parsing**: Integrating automated offline translation models to ingest Sanskrit/Devanagari scripts directly and output answers in native local dialects (Kannada, Hindi, Tamil).
- **Botanical Computer Vision Integration**: Adding camera-based image upload feature allowing users to capture physical medicinal herbs and match visual features directly against classical Dravya Guna catalogs.
- **Air-Gapped Embedded Mobile Deployment**: Packaging the optimized offline TF-IDF vector matrices inside native mobile bundles (React Native / Flutter) to allow complete air-gapped field querying for remote healthcare practitioners.
