# Importar TensorFlow para cargar el modelo previamente entrenado
import tensorflow as tf

# Importar la biblioteca NumPy para manipulación de arrays
import numpy as np

# Importar la parte de backend de Keras de TensorFlow
from tensorflow.keras import backend as K

# Importar OpenCV para el procesamiento de imágenes
import cv2

# Definir una función llamada "model_fun" que carga el modelo pre-entrenado
def model_fun():
    return tf.keras.models.load_model("conv_MLP_84.h5")

# Definir una función llamada "grad_cam" para generar una mapa de atención de gradiente
def grad_cam(array):
    # Realizar el preprocesamiento de la imagen
    img = preprocess(array)
    
    # Cargar el modelo
    model = model_fun()
    
    # Realizar predicciones
    preds = model.predict(img)
    
    # Encontrar la clase con la mayor probabilidad
    argmax = np.argmax(preds[0])
    
    output = model.output[:, argmax]
    
    # Calcular la salida de la última capa convolucional relevante
    last_conv_layer = model.get_layer("conv10_thisone")
    
    # Calcular los gradientes de la salida de la última capa convolucional
    grads = K.gradients(output, last_conv_layer.output)[0]
    
    # Calcular los gradientes promediados
    pooled_grads = K.mean(grads, axis=(0, 1, 2))
    
    # Crear una función iterativa para calcular valores intermedios
    iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
    
    # Calcular los valores intermedios
    pooled_grads_value, conv_layer_output_value = iterate(img)
    
    # Multiplicar cada filtro por su gradiente
    for filters in range(64):
        conv_layer_output_value[:, :, filters] *= pooled_grads_value[filters]
    
    # Calcular el mapa de calor (heatmap)
    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    
    # Redimensionar el heatmap para que coincida con el tamaño de la imagen original
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[2]))
    heatmap = np.uint8(255 * heatmap)
    
    # Aplicar un mapa de colores al heatmap
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Redimensionar la imagen original
    img2 = cv2.resize(array, (512, 512))
    
    # Superponer el heatmap en la imagen original
    hif = 0.8
    transparency = heatmap * hif
    transparency = transparency.astype(np.uint8)
    superimposed_img = cv2.add(transparency, img2)
    superimposed_img = superimposed_img.astype(np.uint8)
    
    # Devolver la imagen superpuesta
    return superimposed_img[:, :, ::-1]

# Definir una función llamada "preprocess" para preprocesar la imagen
def preprocess(array):
    # Redimensionar la imagen a 512x512 píxeles
    array = cv2.resize(array, (512, 512))
    
    # Convertir la imagen a escala de grises
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

# Definir una función llamada "predict" para realizar una predicción
def predict(array):
    # Preprocesar la imagen
    batch_array_img = preprocess(array)
    
    # Cargar el modelo
    model = model_fun()
    
    # Realizar la predicción
    prediction = np.argmax(model.predict(batch_array_img))
    
    # Obtener la probabilidad de la clase predicha
    proba = np.max(model.predict(batch_array_img)) * 100
    
    # Asignar etiquetas a las clases
    label = ""
    if prediction == 0:
        label = "bacteriana"
    if prediction == 1:
        label = "normal"
    if prediction == 2:
        label = "viral"
    
    # Generar un mapa de atención de gradiente (heatmap)
    heatmap = grad_cam(array)
    
    # Devolver la etiqueta, probabilidad y heatmap
    return (label, proba, heatmap)
