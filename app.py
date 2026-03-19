"""
Dashboard de Reservas - Versión Python/Streamlit
Alternativa a la versión HTML/JavaScript

INSTALACIÓN:
pip install streamlit pandas

EJECUCIÓN:
streamlit run app.py

Luego abre: http://localhost:8501
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
import requests

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Dashboard de Reservas",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .header-title {
        color: #667eea;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 20px;
    }
    .metric-container {
        padding: 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .urgente {
        background-color: #ffebee;
        border-left: 5px solid #ef5350;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning {
        background-color: #fffde7;
        border-left: 5px solid #fdd835;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .pending {
        background-color: #fff3e0;
        border-left: 5px solid #ffb74d;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .disponible {
        background-color: #e8f5e9;
        border-left: 5px solid #81c784;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="header-title">🚗 Dashboard de Reservas</h1>', unsafe_allow_html=True)
with col2:
    st.write("")  # Espaciador
    if st.button("🔄 Recargar", key="reload"):
        st.rerun()

# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data(ttl=300)  # Cache de 5 minutos
def load_data():
    """Carga datos del Google Sheet"""
    try:
        # URL del Google Sheet en formato CSV
        GOOGLE_SHEET_ID = '1pbgu_CAaeFcd06-E_DkgOihvCLTzAsM276bOu69rrxQ'
        sheet_gid = '0'
        url = f'https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid={sheet_gid}'
        
        # Descargar datos
        df = pd.read_csv(url)
        
        # Limpiar espacios en blanco
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        st.info("""
        Asegúrate que:
        1. El Google Sheet sea público (Compartir → Cualquier persona)
        2. La URL del Sheet sea correcta
        3. La pestaña "Bookings" exista
        """)
        return None

# ============================================================
# CARGAR DATOS
# ============================================================

df = load_data()

if df is None or len(df) == 0:
    st.warning("⚠️ No se pudieron cargar los datos. Verifica tu conexión.")
    st.stop()

# ============================================================
# PREPARAR DATOS
# ============================================================

# Renombrar columnas si es necesario
expected_cols = ['ID', 'Member', 'Vehicle', 'Lugar', 'Pick up', 'Hora', 
                  'Drop off', 'Hora.1', 'Entrega', 'Devolución', 
                  'Día Ent', 'Día Dev', 'Próxima Reserva', 'Feriado (Nac)']

# Intentar mapear correctamente
if 'Próxima Reserva' not in df.columns and 'Próxima Reserva' not in df.columns:
    try:
        df.columns = expected_cols
    except:
        pass

# Llenar valores vacíos
df = df.fillna("")

# ============================================================
# FILTROS EN SIDEBAR
# ============================================================

st.sidebar.header("🔍 Filtros")

# Obtener valores únicos para filtros
lugares = sorted(df['Lugar'].unique())
vehiculos = sorted(df['Vehicle'].unique())

# Crear filtros
filter_lugar = st.sidebar.multiselect(
    "📍 Lugar",
    options=lugares,
    default=lugares,
    key="filter_lugar"
)

filter_vehicle = st.sidebar.multiselect(
    "🚙 Vehículo",
    options=vehiculos,
    key="filter_vehicle"
)

filter_member = st.sidebar.text_input(
    "🔍 Buscar Miembro",
    key="filter_member"
)

# Opciones de estado
estado_opciones = ["Todos", "🚨 URGENTE", "⚠️ Advertencia", "⏳ Pendiente", "✅ Disponible"]
filter_estado = st.sidebar.selectbox(
    "⚠️ Estado Próxima Reserva",
    options=estado_opciones,
    key="filter_estado"
)

# Botón de limpiar
if st.sidebar.button("🔄 Limpiar Filtros", key="clear_filters"):
    st.rerun()

# ============================================================
# APLICAR FILTROS
# ============================================================

df_filtered = df.copy()

# Filtro por lugar
if filter_lugar:
    df_filtered = df_filtered[df_filtered['Lugar'].isin(filter_lugar)]

# Filtro por vehículo
if filter_vehicle:
    df_filtered = df_filtered[df_filtered['Vehicle'].isin(filter_vehicle)]

# Filtro por miembro
if filter_member:
    df_filtered = df_filtered[
        df_filtered['Member'].str.contains(filter_member, case=False, na=False)
    ]

# Filtro por estado
if filter_estado != "Todos":
    if filter_estado == "🚨 URGENTE":
        df_filtered = df_filtered[
            df_filtered['Próxima Reserva'].str.contains('URGENTE', case=False, na=False)
        ]
    elif filter_estado == "⚠️ Advertencia":
        df_filtered = df_filtered[
            df_filtered['Próxima Reserva'].str.contains('⚠️', case=False, na=False)
        ]
    elif filter_estado == "⏳ Pendiente":
        df_filtered = df_filtered[
            df_filtered['Próxima Reserva'].str.contains('⏳', case=False, na=False)
        ]
    elif filter_estado == "✅ Disponible":
        df_filtered = df_filtered[
            df_filtered['Próxima Reserva'].str.contains('Disponible', case=False, na=False) |
            (df_filtered['Próxima Reserva'] == "")
        ]

# ============================================================
# ESTADÍSTICAS
# ============================================================

st.markdown("---")

# Contar estados
urgente_count = len(df_filtered[df_filtered['Próxima Reserva'].str.contains('URGENTE', case=False, na=False)])
warning_count = len(df_filtered[df_filtered['Próxima Reserva'].str.contains('⚠️', case=False, na=False)])
pending_count = len(df_filtered[df_filtered['Próxima Reserva'].str.contains('⏳', case=False, na=False)])
disponible_count = len(df_filtered[
    (df_filtered['Próxima Reserva'].str.contains('Disponible', case=False, na=False)) |
    (df_filtered['Próxima Reserva'] == "")
])

# Mostrar métricas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🚨 URGENTES", urgente_count)
with col2:
    st.metric("⚠️ ADVERTENCIAS", warning_count)
with col3:
    st.metric("⏳ PENDIENTES", pending_count)
with col4:
    st.metric("✅ DISPONIBLES", disponible_count)
with col5:
    st.metric("📊 TOTAL", len(df_filtered))

st.markdown("---")

# ============================================================
# MOSTRAR DATOS
# ============================================================

st.subheader(f"📋 Reservas ({len(df_filtered)} de {len(df)} total)")

if len(df_filtered) == 0:
    st.info("📭 No hay reservas que coincidan con los filtros. Intenta cambiarlos.")
else:
    # Ordenar por fecha de pickup
    try:
        df_filtered['Pick up'] = pd.to_datetime(df_filtered['Pick up'], errors='coerce')
        df_filtered = df_filtered.sort_values('Pick up', ascending=True)
    except:
        pass
    
    # Mostrar tabla
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        height=600
    )

# ============================================================
# VISTA DE TARJETAS (OPCIONAL)
# ============================================================

if st.checkbox("📇 Ver como Tarjetas"):
    st.subheader("Tarjetas de Reservas")
    
    cols = st.columns(2)
    
    for idx, (_, row) in enumerate(df_filtered.iterrows()):
        col = cols[idx % 2]
        
        # Determinar clase CSS según estado
        status = row.get('Próxima Reserva', '')
        
        if 'URGENTE' in str(status):
            css_class = 'urgente'
            icon = '🚨'
        elif '⚠️' in str(status):
            css_class = 'warning'
            icon = '⚠️'
        elif '⏳' in str(status):
            css_class = 'pending'
            icon = '⏳'
        else:
            css_class = 'disponible'
            icon = '✅'
        
        with col:
            st.markdown(f"""
            <div class="{css_class}">
            <h4>{icon} {row.get('Member', 'N/A')} - {row.get('Vehicle', 'N/A')}</h4>
            <p><strong>Lugar:</strong> {row.get('Lugar', 'N/A')}</p>
            <p><strong>Pick up:</strong> {row.get('Pick up', 'N/A')} {row.get('Hora', '')}</p>
            <p><strong>Drop off:</strong> {row.get('Drop off', 'N/A')} {row.get('Hora.1', '')}</p>
            <p><strong>Entrega:</strong> {row.get('Entrega', 'N/A')}</p>
            <p><strong>Devolución:</strong> {row.get('Devolución', 'N/A')}</p>
            <p><strong>Próxima Reserva:</strong> <strong>{row.get('Próxima Reserva', 'Disponible')}</strong></p>
            {f'<p><strong>Feriado:</strong> 🎉 {row.get("Feriado (Nac)", "")}</p>' if row.get('Feriado (Nac)', '') else ''}
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# INFORMACIÓN GENERAL
# ============================================================

st.markdown("---")
st.subheader("ℹ️ Información")

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    **Fuente de Datos:**
    - Google Sheet: Bookings
    - Total de Registros: {len(df)}
    - Filtrados: {len(df_filtered)}
    - Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

with col2:
    st.warning("""
    **Notas importantes:**
    - Los datos se actualizan automáticamente cada 5 minutos
    - El Google Sheet debe ser público
    - Verifica que todas las columnas estén presentes (A-N)
    """)

# ============================================================
# EXPORTAR DATOS
# ============================================================

st.subheader("💾 Exportar Datos")

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Descargar CSV"):
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=f"reservas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📊 Descargar Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name='Reservas')
        st.download_button(
            label="Descargar Excel",
            data=buffer.getvalue(),
            file_name=f"reservas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "Dashboard de Reservas • © 2026 • Powered by Streamlit"
    "</div>",
    unsafe_allow_html=True
)
