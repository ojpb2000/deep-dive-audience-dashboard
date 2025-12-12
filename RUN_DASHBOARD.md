# 🚀 Cómo Ejecutar el Dashboard Localmente

## ✅ Validación Completada

Todas las validaciones pasaron exitosamente:
- ✅ Todas las dependencias instaladas
- ✅ Parser funciona correctamente (51 secciones)
- ✅ Todas las columnas requeridas presentes
- ✅ Sin errores de importación

## 📋 Pasos para Ejecutar

### Opción 1: Ejecutar desde Terminal

1. **Abre una terminal/PowerShell** en el directorio del proyecto:
   ```powershell
   cd "C:\Users\oscar.perez\OneDrive - OneWorkplace\Documentos\2025\Hilton\Hilton - Deep Divers"
   ```

2. **Ejecuta el dashboard**:
   ```bash
   streamlit run app.py
   ```

3. **Abre tu navegador**:
   - El dashboard debería abrirse automáticamente
   - Si no, ve a: `http://localhost:8501`

### Opción 2: Ejecutar desde VS Code / Cursor

1. Abre el archivo `app.py`
2. Haz clic derecho → "Run Python File in Terminal"
3. O usa la terminal integrada y ejecuta: `streamlit run app.py`

## 🎯 Qué Verificar Cuando el Dashboard Esté Corriendo

### 1. Carga Inicial
- [ ] El dashboard carga sin errores
- [ ] Se muestra el header "Hilton Deep Divers Analytics Dashboard"
- [ ] El sidebar aparece con los filtros

### 2. Navegación
- [ ] Puedes seleccionar una categoría del dropdown
- [ ] Puedes seleccionar una sección
- [ ] Los filtros (Top N, Index mínimo) funcionan

### 3. Visualizaciones
- [ ] **Tab 1 - Comparison Chart**: Muestra gráficos de barras comparando Target vs Control
- [ ] **Tab 2 - Index Analysis**: Muestra gráfico de barras horizontales con colores
- [ ] **Tab 3 - Scatter Plot**: Muestra gráfico de dispersión
- [ ] **Tab 4 - Data Table**: Muestra tabla con datos

### 4. Funcionalidades
- [ ] Las métricas se calculan correctamente (High Affinity Items, Average Index, etc.)
- [ ] Los insights se generan automáticamente
- [ ] El botón de descarga CSV funciona
- [ ] Los gráficos son interactivos (hover, zoom, etc.)

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "File not found" (CSV)
- Verifica que el archivo `Various_HIlton - Deep DiversvsNationally representative.csv` está en el mismo directorio que `app.py`

### Error: "Port already in use"
- Cierra otras instancias de Streamlit
- O usa otro puerto: `streamlit run app.py --server.port 8502`

### El dashboard no se abre automáticamente
- Abre manualmente: `http://localhost:8501`
- Verifica que no hay un firewall bloqueando

## 📊 Datos Esperados

Cuando el dashboard funcione correctamente, deberías ver:
- **51 secciones** disponibles para análisis
- **4 categorías** principales:
  - Travel & Hospitality
  - Lifestyle & Interests
  - Sports & Entertainment
  - Brands & Products

## ✨ Características a Probar

1. **Filtros**:
   - Cambia la categoría y verifica que las secciones se actualizan
   - Ajusta el slider de "Top N" y verifica que los gráficos cambian
   - Cambia el "Minimum Index" y verifica el filtrado

2. **Gráficos**:
   - Haz hover sobre los gráficos para ver tooltips
   - Prueba hacer zoom en los gráficos de Plotly
   - Cambia entre las diferentes métricas (Index, Target %, Difference)

3. **Insights**:
   - Verifica que los insights se generan para cada sección
   - Revisa que los números en los insights coinciden con los datos

4. **Exportación**:
   - Prueba descargar datos filtrados como CSV
   - Verifica que el archivo descargado tiene los datos correctos

## 🎉 Siguiente Paso

Una vez que hayas verificado que todo funciona localmente, el siguiente paso es:
- **Deploy en Replit** siguiendo las instrucciones en `DEPLOYMENT_GUIDE.md`

