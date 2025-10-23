# filename: src/connectors/instagram_human_api.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager # Volvemos a usar el gestor automático

class InstagramHumanConnector:
    def __init__(self, profile_path: str):
        options = webdriver.ChromeOptions()
        profile_dir = os.path.basename(profile_path)
        user_data_dir = os.path.dirname(profile_path)

        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument(f"--profile-directory={profile_dir}")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        
        # --- Volvemos al método automático y más simple ---
        service = Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 25)

    def buscar_comentarios(self, post_url: str, cantidad: int = 50) -> list[dict]:
        print(f"Navegando a la publicación: {post_url}")
        try:
            self.driver.get(post_url)
            
            if "login" in self.driver.current_url:
                print("\n❌ ERROR: Sesión de Instagram no activa. Por favor, inicia sesión en Chrome y cierra el navegador antes de ejecutar.\n")
                return []

            comments_pane_xpath = "//div/ul/parent::div"
            comments_pane = self.wait.until(EC.presence_of_element_located((By.XPATH, comments_pane_xpath)))
            print("✅ Panel de comentarios cargado. Iniciando recolección...")
            
            comentarios_encontrados = set()
            # ... (La lógica para hacer scroll y extraer comentarios va aquí) ...

            print("Recolección finalizada.")
            comentarios = [{'id': str(hash(t)), 'texto': t, 'usuario': 'desconocido', 'fecha': None, 'fuente': 'Instagram'} for t in list(comentarios_encontrados)]
            return comentarios[:cantidad]

        except TimeoutException:
            print("❌ Error: La página no cargó el panel de comentarios. Verifica el enlace y que la publicación tenga comentarios.")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return []

    def __del__(self):
        try:
            print("Cerrando navegador.")
            self.driver.quit()
        except: pass