# Utiliza una imagen base de Python
FROM python:3.7.9

# Establece el directorio de trabajo en /app
WORKDIR /app
ENV MYSQL_USER='root'
ENV MYSQL_DATABASE='empleo'
ENV MYSQL_PASSWORD=''
ENV MYSQL_HOST='host.docker.internal'
ENV MYSQL_PORT=3306
ENV SECRET_KEY='b631b80081d6bed380379faf676c8254e66ea8d3df0e15ebfc38acfebac21859'

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia todo el código de la aplicación al contenedor
COPY src/ .

# Expone el puerto en el que se ejecutará la aplicación
#EXPOSE 5000

# Define el comando para ejecutar la aplicación
CMD ["python", "index.py"]