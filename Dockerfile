FROM python:3.11.5

# Instala las dependencias necesarias
RUN apt-get update -y \
    && apt-get install -y python3-opencv x11-apps libgtk2.0-0 libgdk-pixbuf2.0-dev xvfb xauth \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Establece el directorio de trabajo
WORKDIR /home/src

# Copia el archivo requirements.txt a la imagen
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia tu archivo .py a la imagen
COPY . .


# Especifica el comando que se ejecutará al iniciar el contenedor
CMD ["python", "app.py"]

#para cargar una imagen nueva
#docker build -t img_neumo .

#para que se meustre el display
#docker run -e DISPLAY=host.docker.internal:0.0 -it img_neumo
