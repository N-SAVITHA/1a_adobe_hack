import json
from pdfsix_miner import extract_pdf_features
from features import convert_to_dataframe
from predictor import load_model, predict_labels


def run_pipeline(pdf_path, model_path='random_forest_model.pkl', output_json='output_with_predictions.json'):
    # Step 1: Extract raw features from the PDF
    extracted_data = extract_pdf_features(pdf_path)
    # Save to temp file
    temp_json = "temp_extracted.json"
    with open(temp_json, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)

    # Step 2: Convert raw features to DataFrame
    df, original_json_data = convert_to_dataframe(temp_json)

    # Step 3: Load model
    model = load_model(model_path)

    # Step 4: Predict labels
    predictions = predict_labels(model, df)

    # Step 5: Store predictions in desired format
    def store_predictions_json(original_json_data, predictions, output_json):
        # Combine original data and predictions
        for item, pred in zip(original_json_data, predictions):
            item['prediction'] = pred
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(original_json_data, f, ensure_ascii=False, indent=4)

    store_predictions_json(original_json_data, predictions, output_json)

    print(f"✅ Prediction pipeline complete. Output saved to {output_json}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <path_to_pdf>")
    else:
        run_pipeline(sys.argv[1])
