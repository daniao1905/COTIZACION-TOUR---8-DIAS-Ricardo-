
# Cotización Tour Japón – Travel Viajes Intl

Aplicación interactiva desarrollada con **Streamlit** para calcular cotizaciones de tours en Japón. Permite a los clientes simular costos diarios de transporte, guías, asistentes, tren bala y otros servicios turísticos.

## 🧩 Funcionalidades

- Selección de **cantidad de personas** en el tour
- Elección de **vehículo por día** (Hiace o Alphard)
- Opciones para agregar **guía** y **asistente** por jornada
- Cálculo automático de:
  - Transporte por día
  - Shinkansen (Nagoya → Kioto) – ¥6,000 por persona
  - Hotel del conductor (opcional, ¥20,000 por noche)
- **Desglose diario de costos**
- Exportación de la cotización en archivo **Excel**

## 🚀 Requisitos

- Python 3.8+
- Streamlit
- Pandas
- OpenPyXL

Instalación de dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Cómo Ejecutar

1. Clona el repositorio o descarga los archivos.
2. Ejecuta la app:
```bash
streamlit run streamlit_app.py
```

3. Abre la URL local que te entrega Streamlit en el navegador.
4. ¡Interpreta, ajusta y exporta tu cotización en tiempo real!

## 📁 Archivos

- `streamlit_app.py` – Código principal de la app
- `requirements.txt` – Dependencias necesarias
- `README.md` – Este archivo

## 📌 Nota

Este proyecto fue desarrollado para **Travel Viajes Intl** con base en las tarifas de 2025 para itinerarios entre Tokio, Kioto, Nagoya, Nara y Hakone.
