from reportlab.pdfgen import canvas
def txt_to_pdf(txt_file, pdf_file):
    c = canvas.Canvas(pdf_file)
    with open(txt_file, "r") as file:
        y = 800
        for line in file:
            c.drawString(100, y, line.strip())
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
    c.save()
txt_to_pdf("clcoding.txt", "notes.pdf")
