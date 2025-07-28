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
    ]

def predict_labels(input_json_path, model=None):
    if model is None:
        model = load_model()
    with open(input_json_path, "r") as f:
        pages = json.load(f)

    predictions = []
    for page in pages:
        for group in page["groups"]:
            features = extract_features(group)
            label = model.predict([features])[0]
            if label in ["Title", "H1", "H2", "H3"]:
                predictions.append({
                    "level": label,
                    "text": group["text"],
                    "page": group["page"]
                })
    return predictions
