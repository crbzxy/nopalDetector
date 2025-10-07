# Nopal Detector con YOLOv11 🌵

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-orange)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Proyecto de detección de nopales y personas usando YOLOv11, optimizado para entrenamiento local y en Google Colab.

## 🚀 Características

- ✅ **Detección Dual:** Nopales + Personas en tiempo real
- ✅ **YOLOv11:** Última versión de YOLO optimizada
- ✅ **Dataset Automático:** Integración con Roboflow
- ✅ **Arquitectura Modular:** Código organizado y extensible
- ✅ **Multi-Entorno:** Compatible con local y Google Colab
- ✅ **Visualizaciones:** Gráficos automáticos de resultados
- ✅ **Seguridad:** Variables de entorno para API keys

## 🛠️ Instalación Rápida

### Opción 1: Script Automático (Recomendado)
```bash
git clone tu-repositorio
cd nopalDetector
./setup.sh
```

### Opción 2: Manual
```bash
# 1. Clonar repositorio
git clone tu-repositorio
cd nopalDetector

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu API key
```

## 📋 Requisitos

- **Python:** 3.8 o superior
- **RAM:** 8GB mínimo (16GB recomendado)
- **GPU:** Opcional pero recomendada para entrenamiento
- **Espacio:** 5GB libres

### Dependencias Principales
```bash
ultralytics>=8.0.0     # YOLOv11
roboflow>=1.1.0        # Dataset management
opencv-python>=4.8.0   # Computer vision
python-dotenv>=1.0.0   # Environment variables
```

## ⚙️ Configuración

### 1. Variables de Entorno
```bash
# Copia la plantilla
cp .env.example .env

# Edita el archivo .env
nano .env
```

### 2. Obtener API Key de Roboflow
1. Ve a [Roboflow.com](https://roboflow.com/)
2. Crea una cuenta o inicia sesión
3. Ve a **Settings → API Keys**
4. Copia tu API key
5. Pégala en el archivo `.env`:
   ```bash
   ROBOFLOW_API_KEY=tu_api_key_aqui
   ```

### 3. Configuración Opcional
```bash
# Ajustar parámetros del modelo (opcional)
MODEL_CONFIDENCE_THRESHOLD=0.3
MODEL_IOU_THRESHOLD=0.5
```

## 🗂️ Estructura del Proyecto

```
nopalDetector/
├── 📋 README.md                      # Documentación
├── 📋 requirements.txt               # Dependencias Python
├── 🚀 main.py                        # Script principal CLI
├── ⚙️ setup.sh                       # Configuración automática
├── 🔒 .env.example                   # Plantilla de variables
├── 🔒 .gitignore                     # Archivos ignorados por Git
│
├── 📁 config/                        # Configuraciones
│   ├── model_config.yaml            # Config principal
│   └── training_config.yaml         # Config por entornos
│
├── 📁 src/                           # Código fuente
│   ├── data/
│   │   └── dataset_manager.py       # Gestión de datasets
│   ├── models/
│   │   └── detector.py              # Detector YOLOv11
│   └── utils/
│       ├── config.py                # Utilidades de configuración
│       ├── visualization.py         # Gráficos y visualizaciones
│       └── video_processor.py       # Procesamiento de video
│
├── 📁 notebooks/
│   └── nopal_detector_training.ipynb # Notebook completo
│
├── 📁 data/
│   ├── raw/                         # Datos sin procesar
│   └── processed/                   # Datos procesados
│
├── 📁 models/
│   └── weights/                     # Modelos entrenados
│
├── 📁 outputs/
│   ├── predictions/                 # Imágenes con detecciones
│   ├── videos/                      # Videos procesados
│   └── visualizations/              # Gráficos y estadísticas
│
└── 📁 logs/                         # Archivos de log
```

## 🎯 Uso

### Método 1: Notebook Interactivo (Recomendado)
```bash
# Activar entorno
source venv/bin/activate

# Abrir Jupyter Lab
jupyter lab notebooks/nopal_detector_training.ipynb
```

### Método 2: Línea de Comandos
```bash
# Activar entorno
source venv/bin/activate

# Entrenar modelo
python main.py --mode train

# Predicciones en imágenes
python main.py --mode predict --input /ruta/a/imagenes/

# Procesar video
python main.py --mode video --input video.mp4 --output resultado.mp4
```

### Método 3: Google Colab
1. Sube el notebook a Google Colab
2. Ejecuta las celdas en orden
3. Cuando se solicite, ingresa tu API key de Roboflow

## 📊 Configuraciones Predefinidas

El proyecto incluye 3 configuraciones optimizadas:

### 🔧 Desarrollo (Rápido)
```yaml
# config/training_config.yaml -> development
epochs: 10
batch_size: 8
image_size: 416
model: yolo11s.pt
```

### 🎯 Producción (Balanceado)
```yaml
# config/training_config.yaml -> production  
epochs: 100
batch_size: 16
image_size: 640
model: yolo11m.pt
```

### 🧪 Experimento (Máxima Precisión)
```yaml
# config/training_config.yaml -> experiment
epochs: 200
batch_size: 8
image_size: 832
model: yolo11l.pt
```

## 📈 Flujo de Trabajo

1. **📥 Instalación:** Ejecutar `./setup.sh`
2. **🔑 Configuración:** Editar `.env` con API key
3. **📊 Entrenamiento:** Usar notebook o CLI
4. **🖼️ Predicciones:** Procesar imágenes de test
5. **🎥 Videos:** Procesar videos con detecciones
6. **📈 Análisis:** Revisar visualizaciones automáticas

## 🔧 Personalización

### Cambiar Dataset
Edita en `config/model_config.yaml`:
```yaml
roboflow:
  workspace: "tu_workspace"
  project: "tu_project"
  version: 1
```

### Ajustar Modelo
```yaml
model:
  base_model: "yolo11n.pt"  # nano, s, m, l, x
  training:
    epochs: 50
    batch_size: 16
    image_size: 640
```

### Personalizar Detección
```yaml
prediction:
  confidence_threshold: 0.25  # Más sensible
  iou_threshold: 0.45         # Menos superposición
```

## 🐛 Solución de Problemas

### Error: "ROBOFLOW_API_KEY not found"
```bash
# Verificar archivo .env
cat .env

# Debe contener:
ROBOFLOW_API_KEY=tu_api_key_real
```

### Error: "No module named 'ultralytics'"
```bash
# Activar entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error de memoria durante entrenamiento
```yaml
# Reducir batch_size en config/model_config.yaml
training:
  batch_size: 4  # Reducir de 16 a 4
  image_size: 416  # Reducir de 640 a 416
```

### GPU no detectada
```bash
# Verificar CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Instalar PyTorch con CUDA si es necesario
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 📝 Archivos Requeridos

### ✅ Lo que SÍ debes subir a Git:
- `README.md`, `requirements.txt`, `main.py`
- Todo el directorio `src/`
- Todo el directorio `config/`
- `notebooks/nopal_detector_training.ipynb`
- `.env.example` (plantilla sin API key real)
- `.gitignore`

### ❌ Lo que NO debes subir a Git:
- `.env` (contiene tu API key real)
- `venv/` (entorno virtual)
- `models/weights/*.pt` (modelos entrenados)
- `outputs/` (resultados generados)
- `data/raw/` (datasets descargados)
- `logs/` (archivos de log)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Ultralytics](https://ultralytics.com/) por YOLOv11
- [Roboflow](https://roboflow.com/) por la gestión de datasets
- Comunidad de Computer Vision por el soporte

---

**¿Problemas o preguntas?** Abre un [issue](../../issues) o contáctanos.

## 🎯 Uso Rápido

1. Abrir el notebook `notebooks/nopal_detector_training.ipynb`
2. Ejecutar las celdas en orden
3. Los resultados se guardarán en `outputs/`

## 🔧 Configuración

Editar los archivos en `config/` para personalizar:
- Parámetros del modelo
- Configuración de entrenamiento
- Rutas de datos

## 📊 Resultados

- Imágenes procesadas: `outputs/predictions/`
- Videos procesados: `outputs/videos/`
- Pesos del modelo: `models/weights/`