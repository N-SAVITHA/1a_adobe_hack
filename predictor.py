import json
import joblib
import pandas as pd

def load_model(model_path="random_forest_model.pkl"):
    return joblib.load(model_path)

def extract_features(group):
    return [
        group["font_size"],
        int(group["is_bold"]),
        int(group["is_italic"]),
        len(group["text"]),
        group["page"],
        int(group["text"][0].isdigit()) if group["text"] else 0,
        len(group.get("font_name", "")), 
    ]

def predict_labels(model, df):
    predictions = model.predict(df)
    return predictions.tolist()

def convert_to_dataframe(extracted_data):
    rows = []
    for page in extracted_data:
        for group in page["groups"]:
            rows.append([
                group["font_size"],
                int(group["is_bold"]),
                int(group["is_italic"]),
                len(group["text"]),
                group["page"],
                int(group["text"][0].isdigit()) if group["text"] else 0,
                len(group.get("font_name", "")),
            ])
    df = pd.DataFrame(rows, columns=[
        "font_size",
        "is_bold",
        "is_italic",
        "text_length",
        "page",
        "starts_with_digit",
        "font_name_length"
    ])
    return df, rows  # or df, extracted_data if you want the original structure
