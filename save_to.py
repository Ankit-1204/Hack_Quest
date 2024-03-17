import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import textwrap

def text_to_pdf(text, filename=None):
    if filename is None:
     
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        filename = temp.name
        temp.close()
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter


    c.setFont("Helvetica", 12)


    lines = textwrap.wrap(text, width=70)


    x = 50  # Left margin
    y = height - 50  # Top margin

 
    for line in lines:
        c.drawString(x, y, line)
        y -= 20  

        
        if y <= 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50 

    # Save PDF
    c.save()
    return filename



