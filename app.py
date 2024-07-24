from tkinter import *
from tkinter import ttk, font, filedialog, Entry
import pydicom
import os # importar el módulo os
from tkinter.messagebox import askokcancel, showinfo, WARNING
import tkinter as tk # importar la biblioteca tkinter

import tkinter.simpledialog as tksd # importar el módulo simpledialog de tkinter
import tkinter.filedialog as tkfd # importar el módulo filedialog de tkinter
import getpass
from PIL import ImageTk, Image
import tensorflow as tf
from tensorflow.keras import backend as K
import img2pdf # importar la biblioteca img2pdf

import csv
import pyautogui
import tkcap
import numpy as np
import time
tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)
import cv2

# Importar la función de predicción

# Importar la función de carga del modelo
from prediction import predict
from load_model import model_fun
from image_reader import DicomReader, JpegReader, PngReader

# Definir la clase de la aplicación principal
class App:
    def __init__(self, reader):
        # Crear la ventana principal
        self.root = Tk()
        self.reader = reader
        self.root.title("Herramienta para la detección rápida de neumonía")

        fonti = font.Font(weight="bold")

        self.root.geometry("815x560")
        self.root.resizable(0, 0)

        # Etiquetas y elementos visuales
        self.lab1 = ttk.Label(self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con Heatmap", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Resultado:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Cédula Paciente:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE NEUMONÍA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Probabilidad:", font=fonti)

        # Variables para ID y resultado
        self.ID = StringVar()
        self.result = StringVar()

        # Cuadro de entrada para ID
        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)
        self.ID_content = self.text1.get()

        # Cuadros de texto para imágenes y resultados
        self.text_img1 = Text(self.root, width=31, height=15)
        self.text_img2 = Text(self.root, width=31, height=15)
        self.text2 = Text(self.root)
        self.text3 = Text(self.root)

        # Botones
        self.button1 = ttk.Button(
            self.root, text="Predecir", state="disabled", command=self.run_model
        )
        self.button2 = ttk.Button(
            self.root, text="Cargar Imagen", command=self.load_img_file
        )
        self.button3 = ttk.Button(self.root, text="Borrar", command=self.delete)
        self.button4 = ttk.Button(self.root, text="PDF", command=self.create_pdf)
        self.button6 = ttk.Button(
            self.root, text="Guardar", command=self.save_results_csv
        )

        # Posicionamiento de elementos visuales
        self.lab1.place(x=110, y=65)
        self.lab2.place(x=545, y=65)
        self.lab3.place(x=500, y=350)
        self.lab4.place(x=65, y=350)
        self.lab5.place(x=122, y=25)
        self.lab6.place(x=500, y=400)
        self.button1.place(x=220, y=460)
        self.button2.place(x=70, y=460)
        self.button3.place(x=670, y=460)
        self.button4.place(x=520, y=460)
        self.button6.place(x=370, y=460)
        self.text1.place(x=200, y=350)
        self.text2.place(x=610, y=350, width=90, height=30)
        self.text3.place(x=610, y=400, width=90, height=30)
        self.text_img1.place(x=65, y=90)
        self.text_img2.place(x=500, y=90)

        # Establecer el foco en el cuadro de entrada de ID
        self.text1.focus_set()

        self.array = None
        self.reportID = 0

        # Iniciar el bucle principal de la interfaz gráfica
        self.root.mainloop()

    # Métodos de la aplicación
    def load_img_file(self):
        # Pedir al usuario que seleccione un archivo de imagen
        filepath = tkfd.askopenfilename(
            initialdir="/",
            title="Select image",
            filetypes=(
                ("DICOM", "*.dcm"),
                ("JPEG", "*.jpeg"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
            ),
        )
        if filepath:
            
            file_extension = os.path.splitext(filepath)[1]
            
            if file_extension == ".dcm":
                self.reader = DicomReader()
            elif file_extension in (".jpeg", ".jpg"):
                self.reader = JpegReader()
            elif file_extension == ".png":
                self.reader = PngReader()
            
            # Usar el atributo reader para leer el archivo
            self.array, img2show = self.reader.read_file(filepath)
            # Mostrar la imagen en la interfaz gráfica
            self.img1 = img2show.resize((250, 250), Image.LANCZOS)
            self.img1 = ImageTk.PhotoImage(self.img1)
            print(self.img1)
            self.text_img1.image_create(END, image=self.img1)
            # Habilitar el botón correspondiente
            self.button1["state"] = "enabled"
         
    def run_model(self):
        self.label, self.proba, self.heatmap = predict(self.array)
        self.img2 = Image.fromarray(self.heatmap)
        self.img2 = self.img2.resize((250, 250), Image.LANCZOS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.text_img2.image_create(END, image=self.img2)
        self.text2.insert(END, self.label)
        self.text3.insert(END, "{:.2f}".format(self.proba) + "%")

    def save_results_csv(self):
        with open("historial.csv", "a") as csvfile:
            w = csv.writer(csvfile, delimiter="-")
            w.writerow(
                [self.text1.get(), self.label, "{:.2f}".format(self.proba) + "%"]
            )
            showinfo(title="Guardar", message="Los datos se guardaron con éxito.")

    def create_pdf(self):

        # showinfo(title="PDF", message="El PDF fue generado con éxito en {}".format(pdf_file))
        cap = tkcap.CAP(self.root)
        ID = "Reporte" + str(self.reportID) + ".jpg"
        img = cap.capture(ID)
        img = Image.open(ID)
        img = img.convert("RGB")
        pdf_path = r"Reporte" + str(self.reportID) + ".pdf"
        img.save(pdf_path)
        self.reportID += 1
        showinfo(title="PDF", message="El PDF fue generado con éxito.")

    def delete(self):
        answer = askokcancel(
            title="Confirmación", message="Se borrarán todos los datos.", icon=WARNING
        )
        if answer:
            self.text1.delete(0, "end")
            self.text2.delete(1.0, "end")
            self.text3.delete(1.0, "end")
            self.text_img1.delete(self.img1, "end")
            self.text_img2.delete(self.img2, "end")
            showinfo(title="Borrar", message="Los datos se borraron con éxito")

# Para probar el código directamente desde app.py sin necesidad de importar
if __name__ == "__main__":
    loader = App(None)
