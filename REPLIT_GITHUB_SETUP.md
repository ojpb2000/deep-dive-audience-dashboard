# 🔗 Configurar Replit con GitHub como Repositorio

## 📋 Arquitectura Recomendada

```
GitHub (Repositorio de Código)
    ↓
Replit (Importa y Hostea la Aplicación)
    ↓
Dashboard Público (URL de Replit)
```

**Ventajas:**
- ✅ Código versionado en GitHub
- ✅ Replit hostea la aplicación completa
- ✅ Actualizaciones automáticas desde GitHub
- ✅ Fácil colaboración

## 🚀 Pasos para Configurar

### Paso 1: Subir Código a GitHub

Primero, asegúrate de que tu código esté en GitHub:

```bash
# Si aún no lo has subido
git init
git remote add origin https://github.com/ojpb2000/deep-divers-yougov.git
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

### Paso 2: Importar desde GitHub en Replit

1. **Ve a Replit**: https://replit.com
2. **Click en "Create Repl"**
3. **Selecciona "Import from GitHub"**
4. **Ingresa la URL de tu repositorio**:
   ```
   https://github.com/ojpb2000/deep-divers-yougov.git
   ```
5. **Click "Import"**

### Paso 3: Configurar Replit

Replit automáticamente:
- ✅ Detectará que es un proyecto Python
- ✅ Instalará dependencias desde `requirements.txt`
- ✅ Usará el archivo `.replit` para configurar el comando de ejecución

### Paso 4: Ejecutar la Aplicación

1. **Click en "Run"** en Replit
2. El dashboard se ejecutará automáticamente
3. **Accede al dashboard** en el webview de Replit

### Paso 5: Configurar Auto-Sync con GitHub (Opcional)

Para que Replit se actualice automáticamente cuando hagas cambios en GitHub:

1. En Replit, ve a **"Version Control"** (panel izquierdo)
2. Click en **"Connect to Git"**
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio: `ojpb2000/deep-divers-yougov`
5. Replit se sincronizará automáticamente

## 🔄 Flujo de Trabajo Recomendado

### Desarrollo Local → GitHub → Replit

```bash
# 1. Hacer cambios localmente
# (editar archivos en tu computadora)

# 2. Subir cambios a GitHub
git add .
git commit -m "Descripción de cambios"
git push

# 3. En Replit, hacer "Pull" para obtener cambios
# O configurar auto-sync para que se actualice automáticamente
```

### O: Desarrollo Directo en Replit → GitHub

1. **Editar código directamente en Replit**
2. **Hacer commit y push desde Replit**:
   - Ve a "Version Control"
   - Click "Commit & push"
   - Los cambios se guardan en GitHub

## 📁 Archivos Importantes

Asegúrate de que estos archivos estén en GitHub:

- ✅ `.replit` - Configuración de Replit
- ✅ `replit.nix` - Dependencias del sistema
- ✅ `requirements.txt` - Dependencias Python
- ✅ `.streamlit/config.toml` - Configuración Streamlit
- ✅ `app.py` - Aplicación principal
- ✅ `data_parser.py` - Parser de datos
- ✅ `Various_HIlton - Deep DiversvsNationally representative.csv` - Datos

## 🔐 Configuración de Secretos (Si es necesario)

Si en el futuro necesitas variables de entorno:

1. En Replit, ve a **"Secrets"** (🔒 icono)
2. Agrega variables como:
   - `STREAMLIT_SERVER_PORT=8080`
   - `STREAMLIT_SERVER_ADDRESS=0.0.0.0`

## 🌐 Hacer el Dashboard Público en Replit

### Opción 1: Webview de Replit (Gratis)
- El dashboard está disponible en el webview de Replit
- Solo tú puedes acceder (requiere login)

### Opción 2: Replit Deployments (Requiere cuenta Pro)
1. Click en "Deploy" en Replit
2. Configura el deployment
3. Obtendrás una URL pública

### Opción 3: Streamlit Community Cloud (⭐ Recomendado - Gratis)
- Conecta GitHub directamente
- URL pública automática
- Ver `GITHUB_SETUP.md` para instrucciones

## ⚠️ Nota sobre "Frontend y Backend"

**Streamlit es una aplicación monolítica:**
- No se puede separar frontend y backend
- El frontend (UI) y backend (lógica Python) están integrados
- Replit hostea TODO (frontend + backend juntos)

**Si necesitas separar frontend/backend:**
- Necesitarías reescribir la aplicación
- Frontend: React/Vue/HTML estático
- Backend: API Python (FastAPI/Flask)
- Esto es mucho más complejo y no es necesario para este proyecto

## ✅ Checklist

- [ ] Código subido a GitHub
- [ ] Replit importado desde GitHub
- [ ] Dependencias instaladas automáticamente
- [ ] Dashboard ejecutándose en Replit
- [ ] (Opcional) Auto-sync configurado
- [ ] (Opcional) Deployment público configurado

## 🎯 Resultado Final

Tendrás:
- **GitHub**: Código versionado y accesible
- **Replit**: Aplicación hosteada y ejecutándose
- **Dashboard**: Disponible en el webview de Replit

## 📚 Recursos Adicionales

- [Replit Docs](https://docs.replit.com)
- [Replit + GitHub Integration](https://docs.replit.com/version-control/connecting-github)

