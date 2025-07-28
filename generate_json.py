from pdfsix_miner import extract_pdf_details
from predictor import predict_labels
import os
import json

def extract_title(predicted_headings):
    for item in predicted_headings:
        if item["level"] == "Title":
            return item["text"]
    return predicted_headings[0]["text"]

def process_pdf(pdfname):
    base_name = pdfname.replace(".pdf", "")
    raw_json_path = f"/app/temp/{base_name}.json"

    # STEP 5A: Extract raw content using your miner
    extract_pdf_details(f"/app/input/{pdfname}", raw_json_path)

    # STEP 5B: Predict headings from that JSON
    headings = predict_labels(raw_json_path)

    # STEP 5C: Build final structured output
    output_json = {
        "title": extract_title(headings),
        "outline": [h for h in headings if h["level"] != "Title"]
    }

    # STEP 5D: Write the final output JSON
    with open(f"/app/output/{base_name}.json", "w") as f:
        json.dump(output_json, f, indent=2)

if __name__ == "__main__":
    for file in os.listdir("/app/input"):
        if file.endswith(".pdf"):
            process_pdf(file)
