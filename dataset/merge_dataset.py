import pandas as pd
import glob
import os

folder = "dataset"

files = glob.glob(os.path.join(folder, "*.parquet"))

print("Files Found:")
for f in files:
    print(os.path.basename(f))

dfs = []

for file in files:
    print("Loading:", os.path.basename(file))

    df = pd.read_parquet(file)

    print("Shape:", df.shape)

    dfs.append(df)

print("\nMerging...")

merged = pd.concat(dfs, ignore_index=True)

print("Final Shape:", merged.shape)

merged.to_csv("dataset/final_dataset.csv", index=False)

print("\nSaved as dataset/final_dataset.csv")