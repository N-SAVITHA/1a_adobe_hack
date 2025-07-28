import fitz  # PyMuPDF
import json
import os
from pathlib import Path


def extract_pdf_features(pdf_path):
    doc = fitz.open(pdf_path)
    all_pages = []

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        groups = []

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    group = {
                        "text": text,
                        "bbox": span["bbox"],
                        "font_name": span.get("font", ""),
                        "font_size": round(span.get("size", 0.0), 2),
                        "is_bold": "Bold" in span.get("font", ""),
                        "is_italic": "Italic" in span.get("font", "") or "Oblique" in span.get("font", ""),
                        "page": page_number
                    }
                    groups.append(group)

        all_pages.append({
            "page": page_number,
            "groups": groups
        })

    return all_pages


def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main(input_pdf_path, output_json_path):
    print(f"[INFO] Extracting text from: {input_pdf_path}")
    extracted_data = extract_pdf_features(input_pdf_path)
    save_json(extracted_data, output_json_path)
    print(f"[SUCCESS] Output saved to: {output_json_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PDF Text Extractor using PyMuPDF (pdfsix_miner)")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_json", help="Path to the output JSON file")

    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = Path(args.output_json).parent
    os.makedirs(output_dir, exist_ok=True)

    main(args.input_pdf, args.output_json)
