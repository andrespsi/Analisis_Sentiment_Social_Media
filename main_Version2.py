import os
from dotenv import load_dotenv
from src.connectors.twitter_api import TwitterConnector
from src.utils.preprocesamiento import LimpiaTexto
from src.analysis.analizador import AnalizadorSentimiento
import pandas as pd
import asyncio

def ejecutar_analisis_batch(keyword: str, cantidad: int = 10):
    """
    Realiza un análisis de sentimiento batch sobre tweets simulados por una palabra clave,
    exporta los resultados a un archivo CSV.

    Args:
        keyword (str): Palabra clave para buscar tweets simulados.
        cantidad (int): Número de tweets a analizar.
    """
    # Cargar variables de entorno (no usadas en el simulador)
    load_dotenv()
    api_key = os.getenv("API_KEY", "fake_key")
    api_secret = os.getenv("API_SECRET", "fake_secret")

    # Instanciar conector simulado
    connector = TwitterConnector(api_key, api_secret)
    tweets = connector.buscar_tweets(keyword, cantidad)

    # Instanciar limpiador y analizador
    limpiador = LimpiaTexto()
    analizador = AnalizadorSentimiento()

    resultados = []

    async def analizar_tweets():
        for tweet in tweets:
            texto_original = tweet['texto']
            texto_limpio = limpiador.limpiar(texto_original)
            try:
                resultado = await analizador.analizar(texto_limpio)
                tweet_resultado = {
                    **tweet,
                    'texto_limpio': texto_limpio,
                    'sentimiento': resultado['sentimiento'],
                    'confianza': resultado['confianza']
                }
            except Exception as e:
                tweet_resultado = {
                    **tweet,
                    'texto_limpio': texto_limpio,
                    'sentimiento': 'ERROR',
                    'confianza': 0.0,
                    'error': str(e)
                }
            resultados.append(tweet_resultado)

    asyncio.run(analizar_tweets())

    # Convertir resultados en DataFrame y exportar a CSV
    df = pd.DataFrame(resultados)
    nombre_csv = f"reporte_sentimiento_{keyword}.csv"
    df.to_csv(nombre_csv, index=False)
    print(f"Reporte exportado a: {nombre_csv}")

if __name__ == '__main__':
    ejecutar_analisis_batch('mi-marca-de-gaseosa', 10)