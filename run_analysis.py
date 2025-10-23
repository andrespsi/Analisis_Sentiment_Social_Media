# filename: run_analysis.py

import os
import asyncio
from dotenv import load_dotenv
from urllib.parse import urlparse

# --- Importaciones de Conectores ---
# Se importa el conector de inicio de sesión asistido
from src.connectors.instagram_assisted_connector import InstagramAssistedConnector

# --- Importaciones del Núcleo del Sistema ---
from src.analysis.analizador import AnalizadorSentimiento
from src.utils.preprocesamiento import LimpiaTexto
from src.core.database import DatabaseManager


def obtener_conector(termino_o_url: str):
    """
    Discrimina la plataforma a partir de la URL y devuelve la instancia
    del conector apropiado.
    """
    hostname = urlparse(termino_o_url).hostname
    
    if "instagram.com" in hostname:
        print("Fuente detectada: Instagram (Modo Asistido)")
        # Se invoca al conector asistido (no necesita credenciales)
        return InstagramAssistedConnector()
    
    # Aquí puedes añadir la lógica para otros conectores si los necesitas
    # if "youtube.com" in hostname:
    #     return YouTubeConnector(...)

    raise ValueError(f"No se encontró un conector para la URL: {termino_o_url}")

async def main(termino_o_url: str, cantidad: int):
    """
    Función principal que orquesta la extracción, análisis y guardado de datos.
    """
    # Para este método, ya no es necesario cargar credenciales de .env para Instagram
    
    limpiador = LimpiaTexto()
    analizador = AnalizadorSentimiento()
    db = DatabaseManager()
    
    conector = None
    try:
        print("1. Inicializando conector...")
        # Se llama al conector sin pasarle credenciales
        conector = obtener_conector(termino_o_url)
        fuente = "Instagram"
        
        print(f"\n2. Extrayendo contenido de {fuente}...")
        contenido = conector.buscar_comentarios(termino_o_url, cantidad=cantidad)
        
        if not contenido:
            print("No se encontró contenido o hubo un error en la extracción.")
            return

        print(f"\n3. Se encontraron {len(contenido)} items. Analizando y guardando...")
        for i, item in enumerate(contenido):
            texto_original = item.get('texto', '')
            if not texto_original or not isinstance(texto_original, str):
                continue
            
            texto_limpio = limpiador.limpiar(texto_original)
            resultado_analisis = await analizador.analizar(texto_limpio)
            
            db.guardar_analisis(texto_original, resultado_analisis, fuente=fuente)
            print(f"   - Item {i+1}/{len(contenido)} de {fuente} analizado y guardado.")
            
        print(f"\n¡Análisis de {fuente} completado y guardado en la base de datos!")
    
    except Exception as e:
        print(f"Ha ocurrido un error inesperado en el flujo principal: {e}")
    
    finally:
        if conector:
            print("Finalizando operación.")

if __name__ == "__main__":
    # --- CONFIGURA AQUÍ TU ANÁLISIS ---
    # Asegúrate de que esta URL sea de una publicación con comentarios ACTIVOS
    analisis_objetivo = "https://www.instagram.com/p/C7mTbnJsX2u/" 
    cantidad_a_analizar = 50
    
    asyncio.run(main(analisis_objetivo, cantidad_a_analizar))