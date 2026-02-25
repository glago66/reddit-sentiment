import json
import pandas as pd

# Load the data
with open('data/cleaned/RC_2025-12_music_subreddits.ndjson', 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]

df = pd.DataFrame(data)

# Summary stats
print("=== DATA OVERVIEW ===")
print(f"Shape: {df.shape}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nNull counts:\n{df.isnull().sum()}")
print(f"\nMemory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Get sample
sample = df.sample(n=1000, random_state=42)
sample.to_json('sample_1000.ndjson', orient='records', lines=True)
print(f"\nSaved 1000-row sample to sample_1000.ndjson")