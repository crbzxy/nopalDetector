# 🚀 Guía de Inicio Rápido - Nopal Detector

**¡Bienvenido! Esta guía te ayudará a usar el detector de nopales en menos de 5 minutos.**

## 🎯 ¿Qué Vas a Lograr?

Al final de esta guía podrás:
- ✅ Detectar nopales usando tu cámara web en tiempo real
- ✅ Procesar imágenes para encontrar nopales automáticamente  
- ✅ Entender cómo funciona el sistema sin conocimientos técnicos

## 📋 ¿Qué Necesitas Antes de Empezar?

### 💻 **Requisitos del Sistema (Verificar ANTES de instalar)**
- **Sistema Operativo:** Windows 10+, macOS 10.14+, o Linux Ubuntu 18.04+
- **Python:** Versión 3.8 o más nueva - [Descargar aquí](https://python.org)
- **Memoria RAM:** Mínimo 4GB (8GB recomendado)
- **Espacio en disco:** 3GB libres
- **Cámara web:** Cualquier cámara USB o integrada
- **Internet:** Para descargar las librerías (solo durante instalación)

### 🔧 **¿Cómo verificar si tienes Python?**
```bash
# Abre tu terminal y ejecuta:
python --version
# O en algunos sistemas:
python3 --version
```

**Deberías ver algo como:** `Python 3.9.6` o `Python 3.8.10`

**Si ves un error:** Instala Python desde [python.org](https://python.org)

### 📱 **¿Cómo verificar tu cámara?**
- **Windows:** Abre la app "Cámara"
- **macOS:** Abre "Photo Booth" 
- **Linux:** Ejecuta `cheese` o similar

Si tu cámara funciona en estas apps, funcionará con el detector.

## ⚡ Inicio Súper Rápido (3 pasos)

### Paso 1: Preparar el Sistema
```bash
# Copia y pega esto en tu terminal:
git clone https://github.com/crbzxy/nopalDetector.git
cd nopalDetector
```

### Paso 2: Instalación Automática
```bash
# Este script instala TODO automáticamente:
./setup.sh
```
*Esto puede tomar 2-3 minutos. ¡Ve por un café! ☕*

**🔧 ¿Qué instala automáticamente el script?**
- ✅ **Entorno virtual Python** (`venv/`) - Aísla las dependencias del proyecto
- ✅ **YOLOv11** - La inteligencia artificial para detectar objetos
- ✅ **OpenCV** - Para procesar imágenes y acceder a la cámara
- ✅ **Roboflow** - Para gestión de datasets (opcional)
- ✅ **Todas las librerías necesarias** - Ver `requirements.txt` para lista completa
- ✅ **Estructura de carpetas** - Crea `data/`, `outputs/`, `models/`, etc.
- ✅ **Archivos de configuración** - Prepara `.env.example` y configs

### 📦 **¿Qué archivos se descargan y dónde?**

**Durante la instalación verás:**
```
Collecting ultralytics...
Downloading ultralytics-8.0.20-py3-none-any.whl (525 kB)
Installing collected packages: ultralytics...
Successfully installed ultralytics-8.0.20
```

**Archivos que se crean:**
```
nopalDetector/
├── venv/                          # Entorno virtual (📁 ~500MB)
│   ├── lib/python3.9/site-packages/  # Todas las librerías aquí
│   └── bin/activate               # Script para activar entorno
├── yolo11s.pt                     # Modelo base YOLO (📄 ~22MB)
├── runs/detect/train/weights/     # Modelos entrenados (📄 ~45MB)
├── data/                          # Tus imágenes y datasets
├── outputs/                       # Resultados de detecciones
└── .env                          # Tu configuración personal
```

**💾 Espacio total usado:** ~600MB aproximadamente

### 📊 **¿Qué verás durante la instalación?**

```
🚀 Iniciando configuración de Nopal Detector...
📦 Creando entorno virtual...
✅ Entorno virtual creado en: venv/

📥 Instalando dependencias principales...
✅ ultralytics instalado correctamente
✅ opencv-python instalado correctamente  
✅ roboflow instalado correctamente
... (continúa con ~15 librerías más)

📁 Creando estructura de directorios...
✅ data/ creado
✅ outputs/ creado
✅ models/ creado

🔧 Configurando archivos de configuración...
✅ .env.example creado
✅ config/ configurado

🎉 ¡Instalación completada exitosamente!
⏱️ Tiempo total: ~2-3 minutos
```

### Paso 3: ¡Probar que Funciona!
```bash
# Verifica que todo esté bien:
python verify_setup.py
```

**¡Si ves "✅ TODO CONFIGURADO CORRECTAMENTE", ya puedes empezar!**

### 🔍 ¿Qué verifica el script de prueba?
- ✅ **Python 3.8+** - Versión compatible
- ✅ **Entorno virtual** - Que esté activo
- ✅ **Librerías instaladas** - Ultralytics, OpenCV, etc.
- ✅ **Estructura de carpetas** - Que existan todas las carpetas necesarias
- ✅ **Acceso a cámara** - Que se pueda conectar a tu webcam
- ✅ **Modelos de IA** - Que los archivos de YOLOv11 estén listos

## 🔧 Instalación Manual (Para Usuarios Avanzados)

<details>
<summary>🤓 Si prefieres instalar paso a paso (haz clic aquí)</summary>

### Paso 1: Crear Entorno Virtual
```bash
# Crear entorno aislado:
python3 -m venv venv

# Activar entorno:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Paso 2: Instalar Dependencias Principales
```bash
# Instalar YOLO y Computer Vision:
pip install ultralytics>=8.0.0

# Instalar procesamiento de imágenes:
pip install opencv-python>=4.8.0

# Instalar herramientas de datos:
pip install roboflow>=1.1.0

# O instalar todo de una vez:
pip install -r requirements.txt
```

### Paso 3: Crear Estructura de Carpetas
```bash
# Crear carpetas necesarias:
mkdir -p data/{raw,processed}
mkdir -p outputs/{predictions,videos,visualizations}
mkdir -p models/weights
mkdir -p logs
```

### Paso 4: Configurar Variables de Entorno
```bash
# Copiar plantilla:
cp .env.example .env

# Editar si tienes API key de Roboflow:
nano .env  # o usar tu editor preferido
```

### Paso 5: Verificar Instalación
```bash
python verify_setup.py
```

**💡 Ventajas de instalación manual:**
- 🎛️ Control total sobre cada paso
- 🔍 Puedes ver qué se instala exactamente
- 🚀 Más rápido si ya tienes algunas dependencias
- 🛠️ Perfecto para desarrollo y personalización

</details>

## 🎮 Usar el Detector

### 🎥 Opción 1: Cámara en Tiempo Real (¡Recomendado!)

```bash
# Activa el entorno:
source venv/bin/activate

# ¡Inicia la detección! (COMANDO CORRECTO QUE FUNCIONA)
python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt
```

> **📍 IMPORTANTE:** Siempre usar el comando completo con `--weights` y `--camera` para evitar errores.

### 🤔 **¿Qué significa "activar el entorno"?**

**¿Por qué `source venv/bin/activate`?**
- 🔒 **Aísla el proyecto** - Las librerías solo se instalan para este proyecto
- 🚫 **No afecta tu sistema** - No modifica tu Python global
- ✅ **Versiones correctas** - Garantiza que uses las versiones exactas que funcionan
- 🧹 **Fácil de limpiar** - Puedes borrar `venv/` para desinstalar todo

**¿Cómo saber si está activo?**
Tu terminal debería mostrar `(venv)` al inicio:
```
(venv) ❯ python main.py --mode camera ...
```

**Si no ves `(venv)`:**
```bash
# Ejecuta esto primero:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

**🎮 Controles mientras usas la cámara:**
- **Q** = Salir
- **S** = Guardar la imagen actual
- **ESPACIO** = Pausar/reanudar
- **C** = Hacer detección más estricta (menos falsos positivos)
- **V** = Hacer detección más permisiva (detecta más objetos)
- **F** = Activar/desactivar filtros inteligentes

### 🛠️ Comandos Alternativos Probados

```bash
# Si cámara 1 no funciona, prueba cámara 0:
python main.py --mode camera --camera 0 --weights runs/detect/train/weights/best.pt

# Con resolución específica (opcional):
python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt --resolution 1280x720
```

### 📸 Opción 2: Analizar una Imagen

```bash
# Para analizar una imagen específica:
python main.py --mode predict --source "ruta/a/tu/imagen.jpg"
```

### 🎬 Opción 3: Procesar un Video

```bash
# Para procesar un video completo:
python main.py --mode video --source "ruta/a/tu/video.mp4"
```

## 💡 Consejos para Mejores Resultados

### 🎯 Para Reducir Falsas Detecciones:
1. **Usa buena iluminación** - Evita sombras fuertes
2. **Mantén la cámara estable** - Los movimientos bruscos confunden al detector
3. **Ajusta la sensibilidad** - Presiona **C** durante la detección para hacerla más estricta
4. **Activa los filtros** - Presiona **F** para filtrar objetos demasiado grandes

### 📱 Para Mejores Detecciones:
- **Distancia ideal:** 1-3 metros del nopal
- **Ángulo:** Frontal o ligeramente lateral
- **Fondo:** Preferiblemente despejado
- **Iluminación:** Natural durante el día es ideal

## ❓ ¿Algo No Funciona?

### 🚨 Problemas Comunes (Basados en Pruebas Reales):

**"Error: Se requieren pesos del modelo"**
```bash
# SIEMPRE usa el comando completo con weights:
python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt
```

**"No se encuentra la cámara"**
```bash
# Prueba con diferentes cámaras (COMANDOS PROBADOS):
python main.py --mode camera --camera 0 --weights runs/detect/train/weights/best.pt  # Cámara principal
python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt  # Cámara secundaria
```

**"Error leyendo frame de la cámara"**
```bash
# Si la cámara se desconecta, intenta:
# 1. Cambiar a la otra cámara (0 o 1)
# 2. Reiniciar el programa
# 3. Verificar que no hay otra app usando la cámara
```

**"El detector detecta personas como nopales"**
```bash
# Durante la detección, presiona:
# C = Aumentar precisión
# F = Activar filtros de tamaño
```

**"Error de instalación"**
```bash
# Reinstala todo desde cero:
rm -rf venv/
./setup.sh
```

**"Python no encontrado"**
- Instala Python desde [python.org](https://python.org)
- En macOS/Linux usa `python3` en lugar de `python`

**"No module named 'ultralytics'"**
```bash
# El entorno virtual no está activo:
source venv/bin/activate
# Luego ejecuta el comando nuevamente
```

**"Permission denied: ./setup.sh"**
```bash
# En macOS/Linux, dar permisos de ejecución:
chmod +x setup.sh
./setup.sh
```

**"pip: command not found"**
```bash
# Python no incluye pip, instalar:
python -m ensurepip --upgrade
# O reinstalar Python desde python.org
```

### 💡 Consejos de Estabilidad

1. **Usa siempre el comando completo** - No omitas `--weights` ni `--camera`
2. **Si se crashea la cámara** - Simplemente vuelve a ejecutar el comando
3. **Si hay conflictos de cámara** - Cierra otras apps que usen la cámara (Zoom, Teams, etc.)
4. **Para máxima estabilidad** - Usa cámara 1 en lugar de cámara 0 si tienes ambas

## 🎓 ¿Quieres Aprender Más?

### 📚 Documentación Completa:
- Lee el `README.md` para información técnica detallada
- Explora la carpeta `notebooks/` para ejemplos interactivos

### 🛠️ Personalización:
- Edita `config/model_config.yaml` para cambiar configuraciones
- Modifica umbrales de detección para tu caso específico

### 🔬 Modo Avanzado:
```bash
# Entrenar tu propio modelo con tus imágenes:
python main.py --mode train
```

## 🎯 Resumen de Comandos Importantes

```bash
# SETUP (solo una vez)
./setup.sh
python verify_setup.py

# USO DIARIO (COMANDOS PROBADOS Y FUNCIONANDO)
source venv/bin/activate                                              # Activar entorno
python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt  # Cámara en tiempo real
python main.py --mode predict --source imagen.jpg                     # Analizar imagen
python main.py --mode video --source video.mp4                        # Procesar video

# SOLUCIÓN DE PROBLEMAS
python verify_setup.py               # Verificar instalación
./setup.sh                          # Reinstalar si hay problemas
```

## 🆘 Comandos de Emergencia (Copia y Pega)

```bash
# 🎯 COMANDO PRINCIPAL QUE SIEMPRE FUNCIONA:
source venv/bin/activate && python main.py --mode camera --camera 1 --weights runs/detect/train/weights/best.pt

# 🔄 Si falla, prueba con cámara 0:
source venv/bin/activate && python main.py --mode camera --camera 0 --weights runs/detect/train/weights/best.pt

# 🔧 Si todo falla, reinstala:
rm -rf venv/ && ./setup.sh && python verify_setup.py
```

## 🗑️ ¿Cómo Desinstalar Completamente?

Si ya no quieres el proyecto en tu sistema:

```bash
# Ir al directorio del proyecto:
cd nopalDetector

# Desactivar entorno si está activo:
deactivate

# Borrar todo el proyecto:
cd ..
rm -rf nopalDetector/
```

**🧹 Esto elimina:**
- ✅ Todo el código del proyecto
- ✅ El entorno virtual y todas las librerías
- ✅ Todos los modelos descargados
- ✅ Todas las configuraciones y resultados

**🔒 NO afecta:**
- ✅ Tu instalación de Python sistema
- ✅ Otras librerías instaladas globalmente
- ✅ Otros proyectos en tu computadora

## 📞 ¿Necesitas Ayuda?

1. **Primero:** Lee esta guía completa
2. **Segundo:** Ejecuta `python verify_setup.py` para diagnósticos
3. **Tercero:** Revisa las secciones de problemas comunes
4. **Último recurso:** Abre un issue en GitHub

---

**¡Disfruta detectando nopales! 🌵✨**

*Esta guía te debe haber tomado menos de 5 minutos. Si algo no está claro, ¡mejoremos la documentación juntos!*