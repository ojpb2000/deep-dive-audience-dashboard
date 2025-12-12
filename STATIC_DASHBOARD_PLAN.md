# 📋 Plan: Dashboard HTML Estático para GitHub Pages

## 🎯 Objetivo

Crear un dashboard HTML estático que:
- ✅ Se pueda publicar fácilmente en GitHub Pages
- ✅ Muestre todos los datos necesarios
- ✅ Sea interactivo (usando JavaScript)
- ✅ Use gráficos similares a los de Streamlit
- ✅ No requiera backend/servidor

## 🏗️ Arquitectura

```
CSV Data
    ↓
Python Script (generate_static_dashboard.py)
    ↓
HTML + JavaScript + JSON Data
    ↓
GitHub Pages (Hosting Estático)
    ↓
Dashboard Público
```

## 📁 Archivos a Crear

### 1. `generate_static_dashboard.py`
- Lee el CSV usando `data_parser.py`
- Procesa todos los datos
- Genera un archivo `index.html` con:
  - HTML estructura
  - CSS estilos
  - JavaScript para interactividad
  - Datos embebidos como JSON

### 2. `index.html` (generado)
- Dashboard completo en un solo archivo
- Usa Plotly.js para gráficos (similar a Plotly Python)
- Filtros interactivos con JavaScript
- Tabs para diferentes vistas de gráficos
- Insights automáticos

### 3. `.github/workflows/deploy.yml`
- Auto-genera el dashboard cuando haces push
- Auto-deploy a GitHub Pages
- Todo automático

## 🎨 Características del Dashboard

### Funcionalidades
- ✅ Filtros: Categoría, Sección, Ordenar por, Top N, Mínimo Index
- ✅ Gráficos: Comparación, Index Analysis, Scatter Plot
- ✅ Insights: Generados automáticamente
- ✅ Responsive: Funciona en móvil y desktop
- ✅ Interactivo: Sin necesidad de servidor

### Tecnologías
- **HTML5**: Estructura
- **CSS3**: Estilos modernos
- **JavaScript**: Interactividad
- **Plotly.js**: Gráficos interactivos (CDN)
- **JSON**: Datos embebidos

## 🚀 Flujo de Trabajo

### Desarrollo Local
```bash
# 1. Generar dashboard
python generate_static_dashboard.py

# 2. Abrir en navegador
# Abre index.html en tu navegador
```

### Deployment a GitHub Pages

**Opción 1: Manual**
1. Genera `index.html` localmente
2. Sube `index.html` a GitHub
3. Activa GitHub Pages en settings
4. ¡Listo!

**Opción 2: Automático (GitHub Actions)**
1. Push código a GitHub
2. GitHub Actions genera `index.html` automáticamente
3. GitHub Pages se actualiza automáticamente
4. ¡Todo automático!

## 📊 Datos Incluidos

El dashboard incluirá:
- ✅ Todas las secciones con datos válidos
- ✅ Preguntas asociadas a cada sección
- ✅ Items con Index, Target %, Control %, Diferencia
- ✅ Categorías organizadas
- ✅ Metadata (target group, control group, data source)

## 🎯 Ventajas de este Enfoque

✅ **GitHub Pages**: Gratis, fácil, automático
✅ **Sin Backend**: Todo estático, carga rápido
✅ **Control Total**: Tienes control completo del código
✅ **Fácil de Compartir**: Solo compartes la URL
✅ **Versionado**: Todo en GitHub con historial
✅ **Sin Límites**: GitHub Pages es generoso con el ancho de banda

## ⚠️ Limitaciones vs Streamlit

- ❌ No hay actualización en tiempo real (necesitas regenerar HTML)
- ❌ No hay sesiones de usuario (todo es cliente)
- ❌ Datos embebidos en HTML (archivo puede ser grande)
- ✅ Pero: Funciona perfectamente para visualización estática

## 📝 Checklist de Implementación

- [x] Crear `generate_static_dashboard.py`
- [x] Crear template HTML con JavaScript
- [x] Integrar Plotly.js para gráficos
- [x] Crear sistema de filtros
- [x] Generar insights automáticos
- [x] Crear GitHub Actions workflow
- [ ] Probar generación local
- [ ] Subir a GitHub
- [ ] Activar GitHub Pages
- [ ] Verificar funcionamiento

## 🔄 Actualización de Datos

Cuando tengas nuevos datos:
1. Reemplaza el CSV
2. Ejecuta `python generate_static_dashboard.py`
3. Commit y push `index.html`
4. GitHub Pages se actualiza automáticamente

O usa GitHub Actions para que sea automático.

