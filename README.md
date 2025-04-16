
# 🧠 Ojo de Dios Definitivo

Herramienta automatizada de enriquecimiento de datos personales con ejecución web vía Flask + Selenium.

## 🚀 ¿Qué hace?

- Búsqueda por código postal o localidad
- Ejecución de scrapers paralelos
- Enriquecimiento con CUIT, grupo familiar, vínculos y fecha de nacimiento
- Consola en vivo desde navegador

## 📦 Tecnologías

- Python 3.11
- Flask
- Selenium + Chromium Headless
- Pandas / Excel
- Railway (deploy con Docker)

## 📂 Estructura

```
📁 OjoDeDiosD/
├── app.py
├── Zeuz.py
├── scripts_x.py
├── templates/
├── static/
├── Dockerfile
├── Procfile
├── requirements.txt
```

## ▶️ Uso local

```bash
git clone https://github.com/martino3232/odd
cd odd
pip install -r requirements.txt
python app.py
```

Acceder a `http://localhost:5501`

## ☁️ Deploy a Railway

1. Subí este repo completo (con Dockerfile y Procfile)
2. En Railway: “Deploy from GitHub repo”
3. Railway detecta automáticamente el Dockerfile
4. Se expone en `https://NOMBRE.up.railway.app`

## 🧠 Autor

Ezequiel Martino – CEO @ SisApp 🚀
