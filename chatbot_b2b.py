import streamlit as st
import pandas as pd

# Cargar los datos
@st.cache_data
def load_data():
    file_path = "ChatbotB2b.xlsx"  # Nombre del archivo en el repositorio
    xls = pd.ExcelFile(file_path)
    pedidos = pd.read_excel(xls, sheet_name="Pedidos")
    credenciales = pd.read_excel(xls, sheet_name="Credenciales")
    credenciales.columns = credenciales.columns.str.strip()  # Eliminar espacios en los nombres de columnas
    return pedidos, credenciales

pedidos_df, credenciales_df = load_data()

# Título de la App
st.title("📦 Chatbot B2B - Seguimiento de Pedidos")

# Ingreso de contraseña por chat
clave_ingresada = st.text_input("🔐 Ingrese su contraseña para ver sus pedidos:", type="password")

# Verificar la contraseña ingresada
def verificar_contraseña(clave):
    if clave in credenciales_df["Clave"].values:
        cliente = credenciales_df[credenciales_df["Clave"] == clave]["Cliente"].values[0]
        return cliente
    return None

# Mostrar los pedidos del cliente autenticado y habilitar descarga
if clave_ingresada:
    cliente_autenticado = verificar_contraseña(clave_ingresada)
    
    if cliente_autenticado:
        st.success(f"🔓 Acceso concedido. Mostrando pedidos de {cliente_autenticado}.")
        pedidos_cliente = pedidos_df[pedidos_df["Cliente"] == cliente_autenticado]
        st.dataframe(pedidos_cliente)

        # Botón para descargar pedidos en Excel
        @st.cache_data
        def generar_excel(df):
            output = pd.ExcelWriter("pedidos_cliente.xlsx", engine="xlsxwriter")
            df.to_excel(output, index=False, sheet_name="Pedidos")
            output.close()
            return output

        excel = pedidos_cliente.to_excel(index=False, engine="openpyxl")
        st.download_button(
            label="📥 Descargar Pedidos en Excel",
            data=excel,
            file_name=f"Pedidos_{cliente_autenticado}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    elif clave_ingresada == "admin123":
        st.success("🔓 Acceso total concedido. Mostrando todos los pedidos.")
        st.dataframe(pedidos_df)
    else:
        st.error("❌ Contraseña incorrecta. Inténtalo de nuevo.")
