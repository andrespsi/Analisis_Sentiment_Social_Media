from typing import Dict, Optional
from transformers import pipeline
import asyncio

class AnalizadorSentimiento:
    """
    Clase para realizar análisis de sentimiento en español usando un modelo
    personalizado de Hugging Face.
    """

    MODELO_PREENTRENADO: str = './modelo_fine_tuned'
    _pipeline: Optional[pipeline] = None

    def __init__(self) -> None:
        """
        Inicializa el pipeline de análisis de sentimiento.
        """
        if AnalizadorSentimiento._pipeline is None:
            try:
                AnalizadorSentimiento._pipeline = pipeline(
                    "sentiment-analysis",
                    model=self.MODELO_PREENTRENADO
                )
            except Exception as e:
                raise RuntimeError(f"Error cargando el modelo de Transformers: {e}")

    async def analizar(self, texto_limpio: str) -> Dict[str, any]:
        """
        Analiza el sentimiento de un texto y aplica la lógica de negocio.
        """
        if not isinstance(texto_limpio, str) or not texto_limpio.strip():
            # Si el texto está vacío después de la limpieza, lo marcamos como Neutro.
            return {
                'sentimiento': 'NEU',
                'confianza': 1.0,
                'scores_detallados': {'NEU': 1.0, 'POS': 0.0, 'NEG': 0.0}
            }

        try:
            loop = asyncio.get_event_loop()
            # --- INICIO DE LA CORRECCIÓN ---
            # Añadimos truncation=True para recortar textos largos automáticamente
            resultados = await loop.run_in_executor(
                None,
                lambda: AnalizadorSentimiento._pipeline(texto_limpio, return_all_scores=True, truncation=True)
            )
            # --- FIN DE LA CORRECCIÓN ---

            scores = {r['label'].upper(): r['score'] for r in resultados[0]}

            etiqueta_principal = max(scores, key=scores.get)
            confianza_principal = scores[etiqueta_principal]

            if etiqueta_principal == 'NEU' and confianza_principal < 0.6:
                pos_score = scores.get('POS', 0.0)
                neg_score = scores.get('NEG', 0.0)
                
                if pos_score > neg_score:
                    sentimiento_final = 'POS'
                    confianza_final = pos_score
                else:
                    sentimiento_final = 'NEG'
                    confianza_final = neg_score
            else:
                sentimiento_final = etiqueta_principal
                confianza_final = confianza_principal
            
            return {
                'sentimiento': sentimiento_final,
                'confianza': confianza_final,
                'scores_detallados': scores
            }

        except Exception as e:
            raise RuntimeError(f"Error durante el análisis de sentimiento: {e}")