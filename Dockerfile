FROM python:3.10

# Configuración del entorno
WORKDIR /app

# Instalar dependencias
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente, pruebas y configuración de logs
COPY ./app ./app
COPY ./tests ./tests
COPY ./logging_config.json ./logging_config.json

# Definir el comando por defecto (puede ser sobrescrito)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-config", "./logging_config.json"]
