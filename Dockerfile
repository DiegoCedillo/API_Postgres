# Utiliza una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y luego instálalos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Expone el puerto en el que Uvicorn ejecutará la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
