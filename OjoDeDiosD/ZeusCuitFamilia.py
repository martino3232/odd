import os
BASE_DIR = os.path.dirname(__file__)
import pandas as pd
import time
import urllib.parse
import numpy as np
from sklearn.linear_model import LinearRegression
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Archivos
archivo_entrada = "Base_Enriquecida_Estructurada.xlsx"
archivo_salida = "Base_Final_Con_Cuits_Fecha.xlsx"

df = pd.read_excel(archivo_entrada)

#  Entrenamos el modelo de regresión DNI → Año Nacimiento
dni_ref = np.array([44143744, 21920804, 16000000, 43020840]).reshape(-1, 1)
nac_ref = np.array([2002, 1970, 1964, 2000])
modelo = LinearRegression()
modelo.fit(dni_ref, nac_ref)

def estimar_fecha_nacimiento(cuit):
    try:
        dni_str = str(cuit)[3:-2]
        if not dni_str.isnumeric():
            return "No estimable"
        if dni_str.startswith("9"):
            return "EXTRANJERO"
        dni = int(dni_str)
        anio_estimado = int(modelo.predict([[dni]])[0])
        mes = np.random.randint(1, 13)
        return f"{mes:02d}-{anio_estimado}"
    except:
        return "No estimable"

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)
url_base = "https://www.cuitonline.com/search.php?q="

familiares = ["Familiar 2", "Familiar 3", "Familiar 4", "Familiar 5"]
telefonos = ["Telefono 2", "Telefono 3", "Telefono 4", "Telefono 5"]

print(f" Procesando {len(df)} filas...")

for index, row in df.iterrows():
    print(f"\n Fila {index+1} - Procesando familiares...")

    salida_final = {}

    for i, familiar_col in enumerate(familiares):
        nombre_familiar = str(row.get(familiar_col, "")).strip()
        telefono_familiar = str(row.get(telefonos[i], "")).strip()

        if nombre_familiar == "" or nombre_familiar == "nan":
            print(f" {familiar_col} vacío, salto...")
            salida_final[f"{familiar_col}"] = ""
            salida_final[f"Fecha {familiar_col}"] = ""
            salida_final[f"Cuit {familiar_col}"] = ""
            salida_final[f"Tel {familiar_col}"] = telefono_familiar
            continue

        # Buscar CUIT
        print(f" Buscando CUIT de: {nombre_familiar}")
        try:
            nombre_encoded = urllib.parse.quote(nombre_familiar)
            url = url_base + nombre_encoded
            driver.get(url)
            time.sleep(3)

            try:
                cuit_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cuit"))
                )
                cuit = cuit_element.text.strip()
            except:
                cuit = "No encontrado"
        except Exception as e:
            print(f" Error en búsqueda: {e}")
            cuit = "No encontrado"

        # Estimar fecha si hay CUIT válido
        fecha_estimada = estimar_fecha_nacimiento(cuit) if "No encontrado" not in cuit else "No estimable"

        # Guardar en orden Familiar - Fecha - CUIT - Tel
        salida_final[f"{familiar_col}"] = nombre_familiar
        salida_final[f"Fecha {familiar_col}"] = fecha_estimada
        salida_final[f"Cuit {familiar_col}"] = cuit
        salida_final[f"Tel {familiar_col}"] = telefono_familiar

    # Guardar por fila
    for key, value in salida_final.items():
        df.at[index, key] = value

    #  Guardar en cada iteración
    df.to_excel(archivo_salida, index=False)
    print(f" Fila {index+1} guardada")

driver.quit()
print(f" PROCESO COMPLETO - Archivo generado: {archivo_salida}")
