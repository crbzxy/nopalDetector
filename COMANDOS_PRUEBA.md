# 🧪 Comandos de Prueba - Nopal Detector

**Basado en pruebas reales realizadas el 7 de octubre de 2025**

## ✅ Comandos que SÍ funcionan

### 🎥 Detección con Cámara (RECOMENDADO)
```bash
# Comando principal probado:
source venv/bin/activate && python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt

# Alternativa con cámara 0:
source venv/bin/activate && python main.py --mode camera --camera 0 --weights runs/detect/train/weights/best.pt
```

**Resultados de prueba:**
- ✅ Procesó 1353 frames sin errores
- ✅ Controles interactivos funcionando
- ✅ Filtros de precisión operativos
- ✅ Sistema de fallback automático

### 📊 Verificación del Sistema
```bash
# Comando de diagnóstico:
python verify_setup.py
```

**Resultado esperado:**
```
🎉 ¡CONFIGURACIÓN EXITOSA!
✅ Todos los componentes críticos están listos
```

## ❌ Comandos que NO funcionan

### ⚠️ Comando incompleto
```bash
# ESTO FALLA:
python main.py --mode camera
```

**Error:**
```
❌ Error: Se requieren pesos del modelo para detección en cámara
Uso: python main.py --mode camera --weights models/weights/best_nopal.pt
```

### ⚠️ Ruta incorrecta de modelo
```bash
# ESTO FALLA:
python main.py --mode camera --weights models/weights/best_nopal.pt
```

**Error:**
```
❌ Error cargando modelos: [Errno 2] No such file or directory: 'models/weights/best_nopal.pt'
```

## 🔧 Soluciones a Problemas Comunes

### Problema: "Error leyendo frame de la cámara"
**Síntomas:**
```
⚠️ Error leyendo frame de la cámara (intento 1/5)
⚠️ Error leyendo frame de la cámara (intento 2/5)
🔄 Intentando reconectar cámara...
❌ No se pudo reconectar la cámara
```

**Solución:**
1. Cerrar otras apps que usen la cámara (Zoom, Teams, etc.)
2. Cambiar de cámara 1 a cámara 0 o viceversa
3. Reiniciar el comando

### Problema: Crash de Python
**Comando que crashea:**
```bash
source venv/bin/activate && py
```

**Solución:** Usar `python` en lugar de `py`:
```bash
source venv/bin/activate && python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt
```

## 📈 Estadísticas de Rendimiento

### Prueba 1: Comando incompleto
- **Comando:** `python main.py --mode camera --weights models/weights/best_nopal.pt`
- **Resultado:** 69 frames procesados, modelo fallback usado
- **Estado:** ⚠️ Funcional pero subóptimo

### Prueba 2: Comando completo
- **Comando:** `python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt`
- **Resultado:** 141 frames procesados antes de problema de cámara
- **Estado:** ✅ Óptimo hasta desconexión externa

### Prueba 3: Comando corregido
- **Comando:** `python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt`
- **Resultado:** 1353 frames procesados sin errores
- **Estado:** ✅ Completamente funcional

## 🎯 Comando Recomendado Final

```bash
# ESTE ES EL COMANDO QUE SIEMPRE FUNCIONA:
source venv/bin/activate && python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt
```

**Características:**
- ✅ Usa modelo entrenado completo
- ✅ Especifica cámara explícitamente  
- ✅ Incluye todos los parámetros requeridos
- ✅ Activación de entorno incluida
- ✅ Probado con 1353 frames exitosos

## 🚨 Comandos de Emergencia

Si nada funciona, ejecuta en orden:

```bash
# 1. Verificar estado
python verify_setup.py

# 2. Si falla, reinstalar
rm -rf venv/
./setup.sh

# 3. Verificar nuevamente
python verify_setup.py

# 4. Usar comando principal
source venv/bin/activate && python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt
```

---
**Actualizado:** 7 de octubre de 2025  
**Pruebas realizadas en:** macOS con Python 3.9.6