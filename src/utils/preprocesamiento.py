import re
import spacy
import unicodedata

class LimpiaTexto:
    """
    Clase para limpiar y normalizar texto en español extraído de redes sociales.
    Aplica múltiples técnicas de preprocesamiento, incluyendo lematización, remoción de stopwords,
    eliminación de URLs, menciones, hashtags, puntuación, números y emojis.
    """

    def __init__(self):
        """
        Inicializa la clase cargando el modelo de spaCy y creando una lista
        de stopwords personalizada para no eliminar negaciones importantes que
        cambian el significado del sentimiento.
        """
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except OSError:
            raise ImportError(
                "El modelo 'es_core_news_sm' de spaCy no está instalado. "
                "Instálalo ejecutando: python -m spacy download es_core_news_sm"
            )

        # --- INICIO DE LA CORRECCIÓN DE STOPWORDS ---
        # 1. Cargar la lista de stopwords por defecto de spaCy
        stopwords_por_defecto = self.nlp.Defaults.stop_words
        
        # 2. Definir palabras que son cruciales para el sentimiento y NO deben ser eliminadas
        palabras_a_conservar = {'sin', 'no', 'ni', 'nunca', 'tampoco', 'falta', 'problema', 'bien', 'bueno','buena','más o menos'}
        
        # 3. Crear la nueva lista de stopwords personalizada restando las palabras a conservar
        self.stopwords = stopwords_por_defecto - palabras_a_conservar
        # --- FIN DE LA CORRECCIÓN DE STOPWORDS ---

        # Diccionario básico de emojis comunes en español
        self.emoji_dict = {
            '❤️': 'corazon', '😂': 'risa', '😍': 'amor', '😢': 'tristeza',
            '🙏': 'gracias', '😊': 'sonrisa', '👍': 'pulgar_arriba', '😭': 'llanto',
            '😎': 'cool', '😉': 'guiño',
        }

    def limpiar(self, texto: str) -> str:
        """
        Método principal para limpiar el texto. Aplica los pasos de preprocesamiento en orden.

        Args:
            texto (str): Texto original extraído de redes sociales.

        Returns:
            str: Texto procesado y limpio.
        """
        texto = self._a_minusculas(texto)
        texto = self._remover_urls(texto)
        texto = self._remover_menciones_hashtags(texto)
        texto = self._remover_emojis(texto)
        texto = self._remover_puntuacion_y_numeros(texto)
        texto = self._remover_stopwords(texto)
        texto = self._lematizar(texto)
        # Quitar espacios extra que puedan quedar
        return " ".join(texto.split())

    def _a_minusculas(self, texto: str) -> str:
        """Convierte todo el texto a minúsculas."""
        return texto.lower()

    def _remover_urls(self, texto: str) -> str:
        """Elimina cualquier URL (http/https) del texto."""
        return re.sub(r'https?://\S+|www\.\S+', '', texto)

    def _remover_menciones_hashtags(self, texto: str, conservar_hashtag=False) -> str:
        """Elimina menciones (@usuario) y hashtags (#tema) del texto."""
        texto = re.sub(r'@\w+', '', texto)
        if conservar_hashtag:
            texto = re.sub(r'#(\w+)', r'\1', texto)
        else:
            texto = re.sub(r'#\w+', '', texto)
        return texto

    def _remover_emojis(self, texto: str) -> str:
        """Convierte emojis comunes a texto o los elimina."""
        for emoji, palabra in self.emoji_dict.items():
            texto = texto.replace(emoji, f" {palabra} ")
        
        # Eliminar otros emojis no definidos en el diccionario
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticonos
            "\U0001F300-\U0001F5FF"  # símbolos y pictogramas
            "\U0001F680-\U0001F6FF"  # transporte y símbolos
            "\U0001F1E0-\U0001F1FF"  # banderas
            "\U00002700-\U000027BF"
            "\U0001F900-\U0001F9FF"
            "\U00002600-\U000026FF"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', texto)

    def _remover_puntuacion_y_numeros(self, texto: str) -> str:
        """Elimina signos de puntuación y números."""
        return re.sub(r'[^a-záéíóúüñ\s]', '', texto)

    def _remover_stopwords(self, texto: str) -> str:
        """Elimina stopwords usando la lista personalizada."""
        doc = self.nlp(texto)
        palabras_filtradas = [
            token.text for token in doc if token.text not in self.stopwords
        ]
        return ' '.join(palabras_filtradas)

    def _lematizar(self, texto: str) -> str:
        """Aplica lematización para reducir cada palabra a su raíz."""
        doc = self.nlp(texto)
        lemas = [token.lemma_ for token in doc if not token.is_space]
        return ' '.join(lemas)