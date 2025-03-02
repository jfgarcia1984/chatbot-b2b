import pandas as pd
import os

def procesar_archivo(input_path, output_path):
    # Cargar archivo
    df = pd.read_excel(input_path, sheet_name="Pedidos")
    
    # 1. Eliminar espacios adicionales en los nombres de columnas
    df.columns = df.columns.str.strip()
    
    # 2. Convertir fechas a formato DD/MM/AAAA
    date_columns = ["ETD", "ETA", "Fecha de Alistamiento"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y')
    
    # 3. Guardar con formato y ajustar columnas automáticamente
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Pedidos", index=False)
        workbook = writer.book
        worksheet = writer.sheets["Pedidos"]
        
        for i, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_length)
    
    print(f"✅ Archivo procesado y guardado como: {output_path}")

# Definir rutas de entrada y salida
input_file = "ChatbotB2B.xlsx"
output_file = "ChatbotB2B_Procesado.xlsx"

# Verificar si el archivo existe y procesarlo
os.makedirs("procesados", exist_ok=True)
if os.path.exists(input_file):
    procesar_archivo(input_file, os.path.join("procesados", output_file))
else:
    print("❌ No se encontró el archivo. Asegúrate de subirlo con el nombre correcto.")
