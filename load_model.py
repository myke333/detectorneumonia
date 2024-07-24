# Importar la biblioteca de TensorFlow
import tensorflow as tf

# Definir una función para cargar un modelo pre-entrenado desde un archivo .h5
def model_fun():
    # Cargar el modelo pre-entrenado desde la ubicación del archivo .h5
    return tf.keras.models.load_model("conv_MLP_84.h5")
