import snscrape.modules.twitter as sntwitter

class TwitterConnector:
    def __init__(self):
        """
        Inicializa el conector de Twitter (no requiere API keys).
        """
        pass

    def buscar_por_palabra_clave(self, palabra_clave: str, cantidad: int = 50) -> list[dict]:
        """
        Busca tuits reales que contengan la palabra_clave usando snscrape.
        Devuelve una lista de diccionarios con la estructura:
        {'id': '...', 'texto': '...', 'usuario': '...', 'fecha': '...', 'fuente': 'Twitter'}
        """
        tweets = []
        try:
            scraper = sntwitter.TwitterSearchScraper(palabra_clave)
            for i, tweet in enumerate(scraper.get_items()):
                if i >= cantidad:
                    break
                tweet_dict = {
                    'id': str(tweet.id),
                    'texto': tweet.rawContent,
                    'usuario': tweet.user.username,
                    'fecha': tweet.date.isoformat(),
                    'fuente': 'Twitter'
                }
                tweets.append(tweet_dict)
            return tweets
        except Exception as ex:
            print(f"Error al buscar tuits con snscrape: {str(ex)}")
            return []