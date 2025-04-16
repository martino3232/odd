import pandas as pd
import os

# Nombre del archivo de salida
archivo_salida = "BaseFinal.xlsx"

# Obtener la lista de archivos .xlsx en la carpeta actual
archivos = [f for f in os.listdir() if f.endswith(".xlsx") and f != archivo_salida]

# Crear una lista para almacenar los datos
datos_totales = []

print(f" Se encontraron {len(archivos)} archivos Excel para procesar.")

# Procesar cada archivo Excel
for archivo in archivos:
    print(f" Procesando: {archivo}")

    try:
        # Cargar el archivo Excel
        df = pd.read_excel(archivo, usecols="A:D")  #  Solo las columnas A a D

        # Agregar los datos a la lista
        datos_totales.append(df)

    except Exception as e:
        print(f" Error al procesar {archivo}: {e}")

# Unir todos los datos en un solo DataFrame
if datos_totales:
    df_final = pd.concat(datos_totales, ignore_index=True)

    # Guardar en un archivo Excel final
    df_final.to_excel(archivo_salida, index=False)

    print(f" Base final generada con éxito: {archivo_salida}")
else:
    print(" No se encontraron datos para combinar.")
