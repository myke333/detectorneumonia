# Importar las bibliotecas necesarias
import pydicom  # Para trabajar con imágenes DICOM
import cv2  # Para cargar imágenes en formato JPEG y JPG
import numpy as np  # Para realizar operaciones numéricas en matrices
from PIL import Image  # Para crear objetos de imágenes

# Clase base abstracta para leer imágenes
class ImageReader:
    def read_file(self, filename):
        raise NotImplementedError  # Método abstracto que debe ser implementado por las clases hijas

# Clase para leer imágenes en formato DICOM
class DicomReader(ImageReader):
    def read_file(self, filename):
        ds = pydicom.dcmread(filename)  # Leer archivo DICOM
        img_array = ds.pixel_array  # Obtener la matriz de píxeles
        img2show = Image.fromarray(img_array)  # Crear una imagen desde la matriz de píxeles
        img_array = img_array.astype(float)  # Convertir la matriz a tipo float
        img_array = (np.maximum(img_array, 0) / img_array.max()) * 255.0  # Ajustar los valores de píxeles
        img_array = np.uint8(img_array)  # Convertir la matriz a tipo uint8
        return img_array, img2show  # Devolver la matriz de píxeles y la imagen

# Clase para leer imágenes en formato JPEG
class JpegReader(ImageReader):
    def read_file(self, filename):
        img = cv2.imread(filename)  # Cargar la imagen en formato JPEG
        img_array = np.asarray(img)  # Obtener la matriz de píxeles
        img2show = Image.fromarray(img_array)  # Crear una imagen desde la matriz de píxeles
        img2 = img_array.astype(float)  # Convertir la matriz a tipo float
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0  # Ajustar los valores de píxeles
        img2 = np.uint8(img2)  # Convertir la matriz a tipo uint8
        return img2, img2show  # Devolver la matriz de píxeles y la imagen

# Clase para leer imágenes en formato JPG
class JpgReader(ImageReader):
    def read_file(self, filename):
        img = cv2.imread(filename)  # Cargar la imagen en formato JPG
        img_array = np.asarray(img)  # Obtener la matriz de píxeles
        img2show = Image.fromarray(img_array)  # Crear una imagen desde la matriz de píxeles
        img_array = img_array.astype(float)  # Convertir la matriz a tipo float
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0  # Ajustar los valores de píxeles
        img2 = np.uint8(img2)  # Convertir la matriz a tipo uint8
        return img2, img2show  # Devolver la matriz de píxeles y la imagen

# Clase para leer imágenes en formato PNG
class PngReader(ImageReader):
    def read_file(self, filename):
        img = Image.open(filename)  # Abrir la imagen en formato PNG
        array = img.load()  # Cargar la matriz de píxeles de la imagen
        return array, img  # Devolver la matriz de píxeles y la imagen
