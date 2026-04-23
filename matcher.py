"""
matcher.py
AIMS KTT Hackathon 2026 - Day 2 - T2.2
Multilingual Grant & Tender Matcher with Summarizer
- Parses tenders/ (.txt, .html, .pdf)
- Detects language (EN/FR)
- Translates cross-lingual content
- Ranks top-K using TF-IDF + BM25 combined
- Writes ≤80-word summary per match in profile's language
- CLI: python matcher.py --profile 02 --topk 5
Author: Sltanu Kifile Alemu
"""

import os
import json
import argparse
import re
import math
from collections import Counter
from bs4 import BeautifulSoup
from langdetect import detect
from rank_bm25 import BM25Okapi
from deep_translator import GoogleTranslator

DATASET_DIR   = "dataset"
TENDERS_DIR   = os.path.join(DATASET_DIR, "tenders")
PROFILES_FILE = os.path.join(DATASET_DIR, "profiles.json")
SUMMARIES_DIR = "summaries"

# ── TRANSLATOR ───────────────────────────────────────────────────────────────
def translate_to_english(text, source_lang="fr"):
    """Translate any text to English for unified BM25+TF-IDF indexing."""
    try:
        if source_lang == "en":
            return text
        translated = GoogleTranslator(
            source=source_lang, target="en"
        ).translate(text[:3000])
        return translated if translated else text
    except Exception:
        return text

def translate_text(text, target_lang="fr"):
    """Translate English text to target language for summaries."""
    try:
        if target_lang == "en":
            return text
        translated = GoogleTranslator(
            source="en", target=target_lang
        ).translate(text)
        return translated if translated else text
    except Exception:
        return text

# ── PARSE TENDERS ────────────────────────────────────────────────────────────
def parse_tender(filepath):
    """Parse .txt, .html, .pdf and extract structured fields."""
    ext     = os.path.splitext(filepath)[1].lower()
    content = ""

    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

    elif ext == ".html":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            soup    = BeautifulSoup(f.read(), "html.parser")
            content = soup.get_text(separator="\n")

    elif ext == ".pdf":
        try:
            import PyPDF2
            with open(filepath, "rb") as f:
                reader  = PyPDF2.PdfReader(f)
                content = "\n".join(
                    page.extract_text() or "" for page in reader.pages
                )
        except Exception:
            content = ""

    # Detect language
    try:
        language = detect(content[:500]) if content.strip() else "en"
    except Exception:
        language = "en"

    # Translate to English for unified indexing
    content_en = translate_to_english(content[:2000], source_lang=language)

    # Extract fields
    sector   = extract_field(content, ["sector", "secteur"])
    budget   = extract_budget(content)
    deadline = extract_field(content, ["deadline", "date limite"])
    region   = extract_field(content, ["region", "région"])
    title    = extract_field(content, ["title", "titre"])

    return {
        "id":         os.path.splitext(os.path.basename(filepath))[0],
        "filename":   os.path.basename(filepath),
        "content":    content,
        "content_en": content_en,
        "language":   language,
        "sector":     sector,
        "budget":     budget,
        "deadline":   deadline,
        "region":     region,
        "title":      title,
    }

def extract_field(content, keys):
    """Extract field value by searching key labels."""
    lines = content.lower().split("\n")
    for line in lines:
        for key in keys:
            if key in line and ":" in line:
                value = line.split(":", 1)[-1].strip()
                if value:
                    return value.title()
    return "Unknown"

def extract_budget(content):
    """Extract and normalize budget to integer USD."""
    patterns = [
        r"USD\s*([\d,]+)",
        r"\$([\d,]+)",
        r"([\d,]+)\s*USD",
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            raw = match.group(1).replace(",", "")
            try:
                return int(raw)
            except ValueError:
                return 0
    return 0

# ── LOAD TENDERS ─────────────────────────────────────────────────────────────
def load_tenders(tenders_dir=TENDERS_DIR):
    """Load and parse all tenders."""
    tenders = []
    for filename in sorted(os.listdir(tenders_dir)):
        if filename.endswith((".txt", ".html", ".pdf")):
            filepath = os.path.join(tenders_dir, filename)
            tenders.append(parse_tender(filepath))
    print(f"📂 Loaded {len(tenders)} tenders")
    return tenders

# ── TF-IDF ───────────────────────────────────────────────────────────────────
def compute_tfidf_scores(query_tokens, tenders):
    """
    Compute TF-IDF scores for each tender against the query.
    TF  = term frequency in tender
    IDF = log(N / df) where df = number of tenders containing term
    """
    N  = len(tenders)
    corpus = [t["content_en"].lower().split() for t in tenders]

    # Document frequency per term
    df = Counter()
    for doc in corpus:
        for term in set(doc):
            df[term] += 1

    tfidf_scores = []
    for doc in corpus:
        doc_counter = Counter(doc)
        score = 0.0
        for term in query_tokens:
            tf  = doc_counter.get(term, 0) / (len(doc) + 1)
            idf = math.log((N + 1) / (df.get(term, 0) + 1))
            score += tf * idf
        tfidf_scores.append(score)

    return tfidf_scores

# ── BM25 ─────────────────────────────────────────────────────────────────────
def build_bm25_index(tenders):
    """Build BM25 index on English-translated tender content."""
    corpus = [t["content_en"].lower().split() for t in tenders]
    return BM25Okapi(corpus)

# ── SUMMARY GENERATOR ────────────────────────────────────────────────────────
def generate_summary(profile, tender, rank_num):
    """
    Generate ≤80-word summary explaining why tender matches profile.
    Cites: sector fit, budget fit, deadline.
    Written in profile's preferred language (EN or FR).
    """
    profile_lang = profile["languages"][0] if profile["languages"] else "en"

    # Budget label
    budget = tender["budget"]
    if budget >= 1000000:
        budget_label = "USD 1M"
    elif budget >= 200000:
        budget_label = "USD 200k"
    elif budget >= 50000:
        budget_label = "USD 50k"
    elif budget > 0:
        budget_label = "USD 5k"
    else:
        budget_label = "unspecified budget"

    # Build English summary first
    summary_en = (
        f"This grant matches your {profile['sector']} business in {profile['country']}. "
        f"The tender focuses on {tender['sector']}, aligning with your sector needs. "
        f"It offers {budget_label} in funding, which fits your team size of "
        f"{profile['employees']} employees. "
        f"The deadline is {tender['deadline']}, giving you sufficient time to apply. "
        f"Region coverage includes {tender['region']}."
    )

    # Translate to French if profile prefers French
    if profile_lang == "fr":
        summary = translate_text(summary_en, target_lang="fr")
    else:
        summary = summary_en

    # Enforce ≤80 words
    words = summary.split()
    if len(words) > 80:
        summary = " ".join(words[:80]) + "..."

    return summary

# ── SAVE SUMMARY TO FILE ─────────────────────────────────────────────────────
def save_summary(profile, tender, summary, rank_num):
    """Save summary as .md file in summaries/ folder."""
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    filename = f"profile_{profile['id']}_{tender['id']}.md"
    filepath = os.path.join(SUMMARIES_DIR, filename)

    profile_lang = profile["languages"][0] if profile["languages"] else "en"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Match Summary\n\n")
        f.write(f"**Profile ID:** {profile['id']}\n")
        f.write(f"**Tender ID:** {tender['id']}\n")
        f.write(f"**Rank:** {rank_num}\n")
        f.write(f"**Score:** {tender['score']}\n")
        f.write(f"**Language:** {profile_lang}\n\n")
        f.write(f"## Why This Tender Matches\n\n")
        f.write(f"{summary}\n\n")
        f.write(f"## Tender Details\n\n")
        f.write(f"- **Sector:** {tender['sector']}\n")
        f.write(f"- **Budget:** {tender['budget']}\n")
        f.write(f"- **Deadline:** {tender['deadline']}\n")
        f.write(f"- **Region:** {tender['region']}\n")

    return filepath

# ── CORE RANK FUNCTION ───────────────────────────────────────────────────────
def rank(profile, tenders, bm25, topk=5):
    """
    matcher.py::rank(profile)
    Combines TF-IDF + BM25 scores with boosters:
    1. TF-IDF score  — term importance across corpus
    2. BM25 score    — probabilistic keyword ranking
    3. Language boost — +0.5 if tender language matches profile
    4. Sector boost   — +2.0 if sector matches exactly
    5. Region boost   — +0.5 if region matches profile country
    6. Budget penalty — -0.3 if budget unparseable
    Cross-lingual: profile needs_text translated to EN before querying.
    """
    profile_lang = profile["languages"][0] if profile["languages"] else "en"

    # Translate profile query to English
    needs_en = translate_to_english(
        profile["needs_text"], source_lang=profile_lang
    )
    query_text   = f"{profile['sector']} {needs_en} {profile['country']}"
    query_tokens = query_text.lower().split()

    # Get BM25 scores
    bm25_scores   = bm25.get_scores(query_tokens)

    # Get TF-IDF scores
    tfidf_scores  = compute_tfidf_scores(query_tokens, tenders)

    # Normalize scores to [0,1]
    def normalize(scores):
        max_s = max(scores) if max(scores) > 0 else 1
        return [s / max_s for s in scores]

    bm25_norm  = normalize(list(bm25_scores))
    tfidf_norm = normalize(tfidf_scores)

    # Combine: 60% BM25 + 40% TF-IDF
    scored = []
    for i, tender in enumerate(tenders):
        score = (0.6 * bm25_norm[i]) + (0.4 * tfidf_norm[i])

        # Boosters
        if tender["language"] == profile_lang:
            score += 0.5
        if profile["sector"].lower() in tender["sector"].lower():
            score += 2.0
        if profile["country"].lower() in tender["region"].lower():
            score += 0.5
        if tender["budget"] == 0:
            score -= 0.3

        scored.append({**tender, "score": round(score, 4)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:topk]

# ── DISPLAY ───────────────────────────────────────────────────────────────────
def display_results(profile, results):
    """Print ranked results to terminal."""
    print("\n" + "=" * 65)
    print(f"🏢 PROFILE {profile['id']} | {profile['sector'].upper()} | {profile['country']}")
    print(f"   Language : {profile['languages']}")
    print(f"   Needs    : {profile['needs_text'][:80]}")
    print("=" * 65)
    print(f"{'Rank':<5} {'Tender ID':<15} {'Score':<8} {'Sector':<12} {'Lang':<6} {'Region'}")
    print("-" * 65)
    for i, t in enumerate(results, 1):
        print(f"{i:<5} {t['id']:<15} {t['score']:<8} {t['sector']:<12} {t['language']:<6} {t['region']}")
    print("=" * 65)

# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="T2.2 Multilingual Grant & Tender Matcher"
    )
    parser.add_argument("--profile", type=str, required=True,
                        help="Profile ID (e.g. 02)")
    parser.add_argument("--topk", type=int, default=5,
                        help="Top K results (default: 5)")
    args = parser.parse_args()

    # Load profiles
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    profile = next((p for p in profiles if p["id"] == args.profile), None)
    if not profile:
        print(f"❌ Profile '{args.profile}' not found.")
        return

    # Load + index tenders
    tenders = load_tenders()
    bm25    = build_bm25_index(tenders)

    # Rank
    results = rank(profile, tenders, bm25, topk=args.topk)

    # Display results
    display_results(profile, results)

    # Generate + save summaries
    print("\n📝 Generating summaries...")
    for rank_num, tender in enumerate(results, 1):
        summary  = generate_summary(profile, tender, rank_num)
        filepath = save_summary(profile, tender, summary, rank_num)
        print(f"   ✅ Rank {rank_num}: {filepath}")

    print(f"\n✅ Done! Summaries saved in '{SUMMARIES_DIR}/'")

if __name__ == "__main__":
    main()