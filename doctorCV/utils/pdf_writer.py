# utils/pdf_writer.py

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
import os

def save_cv_as_pdf(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Dinamik font yolu (hem yerel hem Cloud için)
    base_dir = os.path.dirname(__file__)
    font_path = os.path.join(base_dir, "fonts", "DejaVuSans.ttf")
    bold_font_path = os.path.join(base_dir, "fonts", "DejaVuSans-Bold.ttf")

    pdfmetrics.registerFont(TTFont("DejaVu", font_path))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", bold_font_path))

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    margin_x = 25 * mm
    y = height - 30 * mm
    line_spacing = 6 * mm

    lines = text.split("\n")

    for line in lines:
        clean = line.strip()

        # Sayfa sonu kontrolü
        if y < 25 * mm:
            c.showPage()
            c.setFont("DejaVu", 11)
            y = height - 30 * mm

        # Boş satır → 1 satır aşağı
        if not clean:
            y -= line_spacing / 2
            continue

        # Başlıklar büyük harfli ve kalın
        if clean.lower() in {
            "eğitim", "hakkımda", "iş deneyimi", "teknik yetenekler",
            "diller", "ilgi alanları", "education", "work experience",
            "skills", "languages", "interests"
        }:
            c.setFont("DejaVu-Bold", 12)
            c.drawString(margin_x, y, clean.upper())
            y -= line_spacing
            continue

        # Bullet point'li satırlar
        if clean.startswith("-") or clean.startswith("•"):
            bullet = "• " + clean.lstrip("-•").strip()
            c.setFont("DejaVu", 11)
            c.drawString(margin_x + 5, y, bullet)
        else:
            c.setFont("DejaVu", 11)
            c.drawString(margin_x, y, clean)

        y -= line_spacing

    c.save()
    print(f"✅ PDF çıktı başarıyla oluşturuldu: {output_path}")
