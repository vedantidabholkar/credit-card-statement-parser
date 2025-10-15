# Credit Card Statement PDF Parser

A Python project to extract key information from credit card statements (PDF) and save it in JSON-style format as a PDF.  
This tool is useful for automating the extraction of billing details from bank statements.

---

## Features

- Extracts the following fields from a credit card PDF:
  - Issuer Bank
  - Last 4 digits of the card
  - Card variant/type
  - Billing cycle start and end dates
  - Payment due date
  - Total amount due
- Saves extracted information in JSON format inside a generated PDF.
- Handles PDFs with different formats, spacing, or currency symbols (₹, Rs.).
- Easy to extend for additional fields or banks.
- Can be run through a CLI or via a simple web interface (Streamlit).

---

## Requirements

- Python 3.8 or higher
- Libraries:
  - pdfplumber
  - fpdf
  - pandas
  - streamlit
  - python-dateutil

Install dependencies using:

```bash
pip install -r requirements.txt

Usage
Place your credit card statement PDF in the input/ folder.

Update the input and output file paths in credit_card_parser.py (or main.py) if needed:

input_pdf = "input/Sample_HDFC_Statement_001.pdf"
output_pdf = "output/credit_card_json.pdf"

Run the script
python credit_card_parser.py


or if using main.py:

python main.py

Output

Extracted JSON data will be printed in the console.
A JSON-style PDF will also be saved in the output/ folder.

Example:

{
    "issuer": "HDFC",
    "card_last4": "5678",
    "card_variant": "Regalia Gold",
    "billing_cycle_start": "01 Sep 2025",
    "billing_cycle_end": "30 Sep 2025",
    "payment_due_date": "20 Oct 2025",
    "total_amount_due": "23,542.67"
}

Streamlit Web App (Optional)

You can run the Streamlit interface for uploading and parsing PDFs visually.

streamlit run app.py


Steps:

Upload your statement PDF (e.g., HDFC, SBI, or ICICI).

Wait a few seconds for parsing.

View the extracted details and download the JSON result.

How It Works

pdfplumber extracts raw text from the PDF file.

Regular expressions (re) identify and capture required fields.

Data is cleaned and standardized using helper functions in utils.py.

Extracted data is stored in JSON format and optionally exported into a PDF via fpdf.

The parser architecture uses a factory design pattern to support multiple banks.
