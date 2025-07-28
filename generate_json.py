import os
import json
from pdfsix_miner import extract_pdf_details
from predictor import predict_labels

def extract_title(predicted_headings):
    for item in predicted_headings:
        if item.get("level", "").lower() == "title":
            return item["text"]
    return predicted_headings[0]["text"] if predicted_headings else ""

def process_pdf(pdfname, input_dir="/app/input", temp_dir="/app/temp", output_dir="/app/output"):
    base_name = os.path.splitext(pdfname)[0]
    raw_json_path = os.path.join(temp_dir, f"{base_name}.json")
    input_pdf_path = os.path.join(input_dir, pdfname)
    output_json_path = os.path.join(output_dir, f"{base_name}.json")

    # STEP 5A: Extract raw content using your miner
    extract_pdf_details(input_pdf_path, raw_json_path)

    # STEP 5B: Predict headings from that JSON
    headings = predict_labels(raw_json_path)

    # STEP 5C: Build final structured output
    output_json = {
        "title": extract_title(headings),
        "outline": [h for h in headings if h.get("level", "").lower() != "title"]
    }

    # STEP 5D: Write the final output JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    input_dir = "/app/input"
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            process_pdf(file)
