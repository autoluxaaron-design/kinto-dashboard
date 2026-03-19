# 🔧 Soluciones de Problemas CORS y Alternativas Técnicas

## Problema: "CORS Error" o "No se puede cargar desde Google Sheets"

Si al abrir el archivo `index.html` ves un error de CORS en la consola del navegador, aquí hay varias soluciones:

---

## ✅ Solución 1: Usar un Proxy CORS (RECOMENDADO - Fácil)

### Paso 1: Editar index.html
Busca esta línea:
```javascript
const CSV_URL = `https://docs.google.com/spreadsheets/d/${GOOGLE_SHEET_ID}/export?format=csv&gid=${SHEET_GID}`;
```

Reemplázala por:
```javascript
const CSV_URL = `https://cors-anywhere.herokuapp.com/https://docs.google.com/spreadsheets/d/${GOOGLE_SHEET_ID}/export?format=csv&gid=${SHEET_GID}`;
```

**¿Qué hace?** Un servicio gratuito que actúa como intermediario.

**Ventajas:**
- ✅ Muy fácil de implementar
- ✅ No requiere backend propio
- ✅ Funciona inmediatamente

**Desventajas:**
- ⚠️ Depende de un servicio externo (puede no estar disponible)
- ⚠️ Puede ser más lento

**Alternativas de Proxy:**
- `https://api.allorigins.win/get?url=` (mejor estabilidad)
- `https://thingproxy.freeboard.io/fetch/`

---

## ✅ Solución 2: Usar Google Sheets API (RECOMENDADO - Más robusto)

### Paso 1: Obtener una API Key
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita "Google Sheets API"
4. Crea una "Clave API" (API Key)
5. Copia la clave

### Paso 2: Reemplazar el código de carga en index.html

Busca la función `loadBookings()` y reemplázala con:

```javascript
async function loadBookings() {
    try {
        const container = document.getElementById('bookingsContainer');
        container.innerHTML = '<div class="loading"><div class="loading-spinner"></div><p>Cargando reservas...</p></div>';

        // Tu API Key de Google
        const API_KEY = 'TU_CLAVE_API_AQUI'; // Reemplaza esto
        
        // URL de la API
        const apiUrl = `https://sheets.googleapis.com/v4/spreadsheets/${GOOGLE_SHEET_ID}/values/Bookings!A:N?key=${API_KEY}`;
        
        const response = await fetch(apiUrl);
        const data = await response.json();

        if (!data.values || data.values.length < 2) {
            showEmptyState();
            return;
        }

        // Procesar datos
        allBookings = data.values.slice(1).filter(row => row[0] && row[0].trim());
        vehicles = [...new Set(allBookings.map(b => b[COLUMNS.VEHICLE]).filter(v => v))].sort();
        populateVehicleFilter();
        filterAndDisplay();

    } catch (error) {
        console.error('Error loading bookings:', error);
        showErrorState('Error al cargar desde Google Sheets API. Verifica tu API Key.');
    }
}
```

**Ventajas:**
- ✅ Solución oficial de Google
- ✅ Mejor estabilidad
- ✅ No requiere parseo de CSV
- ✅ Más control

**Desventajas:**
- ⚠️ Requiere configuración inicial
- ⚠️ Expones tu API Key en el HTML (considera restricciones HTTP)

---

## ✅ Solución 3: Usar Python con Streamlit (OPCIÓN B)

Si los problemas persisten, aquí está la versión en Python:

### Requisitos:
```bash
pip install streamlit pandas google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Crear archivo `app.py`:

```python
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Dashboard de Reservas", layout="wide")

# Estilos CSS personalizados
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Dashboard de Reservas")

# URL del Google Sheet (públicamente accesible)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1pbgu_CAaeFcd06-E_DkgOihvCLTzAsM276bOu69rrxQ/edit?usp=sharing"

try:
    # Intentar cargar desde CSV
    csv_url = "https://docs.google.com/spreadsheets/d/1pbgu_CAaeFcd06-E_DkgOihvCLTzAsM276bOu69rrxQ/export?format=csv"
    df = pd.read_csv(csv_url)
    
    st.success(f"✅ {len(df)} reservas cargadas")
    
    # Filtros en la barra lateral
    st.sidebar.header("🔍 Filtros")
    
    filter_lugar = st.sidebar.multiselect(
        "📍 Lugar",
        options=df["Lugar"].unique(),
        default=df["Lugar"].unique()
    )
    
    filter_vehicle = st.sidebar.multiselect(
        "🚙 Vehículo",
        options=df["Vehicle"].unique(),
        default=df["Vehicle"].unique()
    )
    
    filter_member = st.sidebar.text_input("🔍 Buscar miembro")
    
    # Aplicar filtros
    filtered_df = df[
        (df["Lugar"].isin(filter_lugar)) &
        (df["Vehicle"].isin(filter_vehicle))
    ]
    
    if filter_member:
        filtered_df = filtered_df[filtered_df["Member"].str.contains(filter_member, case=False, na=False)]
    
    # Mostrar estadísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        urgent = len(filtered_df[filtered_df["Póxima Reserva"].str.contains("URGENTE", na=False)])
        st.metric("🚨 URGENTES", urgent)
    
    with col2:
        warning = len(filtered_df[filtered_df["Póxima Reserva"].str.contains("⚠️", na=False)])
        st.metric("⚠️ ADVERTENCIAS", warning)
    
    with col3:
        pending = len(filtered_df[filtered_df["Próxima Reserva"].str.contains("⏳", na=False)])
        st.metric("⏳ PENDIENTES", pending)
    
    with col4:
        available = len(filtered_df[filtered_df["Próxima Reserva"].str.contains("Disponible", na=False)])
        st.metric("✅ DISPONIBLES", available)
    
    # Mostrar tabla
    st.subheader(f"📋 Reservas ({len(filtered_df)} total)")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Ordenar por fecha de pickup
    if "Pick up" in filtered_df.columns:
        filtered_df["Pick up"] = pd.to_datetime(filtered_df["Pick up"], errors='coerce')
        filtered_df = filtered_df.sort_values("Pick up")
    
except Exception as e:
    st.error(f"❌ Error al cargar los datos: {str(e)}")
    st.info("Asegúrate que el Google Sheet sea público y accesible")
```

### Ejecutar:
```bash
streamlit run app.py
```

**Ventajas:**
- ✅ Sin problemas de CORS
- ✅ Más funcionalidades
- ✅ Interfaz moderna
- ✅ Fácil actualizar

**Desventajas:**
- ⚠️ Requiere Python instalado
- ⚠️ Necesita servidor ejecutándose

---

## ✅ Solución 4: Permitir CORS en Chrome (Temporal, solo para testing)

### Por línea de comandos (Windows):
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --disable-web-security --user-data-dir="c:/chromeTemp"
```

⚠️ **ADVERTENCIA:** Solo para testing local, NO es seguro para uso en producción.

---

## 📊 Resumen de Opciones

| Opción | Dificultad | Velocidad | Estabilidad | Instalación |
|--------|-----------|-----------|-------------|-------------|
| **1. HTML + Proxy CORS** | ⭐ Fácil | Media | Media | Ninguna |
| **2. HTML + API Google** | ⭐⭐ Media | Rápida | Alta | API Key |
| **3. Python + Streamlit** | ⭐⭐ Media | Media | Alta | pip install |
| **4. Servidor Backend** | ⭐⭐⭐ Difícil | Rápida | Alta | Setup complejo |

---

## 🎯 Recomendación Final

**Para uso rápido:** Opción 1 (Proxy CORS)
**Para producción:** Opción 2 (Google Sheets API) o Opción 3 (Streamlit)
**Para máxima confiabilidad:** Opción 3 (Streamlit con Python)

---

## 📞 Debugging

Si aún tienes problemas:

1. **Abre la Consola** (F12 en Chrome)
   - Ve a la pestaña "Console"
   - Busca mensajes de error rojo

2. **Verifica el Network Tab**
   - Ve a "Network"
   - Reload la página
   - Busca la solicitud a Google Sheets
   - Revisa el estado (200 = bien, 4xx = error)

3. **Prueba la URL CSV directamente**
   - Abre en el navegador:
   - `https://docs.google.com/spreadsheets/d/1pbgu_CAaeFcd06-E_DkgOihvCLTzAsM276bOu69rrxQ/export?format=csv`
   - Debe descargar un archivo CSV

---

**¡Elige la solución que se adapte mejor a tu caso!** 🚀
