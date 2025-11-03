# 🚀 Guía Completa de Setup - Nopal Detector

**Para: Nuevos desarrolladores o personas ajenas al proyecto**

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación Rápida (Recomendado)](#instalación-rápida)
3. [Instalación Manual Paso a Paso](#instalación-manual-paso-a-paso)
4. [Configuración de Credenciales](#configuración-de-credenciales)
5. [Descarga del Dataset](#descarga-del-dataset)
6. [Entrenamiento del Modelo](#entrenamiento-del-modelo)
7. [Levantamiento de la App](#levantamiento-de-la-app)
8. [Verificación del Sistema](#verificación-del-sistema)
9. [Solución de Problemas](#solución-de-problemas)

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ **Python 3.8 o superior**
- ✅ **pip** (gestor de paquetes de Python)
- ✅ **git** (para clonar el repositorio)
- ✅ **Cuenta en Roboflow** (para descargar datasets)
- ✅ **Cámara web** (opcional, para pruebas en tiempo real)
- ✅ **Al menos 10GB de espacio en disco** (para modelos y datasets)
- ✅ **4GB de RAM mínimo** (8GB recomendado)

### Verificar Versiones

```bash
# Verificar Python
python3 --version    # Debe ser 3.8+

# Verificar pip
pip3 --version

# Verificar git
git --version
```

---

## ⚡ Instalación Rápida (RECOMENDADO)

**Para usuarios que desean empezar en ~5 minutos:**

### 1. Clonar el Repositorio

```bash
git clone https://github.com/crbzxy/nopalDetector.git
cd nopalDetector
```

### 2. Script de Instalación Automatizada

```bash
# Dar permisos de ejecución
chmod +x setup_complete.sh

# Ejecutar el script
./setup_complete.sh
```

**El script hace automáticamente:**
- ✅ Crea entorno virtual
- ✅ Instala dependencias
- ✅ Verifica Python y pip
- ✅ Crea estructura de directorios
- ✅ Configura variables de entorno
- ✅ Descarga modelo base de YOLO

**Tiempo estimado:** 3-5 minutos

### 3. Configurar Credenciales de Roboflow

```bash
# Editar el archivo .env
nano .env    # o usa tu editor favorito
```

Asegúrate de que contenga:
```bash
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4
```

**¿Dónde obtener tu API key de Roboflow?**
1. Ve a https://roboflow.com/settings/api
2. Copia tu API key
3. Pégala en `.env`

### 4. Verificar Instalación

```bash
python3 verify_environment.py
```

**Salida esperada:**
```
✅ Python 3.8+
✅ Pip instalado
✅ Dependencias instaladas
✅ Estructura de directorios
✅ Variables de entorno
```

### ¡Listo! Ahora puedes [Descargar Dataset](#descarga-del-dataset)

---

## 🛠️ Instalación Manual Paso a Paso

**Para usuarios que prefieren control granular**

### Paso 1: Clonar Repositorio

```bash
git clone https://github.com/crbzxy/nopalDetector.git
cd nopalDetector
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear venv
python3 -m venv venv

# Activar venv
# En macOS/Linux:
source venv/bin/activate

# En Windows (PowerShell):
venv\Scripts\Activate.ps1

# En Windows (cmd):
venv\Scripts\activate.bat
```

**Verificar que esté activo:**
```bash
# Deberías ver (venv) al inicio de tu terminal
(venv) $ _
```

### Paso 3: Actualizar pip

```bash
pip install --upgrade pip
```

### Paso 4: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Esto instala:**
- ultralytics (YOLOv11)
- roboflow (datasets)
- opencv-python (visión)
- pyyaml (configuración)
- python-dotenv (variables de entorno)
- numpy, pillow, matplotlib

### Paso 5: Crear Directorios

```bash
mkdir -p data/raw
mkdir -p models/weights
mkdir -p outputs/predictions
mkdir -p outputs/videos
mkdir -p outputs/visualizations
mkdir -p logs
```

### Paso 6: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env
nano .env    # o tu editor favorito
```

**Contenido requerido en .env:**
```bash
# MÍNIMO REQUERIDO
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4

# OPCIONAL
MODEL_CONFIDENCE_THRESHOLD=0.3
DEVICE=cpu  # o 'cuda' si tienes NVIDIA, 'mps' si tienes Mac M1/M2
```

### Paso 7: Verificar Instalación

```bash
python3 verify_environment.py
```

---

## 🔐 Configuración de Credenciales

### Obtener API Key de Roboflow

1. **Crear cuenta** (si no la tienes): https://roboflow.com
2. **Ir a Settings**: https://roboflow.com/settings/api
3. **Copiar tu API key**
4. **Pegar en `.env`**

### ¿Qué es Roboflow?

Roboflow es una plataforma que gestiona datasets de visión por computadora. Te permite:
- ✅ Descargar datasets etiquetados
- ✅ Versionar tus datasets
- ✅ Aumentar datos automáticamente
- ✅ Acceder a datasets públicos

### Validar Credenciales

```bash
python3 -c "
from src.utils.config import validate_api_key
if validate_api_key():
    print('✅ API key válida')
else:
    print('❌ API key inválida')
"
```

---

## 📊 Descarga del Dataset

### Opción 1: Descargar Automáticamente

```bash
python3 main.py --mode train --multi-class --data nopal-detector-4/data.yaml
```

**Esto:**
- ✅ Detecta datasets disponibles
- ✅ Descarga automáticamente si falta
- ✅ Prepara la estructura

### Opción 2: Descargar Manualmente

```bash
# Ver tus datasets
ls nopal-detector-*/

# Si no existen, el script los descarga automáticamente
```

### Verificar Dataset

```bash
# Ver estructura
tree nopal-detector-4/
# Salida esperada:
# nopal-detector-4/
# ├── images/
# │   ├── train/     (80% de imágenes)
# │   ├── val/       (20% de imágenes)
# │   └── test/      (para predicciones)
# ├── labels/        (anotaciones)
# └── data.yaml      (configuración)
```

---

## 🤖 Entrenamiento del Modelo

### Entrenar Modelo Nuevo

```bash
# Activar venv primero
source venv/bin/activate

# Entrenar con defaults
python3 main.py --mode train --multi-class --data nopal-detector-4/data.yaml
```

**Parámetros personalizables:**
```bash
# Con parámetros custom
python3 main.py --mode train --multi-class \
  --data nopal-detector-4/data.yaml \
  --skip-update-check
```

### Entrenamiento con Make (Más Fácil)

```bash
# Si tienes Make instalado (macOS/Linux)
make train DATA=nopal-detector-4/data.yaml
```

### Monitorear Entrenamiento

Durante el entrenamiento verás:
```
Epoch 1/100: 95%|███████| 150/150 [00:45<00:02, 3.3it/s]
Loss: 0.234, mAP50: 0.821
```

**Tiempo estimado:**
- GPU NVIDIA: 2-4 horas
- CPU: 8-12 horas
- Mac M1/M2: 4-6 horas

### Dónde Se Guardan los Pesos

```bash
# Los modelos entrenados se guardan en:
runs/detect/train/weights/best.pt   # Primer entrenamiento
runs/detect/train2/weights/best.pt  # Segundo entrenamiento
runs/detect/train3/weights/best.pt  # Tercero, etc.

# Ver último entrenamiento
ls -lt runs/detect/*/weights/best.pt | head -1
```

---

## 🚀 Levantamiento de la App

### Opción 1: Predicción en Imagen

```bash
python3 main.py --mode predict --multi-class \
  --weights runs/detect/train/weights/best.pt \
  --input imagen.jpg
```

**Resultado:**
```
✅ Predicción completada!
📊 Detecciones: [
    {'clase': 'nopal', 'confianza': 0.95, 'bbox': [100, 200, 300, 400]},
    {'clase': 'person', 'confianza': 0.87, 'bbox': [400, 50, 500, 300]}
]
```

### Opción 2: Predicción en Directorio

```bash
python3 main.py --mode predict \
  --source nopal-detector-4/images/val \
  --weights runs/detect/train/weights/best.pt
```

### Opción 3: Procesamiento Batch

```bash
python3 main.py --mode batch \
  --batch-dir ./imagenes/ \
  --multi-class \
  --weights runs/detect/train/weights/best.pt
```

### Opción 4: Detección en Cámara (Tiempo Real)

```bash
# Listar cámaras disponibles
python3 main.py --mode list-cameras

# Usar cámara
python3 main.py --mode camera --multi-class \
  --weights runs/detect/train/weights/best.pt \
  --camera 0
```

**Controles en cámara:**
- `Q` - Salir
- `S` - Guardar frame
- `Space` - Pausa
- `C/V` - Ajustar confianza

### Opción 5: Procesar Video

```bash
python3 main.py --mode video \
  --weights runs/detect/train/weights/best.pt \
  --input video.mp4 \
  --output output_video.mp4
```

### Usar Make para Facilidad

```bash
# Predicción en imagen
make predict-image WEIGHTS=runs/detect/train/weights/best.pt INPUT=foto.jpg

# Predicción en directorio
make predict-dir WEIGHTS=runs/detect/train/weights/best.pt SOURCE=imagenes/

# Cámara
make camera WEIGHTS=runs/detect/train/weights/best.pt

# Video
make predict-video WEIGHTS=runs/detect/train/weights/best.pt INPUT=video.mp4
```

---

## ✅ Verificación del Sistema

### Script de Verificación

```bash
# Ejecutar verificación completa
python3 verify_environment.py

# Salida esperada:
✅ Sistema verificado correctamente
  - Python 3.8+
  - Dependencias instaladas
  - Estructura creada
  - Variables de entorno
  - Modelos descargados
```

### Checklist Manual

```bash
# 1. Verificar Python
python3 --version       # Debe ser 3.8+

# 2. Verificar venv activo
which python            # Debe apuntar a venv/bin/python

# 3. Verificar pip
pip list | grep ultralytics

# 4. Verificar .env
cat .env

# 5. Verificar estructura
ls -la runs/detect/ models/weights/

# 6. Probar importes
python3 -c "
from ultralytics import YOLO
from roboflow import Roboflow
print('✅ Imports correctos')
"
```

---

## 🐛 Solución de Problemas

### Problema: `ModuleNotFoundError: No module named 'yaml'`

**Solución:**
```bash
# Asegúrate que el venv está activo
source venv/bin/activate

# Reinstala dependencias
pip install -r requirements.txt
```

---

### Problema: `ROBOFLOW_API_KEY not found`

**Solución:**
```bash
# 1. Verificar .env existe
ls -la .env

# 2. Verificar contenido
cat .env

# 3. Si está vacío, llenar con:
echo "ROBOFLOW_API_KEY=tu_key_aqui" >> .env
```

---

### Problema: `No such file or directory: 'nopal-detector-4/data.yaml'`

**Solución:**
```bash
# 1. El dataset se descarga automáticamente, espera...
python3 main.py --mode train --multi-class

# 2. O descargarlo manualmente:
from roboflow import Roboflow
rf = Roboflow(api_key="TU_KEY")
project = rf.workspace("nopaldetector").project("nopal-detector-0lzvl")
dataset = project.version(4).download("yolov11")

# 3. Verificar que existe
ls nopal-detector-*/data.yaml
```

---

### Problema: `No se pudo abrir la cámara`

**Solución:**
```bash
# 1. Listar cámaras disponibles
python3 main.py --mode list-cameras

# 2. Si no hay cámaras, intenta con índice diferente
python3 main.py --mode camera --camera 1

# 3. En macOS, otorgar permisos:
# Settings > Security & Privacy > Camera > Python
```

---

### Problema: `CUDA not available`

**Solución:**
```bash
# Si no tienes GPU NVIDIA, usa CPU (es normal):
echo "DEVICE=cpu" >> .env

# O en macOS con M1/M2:
echo "DEVICE=mps" >> .env
```

---

### Problema: Entrenamiento muy lento

**Causas y soluciones:**
```bash
# 1. Usando CPU en lugar de GPU
# Solución: Instalar CUDA (si tienes NVIDIA)

# 2. Dataset muy grande
# Solución: Usar dataset versión más pequeña

# 3. Venv incorrecto
# Solución: Verificar que está activo
which python
```

---

## 📚 Comandos Útiles

```bash
# Ver logs en tiempo real
tail -f logs/*.log

# Limpiar caché de Python
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete

# Ver estado del proyecto
make status

# Limpiar directorio
make clean

# Limpiar todo (advertencia: elimina venv)
make clean-all

# Ver ayuda de make
make help
```

---

## 🔍 Estructura del Proyecto Explicada

```
nopalDetector/
├── main.py                           # 🎯 Punto de entrada principal
├── verify_environment.py             # ✅ Verificador de sistema
├── requirements.txt                  # 📦 Dependencias
├── .env                              # 🔐 Variables de entorno (local)
├── .env.example                      # 📋 Plantilla de .env
│
├── src/                              # 💻 Código fuente
│   ├── models/
│   │   ├── detector.py               # Detector clásico (nopales + personas)
│   │   └── multi_class_detector.py   # Detector multi-clase
│   ├── data/
│   │   └── dataset_manager.py        # Gestor de datasets
│   └── utils/
│       ├── validators.py             # ✅ Validadores de entrada
│       ├── error_handler.py          # 🛡️ Context managers
│       ├── config.py                 # ⚙️ Configuración
│       ├── camera_detector.py        # 📹 Detección en cámara
│       └── visualization.py          # 🎨 Visualización
│
├── config/                           # 📄 Archivos YAML de configuración
├── data/                             # 📊 Datos (raw, processed)
├── models/                           # 🤖 Pesos de modelos
├── outputs/                          # 📁 Predicciones
├── runs/                             # 🏃 Resultados de entrenamientos
├── tests/                            # 🧪 Tests unitarios
├── scripts/                          # 🔧 Scripts auxiliares
│
├── README.md                         # 📖 Documentación principal
├── SETUP_GUIDE.md                    # 👈 Esta guía
├── BEST_PRACTICES_REVIEW.md          # 🎯 Análisis de mejoras
└── Makefile                          # ⚙️ Comandos make
```

---

## 🤝 Soporte

### Contacto

- **Autor:** Carlos Boyzo - [crbzxy](https://github.com/crbzxy)
- **Proyecto:** [nopalDetector](https://github.com/crbzxy/nopalDetector)
- **Issues:** [GitHub Issues](https://github.com/crbzxy/nopalDetector/issues)

### Recursos Útiles

- [Documentación YOLOv11](https://docs.ultralytics.com/)
- [Roboflow Docs](https://roboflow.com/docs)
- [OpenCV Docs](https://docs.opencv.org/)

---

## ✨ Próximos Pasos

Después de completar la instalación:

1. ✅ Descargar dataset
2. ✅ Entrenar modelo
3. ✅ Hacer predicciones
4. ✅ Explorar resultados
5. ✅ Leer [README.md](README.md) para más información

¡**Listo para empezar? ¡Ejecuta `./setup_complete.sh`!**
