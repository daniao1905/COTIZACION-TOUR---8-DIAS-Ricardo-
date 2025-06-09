
import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Cotización de Tour", layout="wide")

# Cargar hoteles desde CSV
df_hoteles = pd.read_csv("hoteles_con_impuestos.csv")

st.title("Cotización de Tour Japón – JAPONTOUR360")

# Seleccionar fecha de inicio
fecha_inicio = st.date_input("Selecciona la fecha de inicio del tour", value=datetime.today())
num_personas = st.number_input("Cantidad de personas en el tour", min_value=1, max_value=6, value=2)

# Itinerario base con ciudad por día
itinerario = [
    {"día": 1, "ciudad": "Tokio", "lugar": "Tokyo Airport Pickup", "Hiace": 62000, "Alphard": 42000},
    {"día": 2, "ciudad": "Tokio", "lugar": "Tokyo", "Hiace": 99400, "Alphard": 92000},
    {"día": 3, "ciudad": "Tokio", "lugar": "Kamakura", "Hiace": 136500, "Alphard": 130000},
    {"día": 4, "ciudad": "Hakone", "lugar": "Hakone・Fuji", "Hiace": 170000, "Alphard": 155000},
    {"día": 5, "ciudad": "Monte Fuji", "lugar": "Hakone・Nagoya", "Hiace": 225000, "Alphard": 210000},
    {"día": 6, "ciudad": "Kioto", "lugar": "Kioto", "Hiace": 37000, "Alphard": 33000},
    {"día": 7, "ciudad": "Kioto", "lugar": "Kioto", "Hiace": 98000, "Alphard": 93000},
    {"día": 8, "ciudad": "Osaka", "lugar": "Nara", "Hiace": 119000, "Alphard": 112000},
]

cotizacion = []

st.subheader("Configuración diaria")

for i, dia in enumerate(itinerario):
    fecha_dia = fecha_inicio + timedelta(days=i)
    tipo_dia = "Fin de semana" if fecha_dia.weekday() in [5, 6] else "Día de semana"
    ciudad = dia["ciudad"]

    st.markdown(f"### Día {dia['día']}: {dia['lugar']} ({ciudad}) – {fecha_dia.strftime('%A %d/%m/%Y')}")

    usar_vehiculo = st.checkbox("¿Necesita vehículo?", value=True, key=f"veh_{i}")
    vehiculo = st.selectbox(f"Vehículo", [f"Hiace – ¥{dia['Hiace']:,}", f"Alphard – ¥{dia['Alphard']:,}"], key=f"vehiculo_{i}")
    vehiculo = "Hiace" if "Hiace" in vehiculo else "Alphard"
    precio_vehiculo = dia[vehiculo] if usar_vehiculo else 0

    guia = st.checkbox("¿Necesita guía?", key=f"guia_{i}")
    asistente = st.checkbox("¿Necesita asistente?", key=f"asistente_{i}")
    hotel_conductor = st.checkbox("¿Hotel para conductor este día?", key=f"hotel_cond_{i}")
    shinkansen = num_personas * 6000 if dia["día"] == 5 and st.checkbox("¿Agregar Shinkansen (día 5)?", key="shinkansen") else 0

    # Hoteles disponibles
    hoteles_disponibles = df_hoteles[
        (df_hoteles["Ciudad"] == ciudad) & (df_hoteles["Tipo de día"].str.lower() == tipo_dia.lower())
    ]
    hotel_opciones = hoteles_disponibles["Hotel"].unique().tolist()
    hotel_seleccionado = st.selectbox("Hotel para este día", hotel_opciones, key=f"hotel_{i}") if hotel_opciones else None
    precio_hotel = 0

    if hotel_seleccionado:
        precio_hotel = hoteles_disponibles[
            (df_hoteles["Hotel"] == hotel_seleccionado)
        ]["Total por noche con impuesto (JPY)"].values[0]

    precio_guia = 69000 if guia else 0
    precio_asistente = 32500 if asistente else 0
    precio_hotel_cond = 20000 if hotel_conductor else 0

    total_dia = precio_vehiculo + precio_guia + precio_asistente + precio_hotel_cond + precio_hotel + shinkansen

    cotizacion.append({
        "Día": dia["día"],
        "Ciudad": ciudad,
        "Fecha": fecha_dia.strftime("%Y-%m-%d"),
        "Vehículo": vehiculo if usar_vehiculo else "No requerido",
        "Precio Vehículo": precio_vehiculo,
        "Guía": "Sí" if guia else "No",
        "Precio Guía": precio_guia,
        "Asistente": "Sí" if asistente else "No",
        "Precio Asistente": precio_asistente,
        "Hotel": hotel_seleccionado,
        "Precio Hotel": precio_hotel,
        "Hotel Conductor": "Sí" if hotel_conductor else "No",
        "Precio Hotel Conductor": precio_hotel_cond,
        "Shinkansen": shinkansen,
        "Total Día": total_dia,
        "Total por Persona": total_dia / num_personas if num_personas else 0
    })

df = pd.DataFrame(cotizacion)

st.subheader("Resumen de Cotización")
st.dataframe(df)

st.markdown(f"### Total General: ¥{int(df['Total Día'].sum()):,}")
st.markdown(f"### Total por Persona: ¥{int(df['Total por Persona'].sum()):,}")

# Exportar PDF
st.subheader("Exportar cotización en PDF")
if st.button("Descargar PDF"):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "JAPONTOUR360 – Cotización de Servicios", ln=True)
    pdf.cell(0, 10, f"Fecha de emisión: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)

    for _, row in df.iterrows():
        pdf.set_font("DejaVu", "", 10)
        pdf.cell(0, 8, f"Día {int(row['Día'])} – {row['Fecha']} – {row['Ciudad']}", ln=True)
        pdf.cell(0, 8, f"Vehículo: {row['Vehículo']} - ¥{int(row['Precio Vehículo']):,}", ln=True)
        if row["Guía"] == "Sí":
            pdf.cell(0, 8, f"Guía: Sí - ¥{int(row['Precio Guía']):,}", ln=True)
        if row["Asistente"] == "Sí":
            pdf.cell(0, 8, f"Asistente: Sí - ¥{int(row['Precio Asistente']):,}", ln=True)
        if row["Hotel"]:
            pdf.cell(0, 8, f"Hotel: {row['Hotel']} - ¥{int(row['Precio Hotel']):,}", ln=True)
        if row["Hotel Conductor"] == "Sí":
            pdf.cell(0, 8, f"Hotel Conductor: Sí - ¥{int(row['Precio Hotel Conductor']):,}", ln=True)
        if row["Shinkansen"] > 0:
            pdf.cell(0, 8, f"Shinkansen: ¥{int(row['Shinkansen']):,}", ln=True)
        pdf.cell(0, 8, f"Subtotal Día: ¥{int(row['Total Día']):,} – Por persona: ¥{int(row['Total por Persona']):,}", ln=True)
        pdf.ln(4)

    pdf.output("cotizacion_japontour360.pdf")
    with open("cotizacion_japontour360.pdf", "rb") as f:
        st.download_button("Descargar PDF generado", f, file_name="cotizacion_japontour360.pdf")
