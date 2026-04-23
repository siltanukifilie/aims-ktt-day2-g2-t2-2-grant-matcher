"""
data_generator.py
AIMS KTT Hackathon 2026 - Day 2 - T2.2
Generates: tenders/ (.txt, .html, .pdf), profiles.json, gold_matches.csv
Follows exact specs from challenge brief.
Author: Sltanu Kifile Alemu
"""

import os
import json
import csv
import random

random.seed(42)

# ── EXACT SPECS FROM BRIEF ────────────────────────────────────────────────────
SECTORS = ["agritech", "healthtech", "cleantech", "edtech", "fintech", "wastetech"]

BUDGETS = [
    {"label": "5k",  "value": 5000},
    {"label": "50k", "value": 50000},
    {"label": "200k","value": 200000},
    {"label": "1M",  "value": 1000000},
]

REGIONS   = ["Rwanda", "Kenya", "Senegal", "DRC", "Ethiopia"]
COUNTRIES = ["Rwanda", "Kenya", "Senegal", "DRC", "Ethiopia"]

DEADLINES = [
    "30 June 2025",
    "31 July 2025",
    "31 August 2025",
    "30 September 2025",
    "31 October 2025",
    "31 December 2025",
]

# ── BOILERPLATE PHRASES (bureaucratese) ───────────────────────────────────────
BOILERPLATE_EN = [
    "All applications shall be submitted in accordance with the guidelines set forth by the regional development authority.",
    "Compliance with applicable data protection and privacy regulations is mandatory for all applicants.",
    "The fund reserves the right to request additional documentation at any stage of the review process.",
    "Incomplete applications will not be considered for evaluation.",
    "Applicants must not have any outstanding financial obligations to any regional body.",
    "The decision of the evaluation committee shall be final and binding.",
    "Funding is subject to availability and satisfactory performance reviews.",
    "All funded projects must submit quarterly progress reports to the programme secretariat.",
    "The fund is administered in accordance with African Union procurement and transparency guidelines.",
    "Applicants are advised to retain copies of all submitted documents for their records.",
]

BOILERPLATE_FR = [
    "Toutes les candidatures doivent être soumises conformément aux directives établies par l'autorité de développement régionale.",
    "Le respect des réglementations applicables en matière de protection des données est obligatoire.",
    "Le fonds se réserve le droit de demander des documents supplémentaires à tout moment.",
    "Les candidatures incomplètes ne seront pas prises en compte.",
    "Les candidats ne doivent avoir aucune obligation financière en cours envers un organisme régional.",
    "La décision du comité d'évaluation est définitive et sans appel.",
    "Le financement est soumis à disponibilité et à des examens de performance satisfaisants.",
    "Tous les projets financés doivent soumettre des rapports d'avancement trimestriels.",
    "Le fonds est administré conformément aux directives de passation des marchés de l'Union africaine.",
    "Les candidats sont invités à conserver des copies de tous les documents soumis.",
]

# ── TENDER CONTENT BUILDERS ───────────────────────────────────────────────────
def build_en_tender(idx, sector, budget, deadline, region):
    boilerplate = " ".join(random.sample(BOILERPLATE_EN, 3))
    return f"""TITLE: {sector.upper()} INNOVATION GRANT — REF {idx:02d}

SECTOR:      {sector}
BUDGET:      USD {budget['label']} (up to USD {budget['value']:,})
DEADLINE:    {deadline}
ELIGIBILITY: Small and medium enterprises (SMEs) operating in {region} with a
             minimum of 2 full-time employees and legally registered status.
REGION:      {region}

1. BACKGROUND
The {sector} Innovation Grant is offered to support early-stage and growth-stage
enterprises working in the {sector} sector across {region}. The programme is funded
by the regional development authority in partnership with continental innovation bodies.

2. OBJECTIVES
- Accelerate {sector} solutions that address local market challenges in {region}.
- Support entrepreneurs with access to capital, networks, and technical assistance.
- Promote sustainable and inclusive business models within the {sector} ecosystem.

3. FUNDING DETAILS
Maximum funding available per applicant: USD {budget['value']:,} ({budget['label']}).
Funding is non-repayable and disbursed in tranches upon milestone achievement.
Applications close strictly on {deadline}. Late submissions will not be accepted.

4. ELIGIBILITY CRITERIA
- Business must be registered and operating in {region}.
- Primary sector of operation must be {sector}.
- Minimum 2 full-time employees at time of application.
- Applicant must not have received funding from this programme in the past 2 years.

5. APPLICATION PROCESS
Submit all required documents via the official portal before {deadline}.
Required documents: business registration certificate, audited accounts (if available),
project proposal (max 10 pages), and letters of recommendation.

6. LEGAL AND COMPLIANCE
{boilerplate}
"""

def build_fr_tender(idx, sector, budget, deadline, region):
    boilerplate = " ".join(random.sample(BOILERPLATE_FR, 3))
    return f"""TITRE: SUBVENTION INNOVATION {sector.upper()} — RÉF {idx:02d}

SECTEUR:      {sector}
BUDGET:       USD {budget['label']} (jusqu'à USD {budget['value']:,})
DATE LIMITE:  {deadline}
ÉLIGIBILITÉ:  Petites et moyennes entreprises (PME) opérant en {region} avec
              au moins 2 employés à temps plein et enregistrées légalement.
RÉGION:       {region}

1. CONTEXTE
La subvention Innovation {sector} est proposée pour soutenir les entreprises
en phase de démarrage et de croissance travaillant dans le secteur {sector}
à travers {region}. Le programme est financé par l'autorité de développement
régionale en partenariat avec des organismes d'innovation continentaux.

2. OBJECTIFS
- Accélérer les solutions {sector} qui répondent aux défis du marché local en {region}.
- Soutenir les entrepreneurs avec accès au capital, aux réseaux et à l'assistance technique.
- Promouvoir des modèles économiques durables et inclusifs dans l'écosystème {sector}.

3. DÉTAILS DU FINANCEMENT
Financement maximum disponible par candidat: USD {budget['value']:,} ({budget['label']}).
Le financement est non remboursable et versé par tranches selon les jalons atteints.
Les candidatures se ferment strictement le {deadline}. Les soumissions tardives
ne seront pas acceptées.

4. CRITÈRES D'ÉLIGIBILITÉ
- L'entreprise doit être enregistrée et opérer en {region}.
- Le secteur d'activité principal doit être {sector}.
- Minimum 2 employés à temps plein au moment de la candidature.
- Le candidat ne doit pas avoir reçu de financement de ce programme au cours des 2 dernières années.

5. PROCESSUS DE CANDIDATURE
Soumettre tous les documents requis via le portail officiel avant le {deadline}.
Documents requis: certificat d'enregistrement, comptes vérifiés (si disponibles),
proposition de projet (max 10 pages), et lettres de recommandation.

6. LÉGAL ET CONFORMITÉ
{boilerplate}
"""

# ── FILE FORMAT WRITERS ───────────────────────────────────────────────────────
def write_txt(content, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def write_html(content, filepath, title):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
    h1   {{ color: #8B0000; }}
    pre  {{ white-space: pre-wrap; font-family: inherit; line-height: 1.6; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <pre>{content}</pre>
</body>
</html>"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

def write_pdf(content, filepath, title):
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 13)
        safe_title = title.encode("latin-1", errors="replace").decode("latin-1")
        pdf.multi_cell(0, 10, safe_title)
        pdf.ln(4)
        pdf.set_font("Arial", size=10)
        for line in content.split("\n"):
            safe = line.encode("latin-1", errors="replace").decode("latin-1")
            pdf.multi_cell(0, 6, safe)
        pdf.output(filepath)
    except Exception as e:
        # Fallback: save as txt
        fallback = filepath.replace(".pdf", "_fallback.txt")
        with open(fallback, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ⚠️  PDF fallback → {fallback} ({e})")

# ── GENERATE TENDERS ──────────────────────────────────────────────────────────
def generate_tenders(n=40, out_dir="tenders"):
    os.makedirs(out_dir, exist_ok=True)

    # Exact language split: 60% EN = 24, 40% FR = 16
    languages = ["en"] * 24 + ["fr"] * 16
    random.shuffle(languages)

    # Format split: 14 txt, 13 html, 13 pdf
    formats = ["txt"] * 14 + ["html"] * 13 + ["pdf"] * 13
    random.shuffle(formats)

    tenders_meta = []

    for i in range(1, n + 1):
        sector   = random.choice(SECTORS)
        budget   = random.choice(BUDGETS)
        deadline = random.choice(DEADLINES)
        region   = random.choice(REGIONS)
        lang     = languages[i - 1]
        fmt      = formats[i - 1]

        if lang == "en":
            content = build_en_tender(i, sector, budget, deadline, region)
            title   = f"{sector.title()} Innovation Grant — Ref {i:02d}"
        else:
            content = build_fr_tender(i, sector, budget, deadline, region)
            title   = f"Subvention Innovation {sector.title()} — Réf {i:02d}"

        filename = f"tender_{i:02d}_{lang}.{fmt}"
        filepath = os.path.join(out_dir, filename)

        if fmt == "txt":
            write_txt(content, filepath)
        elif fmt == "html":
            write_html(content, filepath, title)
        elif fmt == "pdf":
            write_pdf(content, filepath, title)

        tenders_meta.append({
            "id":       f"tender_{i:02d}",
            "filename": filename,
            "format":   fmt,
            "sector":   sector,
            "budget":   budget["value"],
            "budget_label": budget["label"],
            "deadline": deadline,
            "region":   region,
            "language": lang,
            "title":    title,
        })

    print(f"✅ Generated {n} tenders in '{out_dir}/'")
    print(f"   Formats  : {formats.count('txt')} .txt | {formats.count('html')} .html | {formats.count('pdf')} .pdf")
    print(f"   Languages: {languages.count('en')} English | {languages.count('fr')} French")
    return tenders_meta

# ── GENERATE PROFILES ─────────────────────────────────────────────────────────
def generate_profiles(tenders_meta, n=10, out_file="profiles.json"):
    needs_en = [
        "We are looking for funding to expand our {sector} solution across {country}.",
        "Our {sector} startup needs a grant to scale operations in {country}.",
        "Seeking financial support for {sector} innovation targeting {country} markets.",
        "We need funding to deploy our {sector} platform to rural areas in {country}.",
        "Our team is building a {sector} product and needs capital to grow in {country}.",
    ]
    needs_fr = [
        "Nous cherchons un financement pour développer notre solution {sector} en {country}.",
        "Notre startup {sector} a besoin d'une subvention pour se développer en {country}.",
        "Nous recherchons un soutien financier pour notre innovation {sector} en {country}.",
        "Nous avons besoin de fonds pour déployer notre plateforme {sector} en {country}.",
        "Notre équipe développe un produit {sector} et a besoin de capital pour grandir en {country}.",
    ]

    profiles = []
    for i in range(1, n + 1):
        sector       = random.choice(SECTORS)
        country      = random.choice(COUNTRIES)
        employees    = random.choice([2, 5, 10, 25, 50])
        lang         = random.choice(["en", "fr"])
        past_funding = random.choice([True, False])
        templates    = needs_en if lang == "en" else needs_fr
        needs_text   = random.choice(templates).format(
            sector=sector, country=country
        )

        profiles.append({
            "id":           f"{i:02d}",
            "sector":       sector,
            "country":      country,
            "employees":    employees,
            "languages":    [lang],
            "needs_text":   needs_text,
            "past_funding": past_funding,
        })

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated {n} profiles → '{out_file}'")
    return profiles

# ── GENERATE GOLD MATCHES ─────────────────────────────────────────────────────
def generate_gold_matches(profiles, tenders_meta, out_file="gold_matches.csv"):
    """
    3 gold matches per profile = 30 rows total.
    Logic: 2 same-sector tenders + 1 cross-sector (simulates expert curation).
    """
    rows = []
    for profile in profiles:
        same_sector = [t for t in tenders_meta if t["sector"] == profile["sector"]]
        other       = [t for t in tenders_meta if t["sector"] != profile["sector"]]

        # Pick 2 from same sector (expert prefers sector match)
        chosen  = random.sample(same_sector, min(2, len(same_sector)))
        # Pick 1 from other sectors (expert allows cross-sector)
        chosen += random.sample(other, 3 - len(chosen))

        for rank, tender in enumerate(chosen, start=1):
            rows.append({
                "profile_id": profile["id"],
                "tender_id":  tender["id"],
                "rank":       rank,
                "sector":     tender["sector"],
                "reason":     (
                    f"Sector match: {profile['sector']} ↔ {tender['sector']} | "
                    f"Region: {tender['region']} | Budget: USD {tender['budget_label']}"
                ),
            })

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["profile_id", "tender_id", "rank", "sector", "reason"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Generated {len(rows)} gold matches → '{out_file}'")
    print(f"   (3 matches × 10 profiles = {len(rows)} rows)")
    return rows

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 T2.2 Data Generator — AIMS KTT Hackathon 2026")
    print("=" * 60)

    # Install fpdf if needed
    os.system("pip install fpdf -q")

    tenders_meta = generate_tenders(40)
    profiles     = generate_profiles(tenders_meta, 10)
    gold         = generate_gold_matches(profiles, tenders_meta)

    print("\n" + "=" * 60)
    print("✅ ALL DONE")
    print(f"   tenders/         → 40 documents (.txt, .html, .pdf)")
    print(f"   profiles.json    → 10 business profiles")
    print(f"   gold_matches.csv → {len(gold)} expert matches")
    print("=" * 60)