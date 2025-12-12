# 🚨 IMPORTANTE: Cómo Ejecutar Streamlit Correctamente

## ❌ NO usar Live Server

**Live Server** es para archivos HTML estáticos. **NO funciona con Streamlit**.

Streamlit es una **aplicación Python** que necesita ejecutarse como un servidor desde la terminal.

## ✅ Forma Correcta: Ejecutar desde Terminal

### Opción 1: Terminal Integrada de Cursor/VS Code

1. **Abre la terminal integrada**:
   - Presiona `` Ctrl + ` `` (backtick) 
   - O ve a: `Terminal` → `New Terminal`

2. **Navega al directorio del proyecto** (si no estás ahí):
   ```powershell
   cd "C:\Users\oscar.perez\OneDrive - OneWorkplace\Documentos\2025\Hilton\Hilton - Deep Divers"
   ```

3. **Ejecuta Streamlit**:
   ```bash
   streamlit run app.py
   ```
   
   O si no funciona, usa:
   ```bash
   python -m streamlit run app.py
   ```

4. **Espera a que aparezca**:
   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

5. **Abre tu navegador** en `http://localhost:8501`

### Opción 2: PowerShell/CMD Externa

1. Abre PowerShell o CMD
2. Navega al directorio:
   ```powershell
   cd "C:\Users\oscar.perez\OneDrive - OneWorkplace\Documentos\2025\Hilton\Hilton - Deep Divers"
   ```
3. Ejecuta:
   ```bash
   streamlit run app.py
   ```

### Opción 3: Desde Cursor (Run Command)

1. Presiona `Ctrl + Shift + P` (o `Cmd + Shift + P` en Mac)
2. Escribe: `Python: Run Python File in Terminal`
3. Selecciona `app.py`
4. Luego ejecuta: `streamlit run app.py` en la terminal

## 🔍 Verificar que Está Funcionando

Cuando Streamlit esté corriendo correctamente, verás en la terminal:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, install the watchdog Python package.
```

Y el dashboard se abrirá automáticamente en tu navegador.

## 🛑 Para Detener Streamlit

En la terminal donde está corriendo, presiona:
- `Ctrl + C` (Windows/Linux)
- `Cmd + C` (Mac)

## ❓ Solución de Problemas

### Error: "streamlit: command not found"
```bash
python -m streamlit run app.py
```

### Error: "Port 8501 already in use"
Cierra otras instancias de Streamlit o usa otro puerto:
```bash
streamlit run app.py --server.port 8502
```

### El navegador no se abre automáticamente
Abre manualmente: `http://localhost:8501`

### Error al importar módulos
```bash
pip install -r requirements.txt
```

## 📝 Diferencia Clave

| Live Server | Streamlit |
|------------|-----------|
| Para archivos HTML/CSS/JS estáticos | Para aplicaciones Python |
| Solo sirve archivos | Ejecuta código Python |
| No procesa datos | Procesa y visualiza datos |
| No funciona con `.py` | Requiere archivos `.py` |

## ✅ Checklist

- [ ] Terminal abierta en el directorio correcto
- [ ] Comando `streamlit run app.py` ejecutado
- [ ] Mensaje "You can now view..." aparece
- [ ] Navegador abierto en `http://localhost:8501`
- [ ] Dashboard se carga correctamente

