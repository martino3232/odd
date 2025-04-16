import os
BASE_DIR = os.path.dirname(__file__)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time

# Configuración
USERNAME = "VazquezJPablo"
PASSWORD = "$AMPlanes2025"
LOGIN_URL = "https://reportes.agd-online.com/"
DETAIL_URL = "https://reportes.agd-online.com/dashboard/personas/detalle/{}"

EXCEL_PATH = "BaseFinalGrupoFamiliar.xlsx"
OUTPUT_PATH = "BaseFinalGrupoFamiliar_Actualizado.xlsx"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def login():
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Usuario"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Usuario"]').send_keys(USERNAME)
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Contraseña"]').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'button.btn-primary').click()
    WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
    print(" Sesión iniciada")

def limpiar_cuit(cuit):
    return re.sub(r'\D', '', cuit)

def extraer_telefonos():
    numeros = []
    try:
        rows = driver.find_elements(By.XPATH, '//h2[contains(text(), "Teléfonos celulares")]/following-sibling::div//tbody/tr')
        for row in rows:
            span = row.find_element(By.XPATH, './/td[1]/span')
            numero = span.text.strip()
            if numero:
                numeros.append(numero)
    except Exception as e:
        print(f" No se encontraron teléfonos: {e}")
    return numeros

def extraer_familia():
    familiares = []
    try:
        rows = driver.find_elements(By.XPATH, '//h2[contains(text(), "Vínculos familiares")]/following-sibling::div//tbody/tr')
        for row in rows:
            celdas = row.find_elements(By.TAG_NAME, 'td')
            if len(celdas) >= 3:
                nombre = celdas[1].text.strip()
                parentesco = celdas[2].text.strip()
                if nombre and parentesco:
                    familiares.append((nombre, parentesco))
    except Exception as e:
        print(f" No se encontró grupo familiar: {e}")
    return familiares

# Leer el Excel
df = pd.read_excel(EXCEL_PATH)

# Crear columnas para teléfonos y familiares
df['Celular 1'] = ""
df['Celular 2'] = ""
for i in range(1, 5):
    df[f'Familiar {i}'] = ""
    df[f'Parentesco {i}'] = ""

login()

for idx, row in df.iterrows():
    cuit_original = str(row['CUIT'])
    cuit_num = limpiar_cuit(cuit_original)

    print(f" Procesando CUIT: {cuit_original} - URL: {DETAIL_URL.format(cuit_num)}")
    driver.get(DETAIL_URL.format(cuit_num))
    time.sleep(2)

    # Extraer teléfonos
    telefonos = extraer_telefonos()
    df.at[idx, 'Celular 1'] = telefonos[0] if len(telefonos) > 0 else ""
    df.at[idx, 'Celular 2'] = telefonos[1] if len(telefonos) > 1 else ""

    # Extraer grupo familiar
    familia = extraer_familia()
    if familia:
        for i, (nombre, par) in enumerate(familia[:4]):  # Hasta 4 familiares
            df.at[idx, f'Familiar {i+1}'] = nombre
            df.at[idx, f'Parentesco {i+1}'] = par

    # Guardado parcial por seguridad
    df.to_excel(OUTPUT_PATH, index=False)
    print(f" Fila {idx+1} procesada y guardada")

print(" Proceso COMPLETO")
driver.quit()
df.to_excel(OUTPUT_PATH, index=False)
