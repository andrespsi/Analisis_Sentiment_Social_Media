import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)

# --- 1. CONFIGURACIÓN ---
MODELO_BASE = 'pysentimiento/robertuito-sentiment-analysis'
NOMBRE_DATASET_CSV = 'dataset_sentimiento.csv'
DIRECTORIO_MODELO_FINAL = './modelo_fine_tuned'

# --- 2. CARGAR Y PREPARAR EL DATASET (VERSIÓN A PRUEBA DE ERRORES) ---
print("Cargando y preparando el dataset...")
try:
    df = pd.read_csv(NOMBRE_DATASET_CSV)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{NOMBRE_DATASET_CSV}'. Asegúrate de que exista.")
    exit()

# Mapeo de etiquetas a números
labels_map = {'NEG': 0, 'NEU': 1, 'POS': 2}
df['label'] = df['etiqueta'].map(labels_map)

# Filtra las filas donde la etiqueta no se pudo mapear (es decir, el valor es None/NaN)
original_rows = len(df)
df = df.dropna(subset=['label'])
cleaned_rows = len(df)

if original_rows > cleaned_rows:
    print(f"Alerta: Se eliminaron {original_rows - cleaned_rows} filas del dataset por tener etiquetas inválidas.")

# Convertir la columna 'label' a tipo entero
df['label'] = df['label'].astype(int)

tokenizer = AutoTokenizer.from_pretrained(MODELO_BASE)
dataset = Dataset.from_pandas(df)

def tokenizar_funcion(examples):
    return tokenizer(examples['texto'], padding="max_length", truncation=True)

dataset_tokenizado = dataset.map(tokenizar_funcion, batched=True)

# --- 3. CARGAR EL MODELO BASE ---
print("Cargando el modelo base...")
model = AutoModelForSequenceClassification.from_pretrained(
    MODELO_BASE,
    num_labels=3,
    id2label={v: k for k, v in labels_map.items()},
    label2id=labels_map
)

# --- 4. CONFIGURAR EL ENTRENAMIENTO (VERSIÓN FINAL SÚPER COMPATIBLE) ---
print("Configurando el entrenamiento...")

# Se definen los argumentos de una forma más simple y directa
# Aumentamos las épocas a 5 para reforzar el aprendizaje
training_args = TrainingArguments(
    output_dir=DIRECTORIO_MODELO_FINAL,
    num_train_epochs=5,  # Aumentado para que el modelo "estudie" más tus ejemplos
    per_device_train_batch_size=4,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset_tokenizado, # Usamos el dataset completo para entrenar
)

# --- 5. INICIAR EL FINE-TUNING ---
print("¡Iniciando el fine-tuning! Esto puede tardar varios minutos...")
trainer.train()

print(f"¡Entrenamiento completado!")
trainer.save_model(DIRECTORIO_MODELO_FINAL)
tokenizer.save_pretrained(DIRECTORIO_MODELO_FINAL) # Se guarda el tokenizer explícitamente
print(f"Modelo y tokenizer guardados correctamente en: {DIRECTORIO_MODELO_FINAL}")