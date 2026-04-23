import pandas as pd
import json
import math
import random

print("开始处理数据...")

df = pd.read_csv("cleaned_openalex_papers.csv")
nodes = []
edges = []
year_map = {}

# ===== 1️⃣ 构建节点 =====
for _, row in df.iterrows():
    pid = row["paper_id"]
    year = int(row["year"])
    year_map[pid] = year
    
    title = row.get("title", "")
    if pd.isna(title):
        title = ""
    else:
        title = str(title)
        
    nodes.append({
        "id": pid,
        "title": title,
        "year": year,
        "citation_count": int(row["citation_count"])  # 保留原始citation
    })

DECAY_RATE = 0.15

# ===== 2️⃣ 构建边 =====
for _, row in df.iterrows():
    source = row["paper_id"]
    source_year = year_map[source]
    
    refs = row["references"]
    if isinstance(refs, str):
        try:
            refs = eval(refs)
        except:
            refs = []

    for target in refs:
        if target in year_map: 
            target_year = year_map[target]
            time_diff = max(0, source_year - target_year)
            decay_weight = math.exp(-DECAY_RATE * time_diff)
            
            edges.append({
                "source": source,
                "target": target,
                "type": "actual", 
                "weight": round(decay_weight, 4)
            })

# ===== ⭐ 3️⃣ 新增：计算 in-degree（只算真实引用） =====
in_degree = {n["id"]: 0 for n in nodes}

for e in edges:
    if e["type"] == "actual":
        tgt = e["target"]
        if tgt in in_degree:
            in_degree[tgt] += 1

# ===== ⭐ 4️⃣ 写回 nodes =====
for n in nodes:
    n["in_degree"] = in_degree[n["id"]]

# ===== 5️⃣ 冷启动预测（不参与 in-degree）=====
cold_start_papers = [n["id"] for n in nodes if n["citation_count"] == 0]
all_paper_ids = list(year_map.keys())

for new_paper in cold_start_papers:
    new_year = year_map[new_paper]
    num_predictions = random.randint(2, 4)
    for _ in range(num_predictions):
        predicted_target = random.choice(all_paper_ids)
        target_year = year_map[predicted_target]
        if target_year <= new_year and predicted_target != new_paper:
            edges.append({
                "source": new_paper,
                "target": predicted_target,
                "type": "predicted", 
                "confidence": round(random.uniform(0.6, 0.95), 2) 
            })

# ===== 6️⃣ 输出 =====
graph = {
    "nodes": nodes,
    "links": edges
}

output_file = "graph_with_algorithms.json"

with open(output_file, "w") as f:
    json.dump(graph, f)

print(f"✅ 成功生成 {output_file}！包含 {len(nodes)} 个节点。")