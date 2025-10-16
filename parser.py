import re
import os
import pandas as pd
from readFile import extract_text_from_pdf  

def extract_info(text):
    info = {}

    bank = re.search(r"([A-Z][A-Za-z& ]+Bank)", text)
    info["Bank"] = bank.group(1).strip() if bank else "Unknown Bank"

    card = re.search(r"(?:X{2,}[- ]?){2,3}(\d{4})|Card.*?(\d{4})", text)
    info["Card Last 4 Digits"] = next(g for g in card.groups() if g) if card else "Not Found"

    billing = re.search(
        r"(Billing|Statement)\s*(Period|Cycle)?[:\s-]+([\d/]+ ?[--to]+ ?[\d/]+)", text, re.IGNORECASE
    )
    info["Billing Period"] = billing.group(3) if billing else "Not Found"

    total_due = re.search(
        r"(Total (Amount )?Due|Amount Payable|Current Balance)[:\s]+(₹[\d,]+\.?\d*)", text, re.IGNORECASE
    )
    info["Total Due"] = total_due.group(3) if total_due else "Not Found"

    due_date = re.search(
        r"(Payment )?Due Date[:\s]+([\d/]+|\d{1,2}[-/ ]?[A-Za-z]{3,9}[-/ ]?\d{2,4})", text, re.IGNORECASE
    )
    info["Due Date"] = due_date.group(2) if due_date else "Not Found"

    return info


def process_pdfs(folder="statements"):
    extracted_data = []

    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder, filename)
            print(f"📄 Reading: {filename}...")
            text = extract_text_from_pdf(pdf_path)
            info = extract_info(text)
            extracted_data.append(info)

    return extracted_data


if __name__ == "__main__":
    results = process_pdfs("statements")
    df = pd.DataFrame(results)
    df.to_csv("output.csv", index=False)
    print("\n✅ Done! Extracted info saved to output.csv")
