# 🌵 Nopal Detector - Variables de Entorno

Esta guía explica todas las variables de entorno disponibles en Nopal Detector y cómo configurarlas.

## 📋 Tabla de Contenidos
- [Configuración Inicial](#configuración-inicial)
- [Variables Requeridas](#variables-requeridas)
- [Variables Opcionales](#variables-opcionales)
- [Ejemplos de Configuración](#ejemplos-de-configuración)
- [Solución de Problemas](#solución-de-problemas)

## Configuración Inicial

### 1. Crear archivo .env
```bash
cp .env.example .env
```

### 2. Editar el archivo
```bash
nano .env  # o usa tu editor favorito
```

### 3. Verificar configuración
```bash
make check-env
```

## Variables Requeridas

### 🔐 ROBOFLOW_API_KEY
**Descripción:** Tu API key de Roboflow para acceder a datasets.

**Requerido:** ✅ Sí (solo si usas Roboflow)

**Dónde obtenerla:**
1. Ve a [roboflow.com](https://roboflow.com)
2. Inicia sesión o crea una cuenta
3. Ve a Settings → API Keys
4. Copia tu Private API Key

**Ejemplo:**
```bash
ROBOFLOW_API_KEY=mZzyyugougnFyIob21zi
```

**Notas:**
- ⚠️ NUNCA compartas esta clave públicamente
- ⚠️ NO la subas a Git (ya está en .gitignore)
- Si trabajas sin Roboflow, puedes dejarla vacía

---

### 🏢 ROBOFLOW_WORKSPACE
**Descripción:** Nombre de tu workspace en Roboflow.

**Requerido:** ✅ Sí (si usas ROBOFLOW_API_KEY)

**Formato:** Texto sin espacios

**Ejemplo:**
```bash
ROBOFLOW_WORKSPACE=nopaldetector
```

**Cómo encontrarlo:**
- En la URL de tu proyecto: `roboflow.com/[workspace]/[project]`
- El primer segmento después del dominio es tu workspace

---

### 📦 ROBOFLOW_PROJECT
**Descripción:** Nombre de tu proyecto en Roboflow.

**Requerido:** ✅ Sí (si usas ROBOFLOW_API_KEY)

**Formato:** Texto con guiones (slug)

**Ejemplo:**
```bash
ROBOFLOW_PROJECT=nopal-detector-0lzvl
```

**Cómo encontrarlo:**
- En la URL de tu proyecto: `roboflow.com/[workspace]/[project]`
- El segundo segmento es el nombre del proyecto

---

### 🔢 ROBOFLOW_VERSION
**Descripción:** Versión del dataset a descargar.

**Requerido:** ✅ Sí (si usas ROBOFLOW_API_KEY)

**Formato:** Número entero positivo

**Ejemplo:**
```bash
ROBOFLOW_VERSION=4
```

**Notas:**
- Cada vez que generas un nuevo dataset en Roboflow, se incrementa la versión
- Usa la versión más reciente para obtener las últimas mejoras

---

## Variables Opcionales

### 🎯 MODEL_CONFIDENCE_THRESHOLD
**Descripción:** Umbral mínimo de confianza para aceptar una detección.

**Requerido:** ❌ No (default: 0.3)

**Rango:** 0.0 a 1.0

**Valores recomendados:**
- `0.3` - Detección general (muchas detecciones, más falsos positivos)
- `0.5` - Balance entre precisión y recall ⭐ **Recomendado**
- `0.7` - Alta precisión (menos falsos positivos)
- `0.9` - Muy estricto (solo detecciones muy seguras)

**Ejemplo:**
```bash
MODEL_CONFIDENCE_THRESHOLD=0.5
```

**Impacto:**
- ⬆️ Valor más alto → Menos detecciones, más precisión
- ⬇️ Valor más bajo → Más detecciones, menos precisión

---

### 🔲 MODEL_IOU_THRESHOLD
**Descripción:** Umbral de Intersection over Union para Non-Maximum Suppression (NMS).

**Requerido:** ❌ No (default: 0.5)

**Rango:** 0.0 a 1.0

**Valores recomendados:**
- `0.3` - Supresión agresiva (menos cajas superpuestas)
- `0.5` - Balance ⭐ **Recomendado**
- `0.7` - Supresión suave (más cajas pueden superponerse)

**Ejemplo:**
```bash
MODEL_IOU_THRESHOLD=0.5
```

**Impacto:**
- ⬆️ Valor más alto → Más cajas detectadas (menos supresión)
- ⬇️ Valor más bajo → Menos cajas detectadas (más supresión)

---

### 💻 DEVICE
**Descripción:** Dispositivo de hardware para ejecutar el modelo.

**Requerido:** ❌ No (default: cpu)

**Opciones:**
- `cpu` - CPU (compatible con todos los sistemas) ⭐ **Default**
- `cuda` - GPU NVIDIA (requiere CUDA Toolkit instalado)
- `mps` - GPU Apple Silicon M1/M2/M3 (requiere macOS 12.3+)

**Ejemplo:**
```bash
DEVICE=cpu
```

**Configuración por sistema:**

**macOS con Apple Silicon (M1/M2/M3):**
```bash
DEVICE=mps  # Más rápido que CPU
```

**Linux/Windows con NVIDIA GPU:**
```bash
DEVICE=cuda  # Requiere drivers CUDA
```

**Cualquier sistema sin GPU dedicada:**
```bash
DEVICE=cpu
```

---

### 📹 CAMERA_INDEX
**Descripción:** Índice de la cámara a usar para detección en tiempo real.

**Requerido:** ❌ No (default: 0)

**Formato:** Número entero (0, 1, 2, ...)

**Ejemplo:**
```bash
CAMERA_INDEX=0
```

**Notas:**
- `0` = Primera cámara (generalmente webcam integrada)
- `1` = Segunda cámara (cámara externa si está conectada)
- Usa `make list-cameras` para ver cámaras disponibles

---

### 🖼️ CAMERA_RESOLUTION
**Descripción:** Resolución de captura de la cámara.

**Requerido:** ❌ No (default: resolución de la cámara)

**Formato:** WIDTHxHEIGHT

**Ejemplos:**
```bash
CAMERA_RESOLUTION=640x480    # SD (rápido)
CAMERA_RESOLUTION=1280x720   # HD (balance)
CAMERA_RESOLUTION=1920x1080  # Full HD (mejor calidad, más lento)
```

**Recomendaciones:**
- Para detección rápida: `640x480`
- Para balance: `1280x720` ⭐ **Recomendado**
- Para mejor calidad: `1920x1080`

---

### ⏱️ FPS_TARGET
**Descripción:** FPS objetivo para procesamiento de video.

**Requerido:** ❌ No (default: 30)

**Formato:** Número entero

**Ejemplo:**
```bash
FPS_TARGET=30
```

---

### 📊 EPOCHS
**Descripción:** Número de épocas para entrenamiento.

**Requerido:** ❌ No (default: 100)

**Formato:** Número entero positivo

**Ejemplo:**
```bash
EPOCHS=100
```

**Recomendaciones:**
- Dataset pequeño: 50-100 épocas
- Dataset mediano: 100-200 épocas
- Dataset grande: 200-300 épocas

---

### 📦 BATCH_SIZE
**Descripción:** Tamaño del batch para entrenamiento.

**Requerido:** ❌ No (default: 16)

**Formato:** Número entero positivo

**Ejemplo:**
```bash
BATCH_SIZE=16
```

**Recomendaciones por RAM/VRAM:**
- 4-8 GB: `BATCH_SIZE=4`
- 8-16 GB: `BATCH_SIZE=8`
- 16-32 GB: `BATCH_SIZE=16` ⭐ **Recomendado**
- 32+ GB: `BATCH_SIZE=32`

---

### 📐 IMAGE_SIZE
**Descripción:** Tamaño de imagen para entrenamiento y detección.

**Requerido:** ❌ No (default: 640)

**Formato:** Número entero (múltiplo de 32)

**Ejemplos:**
```bash
IMAGE_SIZE=416   # Rápido, menos preciso
IMAGE_SIZE=640   # Balance ⭐ **Recomendado**
IMAGE_SIZE=1280  # Lento, más preciso
```

---

### 🛑 PATIENCE
**Descripción:** Paciencia para early stopping durante entrenamiento.

**Requerido:** ❌ No (default: 50)

**Formato:** Número entero

**Ejemplo:**
```bash
PATIENCE=50
```

**Notas:**
- Detiene el entrenamiento si no hay mejora después de N épocas
- Previene overfitting

---

## Ejemplos de Configuración

### 🏠 Configuración Básica (Local CPU)
```bash
# .env
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4

MODEL_CONFIDENCE_THRESHOLD=0.5
MODEL_IOU_THRESHOLD=0.5
DEVICE=cpu
```

### 🚀 Configuración de Producción (GPU)
```bash
# .env
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4

MODEL_CONFIDENCE_THRESHOLD=0.7
MODEL_IOU_THRESHOLD=0.5
DEVICE=cuda  # o mps para Mac

# Entrenamiento optimizado
EPOCHS=200
BATCH_SIZE=32
IMAGE_SIZE=640
PATIENCE=100
```

### 🎥 Configuración para Cámara en Tiempo Real
```bash
# .env
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4

MODEL_CONFIDENCE_THRESHOLD=0.5
DEVICE=cuda  # Usar GPU para mejor rendimiento

CAMERA_INDEX=0
CAMERA_RESOLUTION=1280x720
FPS_TARGET=30
```

### 🔬 Configuración de Desarrollo/Testing
```bash
# .env
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4

# Umbrales relajados para testing
MODEL_CONFIDENCE_THRESHOLD=0.3
MODEL_IOU_THRESHOLD=0.5
DEVICE=cpu

# Entrenamiento rápido para pruebas
EPOCHS=10
BATCH_SIZE=8
PATIENCE=5
```

---

## Solución de Problemas

### ❌ Error: "ROBOFLOW_API_KEY no encontrada"
**Causa:** No has configurado el archivo .env

**Solución:**
```bash
cp .env.example .env
nano .env  # Añade tu API key
```

---

### ❌ Error: "No se pudo conectar a Roboflow"
**Causa:** API key inválida o problemas de red

**Solución:**
1. Verifica que tu API key sea correcta
2. Verifica tu conexión a internet
3. Comprueba que el workspace y project sean correctos

```bash
make check-env  # Verificar configuración
```

---

### ⚠️ Advertencia: "CUDA no disponible"
**Causa:** DEVICE=cuda pero no tienes CUDA instalado

**Solución:**
```bash
# Cambiar a CPU
DEVICE=cpu
```

O instalar CUDA Toolkit desde [nvidia.com](https://developer.nvidia.com/cuda-downloads)

---

### 🐌 Rendimiento lento
**Causa:** Configuración subóptima

**Soluciones:**
- Usar GPU si está disponible: `DEVICE=cuda` o `DEVICE=mps`
- Reducir resolución: `IMAGE_SIZE=416`
- Reducir batch size: `BATCH_SIZE=8`
- Ajustar resolución de cámara: `CAMERA_RESOLUTION=640x480`

---

### 🎯 Muchos falsos positivos
**Causa:** Umbral de confianza muy bajo

**Solución:**
```bash
# Aumentar umbral de confianza
MODEL_CONFIDENCE_THRESHOLD=0.7  # o más alto
```

---

### 🎯 No detecta objetos
**Causa:** Umbral de confianza muy alto

**Solución:**
```bash
# Reducir umbral de confianza
MODEL_CONFIDENCE_THRESHOLD=0.3  # o más bajo
```

---

## Verificar Configuración

Después de modificar tu `.env`, verifica la configuración:

```bash
make check-env
```

Esto mostrará:
- ✅ Versión de Python
- ✅ Paquetes instalados
- ✅ Estado del archivo .env
- ✅ Estado del entorno virtual

---

## Recursos Adicionales

- [Documentación de Roboflow](https://docs.roboflow.com/)
- [Documentación de Ultralytics YOLO](https://docs.ultralytics.com/)
- [README principal](../README.md)
- [Guía de instalación](../README.md#primeros-pasos-recomendado)

---

**Autor:** Carlos Boyzo  
**Proyecto:** Nopal Detector  
**GitHub:** [crbzxy/nopalDetector](https://github.com/crbzxy/nopalDetector)
