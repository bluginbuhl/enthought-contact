"""
Make a branded, printable 4x6 in QR card (PDF) for your contact page.

  pip install "qrcode[pil]" reportlab
  python make_qr_card.py https://YOUR-USERNAME.github.io/business-card/

Writes qr_card.pdf. Run from the repo root so it finds logo.png and fonts/.
"""
import os
import sys

import qrcode
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# ---- Edit these -------------------------------------------------------------
HEADLINE = ["Scan to add Ben", "as a contact"]   # one string per line
FOOTER = "enthought.com"
PAGE_W, PAGE_H = 4 * inch, 6 * inch
OUTPUT = "qr_card.pdf"
# -----------------------------------------------------------------------------

NAVY, TEAL = HexColor("#0F384D"), HexColor("#00767C")
ORANGE = HexColor("#FF7238")
MUTED = HexColor("#55707C")

if len(sys.argv) != 2:
    sys.exit("Usage: python make_qr_card.py <your-site-url>")
URL = sys.argv[1]


def font(name, file, fallback):
    path = os.path.join("fonts", file)
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(name, path))
        return name
    return fallback


DISPLAY = font("Bricolage-Bold", "BricolageGrotesque-Bold.ttf", "Helvetica-Bold")
BODY = font("PublicSans", "PublicSans-Regular.ttf", "Helvetica")
BODY_SEMI = font("PublicSans-SemiBold", "PublicSans-SemiBold.ttf", "Helvetica-Bold")

# High error correction so the logo in the middle doesn't hurt scanning.
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=0)
qr.add_data(URL)
qr.make(fit=True)
matrix = qr.get_matrix()
n = len(matrix)

c = canvas.Canvas(OUTPUT, pagesize=(PAGE_W, PAGE_H))
c.setTitle("Scan to add contact")

# Navy header band with the headline
band_h = 1.85 * inch
c.setFillColor(NAVY)
c.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
c.setFillColor(white)
size = 27
line_gap = size * 1.12
block_h = line_gap * (len(HEADLINE) - 1)
first_baseline = PAGE_H - band_h / 2 + block_h / 2 - size * 0.32
c.setFont(DISPLAY, size)
for i, line in enumerate(HEADLINE):
    c.drawCentredString(PAGE_W / 2, first_baseline - i * line_gap, line)

# Orange accent stripe under the header band
c.setFillColor(ORANGE)
c.rect(0, PAGE_H - band_h - 0.06 * inch, PAGE_W, 0.06 * inch, stroke=0, fill=1)

# Teal footer band
foot_h = 0.5 * inch
c.setFillColor(TEAL)
c.rect(0, 0, PAGE_W, foot_h, stroke=0, fill=1)
c.setFillColor(white)
c.setFont(BODY_SEMI, 10.5)
c.drawCentredString(PAGE_W / 2, foot_h / 2 - 3.6, FOOTER)

# QR code, drawn as vector squares
qr_size = 2.55 * inch
mod = qr_size / n
qr_x = (PAGE_W - qr_size) / 2
qr_top = PAGE_H - band_h - 0.42 * inch          # leaves a white quiet zone
qr_y = qr_top - qr_size


FINDERS = [(0, 0), (0, n - 7), (n - 7, 0)]


def module_color(r, col):
    """Finder eyes: teal ring, orange center. Everything else navy."""
    for r0, c0 in FINDERS:
        if r0 <= r < r0 + 7 and c0 <= col < c0 + 7:
            return ORANGE if 2 <= r - r0 <= 4 and 2 <= col - c0 <= 4 else TEAL
    return NAVY


for r, row in enumerate(matrix):
    for col, on in enumerate(row):
        if on:
            c.setFillColor(module_color(r, col))
            # tiny overlap avoids hairline gaps between modules in some viewers
            c.rect(qr_x + col * mod, qr_top - (r + 1) * mod, mod + 0.05, mod + 0.05,
                   stroke=0, fill=1)

# Logo knockout in the center (about 5% of the code's area)
tile = qr_size * 0.24
tx, ty = qr_x + (qr_size - tile) / 2, qr_y + (qr_size - tile) / 2
c.setFillColor(white)
c.roundRect(tx, ty, tile, tile, tile * 0.18, stroke=0, fill=1)
if os.path.exists("logo.png"):
    pad = tile * 0.16
    c.drawImage("logo.png", tx + pad, ty + pad, tile - 2 * pad, tile - 2 * pad,
                mask="auto", preserveAspectRatio=True)

# Readable URL for anyone who'd rather type it
c.setFillColor(MUTED)
c.setFont(BODY, 8.5)
c.drawCentredString(PAGE_W / 2, qr_y - 0.3 * inch, URL.replace("https://", "").rstrip("/"))

c.showPage()
c.save()
print(f"Saved {OUTPUT} pointing to {URL}")
