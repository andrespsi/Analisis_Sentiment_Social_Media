import sqlite3
from datetime import datetime

class DatabaseManager:
    """
    Gestiona la conexión y las operaciones con la base de datos SQLite.
    """
    def __init__(self, db_name="sentimientos.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.inicializar_tabla()

    def inicializar_tabla(self):
        """
        Crea la tabla 'analisis' si no existe.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS analisis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT NOT NULL,
            texto_original TEXT NOT NULL,
            sentimiento TEXT NOT NULL,
            confianza REAL NOT NULL,
            fecha_analisis TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def guardar_analisis(self, texto_original: str, resultado_analisis: dict, fuente: str):
        """
        Guarda un único resultado de análisis en la base de datos.
        """
        sentimiento = resultado_analisis.get('sentimiento', 'ERROR')
        confianza = resultado_analisis.get('confianza', 0.0)
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute("""
        INSERT INTO analisis (fuente, texto_original, sentimiento, confianza, fecha_analisis)
        VALUES (?, ?, ?, ?, ?)
        """, (fuente, texto_original, sentimiento, confianza, fecha))
        self.conn.commit()

    def obtener_todos_los_analisis(self):
        """
        Obtiene todos los registros de la tabla de análisis.
        """
        self.cursor.execute("SELECT * FROM analisis ORDER BY fecha_analisis DESC")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()