# utils/pdf_writer.py

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
import os
import textwrap

def save_cv_as_pdf(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Font yolu (DejaVu)
    base_dir = os.path.dirname(__file__)
    font_path = os.path.join(base_dir, "fonts", "DejaVuSans.ttf")
    bold_font_path = os.path.join(base_dir, "fonts", "DejaVuSans-Bold.ttf")

    pdfmetrics.registerFont(TTFont("DejaVu", font_path))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", bold_font_path))

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    margin_x = 25 * mm
    y = height - 30 * mm
    line_spacing = 5 * mm
    max_width = width - 2 * margin_x
    
    def draw_wrapped(text, x, y, font_name, font_size):
        c.setFont(font_name, font_size)
        wrapped = textwrap.wrap(text, width=100)
        for line in wrapped:
            c.drawString(x, y, line)
            y -= line_spacing
        return y

    # Başlık tanımları
    section_titles = {
        "eğitim", "hakkımda", "iş deneyimi", "teknik yetenekler",
        "diller", "ilgi alanları", "education", "work experience",
        "skills", "languages", "interests"
    }

    lines = text.split("\n")
    for line in lines:
        clean = line.strip()

        # Sayfa sonu kontrolü
        if y < 25 * mm:
            c.showPage()
            y = height - 30 * mm

        # Boş satır → 1 satır boşluk
        if not clean:
            y -= line_spacing / 2
            continue

        # Başlıklar
        if clean.lower() in section_titles:
            c.setFont("DejaVu-Bold", 13)
            c.drawString(margin_x, y, clean.upper())
            y -= line_spacing * 1.5
            continue

        # Bullet point'li satırlar
        if clean.startswith("-") or clean.startswith("•"):
            bullet = "• " + clean.lstrip("-•").strip()
            y = draw_wrapped(bullet, margin_x + 10, y, "DejaVu", 11)
        else:
            y = draw_wrapped(clean, margin_x, y, "DejaVu", 11)

    c.save()
    print(f"✅ PDF çıktı başarıyla oluşturuldu: {output_path}")
