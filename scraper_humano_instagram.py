import os
import re
import time
import random
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver():
    """Configura e inicializa el navegador Chrome con Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Usar un User-Agent común para parecer menos un bot
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login_asistido(driver):
    """Pide al usuario que inicie sesión manualmente."""
    driver.get("https://www.instagram.com/")
    print("--- ACCIÓN REQUERIDA ---")
    print("Por favor, inicia sesión en la ventana del navegador que se ha abierto.")
    print("Resuelve cualquier verificación de seguridad (CAPTCHA, etc.).")
    input("Una vez que hayas iniciado sesión y estés en la página principal, presiona ENTER aquí para continuar...")
    print("Login confirmado. El script tomará el control.")

def scraper_asistido(driver, post_url: str):
    """Navega a la publicación y extrae los comentarios con una estrategia robusta."""
    print(f"Navegando a la publicación: {post_url}")
    driver.get(post_url)
    wait = WebDriverWait(driver, 15)

    try:
        # Esperar a que el contenido principal de la publicación cargue
        wait.until(EC.presence_of_element_located((By.XPATH, "//article")))
        print("Publicación cargada.")

        # --- Bucle para cargar TODOS los comentarios ---
        print("Buscando y haciendo clic en 'Ver más comentarios' repetidamente...")
        while True:
            try:
                # Busca el botón o enlace para cargar más
                load_more_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Ver más comentarios')] | //button[.//*[local-name()='svg'][@aria-label='Cargar más comentarios']]")
                # Hacemos scroll hasta el botón para asegurarnos de que es visible
                driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                time.sleep(1)
                load_more_button.click()
                print("   - Clic en 'Ver más...'")
                time.sleep(random.uniform(1.5, 3.0)) # Pausa para que carguen
            except NoSuchElementException:
                print("No se encontró el botón 'Ver más comentarios'. Se asume que se han cargado todos.")
                break # Salimos del bucle si ya no hay botón

        # --- Extracción final de comentarios ---
        print("\nExtrayendo todos los comentarios cargados...")
        comentarios_encontrados = set()
        # Selector robusto que busca el texto del comentario (span) dentro de una lista (ul)
        elementos_comentario = driver.find_elements(By.XPATH, "//ul//h3/../div/span")

        for el in elementos_comentario:
            texto = el.text.replace('\n', ' ').strip()
            if texto:
                comentarios_encontrados.add(texto)

        return list(comentarios_encontrados)

    except TimeoutException:
        print("Error: La página de la publicación no cargó a tiempo. ¿La URL es correcta?")
        return []
    except Exception as e:
        print(f"Ha ocurrido un error inesperado durante el scraping: {e}")
        return []

if __name__ == "__main__":
    load_dotenv()
    
    # --- CONFIGURA AQUÍ TU ANÁLISIS ---
    link_objetivo = "https://www.instagram.com/p/DPjFI2zEWbd/" # Asegúrate de que este link funcione
    
    driver = configurar_driver()
    try:
        login_asistido(driver)
        comentarios = scraper_asistido(driver, link_objetivo)
        
        if comentarios:
            shortcode = (re.search(r"/(?:p|reel)/([^/?]+)", link_objetivo)).group(1)
            output_filename = f"comentarios_{shortcode}.txt"
            
            print(f"\nGuardando {len(comentarios)} comentarios en {output_filename}...")
            with open(output_filename, "w", encoding="utf-8") as f:
                for comentario in comentarios:
                    f.write(comentario + '\n')
            print("¡Proceso completado!")
        else:
            print("No se extrajeron comentarios.")
            
    finally:
        print("Cerrando el navegador en 10 segundos...")
        time.sleep(10)
        driver.quit()