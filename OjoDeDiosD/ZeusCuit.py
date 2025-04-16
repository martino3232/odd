import os
BASE_DIR = os.path.dirname(__file__)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import urllib.parse

#  Cargar el archivo BaseFinal.xlsx
archivo_entrada = "BaseFinal.xlsx"
archivo_salida = "BaseFinalDni.xlsx"

# Leer el Excel con nombres
df = pd.read_excel(archivo_entrada)

# Configuración de Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar sin abrir navegador
options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección de bot
options.add_argument("--log-level=3")  # Minimizar logs innecesarios
driver = webdriver.Chrome(options=options)

# URL base de CUIT Online
url_base = "https://www.cuitonline.com/search.php?q="

# Lista para almacenar los resultados
datos_actualizados = []

print(f" Procesando {len(df)} registros desde {archivo_entrada}...")

# Iterar sobre cada fila del Excel
for index, row in df.iterrows():
    nombre = str(row.iloc[0]).strip()  # Primer columna (nombre)

    if pd.isna(nombre) or nombre == "No disponible":
        print(f" Fila {index+1} sin nombre válido, saltando...")
        continue

    print(f" Buscando CUIT para: {nombre}...")

    try:
        # Generar la URL con el nombre buscado
        nombre_encoded = urllib.parse.quote(nombre)  # Codificar para URL
        url_busqueda = url_base + nombre_encoded

        # Acceder a la página de búsqueda
        driver.get(url_busqueda)
        time.sleep(3)  # Esperar a que cargue la página

        # Buscar el primer resultado de CUIT
        try:
            cuit_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cuit"))
            )
            cuit = cuit_element.text.strip()
        except:
            cuit = "No encontrado"

    except Exception as e:
        print(f" Error al buscar CUIT para {nombre}: {e}")
        cuit = "No encontrado"

    print(f" CUIT encontrado: {cuit}")

    # Guardar en lista
    nueva_fila = [cuit] + list(row)  # Agregar CUIT como primera columna
    datos_actualizados.append(nueva_fila)

    # Guardar en el Excel a medida que avanza
    df_salida = pd.DataFrame(datos_actualizados, columns=["CUIT"] + list(df.columns))
    df_salida.to_excel(archivo_salida, index=False)

print(f" Archivo final generado: {archivo_salida}")
driver.quit()
