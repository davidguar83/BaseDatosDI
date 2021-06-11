import sqlite3 as dbapi
import os

from reportlab.platypus import Table
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas


estiloHoja = getSampleStyleSheet()
story = []

fich_imagen = "/home/david/Descargas/Base_Datos.jpg"
imagen_logo = Image(os.path.relpath(fich_imagen),width=400,height=100)
story.append(imagen_logo)


cabecera = estiloHoja['Heading4']
cabecera.pageBreakBefore=0
cabecera.keepWithNext=0
cabecera.backColor=colors.green

parrafo= Paragraph("Bade de Datod DI",cabecera)
story.append(parrafo)

cadena = " Datos de Clientes"
estilo = estiloHoja['BodyText']
parrafo2 = Paragraph(cadena,estilo)
story.append(parrafo2)

story.append(Spacer(0,20))

doc = SimpleDocTemplate("Informe.pdf",pagesize = A4, showBoundary =1)



story.append(Spacer(0,20))



listacli = []
listacli.append(("DNI","NOMBRE","APELLIDO","TELEF","DEUDA"))
listapro = []
listapro.append(("REF","NOMBRE","PVP"))
listaven = []
listaven.append(("REF","NOMBRE","CANTIDAD"))



try:

    conexion = dbapi.connect("baseDI.dat")

except dbapi.StandardError as e:

    print(e)
else:

    print("Base conectada")

try:

    cursor = conexion.cursor()
    cursor.execute("select * from clientes")
    for fila in cursor.fetchall():

        listacli.append(fila)

    cursor.execute("select * from productos")
    for filapro in cursor.fetchall():
        listapro.append(filapro)

    cursor.execute("select * from ventas")
    for filaven in cursor.fetchall():
        listaven.append(filaven)


except dbapi.DatabaseError as e:

    print("Error en consulta cliente: "+ str(e))

else:
    print("Consulta realizada")

finally:
    cursor.close()
    conexion.close()

tablacli = Table(listacli)

tablacli.setStyle([('TEXTCOLOR',(0,0),(-1,0),colors.blueviolet)])
tablacli.setStyle([('BACKGROUND',(0,1),(-1,-1),colors.greenyellow)])
tablacli.setStyle([('INNERGIRD',(0,1),(-1,-1),0.25,colors.blueviolet)])
story.append(tablacli)

story.append(Spacer(0,20))

cadena = " Datos de Producto"
estilo = estiloHoja['BodyText']
parrafo2 = Paragraph(cadena,estilo)
story.append(parrafo2)


story.append(Spacer(0,20))

tablapro = Table(listapro)

tablapro.setStyle([('TEXTCOLOR',(0,0),(-1,0),colors.blueviolet)])
tablapro.setStyle([('BACKGROUND',(0,1),(-1,-1),colors.greenyellow)])
tablapro.setStyle([('INNERGIRD',(0,1),(-1,-1),0.25,colors.blueviolet)])
story.append(tablapro)


story.append(Spacer(0,20))

cadena = " Datos de Producto Ventas"
estilo = estiloHoja['BodyText']
parrafo2 = Paragraph(cadena,estilo)
story.append(parrafo2)

story.append(Spacer(0,20))

tablaven = Table(listaven)

tablaven.setStyle([('TEXTCOLOR',(0,0),(-1,0),colors.blueviolet)])
tablaven.setStyle([('BACKGROUND',(0,1),(-1,-1),colors.greenyellow)])
tablaven.setStyle([('INNERGIRD',(0,1),(-1,-1),0.25,colors.blueviolet)])
story.append(tablaven)





doc.build(story)


