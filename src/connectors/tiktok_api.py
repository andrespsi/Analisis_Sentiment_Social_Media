import pyktok

class TikTokConnector:
    def buscar_comentarios(self, post_url: str, cantidad: int = 50) -> list[dict]:
        """
        Extrae comentarios de un video de TikTok usando pyktok.
        Devuelve una lista de dicts con la estructura estándar:
        {'id': '...', 'texto': '...', 'usuario': '...', 'fecha': '...', 'fuente': 'TikTok'}
        """
        comentarios = []
        try:
            # Obtener el JSON del video
            video_data = pyktok.get_tiktok_json(post_url)
            # Extraer video_id
            video_id = video_data.get("id") or video_data.get("video_id")
            if not video_id:
                raise ValueError("No se pudo extraer el video_id del post_url proporcionado.")

            # Obtener los comentarios
            comments_data = pyktok.get_tiktok_comments(video_id, count=cantidad)

            if not comments_data or "comments" not in comments_data or not comments_data["comments"]:
                # No hay comentarios
                return []

            for comment in comments_data["comments"]:
                comentario = {
                    "id": comment.get("cid", ""),
                    "texto": comment.get("text", ""),
                    "usuario": comment.get("user", {}).get("unique_id", ""),
                    "fecha": comment.get("create_time", ""),  # Normalmente timestamp
                    "fuente": "TikTok"
                }
                comentarios.append(comentario)
            return comentarios

        except Exception as ex:
            # Error con la URL, video no existe, sin comentarios, etc.
            print(f"Error al obtener comentarios de TikTok: {str(ex)}")
            return []