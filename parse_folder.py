import os
import argparse
import json
from parser.parser_factory import get_parser
from parser.logger import get_logger

logger = get_logger(__name__)

def process_pdf(pdf_path):
    """Extract data from a single PDF"""
    try:
        parser = get_parser(pdf_path)
        data = parser.extract_data()
        logger.info(f"Successfully parsed: {pdf_path}")
        return data
    except Exception as e:
        logger.error(f"Failed to parse {pdf_path}: {e}")
        return {"File": pdf_path, "Error": str(e)}

def process_folder(input_folder, output_folder):
    """Batch process all PDFs in a folder"""
    os.makedirs(output_folder, exist_ok=True)
    results = []

    pdf_files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("⚠️  No PDF files found in the input folder.")
        return

    print(f"🔍 Found {len(pdf_files)} PDF(s) to process.\n")

    for pdf in pdf_files:
        print(f"📄 Processing: {os.path.basename(pdf)} ...")
        data = process_pdf(pdf)
        results.append(data)

    # Save final JSON output
    output_path = os.path.join(output_folder, "parsed_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Processing complete! Results saved to {output_path}")
    logger.info(f"Batch processing completed. Output saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Credit Card PDF Parser")
    parser.add_argument("--input", required=True, help="Path to input folder containing PDFs")
    parser.add_argument("--output", required=True, help="Path to output folder for results")

    args = parser.parse_args()
    process_folder(args.input, args.output)
