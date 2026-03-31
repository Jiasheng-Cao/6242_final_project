import pandas as pd
import ast
from tqdm import tqdm

# ===============================
# Step 1: 读取数据
# ===============================
df = pd.read_csv("openalex_papers.csv")

print("Loaded openalex_papers.csv")
print("Total rows:", len(df))


# ===============================
# Step 2: 清洗 paper_id
# ===============================
def clean_id(x):
    if pd.isna(x):
        return None
    return str(x).split("/")[-1]   # 🔥 核心


df["paper_id"] = df["paper_id"].apply(clean_id)


# ===============================
# Step 3: 清洗 references（列表）
# ===============================
def clean_references(ref_str):
    if pd.isna(ref_str):
        return []

    try:
        refs = ast.literal_eval(ref_str)  # 字符串 → list
    except:
        return []

    cleaned = []
    for r in refs:
        if r:
            cleaned.append(str(r).split("/")[-1])

    return cleaned


print("\nCleaning references...")

tqdm.pandas()
df["references"] = df["references"].progress_apply(clean_references)


# ===============================
# Step 4: 保存
# ===============================
output_path = "cleaned_openalex_papers.csv"
df.to_csv(output_path, index=False)

print("\nSaved to:", output_path)