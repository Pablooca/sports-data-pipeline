# Usamos una imagen oficial de Python ligera como base
FROM python:3.10-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos solo el archivo de requerimientos primero (optimiza la caché de Docker)
COPY requirements.txt .

# Instalamos las dependencias sin guardar caché temporal para mantener la imagen ligera
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del proyecto
COPY . .

# Creamos los directorios de salida por si no existen
RUN mkdir -p data/processed

# Definimos el comando de ejecución por defecto del pipeline
ENTRYPOINT ["python", "-m", "src.pipeline"]