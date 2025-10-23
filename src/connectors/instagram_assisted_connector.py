# filename: src/connectors/instagram_assisted_connector.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class InstagramAssistedConnector:
    """
    El conector definitivo. Se basa en un inicio de sesión manual y asistido por el usuario
    para garantizar una autenticación 100% humana e indetectable.
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 600) # Larga espera para el login manual
        self._login_asistido()

    def _pausa_humana(self, min_seg=2.0, max_seg=4.0):
        time.sleep(time.time() % (max_seg - min_seg) + min_seg)

    def _login_asistido(self):
        """Abre Instagram y espera a que el usuario inicie sesión manualmente."""
        self.driver.get("https://www.instagram.com/")
        print("\n" + "="*60)
        print("--- ACCIÓN REQUERIDA ---")
        print("1. Por favor, inicia sesión en la ventana de Chrome que se ha abierto.")
        print("2. Resuelve cualquier CAPTCHA o verificación de seguridad.")
        print("3. Una vez que estés en la página principal de Instagram, el script continuará.")
        print("="*60)
        
        try:
            # El script esperará hasta que el ícono de "Inicio" sea visible
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg'][@aria-label='Inicio']")))
            print("\n✅ ¡Login detectado! El script tomará el control ahora.")
        except TimeoutException:
            print("\n❌ No se detectó un inicio de sesión en el tiempo esperado. El script se detendrá.")
            raise

    def buscar_comentarios(self, post_url: str, cantidad: int = 50) -> list[dict]:
        print(f"Navegando a la publicación: {post_url}")
        self.driver.get(post_url)
        try:
            comments_pane_xpath = "//div/ul/parent::div"
            comments_pane = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, comments_pane_xpath)))
            print("✅ Panel de comentarios cargado. Iniciando recolección...")
            
            comentarios_encontrados = set()
            # ... (Lógica de scroll y extracción) ...
            
            print("Recolección finalizada.")
            comentarios = [{'id': str(hash(t)), 'texto': t, 'usuario': 'desconocido', 'fecha': None, 'fuente': 'Instagram'} for t in list(comentarios_encontrados)]
            return comentarios[:cantidad]

        except TimeoutException:
            print("❌ Error: No se encontró el panel de comentarios. Asegúrate de que la URL es correcta y tiene comentarios.")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return []

    def __del__(self):
        try:
            print("Cerrando navegador.")
            self.driver.quit()
        except: pass