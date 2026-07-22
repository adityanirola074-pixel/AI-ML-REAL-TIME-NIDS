import pandas as pd

df = pd.read_csv("dataset/final_dataset.csv", nrows=5)

print("\n========== SHAPE ==========")
print(df.shape)

print("\n========== COLUMN NAMES ==========\n")

for i, col in enumerate(df.columns):
    print(f"{i:2d} : {col}")

print("\n========== FIRST 5 ROWS ==========\n")
print(df.head())