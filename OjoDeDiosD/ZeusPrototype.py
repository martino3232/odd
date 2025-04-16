import os
BASE_DIR = os.path.dirname(__file__)
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')  # Sacalo si querés ver la ejecución
driver = webdriver.Chrome(options=options)

# Cargar la base
df = pd.read_excel(os.path.join(BASE_DIR, 'BaseFinalGrupoFamiliar_ConDatos.xlsx'))

for index, row in df.iterrows():
    nombre_completo = str(row['Nombre'])
    localidad_raw = str(row['Localidad'])
    apellido = nombre_completo.split()[0]
    localidad = localidad_raw.split('-')[0].strip()

    print(f" Buscando APELLIDO: {apellido} | LOCALIDAD: {localidad}")

    try:
        driver.get("http://www.paginasblancas.com.ar/")
        time.sleep(2)
        driver.find_element(By.ID, "nName").send_keys(apellido)
        driver.find_element(By.ID, "nLocality").send_keys(localidad)
        driver.find_element(By.ID, "btnSrchName").click()
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        resultados = soup.find_all("li", class_="m-results-business m-results-subscriber")

        familiares = []
        telefonos = []

        for res in resultados:
            try:
                nombre = res.find("h3").text.strip()
                telefono = res.find("span", class_="m-icon--single-phone").text.strip()
                if nombre:
                    familiares.append(nombre)
                if telefono:
                    telefonos.append(telefono)
            except:
                continue

        # Escribir familiares como Familiar_1, Familiar_2...
        for i, fam in enumerate(familiares):
            df.at[index, f'Familiar {i+1}'] = fam

        # Escribir teléfonos como Telefono_1, Telefono_2...
        for i, tel in enumerate(telefonos):
            df.at[index, f'Telefono {i+1}'] = tel

    except Exception as e:
        print(f" Error en {apellido}: {e}")
        df.at[index, 'Familiar 1'] = "Error"
        df.at[index, 'Telefono 1'] = "Error"

    # GUARDA EN CADA PASO
    df.pd.read_excel(os.path.join(BASE_DIR, 'Base_Enriquecida_Estructurada.xlsx')), index=False)
    print(f" Registro {index + 1} guardado")

driver.quit()
print(" ENRIQUECIMIENTO COMPLETO - Archivo generado: Base_Enriquecida_Estructurada.xlsx")
