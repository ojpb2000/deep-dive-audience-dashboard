# 🚀 Guía de Deployment en Replit

## ✅ Archivos Necesarios (Ya están listos)

Todos los archivos necesarios ya están en el proyecto:

1. **`.replit`** ✅ - Configuración de Replit (ya existe)
   - Configurado para ejecutar Streamlit en puerto 8080
   
2. **`replit.nix`** ✅ - Configuración de dependencias del sistema (ya existe)
   - Python 3.11 configurado

3. **`requirements.txt`** ✅ - Dependencias de Python (ya existe)
   - streamlit==1.28.0
   - pandas==2.1.3
   - plotly==5.18.0
   - numpy==1.24.3

4. **`.streamlit/config.toml`** ✅ - Configuración de Streamlit (ya existe)
   - Puerto 8080
   - Address 0.0.0.0 (para Replit)

5. **`app.py`** ✅ - Aplicación principal (ya existe)

6. **`data_parser.py`** ✅ - Parser de datos (ya existe)

7. **`Various_HIlton - Deep DiversvsNationally representative.csv`** ✅ - Archivo de datos (ya existe)

## 📋 Pasos para Deployment en Replit

### Paso 1: Crear un nuevo Repl
1. Ve a [Replit](https://replit.com)
2. Inicia sesión o crea una cuenta
3. Click en "Create Repl"
4. Selecciona "Python" como lenguaje

### Paso 2: Subir archivos del proyecto

**Opción A: Subir archivos manualmente**
1. En Replit, click en "Files" (panel izquierdo)
2. Arrastra y suelta TODOS los archivos del proyecto:
   - `app.py`
   - `data_parser.py`
   - `requirements.txt`
   - `.replit`
   - `replit.nix`
   - `.streamlit/config.toml` (crea la carpeta `.streamlit` primero)
   - `Various_HIlton - Deep DiversvsNationally representative.csv`
   - `README.md` (opcional)

**Opción B: Usar Git (si tienes el proyecto en GitHub)**
1. En Replit, click en "Import from GitHub"
2. Ingresa la URL de tu repositorio
3. Replit importará todos los archivos automáticamente

### Paso 3: Verificar estructura de archivos

Asegúrate de que la estructura sea:
```
.
├── app.py
├── data_parser.py
├── requirements.txt
├── .replit
├── replit.nix
├── .streamlit/
│   └── config.toml
├── Various_HIlton - Deep DiversvsNationally representative.csv
└── README.md (opcional)
```

### Paso 4: Instalar dependencias

Replit debería instalar automáticamente las dependencias desde `requirements.txt` cuando ejecutes el proyecto.

Si no se instalan automáticamente:
1. Abre la consola (Shell) en Replit
2. Ejecuta: `pip install -r requirements.txt`

### Paso 5: Ejecutar el dashboard

1. Click en el botón **"Run"** (arriba en Replit)
2. Replit ejecutará automáticamente: `streamlit run app.py --server.port 8080 --server.address 0.0.0.0`
3. El dashboard se abrirá en el panel webview de Replit

### Paso 6: Acceder al dashboard

- El dashboard estará disponible en el webview de Replit
- También puedes acceder desde la URL que aparece en la consola
- Replit generará una URL pública si tienes cuenta Pro, o puedes usar el webview integrado

## 🔧 Configuración Actual

### `.replit`
```
language = "python3"
run = "streamlit run app.py --server.port 8080 --server.address 0.0.0.0"
```

### `.streamlit/config.toml`
```
[server]
port = 8080
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false
```

## ⚠️ Notas Importantes

1. **Archivo CSV**: Asegúrate de que el nombre del archivo CSV sea exactamente:
   `Various_HIlton - Deep DiversvsNationally representative.csv`
   (con mayúsculas y espacios exactos)

2. **Puerto**: El puerto 8080 está configurado. Si hay conflictos, Replit te avisará.

3. **Memoria**: El dataset es grande (1285 filas). Replit debería manejarlo bien, pero si hay problemas de memoria, considera optimizar el parser.

4. **Tiempo de carga**: La primera carga puede tardar unos segundos mientras se parsea el CSV.

## 🐛 Troubleshooting

### Error: "File not found"
- Verifica que el CSV esté en la raíz del proyecto
- Verifica que el nombre del archivo sea exacto (case-sensitive)

### Error: "Module not found"
- Ejecuta: `pip install -r requirements.txt` en la consola de Replit

### Error: "Port already in use"
- Cambia el puerto en `.replit` y `.streamlit/config.toml` a otro número (ej: 8081)

### El dashboard no carga
- Revisa la consola de Replit para ver errores
- Verifica que todos los archivos estén subidos correctamente

## ✅ Checklist Pre-Deployment

- [x] `.replit` configurado
- [x] `replit.nix` configurado
- [x] `requirements.txt` con todas las dependencias
- [x] `.streamlit/config.toml` configurado para Replit
- [x] `app.py` sin errores de sintaxis
- [x] `data_parser.py` sin errores
- [x] Archivo CSV en la raíz del proyecto
- [x] Botones de navegación configurados correctamente

## 🎉 ¡Listo para Deploy!

Una vez que subas todos los archivos a Replit y hagas click en "Run", el dashboard debería funcionar automáticamente.

