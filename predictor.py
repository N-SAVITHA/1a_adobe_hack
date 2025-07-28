import json
import joblib

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
        len(group.get("font_name", "")),  # Example: font_name_length
    ]

def predict_labels(model, df):
    predictions = model.predict(df)
    return predictions.tolist()
