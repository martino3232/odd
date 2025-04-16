import subprocess
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
import os

def obtener_localidad_desde_cp(cp):
    """Consulta codigo-postal.ar con el CP y devuelve la localidad."""
    url_busqueda = "https://codigo-postal.ar/search"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.post(url_busqueda, data={"search": cp}, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        resultado = soup.find("div", class_="postnummer-item")
        if resultado:
            texto = resultado.text.strip()
            if " - " in texto:
                return texto.split(" - ")[1].title()  # Devuelve "Adrogue"
        return None

    except Exception as e:
        print(f" Error buscando la localidad para el CP {cp}: {e}")
        return None


def ejecutar_script(script, *args):
    """Ejecuta un script pasándole argumentos opcionales."""
    script_path = os.path.join(os.path.dirname(__file__), script)
    subprocess.run(["python", script_path, *args], check=True)



if __name__ == "__main__":
    multiprocessing.freeze_support()  #  NECESARIO EN WINDOWS 

    print("""
    =============================================
     BIENVENIDO AL OJO DE DIOS DEFINITIVO 
    =============================================
    """)

    print("1. Buscar por código postal")
    print("2. Buscar por localidad manual")
    print("3. Armar base de la última búsqueda")
    opcion = input("Seleccione una opción (1, 2 o 3): ").strip()

    localidad = None

    if opcion == "1":
        cp = input(" Ingrese el Código Postal (solo números): ").strip()
        localidad = obtener_localidad_desde_cp(cp)

        if not localidad:
            print(" No se pudo obtener la localidad. Finalizando.")
            exit()
        print(f" Localidad encontrada: {localidad}")

    elif opcion == "2":
        localidad = input(" Ingrese la localidad exacta a buscar: ").strip().title()
        if not localidad:
            print(" Localidad inválida. Finalizando.")
            exit()
        print(f" Localidad ingresada: {localidad}")

    if opcion in ["1", "2"]:
        scripts_busqueda = [f"script_{i}.py" for i in range(1, 11)]
        procesos = []

        try:
            for script in scripts_busqueda:
                p = multiprocessing.Process(target=ejecutar_script, args=(script, localidad))
                p.start()
                procesos.append(p)

            for p in procesos:
                p.join()

        except KeyboardInterrupt:
            print("  Búsqueda interrumpida. Guardando datos hasta el momento...")

    if opcion in ["1", "2", "3"]:
        print(" Ahora comenzamos con el procesamiento de datos...")
        ejecutar_script("ZeuzUnifier.py")
        ejecutar_script("ZeusCuit.py")
        ejecutar_script("ZeusFecha.py")
        ejecutar_script("ZeusFamilia.py")
        ejecutar_script("ZeusPrototype.py")
        ejecutar_script("ZeusCuitFamilia.py")
        ejecutar_script("zeuzvinculo.py")
        ejecutar_script("ZeuzFormat.py")

        print(" Todo el proceso ha finalizado con éxito.")
