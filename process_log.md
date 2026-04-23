# process_log.md
## AIMS KTT Hackathon — T2.2
### Multilingual Grant & Tender Matcher

---

## ⏱️ Timeline (10:00 AM – 2:45 PM)

### 10:00 – 10:30 | Review & Understanding
- Carefully reviewed the challenge requirements
- Understood deliverables:
  - matching system
  - evaluation metrics (MRR, Recall)
  - product adaptation (village agent)
  - demo + documentation
- Analyzed dataset structure:
  - tenders
  - profiles
  - gold matches

---

### 10:30 – 11:15 | Data Processing & Parsing
- Built parsing pipeline for:
  - PDF
  - HTML
  - TXT
- Extracted structured fields:
  - sector
  - region
  - budget
  - deadline
- Added language detection (EN/FR)
- Normalized text for consistent processing

---

### 11:15 – 12:00 | Matching System Development
- Implemented BM25 ranking (primary retrieval)
- Added TF-IDF scoring for support
- Combined scoring with:
  - keyword relevance
  - sector match boost
  - region match boost
- Added cross-lingual handling (FR → EN normalization)
- Built ranking pipeline for top-k retrieval

---

### 12:00 – 12:45 | Evaluation & Debugging
- Implemented evaluation metrics:
  - MRR@5
  - Recall@5
- Fixed matching issues:
  - tender ID mismatch
  - ranking inconsistencies
- Achieved:
  - MRR@5 = 0.7167
  - Recall@5 = 0.5667
- Validated results against baseline

---

### 12:45 – 1:15 | Product Design (Village Agent)
- Designed real-world deployment model:
  - WhatsApp audio delivery
- Defined:
  - weekly operational workflow
  - cost model
  - CAC (Cost per Activated Cooperative)
- Focused on:
  - low literacy users
  - low bandwidth environments
  - multilingual access

---

### 1:15 – 2:00 | Demo Development (UI + Deployment)
- Built Gradio interface:
  - profile selection (dropdown)
  - top-k control
  - results table
  - profile summary
- Improved UI using Gradio Blocks:
  - clean layout
  - better interaction
  - structured display
- Prepared Hugging Face Space deployment

---

### 2:00 – 2:30 | Deployment & Integration
- Deployed app to Hugging Face Space
- Debugged runtime issues:
  - dataset not found error
  - .gitignore blocking dataset
- Fixed:
  - dataset upload
  - repository structure
- Verified working live demo

---

### 2:30 – 2:45 | Finalization & Submission
- Completed documentation:
  - README.md
  - process_log.md
  - village_agent.md
- Verified:
  - evaluation results
  - UI functionality
  - deployment link
- Submitted final project

---

## 🛠️ Tools Used

- **Cursor** → development & file management  
- **ChatGPT** → debugging, structuring, explanations  
- **Google Colab** → evaluation notebook  
- **GitHub** → version control  
- **Hugging Face Spaces** → deployment  

---

## 💬 Key Prompts Used

1. "How to implement BM25 ranking in Python?"
2. "Explain MRR@5 and Recall@5 with examples"
3. "How to combine TF-IDF and BM25 effectively?"
4. "Design a system for low-literacy users in Africa"

---

## ❌ Discarded Approach

### LLM-based semantic ranking

**Reason:**
- Too slow for CPU-only constraint
- Unnecessary complexity
- Violates runtime efficiency requirement

---

## 🧠 Key Decision

### BM25 + TF-IDF vs Embeddings

**Chosen:** BM25 + TF-IDF

**Why:**
- Faster
- More explainable
- Works well on structured dataset
- Meets time and resource constraints

---

## 📊 Final Outcome

- MRR@5 = 0.7167  
- Recall@5 = 0.5667  
- Fully working pipeline:
  Parse → Match → Rank → Evaluate → Deploy  

---

## 🎥 Demo & Recording

- Demo prepared using Hugging Face Space
- UI demonstrates:
  - profile selection
  - real-time matching
  - ranked results
- Recording performed between:
  - **1:15 PM – 2:45 PM**

---

## 🌍 Reflection

The most important insight:

> Simple, well-designed retrieval systems outperform complex approaches when working under real-world constraints.

Balancing:
- performance
- usability
- deployment feasibility

was critical to delivering a strong solution.

---

## 🏁 Final Note

This project demonstrates a complete pipeline from:
- raw data → intelligent matching → real-world product deployment

with a focus on accessibility and impact.