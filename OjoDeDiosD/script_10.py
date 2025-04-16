import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

localidad = sys.argv[1] if len(sys.argv) > 1 else "No especificada"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

url_paginas_blancas = "http://www.paginasblancas.com.ar/persona/"

nombres = [
    "Felipe", "Gabriel", "Hernán", "Iñaki", "Joaquín", "Luis", "Maximiliano", "Néstor", "Omar", "Ramón","Diana", "Emilia", "Florencia", "Gloria", "Herminia", "Ivonne", "Julieta", "Miriam", "Nuria", "Patricia"
]

for nombre in nombres:
    print(f" Buscando '{nombre}' en '{localidad}'...")
    driver.get(url_paginas_blancas)
    time.sleep(3)

    try:
        campo_nombre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nName"))
        )
        campo_nombre.clear()
        campo_nombre.send_keys(nombre)
        time.sleep(1)

        campo_localidad = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nLocality"))
        )
        campo_localidad.clear()
        campo_localidad.send_keys(localidad)
        time.sleep(1)

        boton_buscar = driver.find_element(By.ID, "btnSrchName")
        boton_buscar.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "m-results-business"))
        )

        resultados = []
        for elemento in driver.find_elements(By.CLASS_NAME, "m-results-business"):
            try:
                nombre_extraido = elemento.find_element(By.CLASS_NAME, "m-results-business--name").text.strip()
            except:
                nombre_extraido = "No disponible"

            try:
                direccion = elemento.find_element(By.CLASS_NAME, "m-results-business--address").text.strip()
            except:
                direccion = "No disponible"

            try:
                boton_ver_telefono = elemento.find_element(By.CLASS_NAME, "m-button--results-business--see-phone")
                driver.execute_script("arguments[0].click();", boton_ver_telefono)
                time.sleep(2)
                
                telefono_element = elemento.find_element(By.CLASS_NAME, "m-icon--single-phone").find_element(By.TAG_NAME, "a")
                telefono = telefono_element.text.strip()
            except:
                telefono = "No disponible"

            partes_direccion = direccion.split(',')
            calle = partes_direccion[0].strip() if len(partes_direccion) > 0 else "No disponible"
            localidad_res = partes_direccion[1].strip() if len(partes_direccion) > 1 else "No disponible"
            provincia = partes_direccion[2].strip() if len(partes_direccion) > 2 else "No disponible"

            resultados.append({
                "Nombre": nombre_extraido,
                "Teléfono": telefono,
                "Calle": calle,
                "Localidad": localidad_res,
                "Provincia": provincia
            })

        df = pd.DataFrame(resultados)
        df.to_excel(f"{nombre}.xlsx", index=False)

    except Exception as e:
        print(f" Error con '{nombre}' en '{localidad}':", e)

print(" Finalizó la búsqueda para este script.")
driver.quit()
