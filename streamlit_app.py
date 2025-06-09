
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

# Itinerario base con ciudad por día y nuevas tarifas
itinerario = [
    {"día": 1, "ciudad": "Tokio", "lugar": "Tokyo Airport Pickup", "Hiace_Narita": 62000, "Alphard_Narita": 42000, "Hiace_Haneda": 36000, "Alphard_Haneda": 33000},
    {"día": 2, "ciudad": "Tokio", "lugar": "Tokyo", "Hiace": 99400, "Alphard": 92000},
    {"día": 3, "ciudad": "Tokio", "lugar": "Kamakura", "Hiace": 136500, "Alphard": 130000},
    {"día": 4, "ciudad": "Hakone", "lugar": "Hakone・Fuji", "Hiace": 170000, "Alphard": 155000},
    {"día": 5, "ciudad": "Monte Fuji", "lugar": "Hakone・Nagoya", "Hiace": 225000, "Alphard": 210000},
    {"día": 6, "ciudad": "Kioto", "lugar": "Kioto", "Hiace": 37000, "Alphard": 33000},
    {"día": 7, "ciudad": "Kioto", "lugar": "Kioto", "Hiace": 98000, "Alphard": 96600},
    {"día": 8, "ciudad": "Osaka", "lugar": "Nara", "Hiace": 119000, "Alphard": 116000},
]
itinerario = [
    {"día": 1, "ciudad": "Tokio", "lugar": "Tokyo Airport Pickup", "Hiace_Narita": 78000, "Alphard_Narita": 55000, "Hiace_Haneda": 62000, "Alphard_Haneda": 42000},
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
    ciudad = dia["ciudad"]

    dias_semana = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    dia_semana_es = dias_semana[fecha_dia.strftime('%A')]
    st.markdown(f"### Día {dia['día']}: {dia['lugar']} ({ciudad}) – {dia_semana_es} {fecha_dia.strftime('%d/%m/%Y')}")

    usar_vehiculo = st.checkbox("¿Necesita vehículo?", value=True, key=f"veh_{i}")

    if dia["día"] == 1:
        opciones_transporte = {
            "Hiace desde Narita": dia["Hiace_Narita"],
            "Hiace desde Haneda": dia["Hiace_Haneda"],
            "Alphard desde Narita": dia["Alphard_Narita"],
            "Alphard desde Haneda": dia["Alphard_Haneda"],
        }
        seleccion = st.radio("Selecciona el vehículo y aeropuerto", list(opciones_transporte.keys()), key=f"select_vehiculo_{i}")
        precio_vehiculo = opciones_transporte[seleccion] if usar_vehiculo else 0
    else:
        opciones_vehiculo = ["Hiace", "Alphard"]
        seleccion = st.radio("Selecciona el vehículo", opciones_vehiculo, key=f"select_vehiculo_{i}")
        precio_vehiculo = dia[seleccion] if usar_vehiculo else 0

    st.markdown("**Selecciona el hotel:**")
    hoteles_disponibles = df_hoteles["NombreHotel"].tolist()
    precios_hoteles = (df_hoteles["Precio"] + df_hoteles["Impuesto"]).tolist()
    lista_hoteles = [
    f"{row['NombreHotel']} – ¥{row['Precio'] + row['Impuesto']:,}"
    for _, row in df_hoteles.iterrows()
]
    hotel_seleccionado = st.selectbox("Hotel", lista_hoteles, key=f"hotel_{i}")
    opciones_vehiculo = []
    if dia["día"] == 1:
        opciones_vehiculo = ["Hiace", "Alphard"]  # no hay precios directos, se seleccionan después por aeropuerto
    else:
        if "Hiace" in dia and "Alphard" in dia:
            opciones_vehiculo = [f"Hiace – ¥{dia['Hiace']:,}", f"Alphard – ¥{dia['Alphard']:,}"]

    vehiculo = st.selectbox(f"Vehículo", opciones_vehiculo, key=f"select_vehiculo_{i}") if opciones_vehiculo else ""
    vehiculo = "Hiace" if "Hiace" in vehiculo else "Alphard"
    vehiculo = "Hiace" if "Hiace" in vehiculo else "Alphard"
    if dia["día"] == 1:
        aeropuerto = st.radio("Aeropuerto de llegada", ["Haneda", "Narita"], key=f"aeropuerto_{i}")
        if aeropuerto == "Narita":
            precio_vehiculo = dia["Hiace_Narita"] if vehiculo == "Hiace" else dia["Alphard_Narita"]
        else:
            precio_vehiculo = dia["Hiace_Haneda"] if vehiculo == "Hiace" else dia["Alphard_Haneda"]
    else:
        precio_vehiculo = dia[vehiculo] if usar_vehiculo else 0

    guia = st.checkbox("¿Necesita guía?", key=f"guia_{i}")
    asistente = st.checkbox("¿Necesita asistente?", key=f"asistente_{i}")
    hotel_conductor = st.checkbox("¿Hotel para conductor este día?", key=f"hotel_cond_{i}")
    shinkansen = num_personas * 6000 if dia["día"] == 5 and st.checkbox("¿Agregar Shinkansen (día 5)?", key="shinkansen") else 0

    # Mostrar todos los hoteles disponibles en la ciudad sin filtrar por tipo de día

    cantidad_habitaciones = st.number_input("Cantidad de habitaciones", min_value=0, max_value=10, value=1, key=f"habitaciones_{i}")

    hoteles_disponibles = df_hoteles[
        df_hoteles["Ciudad"].str.strip().str.lower() == ciudad.strip().lower()
    ]

    hotel_dropdown = [f"{row['Hotel']} – ¥{int(row['Total por noche con impuesto (JPY)']):,}" for _, row in hoteles_disponibles.iterrows()]
    hotel_seleccionado = st.selectbox("Hotel para este día", hotel_dropdown, key=f"hotel_{i}") if hotel_dropdown else None

    precio_hotel = 0
    if hotel_seleccionado:
        hotel_nombre = hotel_seleccionado.split(" – ")[0]
        fila = hoteles_disponibles[hoteles_disponibles["Hotel"] == hotel_nombre]
        if not fila.empty:
            precio_hotel = int(fila.iloc[0]["Total por noche con impuesto (JPY)"]) * cantidad_habitaciones

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
        "Hotel": hotel_nombre if hotel_seleccionado else "",
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
