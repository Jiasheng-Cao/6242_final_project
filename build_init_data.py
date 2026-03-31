import requests
import pandas as pd
import time
from tqdm import tqdm

# ===============================
# 配置
# ===============================
BASE_URL = "https://api.openalex.org/works"

# Computer Science 的 concept id
CS_CONCEPT = "C41008148"

# 抓多少论文（建议先小规模测试）
TOTAL_PAPERS = 1000
PER_PAGE = 200   # 最大200

# ===============================
# 存储
# ===============================
all_data = []

# ===============================
# 抓取
# ===============================
print("Fetching OpenAlex CS papers...")

cursor = "*"
count = 0

pbar = tqdm(total=TOTAL_PAPERS)

while count < TOTAL_PAPERS:
    params = {
        "filter": f"concepts.id:{CS_CONCEPT}",
        "per-page": PER_PAGE,
        "cursor": cursor
    }

    res = requests.get(BASE_URL, params=params)

    if res.status_code != 200:
        print("Error:", res.status_code)
        time.sleep(2)
        continue

    data = res.json()

    results = data.get("results", [])

    if not results:
        break

    for work in results:
        if count >= TOTAL_PAPERS:
            break

        paper_id = work.get("id")  # OpenAlex ID
        title = work.get("title")
        year = work.get("publication_year")
        citation_count = work.get("cited_by_count")

        references = work.get("referenced_works", [])

        all_data.append({
            "paper_id": paper_id,
            "title": title,
            "year": year,
            "citation_count": citation_count,
            "reference_count": len(references),
            "references": references
        })

        count += 1
        pbar.update(1)

    # 下一页
    cursor = data["meta"]["next_cursor"]

    # ❗ 防止过快
    time.sleep(0.2)

pbar.close()

# ===============================
# 保存
# ===============================
df = pd.DataFrame(all_data)

output_path = "openalex_papers.csv"
df.to_csv(output_path, index=False)

print("\nSaved to:", output_path)