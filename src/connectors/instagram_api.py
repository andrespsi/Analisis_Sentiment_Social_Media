import re
import instaloader

class InstagramConnector:
    def __init__(self, username: str):
        """
        Inicializa el conector cargando la sesión de Instagram desde un
        archivo de sesión específico en la carpeta del proyecto.
        """
        if not username:
            raise ValueError("El 'username' de Instagram es necesario.")
        
        self.loader = instaloader.Instaloader()
        session_filename = f"./session-{username}" # Construye el nombre del archivo
        
        try:
            print(f"Cargando sesión desde el archivo: {session_filename}...")
            self.loader.load_session_from_file(username, session_filename)
            print("Sesión cargada exitosamente.")

        except FileNotFoundError:
            raise RuntimeError(f"No se encontró el archivo de sesión '{session_filename}'. "
                             f"Por favor, ejecuta 'instaloader --login={username} --sessionfile=./session-{username}' en la terminal primero.")
        except Exception as e:
            raise RuntimeError(f"No se pudo cargar la sesión de Instagram. Error: {e}")


    def buscar_comentarios(self, post_url: str, cantidad: int = 50) -> list[dict]:
        # ... (El resto del método buscar_comentarios permanece exactamente igual) ...
        comentarios = []
        try:
            match = re.search(r"/p/([^/?]+)/", post_url) or re.search(r"/reel/([^/?]+)/", post_url)
            if not match:
                raise ValueError("No se pudo extraer el shortcode de la URL de Instagram.")
            shortcode = match.group(1)

            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)

            for idx, comment in enumerate(post.get_comments()):
                if idx >= cantidad:
                    break
                comentario = {
                    'id': str(comment.id),
                    'texto': comment.text,
                    'usuario': comment.owner.username,
                    'fecha': comment.created_at_utc.isoformat(),
                    'fuente': 'Instagram'
                }
                comentarios.append(comentario)
            return comentarios

        except Exception as ex:
            print(f"Error al obtener comentarios de Instagram: {str(ex)}")
            return []