import requests
import pandas as pd
import time
from tqdm import tqdm
import random


BASE_URL = "https://api.openalex.org/works"
CS_CONCEPT = "C41008148"

TOTAL_PAPERS = 20000
PER_PAGE = 200

HEADERS = {
    "User-Agent": "your_email@example.com"
}

all_data = []
visited = set()

def safe_request(url, params=None):
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if res.status_code == 200 and res.text.strip():
            return res.json()
    except:
        pass
    return None

print("Fetching OpenAlex CS papers...")

cursor = "*"
count = 0

pbar = tqdm(total=TOTAL_PAPERS)

while count < TOTAL_PAPERS:

    params = {
        "filter": f"concepts.id:{CS_CONCEPT}",
        "sort": "cited_by_count:desc",
        "per-page": PER_PAGE,
        "cursor": cursor
    }

    data = safe_request(BASE_URL, params)
    if data is None:
        continue

    results = data.get("results", [])
    if not results:
        break

    cursor = data["meta"]["next_cursor"]

    for work in results:
        if count >= TOTAL_PAPERS:
            break

        paper_id = work.get("id")

        if not paper_id or paper_id in visited:
            continue

        visited.add(paper_id)

        all_data.append({
            "paper_id": paper_id,
            "title": work.get("title"),
            "year": work.get("publication_year"),
            "citation_count": work.get("cited_by_count", 0),
            "references": work.get("referenced_works", [])
        })

        count += 1
        pbar.update(1)

    if len(all_data) > 200:

        sorted_data = sorted(all_data, key=lambda x: x["citation_count"], reverse=True)

        top_candidates = sorted_data[:100]
        random_candidates = random.sample(sorted_data, min(30, len(sorted_data)))

        expand_candidates = top_candidates[:20] + random_candidates[:10]

        new_ids = []

        for paper in expand_candidates:
            refs = paper["references"]

            for ref in refs[:3]:
                if ref and ref not in visited:
                    new_ids.append(ref)
                    visited.add(ref)

        for ref_id in new_ids[:30]:

            if count >= TOTAL_PAPERS:
                break

            work = safe_request(ref_id)
            if work is None:
                continue

            all_data.append({
                "paper_id": ref_id,
                "title": work.get("title"),
                "year": work.get("publication_year"),
                "citation_count": work.get("cited_by_count", 0),
                "references": work.get("referenced_works", [])
            })

            count += 1
            pbar.update(1)

            time.sleep(0.15)

    time.sleep(0.2)

pbar.close()

df = pd.DataFrame(all_data)
df.to_csv("openalex_papers.csv", index=False)

print("\nSaved to:", "openalex_papers.csv")