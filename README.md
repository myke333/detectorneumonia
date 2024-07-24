## Hola! Bienvenido a la herramienta para la detección rápida de neumonía

Deep Learning aplicado en el procesamiento de imágenes radiográficas de tórax en formato DICOM con el fin de clasificarlas en 3 categorías diferentes:

1. Neumonía Bacteriana

2. Neumonía Viral

3. Sin Neumonía

Aplicación de una técnica de explicación llamada Grad-CAM para resaltar con un mapa de calor las regiones relevantes de la imagen de entrada.

---

## Uso de la herramienta:

A continuación le explicaremos cómo empezar a utilizarla.

Requerimientos necesarios para el funcionamiento:
-en el repositorio raiz tener el archivo 'conv_MLP_84.h5'
-Tener Docker Instalado
-Tener Xming instalado de https://sourceforge.net/projects/xming/postdownload
-crear la imagen del contenedor docker usando el dockerfile del repositorio y utilizando el comando:
    docker build -t mi-aplicacion:v1 .
-ejecutar el contenedor utilizando el comando: 
    docker run -it  -e DISPLAY=host.docker.internal:0.0 mi-aplicacion:v1 python3 app.py
-al ejecutar el comando anterior se abrira la intefaz de la aplicacion de deteccion de neumonia y al darle cargar imagen en la ruta /home/src encontra un .dcm para utilizarlo como ejemplo



Uso de la Interfaz Gráfica:

- Ingrese la cédula del paciente en la caja de texto
- Presione el botón 'Cargar Imagen', seleccione la imagen del explorador de archivos del computador (Imagenes de prueba en https://drive.google.com/drive/folders/1WOuL0wdVC6aojy8IfssHcqZ4Up14dy0g?usp=drive_link)
- Presione el botón 'Predecir' y espere unos segundos hasta que observe los resultados
- Presione el botón 'Guardar' para almacenar la información del paciente en un archivo excel con extensión .csv
- Presione el botón 'PDF' para descargar un archivo PDF con la información desplegada en la interfaz
- Presión el botón 'Borrar' si desea cargar una nueva imagen

---

## Arquitectura de archivos propuesta.
 
## app.py
la app principal
Este script Python crea una interfaz gráfica para la detección de neumonía. Permite cargar imágenes médicas (DICOM, JPEG, PNG), ejecutar un modelo de predicción, mostrar resultados con un mapa de calor, y guardar informes en CSV y PDF.

## imagen_reader.py 
Este código define clases para leer y procesar imágenes en formatos DICOM, JPEG, JPG y PNG. Utiliza bibliotecas como pydicom, OpenCV, NumPy y Pillow. Cada clase hija de ImageReader implementa el método read_file para cargar la imagen y devolver la matriz de píxeles y la imagen correspondiente en formato PIL. Las operaciones incluyen ajuste de valores de píxeles y conversión de tipos.

## load_model.py
El código importa TensorFlow y define la función model_fun para cargar un modelo preentrenado desde un archivo .h5 en la ubicación especificada. El modelo se carga utilizando la API de Keras de TensorFlow.

## pdf_creator.py
El código importa funciones y clases de varias bibliotecas, incluyendo tkinter, PIL, y img2pdf. Define una función llamada create_pdf que utiliza la biblioteca tkinter para capturar la pantalla, convertir la captura a un formato de imagen y guardarla como un archivo PDF. Si este archivo es el punto de entrada principal, se llama a la función create_pdf.

## prediction.py
El código utiliza TensorFlow y OpenCV para cargar un modelo de red neuronal preentrenado y realizar predicciones sobre imágenes médicas. Define funciones para preprocesar imágenes, generar mapas de atención de gradiente (heatmap), y realizar predicciones utilizando el modelo cargado. La función predict devuelve la etiqueta de la clase predicha, la probabilidad asociada y el mapa de calor. La función grad_cam genera el mapa de atención de gradiente.

## preprocess_imag.py

La función preprocess toma una imagen como entrada y realiza el preprocesamiento necesario para adaptarla al formato de entrada esperado por el modelo. Las operaciones incluyen redimensionar la imagen a 512x512 píxeles, convertirla a escala de grises, aplicar el contraste limitado de adaptación al histograma (CLAHE), normalizar los valores de píxeles al rango [0, 1] y agregar dimensiones adicionales para coincidir con el formato de entrada del modelo. La imagen preprocesada se devuelve como un array NumPy.

## read_img.py
Las funciones read_jpg_file y read_dicom_file leen archivos de imagen JPEG y DICOM respectivamente. Ambas funciones utilizan OpenCV para cargar la imagen, convierten el resultado en un array de NumPy y crean una imagen a partir de este array con PIL. Luego, convierten el array a valores de tipo float, normalizan los valores de píxeles al rango [0, 255], y finalmente convierten los valores a enteros sin signo de 8 bits. Ambas funciones devuelven el array preprocesado y la imagen para mostrar.

## detector_neumonia.py
anexo este archivo donde esta todo el proyecto bueno y corre bien
Este script de Python implementa una interfaz gráfica utilizando Tkinter para una herramienta de diagnóstico médico de neumonía. Aquí hay una explicación en 400 caracteres:

El código define clases para leer imágenes médicas (DICOM, JPEG, JPG, PNG), realizar predicciones de modelos de TensorFlow (Grad-CAM), y presenta una interfaz gráfica. Los botones permiten cargar imágenes, ejecutar predicciones, guardar resultados y generar informes en PDF. Los resultados se guardan en un historial CSV. La aplicación puede manejar varios tipos de archivos de imágenes médicas y utiliza bibliotecas como OpenCV, PIL, TensorFlow y Tkinter para su implementación.


---
test unitarios
## test_read_dicom_file.py
Este test unitario verifica la funcionalidad de la clase DicomReader del módulo detector_neumonia. En resumen, crea una instancia de DicomReader, llama a su método read_file con un archivo DICOM de ejemplo, y realiza aserciones para garantizar que los resultados no sean nulos. El propósito es asegurar que la lectura de archivos DICOM se realiza correctamente. Se ejecuta utilizando python -m unittest test_read_dicom_file.py en la terminal.

## test_read_jpg_file.py
Este test unitario evalúa la capacidad de la clase JpegReader del módulo detector_neumonia para leer archivos JPEG. Crea un objeto JpegReader, lo usa para leer un archivo JPEG de ejemplo y verifica que los resultados no sean nulos mediante aserciones. El objetivo es garantizar una correcta funcionalidad al leer archivos JPEG. Se ejecuta con python -m unittest test_read_jpg_file.py en la terminal.

## Acerca del Modelo

La red neuronal convolucional implementada (CNN) es basada en el modelo implementado por F. Pasa, V.Golkov, F. Pfeifer, D. Cremers & D. Pfeifer
en su artículo Efcient Deep Network Architectures for Fast Chest X-Ray Tuberculosis Screening and Visualization.

Está compuesta por 5 bloques convolucionales, cada uno contiene 3 convoluciones; dos secuenciales y una conexión 'skip' que evita el desvanecimiento del gradiente a medida que se avanza en profundidad.
Con 16, 32, 48, 64 y 80 filtros de 3x3 para cada bloque respectivamente.

Después de cada bloque convolucional se encuentra una capa de max pooling y después de la última una capa de Average Pooling seguida por tres capas fully-connected (Dense) de 1024, 1024 y 3 neuronas respectivamente.

Para regularizar el modelo utilizamos 3 capas de Dropout al 20%; dos en los bloques 4 y 5 conv y otra después de la 1ra capa Dense.

## Acerca de Grad-CAM

Es una técnica utilizada para resaltar las regiones de una imagen que son importantes para la clasificación. Un mapeo de activaciones de clase para una categoría en particular indica las regiones de imagen relevantes utilizadas por la CNN para identificar esa categoría.

Grad-CAM realiza el cálculo del gradiente de la salida correspondiente a la clase a visualizar con respecto a las neuronas de una cierta capa de la CNN. Esto permite tener información de la importancia de cada neurona en el proceso de decisión de esa clase en particular. Una vez obtenidos estos pesos, se realiza una combinación lineal entre el mapa de activaciones de la capa y los pesos, de esta manera, se captura la importancia del mapa de activaciones para la clase en particular y se ve reflejado en la imagen de entrada como un mapa de calor con intensidades más altas en aquellas regiones relevantes para la red con las que clasificó la imagen en cierta categoría.

## Proyecto original realizado por:
Maycol Steven Avendaño Niño 