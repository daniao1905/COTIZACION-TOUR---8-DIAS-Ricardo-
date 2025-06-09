
# Cotización de Tour Japón – JAPONTOUR360

Aplicación web desarrollada en Streamlit para calcular cotizaciones de tours de 8 días por Japón.

## 🧩 Funcionalidades

- Selección de **fecha de inicio del tour**
- Generación automática del itinerario de **8 días consecutivos**
- Cálculo dinámico de:
  - Tipo de día (semana o fin de semana)
  - Costos de transporte (Hiace / Alphard)
  - Guía y asistente
  - Hoteles por ciudad, día y tipo de tarifa
  - Hotel del conductor (opcional)
  - Shinkansen (opcional día 5)
- **Resumen total** por persona y por día
- **Descarga de PDF** con desglose tipo factura
- Compatibilidad total con **Streamlit Cloud** y **GitHub**

## 🗂 Archivos importantes

- `streamlit_app.py`: Aplicación principal
- `hoteles_con_impuestos.csv`: Lista de hoteles con ciudad, tipo de día y precio con impuesto
- `requirements.txt`: Dependencias necesarias
- `/fonts/DejaVuSans.ttf`: Fuente obligatoria para generar PDF (UTF-8 compatible)

## 🚀 Cómo usar

1. Clona el repositorio o descomprime el ZIP.
2. Coloca la fuente `DejaVuSans.ttf` dentro de una carpeta llamada `fonts/` en el mismo directorio del archivo `streamlit_app.py`.
   Puedes descargarla aquí:
   👉 https://github.com/dejavu-fonts/dejavu-fonts/blob/master/ttf/DejaVuSans.ttf?raw=true
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecuta la app:

```bash
streamlit run streamlit_app.py
```

## 📦 Notas

- Desarrollado para tours organizados por **JAPONTOUR360**
- Basado en tarifas de hoteles reales con impuestos incluidos
- Requiere fuente UTF-8 para generación segura de PDF con caracteres especiales

---

¡Disfrútalo y haz tus cotizaciones de forma profesional!

