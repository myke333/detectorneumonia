# Importar OpenCV para trabajar con imágenes
import cv2

# Importar PIL para procesamiento de imágenes
from PIL import Image

# Importar NumPy para manipulación de arrays
import numpy as np

# Definir una función llamada "read_jpg_file" que lee un archivo de imagen JPEG
def read_jpg_file(path):
    # Leer la imagen utilizando OpenCV
    img = cv2.imread(path)
    
    # Convertir la imagen en un array de NumPy
    img_array = np.asarray(img)
    
    # Crear una imagen a partir del array de NumPy
    img2show = Image.fromarray(img_array)
    
    # Convertir el array en valores de tipo float
    img2 = img_array.astype(float)
    
    # Normalizar los valores de píxeles en el rango [0, 255]
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    
    # Convertir los valores a enteros sin signo de 8 bits
    img2 = np.uint8(img2)
    
    # Devolver el array preprocesado y la imagen para mostrar
    return img2, img2show

# Definir una función llamada "read_dicom_file" que lee un archivo DICOM
def read_dicom_file(path):
    # Utilizar la biblioteca pydicom para leer el archivo DICOM
    ds = pydicom.dcmread(path)
    
    # Extraer la matriz de píxeles del archivo DICOM
    img_array = ds.pixel_array
    
    # Crear una imagen a partir del array de píxeles
    img2show = Image.fromarray(img_array)
    
    # Convertir el array en valores de tipo float
    img_array = img_array.astype(float)
    
    # Normalizar los valores de píxeles en el rango [0, 255]
    img_array = (np.maximum(img_array, 0) / img_array.max()) * 255.0
    
    # Convertir los valores a enteros sin signo de 8 bits
    img_array = np.uint8(img_array)
    
    # Devolver el array preprocesado y la imagen para mostrar
    return img_array, img2show
