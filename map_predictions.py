import json
import joblib
import sys
import os

# Usage: python map_predictions.py <input_json>
input_json = sys.argv[1]
base, ext = os.path.splitext(input_json)
output_json = base + "_labeled" + ext

label_encoder = joblib.load("label_encoder.pkl")

with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

predictions = [item["prediction"] for item in data]
labels = label_encoder.inverse_transform(predictions)

for item, label in zip(data, labels):
    item["label"] = label
    if "prediction" in item:
        del item["prediction"]

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ 'prediction' replaced with 'label' and saved to {output_json}")