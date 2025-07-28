import json

def convert_to_dataframe(json_path):
    with open(json_path) as f:
        pages = json.load(f)

    X = []
    metadata = []

    for page in pages:
        page_num = page["page"]
        for item in page["groups"]:
            if not item["text"].strip():
                continue

            # Feature vector with 7 features
            feature = [
                item["x0"],
                item["y0"],
                item["x1"],
                item["y1"],
                item["font_size"],
                1 if item.get("is_bold") else 0,
                1 if item.get("is_italic") else 0
            ]

            X.append(feature)
            metadata.append({
                "text": item["text"],
                "page": page_num
            })

    return X, metadata
