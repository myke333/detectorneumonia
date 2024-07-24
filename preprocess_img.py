# Importar OpenCV para procesamiento de imágenes
import cv2

# Importar NumPy para manipulación de arrays
import numpy as np

# Definir una función llamada "preprocess" que realiza el preprocesamiento de una imagen
def preprocess(array):
    # Redimensionar la imagen a 512x512 píxeles
    array = cv2.resize(array, (512, 512))
    
    # Convertir la imagen a escala de grises (grayscale)
    array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    
    # Aplicar el contraste limitado de adaptación al histograma (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    array = clahe.apply(array)
    
    # Normalizar los valores de píxeles al rango [0, 1]
    array = array / 255
    
    # Agregar dimensiones para que coincidan con el formato de entrada del modelo
    array = np.expand_dims(array, axis=-1)
    array = np.expand_dims(array, axis=0)
    
    # Devolver la imagen preprocesada
    return array
