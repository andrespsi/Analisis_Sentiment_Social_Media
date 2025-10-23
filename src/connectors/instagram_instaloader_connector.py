# filename: src/connectors/instagram_instaloader_connector.py

import instaloader

class InstagramInstaloaderConnector:
    """
    El conector definitivo. Utiliza la librería especializada Instaloader
    para una extracción de datos robusta y fiable.
    """
    def __init__(self, username: str):
        if not username:
            raise ValueError("El 'username' de Instagram es necesario para cargar la sesión.")
        
        self.loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            save_metadata=False,
            compress_json=False
        )
        
        session_filename = f"./session-{username}"
        try:
            # Instaloader usa el nombre de usuario para cargar el archivo de sesión
            print(f"Cargando sesión de Instagram desde: {session_filename}")
            self.loader.load_session_from_file(username, session_filename)
            print("✅ Sesión cargada exitosamente.")
        except FileNotFoundError:
            print(f"❌ ERROR: No se encontró el archivo de sesión '{session_filename}'.")
            print("Asegúrate de que el archivo de tu sesión anterior esté en la carpeta principal del proyecto.")
            raise

    def buscar_comentarios(self, post_url: str, cantidad: int = 50) -> list[dict]:
        print(f"Extrayendo comentarios de: {post_url}")
        try:
            # Instaloader puede trabajar directamente con la URL
            post = instaloader.Post.from_shortcode(self.loader.context, post_url.split("/")[-2])
            
            comentarios = []
            for comment in post.get_comments():
                if len(comentarios) >= cantidad:
                    break
                
                comentarios.append({
                    'id': str(comment.id),
                    'texto': comment.text,
                    'usuario': comment.owner.username,
                    'fecha': comment.created_at_utc.isoformat(),
                    'fuente': 'Instagram'
                })
            
            print(f"✅ Se extrajeron {len(comentarios)} comentarios.")
            return comentarios

        except Exception as e:
            print(f"❌ Error al extraer comentarios con Instaloader: {e}")
            return []