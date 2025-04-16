import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Capturar la localidad pasada como parámetro
localidad = sys.argv[1] if len(sys.argv) > 1 else "No especificada"

# Configuración de Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

# URL de Páginas Blancas
url_paginas_blancas = "http://www.paginasblancas.com.ar/persona/"

# Lista de nombres (200 únicos para este script)
nombres = [
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
    "Manuela", "Marcela Andrea", "Margarita", "Marina", "Marisa", "Marta", "Mercedes", "Mirta", "Mónica", "Mora", "Adela", "Adriana", "Aída", "Alicia", "Amalia", "Ana", "Andrea", "Angela", "Antonia", "Beatriz",
    "Blanca", "Camila", "Candela", "Carina", "Carla", "Carmen", "Cecilia", "Clara", "Claudia", "Cristina",
    "Delfina", "Delia", "Diana", "Dina", "Dorotea", "Elena", "Elisa", "Elizabeth", "Elsa", "Emilia",
    "Estela", "Ester", "Eugenia", "Eva", "Fabiola", "Fátima", "Felisa", "Florencia", "Francisca", "Gabriela",
    "Genoveva", "Georgina", "Gladys", "Gloria", "Graciela", "Guadalupe", "Haydée", "Helena", "Hilda", "Ilda",
    "Inés", "Irma", "Isabel", "Josefina", "Juana", "Julia", "Julieta", "Justina", "Laura", "Leonor",
    "Leticia", "Liliana", "Lina", "Lorena", "Lucía", "Lucrecia", "Luisa", "Luz", "Magdalena", "Manuela",
    "Marcela", "Margarita", "María", "Marina", "Marta", "Martina", "Matilde", "Mercedes", "Micaela", "Miriam",
    "Modesta", "Nélida", "Nidia", "Noemí", "Norma", "Olga", "Patricia", "Paula", "Raquel", "Rebeca",
    "Rita", "Roberta", "Rocío", "Rosa", "Rosalía", "Silvia", "Sonia", "Susana", "Teresa", "Victoria","Aarón","Abel","Abraham","Adrián","Agustín","Alan","Alberto","Alejandro","Alfredo","Alonso",
"Amado","Américo","Andrés","Aníbal","Antonio","Ariel","Armando","Arnaldo","Arturo","Axel",
"Baltasar","Bartolomé","Benjamín","Bernardo","Blas","Brandon","Bruno","Camilo","Carlos","Carmelo",
"Cayetano","César","Cristian","Cristóbal","Damián","Danilo","Daniel","Dante","Darío","David",
"Diego","Dionisio","Domingo","Edgardo","Eduardo","Elías","Emanuel","Emiliano","Emilio","Enrique",
"Eric","Ernesto","Esteban","Eugenio","Ezequiel","Fabián","Facundo","Feliciano","Felipe","Fernando",
"Fermín","Fidel","Flavio","Florencio","Franco","Francisco","Gabriel","Gaspar","Gastón","Germán",
"Gerónimo","Gian","Gino","Gonzalo","Gregorio","Guido","Guillermo","Gustavo","Héctor","Hernán",
"Homero","Horacio","Hugo","Ian","Ignacio","Iker","Isaac","Ismael","Iván","Jacinto",
"Jaime","Javier","Jeremías","Jerónimo","Jesús","Joaquín","Joel","Jonás","Jonathan","Jorge",
"José","Josué","Juan","Julián","Julio","Justo","Kevin","Lautaro","Leandro","Leonardo",
"Lázaro","León","Lisandro","Lorenzo","Lucas","Luciano","Luis","Manuel","Marcelo","Marco",
"Marcos","Mariano","Mario","Martín","Matías","Mauricio","Maximiliano","Miguel","Milton","Nahuel",
"Narciso","Nicolás","Noé","Norberto","Octavio","Oliver","Omar","Oscar","Pablo","Patricio",
"Pedro","Pepe","Próspero","Ramiro","Rafael","Raúl","Renato","Renzo","Ricardo","Roberto",
"Rodrigo","Rolando","Román","Roque","Rubén","Salvador","Samuel","Sandro","Santiago","Sebastián",
"Sergio","Silvio","Simón","Teodoro","Thiago","Tobías","Tomás","Ulises","Valentín","Vicente",
"Víctor","Walter","Washington","Wenceslao","Wilfredo","Xavier","Yamil","Yago","Yeray","Yuri",
"Zacarías","Zaid","Abelardo","Adolfo","Aldo","Alejo","Alonso","Anselmo","Apolinario","Aquilino",
"Arístides","Aron","Asdrúbal","Atilio","Baldomero","Baltazar","Bartolo","Beltrán","Benito","Beremundo",
"Blas","Bonifacio","Braulio","Calixto","Casimiro","Ceferino","Celestino","Ciriaco","Cirilo","Claudio",
"Clemente","Colo","Conrado","Cornelio","Crisanto","Cristóforo","Dámaso","Demetrio","Dionel","Donato",
"Doroteo","Edu","Edelmiro","Edelio","Eleuterio","Eligio","Elvio","Elmer","Epifanio","Erasmo",
"Erico","Ernán","Eufemio","Eulogio","Eusebio","Evangelino","Evaristo","Eze","Fabricio","Fabián",
"Faustino","Favio","Federico","Feliciano","Fermín","Fidel","Filemón","Floro","Froilán","Genaro",
"Gervasio","Gilberto","Gino","Gregorio","Guido","Heladio","Herminio","Heriberto","Higinio","Hipólito",
"Honorio","Humberto","Ildefonso","Inocencio","Isauro","Isidoro","Ivo","Jacobo","Jairo","Jan",
"Jenaro","Jesualdo","Joaquim","Jonatan","Jordán","Josías","Juanjo","Juli","Justino","Lamberto",
"Lázaro","Leopoldo","Liborio","Lino","Lisandro","Lope","Lucio","Luisito","Manolo","Manu",
"Marcial","Margarito","Mariano","Marino","Mauro","Maxi","Melchor","Modesto","Moisés","Nando",
"Napoleón","Nazareno","Nemesio","Nestor","Nevin","Norberto","Olegario","Onésimo","Orlando","Osvaldo",
"Otto","Pancho","Pascual","Pastor","Pelayo","Perfecto","Pericles","Pío","Placido","Porfirio",
"Protasio","Quirino","Rai","Raimundo","Ramón","Reinaldo","Remigio","Reynaldo","Rito","Robín",
"Rodolfo","Rolón","Romualdo","Rosendo","Rubí","Rufino","Salomón","Sandalio","Sansón","Saturnino",
"Segundo","Severo","Silverio","Sixto","Tadeo","Telmo","Telesforo","Teobaldo","Teodoro","Timoteo",
"Tito","Toribio","Tristán","Ubaldo","Urbano","Valerio","Valeriano","Vespasiano","Vicente","Vidal",
"Vito","Wilmer","Yago","Zacarías","Zelmar","Zósimo","Abilio","Adonay","Aureliano","Cristhian",
"Duilio","Edel","Ever","Fermín","Gil","Horacio","Isandro","Jahir","Julen","Levin",
"Maico","Nicanor","Ovidio","Paolo","Quintín","Rodolfo","Salvador","Tadeo","Valentín","Zamir"
]

# Procesar cada nombre
for nombre in nombres:
    print(f" Buscando '{nombre}' en '{localidad}'...")

    driver.get(url_paginas_blancas)
    time.sleep(3)

    try:
        campo_nombre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nName"))
        )
        campo_nombre.clear()
        campo_nombre.send_keys(nombre)
        time.sleep(1)

        campo_localidad = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nLocality"))
        )
        campo_localidad.clear()
        campo_localidad.send_keys(localidad)
        time.sleep(1)

        boton_buscar = driver.find_element(By.ID, "btnSrchName")
        boton_buscar.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "m-results-business"))
        )

        resultados = []
        for elemento in driver.find_elements(By.CLASS_NAME, "m-results-business"):
            try:
                nombre_extraido = elemento.find_element(By.CLASS_NAME, "m-results-business--name").text.strip()
            except:
                nombre_extraido = "No disponible"

            try:
                direccion = elemento.find_element(By.CLASS_NAME, "m-results-business--address").text.strip()
            except:
                direccion = "No disponible"

            try:
                boton_ver_telefono = elemento.find_element(By.CLASS_NAME, "m-button--results-business--see-phone")
                driver.execute_script("arguments[0].click();", boton_ver_telefono)
                time.sleep(2)
                
                telefono_element = elemento.find_element(By.CLASS_NAME, "m-icon--single-phone").find_element(By.TAG_NAME, "a")
                telefono = telefono_element.text.strip()
            except:
                telefono = "No disponible"

            partes_direccion = direccion.split(',')
            calle = partes_direccion[0].strip() if len(partes_direccion) > 0 else "No disponible"
            localidad_res = partes_direccion[1].strip() if len(partes_direccion) > 1 else "No disponible"
            provincia = partes_direccion[2].strip() if len(partes_direccion) > 2 else "No disponible"

            resultados.append({
                "Nombre": nombre_extraido,
                "Teléfono": telefono,
                "Calle": calle,
                "Localidad": localidad_res,
                "Provincia": provincia
            })

        df = pd.DataFrame(resultados)
        df.to_excel(f"{nombre}.xlsx", index=False)

    except Exception as e:
        print(f" Error con '{nombre}' en '{localidad}':", e)

print(" Finalizó la búsqueda para este script.")
driver.quit()
