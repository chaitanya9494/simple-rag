"""Regenerate the fictional, redistributable demo PDF. Requires reportlab."""
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

PAGES = [
    ("Acme Software: Customer Policy", [
        "Fictional sample document for Simple RAG.",
        "Acme Software sells developer productivity subscriptions.",
        "This document describes billing, refunds, and customer support.",
        "These policies are invented for teaching and are not legal advice.",
    ]),
    ("Billing and Cancellation", [
        "Subscriptions renew monthly on the original purchase date.",
        "Customers can cancel from Settings > Billing at any time.",
        "Cancellation stops future renewals; access lasts until the paid term ends.",
        "Cancellation does not automatically create a refund request.",
    ]),
    ("Refund Policy", [
        "Customers may request a refund within 30 days of their first purchase.",
        "Renewal payments are not refundable under the standard policy.",
        "To request a refund, email billing@example.com with the order ID.",
        "Approved refunds return to the original payment method in 5-10 business days.",
        "Enterprise contracts follow their signed agreement instead of this policy.",
    ]),
    ("Support", [
        "Email support@example.com for technical support.",
        "Standard support hours are Monday-Friday, 9 AM-5 PM Central Time.",
        "The standard response target is two business days.",
        "This document does not describe a student discount or data retention policy.",
    ]),
]


def main():
    target = Path(__file__).resolve().parents[1] / "sample_docs" / "acme-policy.pdf"
    target.parent.mkdir(exist_ok=True)
    pdf = canvas.Canvas(str(target), pagesize=letter, invariant=1)
    pdf.setTitle("Acme Software - Fictional Customer Policy")
    for number, (title, lines) in enumerate(PAGES, start=1):
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(54, 730, title)
        pdf.setFont("Helvetica", 11)
        for i, line in enumerate(lines):
            pdf.drawString(54, 680 - i * 30, line)
        pdf.drawString(54, 40, f"PDF page {number} | Fictional teaching sample")
        pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    main()
