import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeConnector:
    """
    Conector real para extraer comentarios de un video de YouTube,
    con capacidad de paginación para obtener más de 100 comentarios.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def _extraer_video_id(self, url: str) -> str | None:
        """
        Extrae el ID del video de una URL de YouTube usando expresiones regulares.
        """
        regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, url)
        return match.group(1) if match else None

    def buscar_comentarios(self, video_url: str, cantidad: int = 500) -> list[dict]:
        video_id = self._extraer_video_id(video_url)
        if not video_id:
            raise ValueError("La URL de YouTube proporcionada es inválida.")

        comentarios = []
        next_page_token = None # Marcador para la siguiente página

        try:
            # --- INICIO DE LA LÓGICA DE PAGINACIÓN ---
            while len(comentarios) < cantidad:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100, # Pedimos el máximo posible por página
                    textFormat="plainText",
                    pageToken=next_page_token # Le pasamos el marcador de la página
                )
                response = request.execute()

                for item in response.get("items", []):
                    comment = item["snippet"]["topLevelComment"]["snippet"]
                    comentarios.append({
                        'id': item["id"],
                        'texto': comment["textDisplay"],
                        'usuario': comment["authorDisplayName"],
                        'fecha': comment["publishedAt"],
                        'fuente': 'YouTube'
                    })
                
                # Verificamos si hay una página siguiente
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break # Si no hay más páginas, salimos del bucle
            # --- FIN DE LA LÓGICA DE PAGINACIÓN ---
            
            # Devolvemos solo la cantidad solicitada
            return comentarios[:cantidad]

        except HttpError as e:
            print(f"Ha ocurrido un error con la API de YouTube: {e}")
            return []