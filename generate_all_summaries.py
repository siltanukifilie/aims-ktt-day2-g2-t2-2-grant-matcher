import os
import json
from matcher import load_tenders, build_bm25_index, rank

DATASET_DIR = "dataset"
PROFILES_FILE = os.path.join(DATASET_DIR, "profiles.json")
SUMMARIES_DIR = "summaries"


def generate_summary(profile, tender):
    return (
        f"This opportunity is in the {tender['sector']} sector located in {tender['region']}. "
        f"It has a budget of {tender['budget']} and a deadline of {tender['deadline']}. "
        f"It matches the needs of the profile in terms of sector and region."
    )


def main():
    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    tenders = load_tenders()
    bm25 = build_bm25_index(tenders)

    total_files = 0

    for profile in profiles:
        results = rank(profile, tenders, bm25, topk=5)

        for rank_num, tender in enumerate(results, start=1):
            summary = generate_summary(profile, tender)

            filename = f"profile_{profile['id']}_{tender['id']}.md"
            filepath = os.path.join(SUMMARIES_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("# Tender Summary\n\n")
                f.write(f"**Profile ID:** {profile['id']}\n")
                f.write(f"**Tender ID:** {tender['id']}\n")
                f.write(f"**Rank:** {rank_num}\n")
                f.write(f"**Sector:** {tender['sector']}\n")
                f.write(f"**Region:** {tender['region']}\n")
                f.write(f"**Budget:** {tender['budget']}\n")
                f.write(f"**Deadline:** {tender['deadline']}\n\n")
                f.write("## Summary\n\n")
                f.write(summary + "\n")

            total_files += 1

    print(f"✅ Generated {total_files} summary files")


if __name__ == "__main__":
    main()