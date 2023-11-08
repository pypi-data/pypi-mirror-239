from reportlab.lib.pagesizes import letter
from reportlab.platypus import PageTemplate, Frame

def configurar_template(doc):
    # Crea un objeto PageTemplate
    template = PageTemplate(id='letter_portrait', frames=[
        Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal_frame'),
        Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 100, id='contenido_frame'),
    ], onPage=header, onPageEnd=footer)

    # Agrega el template al documento
    doc.addPageTemplates(template)     
    

# Define una función para crear el encabezado.
def header(canvas, doc):
    ancho, alto = letter
    encabezado_texto = "Mi Encabezado"
    canvas.saveState()
    canvas.setFont("Helvetica", 12)
    canvas.drawString(ancho / 2, alto - 40, encabezado_texto)
    canvas.restoreState()

# Define una función para crear el pie de página con numeración de páginas.
def footer(canvas, doc):
    ancho, alto = letter
    pie_texto = "Página %d" % (doc.page)
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawString(ancho / 2, 40, pie_texto)
    canvas.restoreState()
    #canvas.showPage()  # Agrega esta línea para mostrar el número de página en todas las páginas
