
import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Cotización de Tour", layout="wide")
st.title("Cotización de Tour Japón – JAPONTOUR360")

# Entradas generales
num_personas = st.number_input("Cantidad de personas en el tour", min_value=1, max_value=6, value=2)

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

cotizacion = []

st.subheader("Configuración diaria")

for dia in itinerario:
    with st.expander(f"Día {dia['día']}: {dia['lugar']}"):
        usar_vehiculo = st.checkbox("¿Necesita vehículo?", value=True, key=f"veh_{dia['día']}")
        vehiculo = st.selectbox(
            "Seleccione vehículo",
            [f"Hiace – ¥{dia['Hiace']:,}", f"Alphard – ¥{dia['Alphard']:,}"],
            key=f"tipo_{dia['día']}"
        )
        vehiculo = "Hiace" if "Hiace" in vehiculo else "Alphard"
    
        guia = st.checkbox("¿Necesita guía?", key=f"guia_{dia['día']}")
        asistente = st.checkbox("¿Necesita asistente?", key=f"asis_{dia['día']}")
        hotel_conductor = st.checkbox("¿Hotel para conductor este día?", key=f"hotel_cond_{dia['día']}")
        shinkansen = num_personas * 6000 if dia["día"] == 5 and st.checkbox("¿Agregar Shinkansen (día 5)?", key="shinkansen") else 0

        precio_vehiculo = dia[vehiculo] if usar_vehiculo else 0
        precio_guia = 69000 if guia else 0
        precio_asistente = 32500 if asistente else 0
        precio_hotel_conductor = 20000 if hotel_conductor else 0

        total_dia = precio_vehiculo + precio_guia + precio_asistente + precio_hotel_conductor + shinkansen

        cotizacion.append({
            "Día": dia["día"],
            "Lugar": dia["lugar"],
            "Vehículo": vehiculo if usar_vehiculo else "No requerido",
            "Precio Vehículo": precio_vehiculo,
            "Guía": "Sí" if guia else "No",
            "Precio Guía": precio_guia,
            "Asistente": "Sí" if asistente else "No",
            "Precio Asistente": precio_asistente,
            "Hotel Conductor": "Sí" if hotel_conductor else "No",
            "Precio Hotel Conductor": precio_hotel_conductor,
            "Shinkansen": shinkansen,
            "Total Día": total_dia,
            "Total por Persona": total_dia / num_personas if num_personas else 0
        })

df = pd.DataFrame(cotizacion)

# Mostrar tabla
st.subheader("Resumen de Cotización")
st.dataframe(df.style.format("¥{:,.0f}", subset=[
    "Precio Vehículo", "Precio Guía", "Precio Asistente",
    "Precio Hotel Conductor", "Shinkansen", "Total Día", "Total por Persona"
]))

total_general = df["Total Día"].sum()
total_persona = df["Total por Persona"].sum()

st.markdown(f"### Total General: ¥{total_general:,.0f}")
st.markdown(f"### Costo por Persona: ¥{total_persona:,.0f}")

# Exportar PDF
st.subheader("Exportar Cotización en PDF")

if st.button("Descargar PDF"):

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "JAPONTOUR360 – Cotización de Servicios", ln=True, align="C")
            self.set_font("Arial", "", 10)
            self.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="R")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, "JAPONTOUR360 - www.japontour360.com", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for _, row in df.iterrows():
        pdf.cell(0, 8, f"Día {int(row['Día'])} – {row['Lugar']}", ln=True)
        pdf.cell(0, 8, f"Vehículo: {row['Vehículo']} - ¥{int(row['Precio Vehículo']):,}", ln=True)
        if row["Guía"] == "Sí":
            pdf.cell(0, 8, f"Guía: Sí - ¥{int(row['Precio Guía']):,}", ln=True)
        if row["Asistente"] == "Sí":
            pdf.cell(0, 8, f"Asistente: Sí - ¥{int(row['Precio Asistente']):,}", ln=True)
        if row["Hotel Conductor"] == "Sí":
            pdf.cell(0, 8, f"Hotel Conductor: Sí - ¥{int(row['Precio Hotel Conductor']):,}", ln=True)
        if row["Shinkansen"] > 0:
            pdf.cell(0, 8, f"Shinkansen: ¥{int(row['Shinkansen']):,}", ln=True)
        pdf.cell(0, 8, f"Subtotal Día: ¥{int(row['Total Día']):,} – Por persona: ¥{int(row['Total por Persona']):,}", ln=True)
        pdf.ln(5)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total General: ¥{int(total_general):,}", ln=True)
    pdf.cell(0, 10, f"Costo por Persona: ¥{int(total_persona):,}", ln=True)

    pdf.output("cotizacion_japontour360.pdf")
    with open("cotizacion_japontour360.pdf", "rb") as f:
        st.download_button("Descargar PDF", f, file_name="cotizacion_japontour360.pdf")
