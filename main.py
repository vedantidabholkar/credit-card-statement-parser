from parser.parser_factory import get_parser
from parser.logger import get_logger
import json
import os

logger = get_logger(__name__)

pdf_files = [
    "data/HDFC_sample_redacted.pdf",
    "data/SBI_sample_redacted.pdf",
    "data/ICICI_sample_redacted.pdf"
]

os.makedirs("output", exist_ok=True)

all_data = []

for pdf in pdf_files:
    try:
        parser = get_parser(pdf)
        extracted = parser.extract_data()
        all_data.append(extracted)
        logger.info(f"Successfully parsed: {pdf}")
        print(f" Extracted data from {pdf}")
    except Exception as e:
        logger.error(f"Error processing {pdf}: {e}")
        print(f" Error processing {pdf}: {e}")

# Save results to JSON file
output_path = "output/final_results.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4)

print(f"\n------ Final Extracted Data Saved To: {output_path} ------")
