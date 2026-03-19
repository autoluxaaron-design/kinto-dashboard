# 🚗 Dashboard de Reservas - Instrucciones de Uso

## 📋 ¿Qué es esto?
Una aplicación web interactiva que **lee datos en tiempo real** de tu Google Sheet de reservas y los muestra en un dashboard visualmente atractivo con filtros, alertas y códigos de color.

---

## ⚡ Inicio Rápido

### **Paso 1: Abrir el archivo**
1. Abre el archivo **`index.html`** con cualquier navegador web (Chrome, Firefox, Edge, Safari, etc.)
2. **¡Listo!** La aplicación cargará automáticamente los datos de tu Google Sheet.

### **Paso 2: Usa los filtros**
- 📍 **Lugar**: Filtra por "Salta", "Aeropuerto" o todos
- 🚙 **Vehículo**: Selecciona un vehículo específico
- ⚠️ **Estado Próxima Reserva**: Filtra por urgencia (URGENTE, Advertencia, etc.)
- 🔍 **Buscar Miembro**: Escribe el nombre del miembro
- 🔄 **Limpiar Filtros**: Restablece todos los filtros

---

## 🎨 Características Principales

### **Códigos de Color**
- 🔵 **Borde/Fondo Azul Claro** = Lugar: Salta
- 🟢 **Borde/Fondo Verde Claro** = Lugar: Aeropuerto
- 🔴 **Borde Rojo + Alerta** = Próxima Reserva: URGENTE

### **Alertas de Estado**
La tarjeta muestra la columna **"Próxima Reserva"** con código de colores:
- 🚨 **Rojo** = "URGENTE" 
- 🟡 **Amarillo** = "⚠️" (Advertencia)
- 🟠 **Naranja** = "⏳" (Pendiente)
- 🟢 **Verde** = "✅ Disponible"

### **Información de Feriados**
- Si la columna "Feriado (Nac)" tiene datos, aparecerá un icono 🎉 en la tarjeta
- Pasa el mouse sobre el icono para ver el detalle del feriado

### **Período de Reserva**
Muestra claramente:
- Fecha y hora de **Pick up** (Recogida)
- Fecha y hora de **Drop off** (Devolución)

### **Procesos**
Muestra el estado de:
- ✅ **Entrega** (con emojis y estado del sheet)
- 🔄 **Devolución** (con emojis y estado del sheet)

### **Barra de Estadísticas**
En la parte superior, ves el conteo en tiempo real:
- Cantidad de reservas **URGENTES**
- Cantidad con **ADVERTENCIAS**
- Cantidad **PENDIENTES**
- Cantidad **DISPONIBLES**

---

## 🔗 Conexión con Google Sheets

### **URL del Google Sheet**
La aplicación se conecta automáticamente a:
```
https://docs.google.com/spreadsheets/d/1pbgu_CAaeFcd06-E_DkgOihvCLTzAsM276bOu69rrxQ/
```

**Pestaña (Sheet):** `Bookings`

### **Estructura de Datos Esperada**
La aplicación lee las **Columnas A a N**:
| Col | Nombre | Contenido |
|-----|--------|-----------|
| A | ID | Identificador de reserva |
| B | Member | Nombre del miembro |
| C | Vehicle | Modelo del vehículo |
| D | Lugar | "Salta" o "Aeropuerto" |
| E | Pick up | Fecha de recogida |
| F | Hora | Hora de recogida |
| G | Drop off | Fecha de devolución |
| H | Hora | Hora de devolución |
| I | Entrega | Estado con emojis (ej: "✅ En uso") |
| J | Devolución | Estado con emojis (ej: "⏳ 2 días") |
| K | Día Ent | Día de entrega |
| L | Día Dev | Día de devolución |
| M | Próxima Reserva | **CRÍTICA** - Estados con emojis (ej: "🚨 URGENTE") |
| N | Feriado (Nac) | Texto de alerta (ej: "FERIADO Pick up: Viernes Santo") |

---

## 🚀 Características Técnicas

### **Tecnología Usada**
- ✅ **HTML5** + **CSS3** + **JavaScript** moderno
- ✅ **PapaParse** (librería para parsear CSV)
- ✅ **Google Sheets CSV Export** (sin necesidad de API key)
- ✅ **Responsive** (funciona en móvil, tablet y escritorio)

### **Ventajas**
- 📱 **Funciona en cualquier navegador**
- 🔄 **Datos en tiempo real** (cada recarga obtiene los últimos datos)
- 🎨 **Diseño moderno y profesional**
- ⚡ **Carga rápida** (archivo HTML estático)
- 📦 **Sin instalación** - Solo abre el archivo
- 🔐 **Sin backend** - Todo ocurre en tu navegador

---

## ⚠️ Solución de Problemas

### **"Error al cargar los datos"**

**Problema 1: Google Sheet no es público**
- Ve a tu Google Sheet → Compartir → Cualquiera con el enlace puede ver
- Asegúrate que la opción sea **"Viewer"** (Visualizador)

**Problema 2: URL del Sheet es incorrecta**
- Verifica que el ID del sheet (`1pbgu_CAaeFcd06...`) sea correcto
- La app usa este ID para generar la URL CSV automáticamente

**Problema 3: La pestaña no se llama "Bookings"**
- Si tu pestaña tiene otro nombre, [contacta para actualizar](mailto:soporte@)
- O edita el archivo `index.html` y busca `SHEET_GID = '0'` para cambiar el ID de la pestaña

### **"No aparecen datos"**
- Recarga la página (Ctrl+R o Cmd+R)
- Verifica que el Google Sheet tenga datos en las columnas A-N
- Abre la consola del navegador (F12) para ver mensajes de error

### **Los filtros no funcionan bien**
- Asegúrate que los datos en el Sheet estén escritos exactamente igual:
  - "Salta" (no "salta", no "SALTA")
  - "Aeropuerto" (no "aeropuerto")
  - Emojis deben estar presentes (ej: "🚨 URGENTE")

---

## 🎯 Personalización

Si necesitas cambiar algo, abre el archivo `index.html` con un editor de texto y busca:

- **Colores**: Sección `<style>` (búsqueda: `#667eea`, `#4dd0e1`, etc.)
- **URL del Sheet**: Línea con `GOOGLE_SHEET_ID = '1pbgu_CAaeFcd06...'`
- **Título o textos**: Sección `<body>` o dentro del JavaScript

---

## 📞 Soporte

Si algo no funciona:
1. Verifica que el archivo esté guardado como `index.html` (.html, no .txt)
2. Intenta abrir con otro navegador
3. Recarga la página (Ctrl+R)
4. Si persiste, revisa la consola del navegador (F12 → Pestaña "Console")

---

## ✨ ¡Disfruta tu Dashboard!

La aplicación se actualiza automáticamente cada vez que recargas la página, reflejando los cambios en tu Google Sheet. 

**¡Manos a la obra!** 🚀
