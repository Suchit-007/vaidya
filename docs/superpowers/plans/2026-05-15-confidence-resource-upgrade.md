# Confidence & Resource Transparency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Elevate query confidence through authoritative Ayurvedic data ingestion and implement a clinical-grade "Resource Verification" UI.

**Architecture:** 
1. **Knowledge Expansion**: Inject high-fidelity context for *Yogavahi* and *Anupana* from classical texts (*Bruhatrayi* and *Laghutrayi*) into the RAG engine's fallback and primary search paths.
2. **Resource UI**: A new `ResourceVerification` module using a "Clinical Sidebar" pattern to display active bibliography and source anchors for each response.

**Tech Stack:** FastAPI (Backend), Vanilla JS/CSS (Frontend), Lucide/Isax Icons.

---

### Task 1: Knowledge Ingestion & Confidence Refinement
**Files:**
- Modify: `backend/main.py`
- Modify: `frontend/app.js`

- [ ] **Step 1: Expand Fallback Logic for Bio-availability**
   Inject authoritative definitions for *Yogavahi* (catalytic enhancers) and *Anupana* (vehicles) derived from *Sharangadhara Samhita*.
   
- [ ] **Step 2: Update Confidence Tier**
   Shift the "bio-availability" response from `LOW` to `HIGH` confidence once the authoritative mapping is verified.

- [ ] **Step 3: Fix 500 Error in Fallback**
   Correct the `RoadmapResponse` fallback schema in `backend/main.py` to use `phases` list instead of `phase_1` etc.

### Task 2: "Resource Library" UI Design
**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/styles.css`
- Modify: `frontend/app.js`

- [ ] **Step 1: Design the "Source Verification" Sidebar**
   Create a bento-style card in `index.html` that lists primary texts and clinical status.
   
- [ ] **Step 2: Implement "Resource Toggle"**
   Add a button in the response footer labeled "View Clinical Sources" that unrolls the resource list.

### Task 3: Data Mapping & Verification
**Files:**
- Modify: `backend/main.py`
- Modify: `frontend/app.js`

- [ ] **Step 1: Update API Response Schema**
   Add a `sources` array to the query response containing `text_name`, `author`, and `relevance_score`.

- [ ] **Step 2: Frontend Data Binding**
   Update `renderResponse` in `app.js` to map this new `sources` array to the UI.
