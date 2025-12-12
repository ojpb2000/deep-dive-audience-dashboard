# 📦 Guía para Subir Proyecto a GitHub

## 🚀 Pasos para Subir el Proyecto

### Paso 1: Inicializar Git (si no está inicializado)

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
git init
```

### Paso 2: Agregar el Remote de GitHub

```bash
git remote add origin https://github.com/ojpb2000/deep-divers-yougov.git
```

### Paso 3: Agregar todos los archivos

```bash
git add .
```

### Paso 4: Hacer el primer commit

```bash
git commit -m "Initial commit: Hilton Deep Divers Dashboard with AI Insights"
```

### Paso 5: Subir a GitHub

```bash
git branch -M main
git push -u origin main
```

Si GitHub te pide autenticación, puedes usar:
- **Personal Access Token** (recomendado)
- O configurar SSH keys

## 🔐 Configurar Autenticación de GitHub

### Opción A: Personal Access Token (Más fácil)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Selecciona permisos: `repo` (acceso completo a repositorios)
4. Copia el token generado
5. Cuando hagas `git push`, usa tu username y el token como password

### Opción B: SSH Keys

```bash
# Generar SSH key (si no tienes una)
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Copiar la clave pública
cat ~/.ssh/id_ed25519.pub

# Agregar la clave en GitHub → Settings → SSH and GPG keys
```

## 📋 Archivos que se Subirán

El `.gitignore` está configurado para excluir:
- Archivos temporales de Python (`__pycache__/`)
- Entornos virtuales (`venv/`, `env/`)
- Archivos del IDE (`.vscode/`, `.idea/`)
- Logs y archivos temporales

**Archivos importantes que SÍ se subirán:**
- ✅ `app.py`
- ✅ `data_parser.py`
- ✅ `requirements.txt`
- ✅ `.replit`
- ✅ `replit.nix`
- ✅ `.streamlit/config.toml`
- ✅ `Various_HIlton - Deep DiversvsNationally representative.csv`
- ✅ `README.md`
- ✅ Todos los archivos de documentación

## ⚠️ Nota sobre GitHub Pages

**GitHub Pages NO puede hostear aplicaciones Streamlit directamente** porque:
- GitHub Pages solo sirve sitios estáticos (HTML, CSS, JS)
- Streamlit necesita un servidor Python ejecutándose
- Streamlit es una aplicación monolítica (frontend + backend integrados)

### Arquitectura Recomendada: GitHub + Replit

**Opción Recomendada:**
```
GitHub (Repositorio) → Replit (Hosting) → Dashboard Público
```

1. **GitHub**: Almacena el código versionado
2. **Replit**: Importa desde GitHub y hostea la aplicación completa
3. **Dashboard**: Disponible en el webview de Replit

Ver `REPLIT_GITHUB_SETUP.md` para instrucciones detalladas.

### Alternativas para Publicar el Dashboard:

#### Opción 1: Streamlit Community Cloud (⭐ RECOMENDADO - Gratis)

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu repositorio de GitHub
3. Selecciona el branch `main`
4. Archivo principal: `app.py`
5. Click "Deploy"
6. ¡Listo! Tu dashboard estará en una URL pública

#### Opción 2: Replit (Ya configurado)

- Ya tienes todos los archivos listos para Replit
- Solo sube el proyecto y haz click en "Run"

#### Opción 3: Railway / Render / Fly.io

Plataformas que pueden hostear aplicaciones Python:
- [Railway](https://railway.app) - Gratis con límites
- [Render](https://render.com) - Gratis con límites
- [Fly.io](https://fly.io) - Gratis con límites

## 🔄 Comandos Rápidos para Futuros Cambios

```bash
# Ver estado de cambios
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push
```

## 📝 README.md para GitHub

Asegúrate de tener un buen README.md. Si quieres, puedo ayudarte a crear uno profesional.

## ✅ Checklist Pre-Push

- [ ] `.gitignore` creado
- [ ] Archivos importantes agregados
- [ ] Remote de GitHub configurado
- [ ] Autenticación configurada (Token o SSH)
- [ ] README.md actualizado (opcional pero recomendado)

## 🎯 Siguiente Paso Después de Subir

Una vez que el proyecto esté en GitHub:

1. **Streamlit Community Cloud**: Conecta el repo y deploya automáticamente
2. **Replit**: Importa desde GitHub
3. **Otras plataformas**: Sigue sus guías de deployment

