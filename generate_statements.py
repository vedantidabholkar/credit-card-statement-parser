from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime, timedelta
import random, os

os.makedirs("statements", exist_ok=True)

def draw_statement(c, bank, user):
    left = 20 * mm
    top = 280 * mm
    gap = 8 * mm

    c.setFont("Times-Bold", 16)
    c.drawString(left, top, f"{bank} Credit Card Statement")

    c.setFont("Times-Roman", 10)
    y = top - 1.5 * gap

    details = [
        ("Cardholder Name", user["name"]),
        ("Card Number", f"XXXX-XXXX-XXXX-{user['last4']}"),
        ("Card Variant", user["variant"]),
        ("Statement Period", user["period"]),
        ("Payment Due Date", user["due_date"]),
        ("Total Amount Due", f"₹{user['total']:,.2f}")
    ]

    for label, val in details:
        c.drawString(left, y, f"{label}:")
        c.drawString(left + 70 * mm, y, str(val))
        y -= gap

    y -= gap
    c.setFont("Times-Bold", 12)
    c.drawString(left, y, "Recent Transactions")
    y -= gap / 2
    c.setFont("Times-Roman", 9)

    for t in user["transactions"]:
        c.drawString(left, y, t["date"])
        c.drawString(left + 30 * mm, y, t["desc"])
        c.drawRightString(180 * mm, y, f"₹{t['amount']:,.2f}")
        y -= gap

    y -= gap
    c.setFont("Times-Roman", 8)
    c.drawString(left, y, f"Generated on {datetime.now().strftime('%d %b %Y %H:%M')} - (Demo PDF, fake data)")

def make_fake_users(base_date, count=5):
    names = ["Aarav Sharma", "Neha Patel", "Rahul Gupta", "Priya Nair", "Kavya Singh", 
             "Vikram Mehta", "Tanya Rao", "Aditya Verma", "Simran Joshi", "Rohit Malhotra"]
    variants = ["Platinum Plus", "Gold Cashback", "Titanium Travel", "Signature Rewards", "SmartPay Elite"]
    tx_types = ["Amazon", "Swiggy", "Zomato", "Myntra", "Uber", "Flipkart", "Netflix"]

    people = []
    used = set()
    for _ in range(count):
        name = random.choice([n for n in names if n not in used])
        used.add(name)
        last4 = str(random.randint(1000, 9999))
        variant = random.choice(variants)
        start_date = (base_date - timedelta(days=random.randint(25, 35))).strftime("%d %b %Y")
        end_date = base_date.strftime("%d %b %Y")
        due_date = (base_date + timedelta(days=random.randint(15, 25))).strftime("%d %b %Y")
        total_due = random.randint(2000, 60000)
        
        transactions = []
        for _ in range(random.randint(4, 7)):
            transactions.append({
                "date": (base_date - timedelta(days=random.randint(1, 25))).strftime("%d %b"),
                "desc": random.choice(tx_types),
                "amount": random.randint(300, 12000)
            })

        people.append({
            "name": name,
            "last4": last4,
            "variant": variant,
            "period": f"{start_date} - {end_date}",
            "due_date": due_date,
            "total": total_due,
            "transactions": transactions
        })
    return people

def generate_statements():
    random.seed(99)
    today = datetime(2025, 10, 1)
    banks = [
        ("HDFC Bank", today),
        ("ICICI Bank", today - timedelta(days=2)),
        ("Axis Bank", today - timedelta(days=4)),
        ("SBI Bank", today - timedelta(days=6)),
        ("Kotak Mahindra Bank", today - timedelta(days=8))
    ]

    for bank, date in banks:
        filename = os.path.join("statements", f"{bank.split()[0].lower()}_auto_statement.pdf")
        c = canvas.Canvas(filename, pagesize=A4)
        users = make_fake_users(date)
        for user in users:
            draw_statement(c, bank, user)
            c.showPage()
        c.save()
        print(f"✅ Created: {filename} ({len(users)} pages)")

if __name__ == "__main__":
    generate_statements()
    print("\nAll dummy bank statements are ready in the 'statements/' folder 🎉")
