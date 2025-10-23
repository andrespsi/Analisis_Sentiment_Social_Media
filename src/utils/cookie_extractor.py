# filename: src/utils/cookie_extractor.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# Ya no necesitamos webdriver_manager

def get_session_cookie_from_browser(profile_path: str, driver_path: str) -> str | None:
    options = webdriver.ChromeOptions()
    profile_dir = os.path.basename(profile_path)
    user_data_dir = os.path.dirname(profile_path)

    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_argument("--start-maximized")
    
    driver = None
    try:
        print("Abriendo navegador con tu perfil y driver manual...")
        
        # --- CAMBIO CLAVE: Usar la ruta manual del driver ---
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://www.instagram.com/")
        print("Navegador abierto. Esperando 15 segundos...")
        time.sleep(15)
        
        print("Extrayendo cookie de sesión...")
        cookie = driver.get_cookie("sessionid")
        
        if cookie and cookie.get("value"):
            session_id = cookie["value"]
            print("✅ Cookie 'sessionid' extraída exitosamente.")
            return session_id
        else:
            print("❌ No se encontró la cookie 'sessionid'. ¿Está la sesión iniciada en este perfil?")
            return None
            
    except Exception as e:
        print(f"❌ Ocurrió un error al intentar obtener la cookie: {e}")
        return None
    finally:
        if driver:
            print("Cerrando navegador de extracción.")
            driver.quit()