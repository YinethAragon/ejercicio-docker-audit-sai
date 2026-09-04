# Usar una imagen más reciente y ligera
FROM python:3.10-slim

# Crear un usuario no-root por seguridad
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copiar e instalar dependencias primero para aprovechar el cache de Docker
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Cambiar los permisos al usuario no-root
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5050

CMD ["python", "app.py"]