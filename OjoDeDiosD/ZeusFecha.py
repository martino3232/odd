import os
BASE_DIR = os.path.dirname(__file__)
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#  Archivos de entrada y salida
archivo_entrada = "BaseFinalDni.xlsx"
archivo_salida = "BaseFinalFechaNac.xlsx"

#  Cargar el archivo de entrada
df = pd.read_excel(archivo_entrada)

# Verificar que la columna CUIT existe
if "CUIT" not in df.columns:
    raise ValueError(" ERROR: El archivo no contiene una columna CUIT.")

#  Extraer DNI correctamente desde CUIT
df["DNI"] = df["CUIT"].astype(str).str[3:-2]  # Elimina los primeros 3 caracteres y los últimos 2

# Filtrar solo DNIs numéricos
df = df[df["DNI"].str.isnumeric()]

# Verificar si la columna DNI quedó vacía
if df.empty:
    raise ValueError(" ERROR: No se encontraron DNIs válidos en el archivo. Revisa que los CUITs sean correctos.")

df["DNI"] = df["DNI"].astype(int)

# 🔢 Datos de referencia (DNI → Año de nacimiento) basados en lo que me diste
dni_referencia = np.array([44143744, 21920804, 16000000, 43020840]).reshape(-1, 1)
nacimiento_referencia = np.array([2002, 1970, 1964, 2000])  # Años reales de nacimiento

#  Ajustar modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(dni_referencia, nacimiento_referencia)

# 📅 Generar la fecha de nacimiento estimada
def estimar_fecha_nacimiento(dni):
    dni_str = str(dni)
    
    # 🚨 Excepción: Si el DNI comienza con 9, asignar "EXTRANJERO"
    if dni_str.startswith("9"):
        return "EXTRANJERO"
    
    # Calcular año de nacimiento usando el modelo
    anio_estimado = int(modelo.predict([[dni]])[0])
    
    # Generar un mes aleatorio entre 1 y 12
    mes_estimado = np.random.randint(1, 13)
    
    return f"{mes_estimado:02d}-{anio_estimado}"  # Formato MM-YYYY

# Aplicar la función a la columna DNI
df["Fecha Nacimiento Estimada"] = df["DNI"].apply(estimar_fecha_nacimiento)

# 🗂️ Reorganizar columnas: Poner la fecha de nacimiento al inicio y mantener TODAS las columnas
columnas_finales = ["Fecha Nacimiento Estimada"] + list(df.columns[:-1])  # Mantenemos todas las columnas
df_final = df[columnas_finales]

#  Guardar archivo final con todas las columnas
df_final.to_excel(archivo_salida, index=False)

print(f" Archivo generado con éxito: {archivo_salida}")
