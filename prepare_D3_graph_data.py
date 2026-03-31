import pandas as pd
import json

# ===============================
# 读取数据
# ===============================
df = pd.read_csv("cleaned_openalex_papers.csv")

# ===============================
# 只保留必要字段
# ===============================
nodes = []
edges = []

# 建一个 id → year 映射
year_map = {}

for _, row in df.iterrows():
    pid = row["paper_id"]
    year = row["year"]

    year_map[pid] = year

    nodes.append({
        "id": pid,
        "year": int(year),
        "citation_count": int(row["citation_count"])
    })

# 构建边
for _, row in df.iterrows():
    source = row["paper_id"]

    refs = row["references"]

    if isinstance(refs, str):
        try:
            refs = eval(refs)
        except:
            refs = []

    for target in refs:
        if target in year_map:  # 只保留存在节点
            edges.append({
                "source": source,
                "target": target
            })

# ===============================
# 保存 JSON
# ===============================
graph = {
    "nodes": nodes,
    "links": edges
}

with open("graph.json", "w") as f:
    json.dump(graph, f)

print("Saved graph.json")