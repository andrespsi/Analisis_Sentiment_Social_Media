import re
import facebook

class FacebookConnector:
    def __init__(self, access_token: str):
        """
        Inicializa el conector de Facebook con el access_token proporcionado.
        """
        if not access_token or not isinstance(access_token, str):
            raise ValueError("Access token inválido o no proporcionado.")
        try:
            self.graph = facebook.GraphAPI(access_token=access_token, version="17.0")
        except Exception as ex:
            raise RuntimeError(f"Error al inicializar el GraphAPI: {str(ex)}")

    def buscar_comentarios(self, post_url: str, cantidad: int = 50) -> list[dict]:
        """
        Busca comentarios en el post indicado y devuelve una lista de diccionarios estandarizados.
        Cada diccionario tiene el formato: {'id': '...', 'texto': '...', 'usuario': '...', 'fecha': '...', 'fuente': 'Facebook'}
        """
        comentarios = []
        try:
            # Extraer el PageName y el post_id de la URL
            # Ejemplo de URL: https://www.facebook.com/PageName/posts/12345
            match = re.search(r"facebook\.com/([^/?]+)/posts/(\d+)", post_url)
            if not match:
                raise ValueError("URL de publicación de Facebook inválida o no soportada. Esperado /PageName/posts/12345")
            page_name = match.group(1)
            post_id = match.group(2)
            full_post_id = f"{page_name}_{post_id}"

            # Obtener los comentarios usando el GraphAPI
            respuesta = self.graph.get_connections(id=full_post_id, connection_name='comments', limit=cantidad)

            if "data" not in respuesta or not respuesta["data"]:
                return []  # No hay comentarios

            for comentario in respuesta["data"]:
                comentario_dict = {
                    'id': comentario.get('id', ''),
                    'texto': comentario.get('message', ''),
                    'usuario': comentario.get('from', {}).get('name', ''),
                    'fecha': comentario.get('created_time', ''),
                    'fuente': 'Facebook'
                }
                comentarios.append(comentario_dict)

            return comentarios

        except facebook.GraphAPIError as e:
            error_msg = str(e)
            if "Invalid OAuth access token" in error_msg:
                raise RuntimeError("El access token de Facebook es inválido.")
            elif "Permissions error" in error_msg or "does not have permission" in error_msg:
                raise RuntimeError("No tienes permisos para acceder a esta publicación o comentarios.")
            elif "Unsupported get request" in error_msg or "Cannot access this post" in error_msg:
                raise RuntimeError("El post no es público o no existe.")
            else:
                raise RuntimeError(f"Error de la API de Facebook: {error_msg}")
        except Exception as ex:
            raise RuntimeError(f"Error inesperado: {str(ex)}")