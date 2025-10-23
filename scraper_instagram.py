import os
import re
import time
import random
import instaloader
from dotenv import load_dotenv

# --- CONFIGURACIÓN DEL SCRAPER PACIENTE ---
MIN_DELAY_INICIAL = 7.0
MAX_DELAY_INICIAL = 15.0
MIN_DELAY_NORMAL = 4.0
MAX_DELAY_NORMAL = 8.0
MIN_DELAY_BLOQUEO = 900
MAX_DELAY_BLOQUEO = 1800
MAXIMOS_REINTENTOS = 5

def contar_comentarios_existentes(filename: str) -> int:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return sum(1 for line in f)
    except FileNotFoundError:
        return 0

def scraper_paciente(post_url: str, session_username: str, max_comentarios: int):
    loader = instaloader.Instaloader(
        download_pictures=False, download_videos=False,
        download_video_thumbnails=False, save_metadata=False, compress_json=False
    )
    
    session_filename = f"./session-{session_username}"
    try:
        loader.load_session_from_file(session_username, session_filename)
        print("Sesión de Instagram cargada exitosamente.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de sesión '{session_filename}'.")
        return

    pausa_inicial = random.uniform(MIN_DELAY_INICIAL, MAX_DELAY_INICIAL)
    print(f"Pausa de calentamiento inicial de {int(pausa_inicial)} segundos...")
    time.sleep(pausa_inicial)

    match = re.search(r"/(?:p|reel)/([^/?]+)", post_url)
    if not match:
        print(f"La URL proporcionada no es válida: {post_url}")
        return
    shortcode = match.group(1)
    
    output_filename = f"comentarios_{shortcode}.txt"
    
    reintentos = 0
    while reintentos < MAXIMOS_REINTENTOS:
        try:
            comentarios_guardados = contar_comentarios_existentes(output_filename)
            if comentarios_guardados >= max_comentarios:
                print(f"Objetivo de {max_comentarios} comentarios ya alcanzado.")
                break
            
            print(f"Iniciando recolección. {comentarios_guardados}/{max_comentarios} comentarios ya guardados.")
            
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            
            # --- INICIO DEL CALENTAMIENTO AVANZADO ---
            print(f"Calentamiento: Visitando perfil del autor @{post.owner_username}...")
            profile = post.owner_profile
            print(f"-> Leyendo biografía y posts (simulado)...")
            time.sleep(random.uniform(MIN_DELAY_NORMAL, MAX_DELAY_NORMAL))
            
            print("-> Viendo los títulos de los últimos posts (simulado)...")
            for i, p in enumerate(profile.get_posts()):
                if i >= 2: break # Solo mira los primeros 3
                time.sleep(random.uniform(1.0, 2.0))
            # --- FIN DEL CALENTAMIENTO AVANZADO ---
            
            print("Calentamiento finalizado. Iniciando recolección de comentarios.")
            comments_iterator = post.get_comments()
            
            for _ in range(comentarios_guardados):
                next(comments_iterator)

            with open(output_filename, "a", encoding="utf-8") as f:
                for comment in comments_iterator:
                    texto_limpio = comment.text.replace('\n', ' ').strip()
                    if texto_limpio:
                        f.write(texto_limpio + '\n')
                        comentarios_guardados += 1
                        print(f"Comentario {comentarios_guardados}/{max_comentarios} guardado.")
                    
                    if comentarios_guardados >= max_comentarios:
                        break
                    
                    time.sleep(random.uniform(MIN_DELAY_NORMAL, MAX_DELAY_NORMAL))
            
            print("\n¡Proceso completado exitosamente!")
            break

        except Exception as e:
            reintentos += 1
            print(f"\nHa ocurrido un error: {e}")
            if reintentos < MAXIMOS_REINTENTOS:
                pausa = random.uniform(MIN_DELAY_BLOQUEO, MAX_DELAY_BLOQUEO)
                print(f"Reintento {reintentos}/{MAXIMOS_REINTENTOS}. Esperando {int(pausa/60)} minutos antes de continuar...")
                time.sleep(pausa)
            else:
                print("Se ha alcanzado el número máximo de reintentos.")

if __name__ == "__main__":
    load_dotenv()
    usuario_sesion = os.getenv("INSTAGRAM_USERNAME")
    link_objetivo = "https://www.instagram.com/p/DPhUcv0ksd4/"
    max_comentarios_a_recoger = 20
    
    if usuario_sesion:
        scraper_paciente(link_objetivo, usuario_sesion, max_comentarios_a_recoger)
    else:
        print("Error: La variable INSTAGRAM_USERNAME no está en tu archivo .env")