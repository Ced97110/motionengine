from datasets import load_dataset
import json
import os

os.makedirs("data", exist_ok=True)

print("Loading SportsSettBasketball dataset from HuggingFace...")
ds = load_dataset("GEM/sportsett_basketball")
print(f"Splits: {list(ds.keys())}")
print(f"Train: {len(ds['train'])} records")
print(f"Validation: {len(ds['validation'])} records")
print(f"Test: {len(ds['test'])} records")

record = ds['train'][0]
print(f"\nKeys: {list(record.keys())}")

with open('data/sample_record.json', 'w') as f:
    json.dump(record, f, indent=2, default=str)

print(f"\nSaved sample to data/sample_record.json")
