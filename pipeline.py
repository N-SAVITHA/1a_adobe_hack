import os
import sys
import json
import subprocess
from pdfsix_miner import extract_pdf_features
from features import convert_to_dataframe
from predictor import load_model, predict_labels

INPUT_DIR = "input"
OUTPUT_DIR = "output"


def run_pipeline(pdf_path, model_path='random_forest_model.pkl'):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_json = os.path.join(OUTPUT_DIR, f"{base_name}_with_predictions.json")

    # Step 1: Extract raw features from the PDF
    extracted_data = extract_pdf_features(pdf_path)

    # Step 2: Convert raw features to DataFrame
    df, original_json_data = convert_to_dataframe(extracted_data)

    # Step 3: Load model
    model = load_model(model_path)

    # Step 4: Predict labels
    predictions = predict_labels(model, df)

    # Step 5: Store predictions in desired format
    for item, pred in zip(original_json_data, predictions):
        item['prediction'] = pred
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(original_json_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Prediction pipeline complete. Output saved to {output_json}")

    # Step 6: Run map_predictions.py to replace prediction with label
    subprocess.run([sys.executable, "map_predictions.py", output_json], check=True)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            run_pipeline(pdf_path)
