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

# Lista de nombres para este script (200 nombres únicos)
nombres = [
    "Agustín", "Alejandro", "Álvaro", "Andrés", "Antonio", "Ariel", "Benjamín", "Bruno", "Carlos", "Cristian",
    "Daniel", "Darío", "David", "Diego", "Eduardo", "Emanuel", "Emiliano", "Esteban", "Facundo", "Federico",
    "Fernando", "Franco", "Gabriel", "Gastón", "Germán", "Gonzalo", "Guillermo", "Hernán", "Ignacio", "Iván",
    "Javier", "Joaquín", "Jorge", "José", "Juan", "Julián", "Leonardo", "Leandro", "Luciano", "Luis",
    "Abigail", "Agustina", "Alejandra", "Alicia", "Andrea", "Antonella", "Beatriz", "Belén", "Brenda", "Camila",
    "Carla", "Carolina", "Cecilia", "Celeste", "Claudia", "Constanza", "Daniela", "Delfina", "Elena", "Emilia", "Alberto", "Aldo", "Alfonso", "Alfredo", "Aníbal", "Antonio", "Armando", "Arturo", "Baltasar", "Benito",
    "Bernardo", "Carlos", "Cayetano", "Ceferino", "César", "Claudio", "Cristóbal", "Damián", "Daniel", "Dardo",
    "David", "Domingo", "Eduardo", "Eladio", "Elías", "Enrique", "Ernesto", "Esteban", "Evaristo", "Facundo",
    "Federico", "Felipe", "Fernando", "Flavio", "Francisco", "Gabino", "Gaspar", "Germán", "Gilberto", "Gregorio",
    "Guillermo", "Gustavo", "Héctor", "Horacio", "Hugo", "Ignacio", "Isidro", "Jacinto", "Jaime", "Javier",
    "Jerónimo", "Jesús", "Joaquín", "Jorge", "José", "Juan", "Julio", "Justo", "Lautaro", "Leandro",
    "Leonardo", "Lino", "Lisandro", "Lorenzo", "Luis", "Manuel", "Marcelo", "Mariano", "Mario", "Martín",
    "Mateo", "Mauricio", "Miguel", "Néstor", "Nicolás", "Norberto", "Octavio", "Omar", "Orlando", "Osvaldo",
    "Pablo", "Pedro", "Ramón", "Raúl", "Ricardo", "Roberto", "Rodolfo", "Roque", "Rubén", "Salvador","Agustina","Ailén","Alba","Alejandra","Alexa","Alexia","Alicia","Alina","Alma","Amanda",
"Amelia","Ana","Andrea","Angela","Antonella","Ariadna","Ariana","Aurora","Azul","Barbara",
"Beatriz","Belén","Bianca","Brenda","Camila","Candela","Carla","Carmen","Carolina",
"Catalina","Cecilia","Celeste","Clara","Clarisa","Claudia","Constanza","Cristina",
"Dafne","Dalila","Daniela","Delfina","Denisse","Diana","Dolores","Elena","Eliana","Elisa",
"Elizabeth","Ella","Elsa","Emilia","Erika","Esmeralda","Esperanza","Estela","Estefanía",
"Eva","Evelyn","Fabiana","Fátima","Federica","Fernanda","Fiorella","Florencia","Francisca",
"Gabriela","Genoveva","Georgina","Gilda","Gimena","Giovanna","Gloria","Graciela","Guadalupe",
"Helen","Helena","Iliana","Inés","Irene","Isabel","Isabella","Ivana","Ivette","Jacinta",
"Jazmín","Jennifer","Jessica","Jimena","Joana","Josefa","Josefina","Judith","Julia","Juliana",
"Julieta","Justina","Karen","Karina","Karla","Kiara","Laura","Lara","Larisa","Laura",
"Laureana","Leila","Leonor","Leticia","Lia","Lila","Liliana","Lina","Lisa","Lola",
"Lucía","Luciana","Lucrecia","Luisa","Luna","Luz","Magalí","Maia","Malena","Manuela",
"Mara","Marcela","Margarita","María","Mariana","Maricel","Marina","Marisol","Marta","Martina",
"Matilde","Melania","Melina","Mercedes","Micaela","Milagros","Mila","Mireia","Mirta","Miriam",
"Mónica","Nadia","Nancy","Naomi","Natalia","Natividad","Nayla","Nicole","Nidia","Noelia",
"Noemí","Nora","Norma","Olga","Olivia","Ornella","Paloma","Pamela","Patricia","Paula",
"Paulina","Paz","Pilar","Priscila","Rafaela","Ramona","Raquel","Rebeca","Regina","Renata",
"Rita","Roberta","Rocío","Romina","Rosa","Rosalía","Rosana","Rosario","Roxana","Ruth",
"Sabrina","Salma","Samanta","Sandra","Sara","Selena","Selva","Silvana","Silvia","Simona",
"Sofía","Sol","Soledad","Stella","Tamara","Tatiana","Teresa","Thalía","Trinidad","Úrsula",
"Valentina","Valeria","Vanesa","Vega","Verónica","Vicky","Victoria","Vilma","Virginia","Violeta",
"Viviana","Ximena","Yamila","Yara","Yesica","Yolanda","Zaira","Zenaida","Zoe","Adela",
"Adriana","Agnés","Alberta","Alida","Amira","Anabella","Anahí","Analia","Anastasia","Angélica",
"Annette","Antonia","Araceli","Areli","Asia","Assunta","Atenea","Augusta","Aurelia","Ayelén",
"Benita","Bertha","Betina","Blanca","Brígida","Brisa","Calista","Camille","Carina","Carlota",
"Carmela","Carola","Casandra","Cata","Charlene","Chelsea","Chiara","Cinthia","Cira","Claribel",
"Clelia","Clotilde","Colomba","Coral","Corina","Cristal","Cruz","Dalma","Damiana","Daniela",
"Deborah","Débora","Desirée","Diana","Dina","Dominga","Dora","Dulce","Edith","Elda",
"Eleonora","Eli","Eloísa","Elsie","Ema","Emilce","Erica","Ester","Estrella","Eudoxia",
"Eugenia","Eulalia","Eunice","Eusebia","Evelina","Fabiola","Felicitas","Filomena","Flavia","Francesca",
"Freda","Freya","Gabrielle","Gala","Geraldine","Gilda","Gina","Giselle","Greta","Griselda",
"Guillermina","Haley","Hanna","Hortensia","Ida","Ignacia","India","Ingrid","Irina","Isadora",
"Isis","Ivonne","Jacqueline","Jana","Janet","Janina","Jaqueline","Javiera","Jenifer","Jesica",
"Johana","Joice","Jorgelina","Josepha","Joselyn","Juana","Judith","Julene","Julisa","Kaia",
"Kalina","Karla","Kassandra","Katherine","Katya","Kayla","Keila","Kiara","Kira","Kristel",
"Kristina","Lali","Lara","Larisa","Laura","Laurentina","Leandra","Leila","Lena","Leonela",
"Leslie","Leti","Lía","Lilian","Lilibeth","Lina","Linda","Lis","Lisandra","Lissette",
"Livia","Lorena","Lorna","Lourdes","Luana","Ludmila","Luisa","Luján","Luna","Lurdes",
"Luz","Mabel","Macarena","Magda","Magdalena","Maia","Malena","Manola","Mara","Marciana",
"Margarita","Marian","Maricruz","Marilina","Marina","Marisa","Marisol","Maritza","Marta","Martina",
"Matilda","Maura","Mayra","Melba","Melisa","Melody","Mercedes","Mía","Mica","Micaela",
"Miguelina","Milagro","Milena","Mimi","Mina","Mireia","Mirna","Miryam","Mona","Monserrat",
"Morgana","Myrna","Nancy","Narella","Nayara","Nayeli","Nazareth","Nélida","Nerea","Nicoletta",
"Nieves","Nilda","Nina","Noa","Noelia","Nora","Norma","Nuria","Olga","Oriana",
"Palma","Paola","Patricia","Paula","Pilar","Prisila","Purificación","Queralt","Rafaela","Ramira",
"Reina","Remedios","Renée","Reyna","Rina","Rita","Robina","Rocío","Romina","Rosaura",
"Rosmery","Rosmira","Rosy","Roxana","Rubí","Rufina","Ruth","Sabina","Sabrina","Salomé",
"Samantha","Samara","Sandra","Sara","Selene","Selva","Serena","Sheila","Sibila","Silvana",
"Silvia","Simona","Soledad","Solange","Sonia","Soraya","Stella","Susana","Susy","Tamara",
"Tania","Tatiana","Teodora","Teresa","Teresita","Thalia","Trinidad","Ursula","Valeria","Valery",
"Vanina","Vania","Vera","Verónica","Vianey","Vicenta","Vicky","Victoria","Violeta","Virginia",
    "Samuel", "Santiago", "Sergio", "Severino", "Teodoro", "Tomás", "Valentín", "Vicente", "Víctor", "Walter"
]

# Procesar cada nombre en la lista
for nombre in nombres:
    print(f" Buscando '{nombre}' en '{localidad}'...")

    # Abrir la página de búsqueda
    driver.get(url_paginas_blancas)
    time.sleep(3)

    try:
        # Buscar el campo de nombre y escribir la búsqueda
        campo_nombre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nName"))
        )
        campo_nombre.clear()
        campo_nombre.send_keys(nombre)
        time.sleep(1)

        # Buscar el campo de localidad e ingresar la localidad proporcionada
        campo_localidad = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nLocality"))
        )
        campo_localidad.clear()
        campo_localidad.send_keys(localidad)
        time.sleep(1)

        # Clic en el botón de búsqueda
        boton_buscar = driver.find_element(By.ID, "btnSrchName")
        boton_buscar.click()

        # Esperar que carguen los resultados
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "m-results-business"))
        )

        # Extraer datos y guardarlos
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
                # Hacer clic en "Ver teléfono" antes de extraer el número
                boton_ver_telefono = elemento.find_element(By.CLASS_NAME, "m-button--results-business--see-phone")
                driver.execute_script("arguments[0].click();", boton_ver_telefono)
                time.sleep(2)
                
                # Extraer el teléfono
                telefono_element = elemento.find_element(By.CLASS_NAME, "m-icon--single-phone").find_element(By.TAG_NAME, "a")
                telefono = telefono_element.text.strip()
            except:
                telefono = "No disponible"

            # Separar la dirección en Calle, Localidad y Provincia
            partes_direccion = direccion.split(',')
            calle = partes_direccion[0].strip() if len(partes_direccion) > 0 else "No disponible"
            localidad_res = partes_direccion[1].strip() if len(partes_direccion) > 1 else "No disponible"
            provincia = partes_direccion[2].strip() if len(partes_direccion) > 2 else "No disponible"

            # Guardar en lista
            resultados.append({
                "Nombre": nombre_extraido,
                "Teléfono": telefono,
                "Calle": calle,
                "Localidad": localidad_res,
                "Provincia": provincia
            })

        # Guardar en Excel con el nombre buscado
        df = pd.DataFrame(resultados)
        df.to_excel(f"{nombre}.xlsx", index=False)

    except Exception as e:
        print(f" Error con '{nombre}' en '{localidad}':", e)

print(" Finalizó la búsqueda para este script.")
driver.quit()
