import streamlit as st
import streamlit_shadcn_ui as ui
import numpy as np
import pandas as pd


# ---- MAINPAGE ----
st.title(":bar_chart: Panel de Movimientos Bancarios")
st.markdown("##")

# Leer el archivo CSV
nombre_archivo = 'taxi-all-23-3.csv'
dataframe = pd.read_csv(nombre_archivo, thousands=',', na_values=['NaN', 'N/A', 'NaT', 'NaN '],encoding='latin1')


# Completar los valores NaN en las columnas 'debito' y 'credito' con 0
dataframe['debito'].fillna(0, inplace=True)
dataframe['credito'].fillna(0, inplace=True)
# Convertir la columna 'Fecha' a tipo de dato de fecha
dataframe['Fecha'] = pd.to_datetime(dataframe['Fecha'], errors='coerce')



# Convertir las columnas 'debito', 'credito' y 'saldo' a tipo de dato float
columnas_numericas = ['debito', 'credito', 'saldo']
for columna in columnas_numericas:
    dataframe[columna] = dataframe[columna].str.replace('.', '').str.replace(',', '.').astype(float)


tipos_de_datos = dataframe.dtypes

# Obtener el mes elegido y convertirlo a número de asiento
mes_elegido = st.selectbox("Selecciona un mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])

mes_a_asiento = {
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12
}

asiento_elegido = mes_a_asiento.get(mes_elegido, None)

# Filtrar los datos para el mes elegido
datos_mes_elegido = dataframe[dataframe['Asiento'] == asiento_elegido]

# Calcular los valores de débito, crédito y saldo para el mes elegido
debito_mes_elegido = round(datos_mes_elegido['debito'].sum(),2)
credito_mes_elegido = round(datos_mes_elegido['credito'].sum(),2)
saldo_mes_elegido = datos_mes_elegido['saldo'].iloc[-1] if not datos_mes_elegido.empty else 0

# Mostrar los resultados en las cards
st.subheader(f"Resumen para el mes de {mes_elegido}:")


cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="Debito", content=debito_mes_elegido, description="", key="card8")
with cols[1]:
    ui.metric_card(title="Credito", content=credito_mes_elegido, description="", key="card9")
with cols[2]:
    ui.metric_card(title="Saldo", content=saldo_mes_elegido, description="", key="card10")

##############
###########
import plotly.express as px


# Filtrar el DataFrame para obtener solo las filas con el concepto "SALDO RES. ANTERIOR"
saldo_anterior_rows = dataframe[dataframe['Concepto'] == 'SALDO RES. ANTERIOR']

# Mostrar las filas en Streamlit
#st.write("Filas con el concepto 'SALDO RES. ANTERIOR':")
#st.write(saldo_anterior_rows)

# Definir los datos de la tabla SALDO RES. ANTERIOR
saldo_anterior_data = [
    (1, 3292112.58),
    (2, 625463.43),
    (3, 623166.54),
    (4, 691768.11),
    (5, 810544.51),
    (6, 384035.94),
    (7, 354512.78),
    (8, 194530.95),
    (9, 972569.29),
    (10, 1295412.71),
    (11, 894850.89),
    (12, 1521975.84)
]

# Crear un diccionario a partir de los datos
saldo_anterior_dict = {}
for mes, saldo in saldo_anterior_data:
    saldo_anterior_dict[f"SALDO RES. ANTERIOR {mes}"] = saldo

# Mostrar el diccionario en Streamlit
#st.write("Diccionario con Concepto y Saldo para 'SALDO RES. ANTERIOR':")
#st.write(saldo_anterior_dict)

# Definir los datos de la tabla SALDO RES. ANTERIOR
saldo_anterior_data = [
    (1, 3292112.58),
    (2, 625463.43),
    (3, 623166.54),
    (4, 691768.11),
    (5, 810544.51),
    (6, 384035.94),
    (7, 354512.78),
    (8, 194530.95),
    (9, 972569.29),
    (10, 1295412.71),
    (11, 894850.89),
    (12, 1521975.84)
]

# Crear un DataFrame a partir de los datos
df_saldo_anterior = pd.DataFrame(saldo_anterior_data, columns=['Mes', 'Saldo'])






# Definir los datos de las ventas por hora
sales_by_hour_data = {
    "hour": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "Total": [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]  # Ejemplo de datos, reemplazar con los reales
}

# Crear un DataFrame a partir de los datos
df_sales_by_hour = pd.DataFrame(saldo_anterior_data, columns=['Mes', 'Saldo'])

# Crear el gráfico de barras
fig_hourly_sales = px.bar(
    df_sales_by_hour,
    x='Mes',
    y='Saldo',
    title="<b>Saldo por mes</b>",
    color='Saldo',
    color_continuous_scale='blues',
    template="plotly_white"
)

# Configurar el diseño del gráfico
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False)
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_hourly_sales, use_container_width=True)


############

df = dataframe

# Ahora, realiza el análisis de datos financieros usando el CSV ya cargado
# Definir las funciones de análisis de datos
def cuentas_unicas(datos):
    return datos['cuenta'].nunique()

def cuentas_mas_repetidas(datos, n=5):
    cuentas_repetidas = datos['cuenta'].value_counts().head(n)
    cuentas_destinatario = {}
    for cuenta in cuentas_repetidas.index:
        destinatario = datos.loc[datos['cuenta'] == cuenta, 'destinatario'].iloc[0]
        cuentas_destinatario[cuenta] = destinatario
    return cuentas_repetidas, cuentas_destinatario

st.title("Análisis de datos financieros")

# Slider para que el usuario elija el número de cuentas repetidas
num_cuentas = st.slider("Selecciona el número de cuentas repetidas:", min_value=1, max_value=10, value=5)

# Botón para ejecutar el análisis
if st.button("Realizar análisis"):
    st.write("Número de cuentas únicas:", cuentas_unicas(df))
    st.write(f"{num_cuentas} cuentas más repetidas:")
    cuentas_repetidas, cuentas_destinatario = cuentas_mas_repetidas(df, n=num_cuentas)
    cuentas_df = pd.DataFrame({'Cuenta': cuentas_repetidas.index, 'Destinatario': [cuentas_destinatario[cuenta] for cuenta in cuentas_repetidas.index], 'Frecuencia': cuentas_repetidas.values})
    ui.table(data=cuentas_df, maxHeight=300)


# Datos de inflación por mes en Argentina para 2023
inflacion_2023 = {
    "Enero": 6,
    "Febrero": 6.6,
    "Marzo": 7.7,
    "Abril": 8.4,
    "Mayo": 7.8,
    "Junio": 6,
    "Julio": 6.3,
    "Agosto": 12.4,
    "Septiembre": 12.7,
    "Octubre": 8.3,
    "Noviembre": 12.8,
    "Diciembre": 25.5
}



# Datos de saldo anterior
saldo_anterior_data1 = [
    ("Enero", 3292112.58),
    ("Febrero", 625463.43),
    ("Marzo", 623166.54),
    ("Abril", 691768.11),
    ("Mayo", 810544.51),
    ("Junio", 384035.94),
    ("Julio", 354512.78),
    ("Agosto", 194530.95),
    ("Septiembre", 972569.29),
    ("Octubre", 1295412.71),
    ("Noviembre", 894850.89),
    ("Diciembre", 1521975.84)
]

# Crear un DataFrame a partir de los datos de saldo anterior
df_saldo_anterior1 = pd.DataFrame(saldo_anterior_data1, columns=['Mes', 'Saldo'])

# Calcular el factor de ajuste para cada mes y aplicarlo al saldo anterior
for mes, tasa_inflacion in inflacion_2023.items():
    factor_ajuste = 1 + (tasa_inflacion / 100)
    df_saldo_anterior1.loc[df_saldo_anterior1['Mes'] == mes, 'Saldo Ajustado'] = round(df_saldo_anterior['Saldo'] * factor_ajuste, 2)

# Mostrar los saldos ajustados por inflación en Streamlit
st.subheader("Saldos ajustados por inflación:")
#st.write(df_saldo_anterior1)

#no se ve??
#ui.table(data=df_saldo_anterior1, maxHeight=300)

# Datos proporcionados
nuevo_data = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "Saldo": [3292112.58, 625463.43, 623166.54, 691768.11, 810544.51, 384035.94, 354512.78, 194530.95, 972569.29, 1295412.71, 894850.89, 1521975.84],
    "Saldo Ajustado": [3489639.33, 666744.02, 671150.36, 749876.63, 873766.98, 407078.1, 376847.09, 218652.79, 1096085.59, 1402931.96, 1009391.8, 1910079.68]
}

# Crear el DataFrame
df_nuevo = pd.DataFrame(nuevo_data)

# Crear el gráfico de barras
fig_sales = px.bar(df_nuevo.melt(id_vars='Mes', var_name='Tipo', value_name='Valor'),
                    x='Mes',
                    y='Valor',
                    color='Tipo',
                    barmode='group',  # Agrupa las barras
                    title="<b>Saldo vs Saldo Ajustado por Mes</b>",
                    color_discrete_sequence=['#1f77b4', '#2ca02c'],  # Colores para las barras
                    template="plotly_white")

# Configurar el diseño del gráfico
fig_sales.update_layout(
    xaxis=dict(title='Mes'),
    yaxis=dict(title='Valor'),
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(title='Tipo', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_sales, use_container_width=True)



ui.table(data=df_saldo_anterior1, maxHeight=300)