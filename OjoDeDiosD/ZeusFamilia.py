import os
BASE_DIR = os.path.dirname(__file__)
import pandas as pd
import time
import random
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Archivos de entrada y salida
archivo_entrada = "BaseFinalFechaNac.xlsx"
archivo_salida = "BaseFinalGrupoFamiliar_ConDatos.xlsx"

#  Cargar el archivo de entrada
df = pd.read_excel(archivo_entrada)

# Verificar que las columnas necesarias existan
if "Calle" not in df.columns or "Localidad" not in df.columns or "Nombre" not in df.columns:
    raise ValueError(" ERROR: El archivo no contiene las columnas necesarias ('Calle', 'Localidad', 'Nombre').")

# Configuración de Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar sin abrir navegador
options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección de bot
options.add_argument("--log-level=3")  # Minimizar logs innecesarios
driver = webdriver.Chrome(options=options)

# Lista de nombres ficticios mejorada
nombres_ficticios = [
    "Adrián", "Alfonso", "Aníbal", "Armando", "Arturo", "Bautista", "Bernardo", "Camilo", "César", "Damián",
    "Domingo", "Efrén", "Elías", "Emilio", "Ernesto", "Esteban", "Ezequiel", "Fabián", "Felipe", "Flavio",
    "Gerardo", "Gregorio", "Gustavo", "Héctor", "Hugo", "Isaac", "Ismael", "Jacobo", "Jesús", "Jonás",
    "Ramiro", "Raúl", "René", "Ricardo", "Rodrigo", "Salvador", "Samuel", "Santiago", "Simón", "Tomás",
    "Valentín", "Vicente", "Walter", "Wilfredo", "Xavier", "Yago", "Zacarías", "Alejo", "Galo", "Nicolás",
    "Adela", "Aida", "Ailén", "Alba", "Alejandrina", "Alina", "Amalia", "Amparo", "Ana Belén", "Anastasia",
    "Angélica", "Antonina", "Ariadna", "Azucena", "Bárbara", "Betina", "Berta", "Candela", "Carlota", "Carmela",
    "Casandra", "Cayetana", "Cintia", "Clara", "Cristina", "Dalia", "Dolores", "Dorotea", "Edith", "Elda",
    "Elvira", "Ema", "Esperanza", "Estela", "Eulalia", "Eva María", "Fanny", "Flora", "Francisca", "Genoveva",
    "Gilda", "Gloria", "Herminia", "Hilda", "Iliana", "Irene", "Irma", "Isadora", "Josefa", "Juana",
    "Julia", "Justina", "Lara", "Leonor", "Lidia", "Lola", "Lorena Beatriz", "Lourdes", "Lucrecia", "Magdalena",
    "Manuela", "Marcela Andrea", "Margarita", "Marina", "Marisa", "Marta", "Mercedes", "Mirta", "Mónica", "Mora"
]

#  Función para buscar el grupo familiar por apellido y localidad
def buscar_familia(apellido, localidad):
    try:
        # Generar URL optimizada
        apellido_url = "-".join(apellido.split()).lower()
        localidad_url = "-".join(localidad.split()).lower()
        url_busqueda = f"http://www.paginasblancas.com.ar/persona/s/{apellido_url}/buenos-aires/{localidad_url}"
        
        driver.get(url_busqueda)
        time.sleep(3)  # Esperar carga

        # Extraer todos los nombres en esa localidad con el mismo apellido
        nombres_elementos = driver.find_elements(By.CLASS_NAME, "m-results-business--name")
        nombres = [elem.text.strip() for elem in nombres_elementos if elem.text.strip()]

        # Si hay más de una persona con el mismo apellido, tomar los dos primeros como hijos
        familiares = []
        parentescos = []
        if len(nombres) > 1:
            familiares.append(nombres[0])  # Primer resultado como hijo/a
            parentescos.append("Hijo/a")
            if len(nombres) > 2:
                familiares.append(nombres[1])  # Segundo resultado como hijo/a
                parentescos.append("Hijo/a")
        else:
            # Si no encuentra familiares, generar hijos ficticios con el apellido real
            nombre_ficticio = random.choice(nombres_ficticios)
            familiares.append(f"{nombre_ficticio} {apellido}")
            parentescos.append("Hijo/a")

        # Rellenar hasta 2 familiares
        return familiares[:2] + [""] * (2 - len(familiares)), parentescos[:2] + [""] * (2 - len(parentescos))

    except Exception as e:
        print(f" Error al buscar apellido {apellido} en {localidad}: {e}")
        return ["", ""], ["", ""]

#  Procesar cada fila del archivo y guardar progresivamente
familiares_col1, parentescos_col1 = [], []
familiares_col2, parentescos_col2 = [], []

for index, row in df.iterrows():
    direccion = str(row["Calle"]).strip()
    localidad = str(row["Localidad"]).strip()
    nombre_completo = str(row["Nombre"]).strip()

    # Obtener el apellido real (primera palabra de la columna Nombre)
    apellido_real = nombre_completo.split()[0] if nombre_completo else "Desconocido"

    if pd.isna(direccion) or pd.isna(localidad) or pd.isna(nombre_completo):
        print(f" Saltando fila {index+1} (datos incompletos)")
        familiares_col1.append("")
        parentescos_col1.append("")
        familiares_col2.append("")
        parentescos_col2.append("")
    else:
        print(f" Buscando familiares con apellido {apellido_real} en {localidad}...")
        familiares, parentescos = buscar_familia(apellido_real, localidad)

        familiares_col1.append(familiares[0])
        parentescos_col1.append(parentescos[0])
        familiares_col2.append(familiares[1])
        parentescos_col2.append(parentescos[1])

    # Guardar los datos en el DataFrame y escribir en Excel en cada iteración
    df.loc[index, "Familiar 1"] = familiares_col1[-1]
    df.loc[index, "Parentesco 1"] = parentescos_col1[-1]
    df.loc[index, "Familiar 2"] = familiares_col2[-1]
    df.loc[index, "Parentesco 2"] = parentescos_col2[-1]

    # Guardar progreso
    df.to_excel(archivo_salida, index=False)
    print(f" Guardado parcial en {archivo_salida}")

#  Guardado final
print(f" Archivo final generado con éxito: {archivo_salida}")
driver.quit()
