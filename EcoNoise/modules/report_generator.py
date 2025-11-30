import csv
import os
from fpdf import FPDF

REPORTS_FOLDER = "C:/PythonReports"
os.makedirs(REPORTS_FOLDER, exist_ok=True)

def generate_csv_report(data, filename="eco_report.csv"):
    """
    data: list of records (dicts)
    filename: name to save in REPORTS_FOLDER
    """
    filepath = os.path.join(REPORTS_FOLDER, filename)
    # Ensure consistent fieldnames (original keys expected)
    fieldnames = ["Location", "Timestamp", "Predicted Class", "Confidence", "Harm Rate"]
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for r in data:
            # Support both original and alternate key names
            loc = r.get("Location") or r.get("location") or r.get("loc") or ""
            ts = r.get("Timestamp") or r.get("timestamp") or ""
            pred = r.get("Predicted Class") or r.get("predicted_class") or r.get("PredictedClass") or ""
            conf = r.get("Confidence") or r.get("confidence") or ""
            harm = r.get("Harm Rate") or r.get("harm_rate") or r.get("HarmRate") or ""
            writer.writerow([loc, ts, pred, conf, harm])
    return filepath

def generate_pdf_report(data, filename="eco_report.pdf"):
    """
    Very simple PDF generator using FPDF (keeps layout simple).
    """
    filepath = os.path.join(REPORTS_FOLDER, filename)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, "EcoNoise Report", ln=True)
    pdf.ln(4)
    # table header
    pdf.set_font("Arial", size=10)
    pdf.cell(40, 8, "Location", 1)
    pdf.cell(50, 8, "Timestamp", 1)
    pdf.cell(50, 8, "Predicted", 1)
    pdf.cell(20, 8, "Conf", 1)
    pdf.cell(20, 8, "Harm", 1)
    pdf.ln()
    for r in data:
        loc = r.get("Location") or r.get("location") or ""
        ts = r.get("Timestamp") or r.get("timestamp") or ""
        pred = r.get("Predicted Class") or r.get("predicted_class") or ""
        conf = r.get("Confidence") or r.get("confidence") or ""
        harm = r.get("Harm Rate") or r.get("harm_rate") or ""
        pdf.cell(40, 8, str(loc)[:20], 1)
        pdf.cell(50, 8, str(ts)[:20], 1)
        pdf.cell(50, 8, str(pred)[:20], 1)
        pdf.cell(20, 8, str(conf)[:8], 1)
        pdf.cell(20, 8, str(harm)[:8], 1)
        pdf.ln()
    pdf.output(filepath)
    return filepath

