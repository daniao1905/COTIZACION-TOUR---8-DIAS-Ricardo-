
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cotización de Tour", layout="wide")

st.title("Cotización de Tour Japón – Travel Viajes Intl")

# Entradas
num_personas = st.number_input("Cantidad de personas en el tour", min_value=1, max_value=100, value=10)

# Itinerario base
itinerario = [
    {"día": 1, "lugar": "Tokyo Airport Pickup", "Hiace": 62000, "Alphard": 42000},
    {"día": 2, "lugar": "Tokyo", "Hiace": 99400, "Alphard": 92000},
    {"día": 3, "lugar": "Kamakura", "Hiace": 136500, "Alphard": 130000},
    {"día": 4, "lugar": "Hakone・Fuji", "Hiace": 170000, "Alphard": 155000},
    {"día": 5, "lugar": "Hakone・Nagoya", "Hiace": 225000, "Alphard": 210000},
    {"día": 6, "lugar": "Kioto", "Hiace": 37000, "Alphard": 33000},
    {"día": 7, "lugar": "Kioto", "Hiace": 98000, "Alphard": 93000},
    {"día": 8, "lugar": "Nara", "Hiace": 119000, "Alphard": 112000},
]

# Configuración diaria
st.subheader("Configuración por día")

cotizacion = []

for dia in itinerario:
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        st.markdown(f"**Día {dia['día']}: {dia['lugar']}**")
    with col2:
        vehiculo = st.selectbox(f"Vehículo Día {dia['día']}", ["Hiace", "Alphard"], key=f"veh_{dia['día']}")
    with col3:
        guia = st.checkbox("Guía", key=f"guia_{dia['día']}")
    with col4:
        asistente = st.checkbox("Asistente", key=f"asis_{dia['día']}")

    precio_vehiculo = dia[vehiculo]
    precio_guia = 69000 if guia else 0
    precio_asistente = 32500 if asistente else 0
    total_dia = precio_vehiculo + precio_guia + precio_asistente

    cotizacion.append({
        "Día": dia["día"],
        "Lugar": dia["lugar"],
        "Vehículo": vehiculo,
        "Precio Vehículo (JPY)": precio_vehiculo,
        "Guía": "Sí" if guia else "No",
        "Precio Guía (JPY)": precio_guia,
        "Asistente": "Sí" if asistente else "No",
        "Precio Asistente (JPY)": precio_asistente,
        "Total Día (JPY)": total_dia
    })

df_cotizacion = pd.DataFrame(cotizacion)

# Costo shinkansen
st.subheader("Shinkansen")
shinkansen_total = num_personas * 6000
st.write(f"Costo total de Shinkansen (Nagoya → Kioto) para {num_personas} personas: ¥{shinkansen_total:,}")

# Hotel conductor
st.subheader("Hotel para conductor")
incluye_hotel_conductor = st.checkbox("Incluir hotel para conductor (¥20,000 por noche)")
hotel_conductor_total = 20000 * len(itinerario) if incluye_hotel_conductor else 0

# Totales
st.subheader("Resumen General")

total_transporte = df_cotizacion["Total Día (JPY)"].sum()
total_general = total_transporte + shinkansen_total + hotel_conductor_total

st.write(f"**Total transporte, guías y asistentes:** ¥{total_transporte:,}")
st.write(f"**Shinkansen:** ¥{shinkansen_total:,}")
st.write(f"**Hotel conductor:** ¥{hotel_conductor_total:,}")
st.markdown("---")
st.write(f"### Total General: ¥{total_general:,}")

# Exportar a Excel
st.subheader("Exportar Cotización")
if st.button("Descargar Excel"):
    df_export = df_cotizacion.copy()
    df_export["Shinkansen Total"] = shinkansen_total
    df_export["Hotel Conductor"] = hotel_conductor_total
    df_export["Total General"] = total_general
    df_export.to_excel("cotizacion_tour.xlsx", index=False)
    with open("cotizacion_tour.xlsx", "rb") as file:
        st.download_button("Haz clic para descargar", file, file_name="cotizacion_tour.xlsx")
