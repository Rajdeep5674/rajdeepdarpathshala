import qrcode
from PIL import Image
from reportlab.pdfgen import canvas

def generate_qr_code(data, qr_filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_filename)
    return qr_filename

def save_qr_to_pdf(qr_filename, pdf_filename):
    img = Image.open(qr_filename)
    pdf = canvas.Canvas(pdf_filename)
    pdf.drawInlineImage(qr_filename, 100, 500, width=200, height=200)
    pdf.save()

data = "https://example.com"
qr_filename = "qrcode.png"
pdf_filename = "qrcode.pdf"

generate_qr_code(data, qr_filename)
save_qr_to_pdf(qr_filename, pdf_filename)
print(f"QR code saved to {pdf_filename}")