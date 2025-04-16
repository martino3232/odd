import os
BASE_DIR = os.path.dirname(__file__)
import pandas as pd
import random

# Rutas
INPUT_PATH = "Base_Final_PRO_Vinculos.xlsx"
OUTPUT_PATH = "Base_Final_PRO_Vinculos_MovilCompleto.xlsx"

# Función para generar número celular con formato fijo
def generar_movil():
    parte1 = random.randint(1000, 9999)
    parte2 = random.randint(1000, 9999)
    return f"(011) {parte1}-{parte2}"

# Cargar Excel original
df = pd.read_excel(INPUT_PATH)

# Ubicación de la columna "Teléfono"
idx_telefono = df.columns.get_loc("Teléfono")

# Insertar móviles ficticios después de "Teléfono"
df.insert(idx_telefono + 1, "Móvil 1", [generar_movil() for _ in range(len(df))])
df.insert(idx_telefono + 2, "Móvil 2", [generar_movil() for _ in range(len(df))])

# Pasar todo a mayúsculas
df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Guardar nuevo archivo
df.to_excel(OUTPUT_PATH, index=False)
print(f" Archivo listo con móviles agregados y todo en MAYÚSCULAS → {OUTPUT_PATH}")
