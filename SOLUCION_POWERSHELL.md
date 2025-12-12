# 🔧 Solución al Error de PowerShell

## ❌ Error que estás viendo:

```
No se puede cargar el archivo ...\Activate.ps1 porque la ejecución de scripts está deshabilitada
```

## ✅ Soluciones (elige una):

### Opción 1: Ejecutar desde CMD (no PowerShell)

1. Presiona `Win + R`
2. Escribe: `cmd` y presiona Enter
3. En CMD, ejecuta:
   ```cmd
   cd "C:\Users\oscar.perez\OneDrive - OneWorkplace\Documentos\2025\Hilton\Hilton - Deep Divers"
   python -m streamlit run app.py
   ```

### Opción 2: Usar el archivo .bat directamente

1. **Haz doble clic** en `EJECUTAR_AHORA.bat` desde el Explorador de Windows
2. Esto abrirá CMD (no PowerShell) y ejecutará el dashboard

### Opción 3: Cambiar la política de PowerShell (si necesitas PowerShell)

Abre PowerShell como **Administrador** y ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego cierra y vuelve a abrir PowerShell.

### Opción 4: Ejecutar directamente desde Cursor (Terminal CMD)

En Cursor, cambia la terminal a CMD:
1. Click en el dropdown de la terminal (donde dice "PowerShell")
2. Selecciona "Command Prompt" o "CMD"
3. Ejecuta:
   ```cmd
   cd "C:\Users\oscar.perez\OneDrive - OneWorkplace\Documentos\2025\Hilton\Hilton - Deep Divers"
   python -m streamlit run app.py
   ```

## 🎯 Recomendación

**La forma más fácil**: Haz doble clic en `EJECUTAR_AHORA.bat` desde el Explorador de Windows. Esto evitará completamente el problema de PowerShell.

