# Importar la función "showinfo" de la biblioteca tkinter.messagebox
from tkinter.messagebox import showinfo

# Importar la biblioteca tkinter con el alias "tk"
import tkinter as tk

# Importar las funciones "askokcancel" y "WARNING" de la biblioteca tkinter.messagebox
from tkinter.messagebox import askokcancel, WARNING

# Importar la clase "Image" de la biblioteca PIL (Pillow)
from PIL import Image

# Importar la biblioteca img2pdf
import img2pdf

# Definir una función llamada "create_pdf" para crear un archivo PDF
def create_pdf():
    # Crear una instancia de la clase "Capturer" de tkinter y pasar una instancia de Tkinter
    cap = tk.Capturer(tk.Tk())
    
    # Crear un nombre de archivo "ID" para el reporte PDF
    ID = "Reporte" + str(cap.reportID) + ".jpg"
    
    # Capturar la pantalla y guardarla en un archivo de imagen
    img = cap.capture(ID)
    
    # Abrir la imagen y convertirla a modo RGB
    img = Image.open(ID)
    img = img.convert("RGB")
    
    # Definir la ruta del archivo PDF
    pdf_path = r"Reporte" + str(cap.reportID) + ".pdf"
    
    # Guardar la imagen como un archivo PDF
    img.save(pdf_path)
    
    # Incrementar el contador de reportes
    cap.reportID += 1
    
    # Mostrar un mensaje informando que el PDF se generó con éxito
    showinfo(title="PDF", message="El PDF fue generado con éxito.")

# Verificar si este archivo es el punto de entrada principal del programa
if __name__ == "__main__":
    # Llamar a la función "create_pdf" para generar el PDF
    create_pdf()

