"""
Make a QR code for your GitHub Pages site.

  pip install "qrcode[pil]"
  python make_qr.py https://bluginbuhl.github.io/business-card/

Writes qr.png (for screens/printing) and qr.svg (scales cleanly for print shops).
"""
import sys
import qrcode
import qrcode.image.svg

if len(sys.argv) != 2:
    sys.exit("Usage: python make_qr.py <your-site-url>")
url = sys.argv[1]

# Error correction "M" keeps the code simple and fast to scan.
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=4)
qr.add_data(url)
qr.make(fit=True)
qr.make_image(fill_color="black", back_color="white").save("qr.png")

qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage).save("qr.svg")
print(f"Saved qr.png and qr.svg pointing to {url}")