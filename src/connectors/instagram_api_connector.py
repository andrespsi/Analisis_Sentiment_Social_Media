# filename: src/connectors/instagram_api_connector.py

import requests
import re

class InstagramApiConnector:
    """
    Versión Definitiva. Utiliza un endpoint de API estable para resolver el
    ID de la publicación a partir de su shortcode, evitando el frágil parseo de HTML.
    """
    def __init__(self, session_id: str):
        if not session_id:
            raise ValueError("El 'session_id' de Instagram es necesario.")
        
        self.base_url = "https://www.instagram.com/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "x-ig-app-id": "936619743392459" # ID de la App Web de Instagram
        })
        self.session.cookies.set("sessionid", session_id)
        print("✅ Conector de API inicializado con la sesión de Instagram.")

    def _get_media_pk_from_url(self, post_url: str) -> str:
        """
        Obtiene la Primary Key (pk) de la publicación usando un endpoint de API
        más estable que el parseo de HTML.
        """
        # 1. Extraer el shortcode de la URL
        match = re.search(r"/(p|reel)/([^/]+)", post_url)
        if not match:
            raise ValueError("No se pudo extraer el shortcode de la URL.")
        shortcode = match.group(2)
        print(f"Shortcode extraído: {shortcode}")

        # 2. Usar el endpoint de 'media info' para obtener el 'pk'
        info_url = f"{self.base_url}/media/by_shortcode/{shortcode}/info/"
        print(f"Consultando endpoint de información: {info_url}")
        
        try:
            response = self.session.get(info_url)
            response.raise_for_status()
            data = response.json()

            # El ID que necesitamos se llama 'pk' en la respuesta de esta API
            media_pk = data.get("items", [{}])[0].get("pk")
            if not media_pk:
                raise ValueError("No se encontró la 'pk' del medio en la respuesta de la API.")
            
            print(f"   - Media PK (ID) encontrado: {media_pk}")
            return media_pk
        except Exception as e:
            print(f"❌ Error al obtener el Media PK desde la API: {e}")
            raise

    def buscar_comentarios(self, post_url: str, cantidad: int = 50) -> list[dict]:
        try:
            media_pk = self._get_media_pk_from_url(post_url)
            
            print(f"Extrayendo comentarios para el Media PK: {media_pk}")
            comments_url = f"{self.base_url}/media/{media_pk}/comments/"
            
            response = self.session.get(comments_url)
            response.raise_for_status()
            data = response.json()

            comentarios = []
            for comment in data.get("comments", []):
                if len(comentarios) >= cantidad:
                    break
                comentarios.append({
                    'id': str(comment.get("pk")),
                    'texto': comment.get("text"),
                    'usuario': comment.get("user", {}).get("username"),
                    'fecha': None,
                    'fuente': 'Instagram'
                })
            
            print(f"✅ Se extrajeron {len(comentarios)} comentarios exitosamente.")
            return comentarios

        except Exception as e:
            print(f"❌ Error al buscar comentarios a través de la API: {e}")
            return []