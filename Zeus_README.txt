
Zeus - Sistema de Enriquecimiento de Datos y Vínculos Familiares

 Descripción General
Zeus es un sistema automatizado de scraping y enriquecimiento de datos familiares. A partir de una base de personas con datos básicos (CUIT, Nombre, Teléfono, Domicilio), el sistema:
- Busca familiares en fuentes públicas
- Obtiene CUIT y teléfonos adicionales
- Calcula la fecha de nacimiento estimada
- Determina el vínculo familiar (Padre, Hijo, Hermano)
- Genera un Excel final estructurado y profesional

 ¿Qué hace exactamente el sistema?
1. Carga la base inicial
2. Scrapea Páginas Blancas por apellido y localidad
3. Scrapea CUIT Online
4. Calcula Fecha de Nacimiento Estimada (Regresión Lineal)
5. Calcula Vínculo Familiar con lógica propia
6. Estructura la base final completa

 Formato de Salida Final (Excel):
Nacimiento | CUIT | Nombre | Teléfono | Calle | Localidad | Familiar 2 | Vínculo 2 | Fecha 2 | CUIT 2 | Teléfono 2 | Familiar 3 | …

 Tecnologías Utilizadas
- Python 3
- Selenium, BeautifulSoup
- Pandas, Numpy, Scikit-Learn

 Características Técnicas Clave
✔ Guarda en cada iteración (robustez)
✔ Escalable (2000+ registros diarios)
✔ Vínculos familiares calculados
✔ Exportable a CRMs y sistemas externos

 Casos de Uso Reales
✔ Enriquecimiento de bases comerciales
✔ Scoring financiero
✔ Marketing familiarizado
✔ Validación de redes familiares
✔ Modelos predictivos

 Requisitos
- Python 3.9+
- Chrome + Chromedriver
- Paquetes: selenium, pandas, numpy, scikit-learn, openpyxl, beautifulsoup4

 Estado: FUNCIONAL - LISTO PARA PRODUCCIÓN

