import os
BASE_DIR = os.path.dirname(__file__)
import pandas as pd

archivo_base = "Base_Final_Con_Cuits_Fecha.xlsx"
archivo_salida = "Base_Final_PRO_Vinculos.xlsx"

df = pd.read_excel(archivo_base)

# 1️⃣ - BORRAR Familiar 1 y eliminar duplicados
if "Familiar 1" in df.columns:
    df.drop(columns=["Familiar 1"], inplace=True)

df = df.drop_duplicates()

# 2️⃣ - Calcular Vínculo Familiar comparando FECHAS
for index, row in df.iterrows():
    try:
        titular_anio = int(str(row["Fecha Nacimiento Estimada"]).split("-")[1])
    except:
        titular_anio = None

    for i in range(2, 6):  # Familiar 2 al 5
        try:
            fam_fecha = str(row[f"Fecha Familiar {i}"])
            fam_anio = int(fam_fecha.split("-")[1])
        except:
            fam_anio = None

        if titular_anio and fam_anio:
            diferencia = fam_anio - titular_anio
            if diferencia <= -18:
                vinculo = "Padre/Madre"
            elif -17 <= diferencia <= -5:
                vinculo = "Hermano/a"
            elif -4 <= diferencia <= 4:
                vinculo = "Hermano/a"
            elif 5 <= diferencia <= 17:
                vinculo = "Hermano/a Menor"
            elif diferencia >= 18:
                vinculo = "Hijo/a"
            else:
                vinculo = "Sin determinar"
        else:
            vinculo = "Sin determinar"

        # Agregar columna de vínculo
        df.at[index, f"Vinculo Familiar {i}"] = vinculo

# 3️⃣ - REORDENAR columnas como pediste:
base_cols = ["Fecha Nacimiento Estimada", "CUIT", "Nombre", "Teléfono", "Calle", "Localidad"]
final_cols = base_cols

for i in range(2, 6):
    final_cols += [
        f"Familiar {i}",
        f"Vinculo Familiar {i}",
        f"Fecha Familiar {i}",
        f"Cuit Familiar {i}",
        f"Tel Familiar {i}"
    ]

# 4️⃣ - Aplicar el orden y exportar
df = df[final_cols]
df.to_excel(archivo_salida, index=False)
df.columns = df.columns.str.strip()


print(f" PROCESO FINALIZADO - Archivo generado: {archivo_salida}")

