
FROM python:3.11-slim

# Instalar dependencias de sistema necesarias
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    xdg-utils libu2f-udev libvulkan1 gnupg ca-certificates chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Configurar Chrome y ChromeDriver
ENV CHROME_BIN=chromium
ENV CHROMEDRIVER_BIN=chromedriver

# Crear carpeta de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exponer el puerto
EXPOSE 5501

# Comando de inicio
CMD ["python", "app.py"]
