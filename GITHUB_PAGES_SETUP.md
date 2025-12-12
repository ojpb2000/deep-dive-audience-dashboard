# 🚀 Configurar GitHub Pages

El código ya está en GitHub. Ahora necesitas activar GitHub Pages para publicar el dashboard.

## Pasos para Activar GitHub Pages

1. **Ve a tu repositorio en GitHub:**
   - https://github.com/ojpb2000/deep-dive-audience-dashboard

2. **Ve a Settings (Configuración):**
   - Haz clic en la pestaña "Settings" en la parte superior del repositorio

3. **Navega a Pages:**
   - En el menú lateral izquierdo, busca y haz clic en "Pages"

4. **Configura la fuente:**
   - En "Source", selecciona:
     - **Branch**: `main`
     - **Folder**: `/ (root)`
   - Haz clic en "Save"

5. **Espera la publicación:**
   - GitHub procesará tu sitio (puede tomar 1-2 minutos)
   - Verás un mensaje verde con la URL de tu sitio publicado
   - La URL será: `https://ojpb2000.github.io/deep-dive-audience-dashboard/`

## ✅ Verificación

Una vez activado, puedes:
- Acceder al dashboard en la URL proporcionada
- Compartir el enlace con tu equipo
- El dashboard se actualizará automáticamente cada vez que hagas push a la rama `main`

## 📝 Notas

- El archivo `index.html` está en la raíz del repositorio, por eso seleccionamos `/ (root)` como carpeta
- Si necesitas actualizar el dashboard, simplemente ejecuta `python generate_static_dashboard.py` y haz push de los cambios
- GitHub Pages es gratuito para repositorios públicos

## 🔧 Actualizar el Dashboard

Si necesitas regenerar el dashboard con nuevos datos:

```bash
# 1. Regenerar el HTML
python generate_static_dashboard.py

# 2. Hacer commit y push
git add index.html
git commit -m "Update dashboard"
git push origin main
```

GitHub Pages se actualizará automáticamente en unos minutos.

