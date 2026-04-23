# aims-ktt-day2-g2-t2-2-grant-matcher

# 🚀 Multilingual Grant & Tender Matcher (AIMS T2.2)

## 📌 Overview

This project builds a lightweight system that matches businesses and cooperatives with relevant funding opportunities (grants and tenders).

It is designed for real-world deployment in low-resource environments, supporting:
- 🌍 Multilingual documents (English & French)
- ⚡ Fast retrieval using BM25 + TF-IDF
- 🧠 Profile-based matching
- 📊 Measurable performance (MRR@5, Recall@5)

---

## 🎯 Problem

Small businesses and cooperatives face major challenges:
- Difficulty finding relevant tenders
- Language barriers (English/French documents)
- Information overload from unstructured sources

---

## 💡 Solution

We built a system that:

1. Parses tender documents (PDF, HTML, TXT)
2. Extracts structured information (sector, region, budget, deadline)
3. Matches tenders to business profiles
4. Ranks the most relevant opportunities
5. Generates short summaries

---

## 🧠 System Pipeline

Parse → Extract → Index → Match → Rank → Summarize

### Matching Logic
- BM25 ranking (primary retrieval)
- TF-IDF scoring (support)
- Sector and region boosting
- Cross-lingual normalization (FR → EN)

---

## 📊 Results

| Metric   | Score  |
|----------|--------|
| MRR@5    | 0.7167 |
| Recall@5 | 0.5667 |

👉 Significantly above random baseline

---

## 🧪 Evaluation

Run locally:

```bash
python evaluate.py
```

Or explore:
- eval.ipynb for reproducible evaluation

---

## 🖥️ Live Demo

👉 Hugging Face Space  
https://huggingface.co/spaces/sltanu/aims-tender-matcher-dataset

Features:
- Select business profile
- View ranked tenders
- Interactive UI

---

## 🧑‍💼 Product Design (Village Agent)

Designed for real-world deployment:

- 📱 WhatsApp audio delivery
- 🌍 Multilingual support
- 📡 Low-bandwidth environments
- 👥 Cooperative-focused access

See: village_agent.md

---

## 📁 Project Structure

.
├── matcher.py  
├── evaluate.py  
├── data_generator.py  
├── eval.ipynb  
├── dataset/  
├── summaries/  
├── village_agent.md  
├── process_log.md  

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Matcher

```bash
python matcher.py --profile_id 02 --top_k 5
```

---

## 🧠 Key Design Decisions

### Why BM25?
- Fast and CPU-efficient
- Strong baseline for retrieval
- Easy to explain and debug

### Why not LLMs?
- Too slow for constraints
- Overkill for dataset size
- Not necessary for strong performance

---

## 🌍 Real-World Impact

This system can:
- Help cooperatives discover funding opportunities
- Reduce language and information barriers
- Scale through WhatsApp-based delivery
- Operate in low-resource environments

---

## 👤 Author

Sltanu Kifile Alemu

---

## 🏁 Final Note

This project demonstrates:

> Well-designed, efficient systems can outperform complex solutions under real-world constraints.