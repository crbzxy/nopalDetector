# 🌵 Nopal Detector - Sistema Multi-Clase Inteligente

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-orange)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Sistema avanzado de detección y clasificación de nopales usando **YOLOv11** con soporte para múltiples especies y actualización automática de etiquetas.

Un proyecto completo que utiliza la tecnología más avanzada (YOLOv11) para identificar múltiples tipos de nopales y personas en imágenes, videos y cámara en vivo. Diseñado para ser fácil de usar, incluso sin conocimientos técnicos previos.

## ✨ Características Principales

### 🎯 **Sistema Multi-Clase**
- **Detección de múltiples tipos** de nopales (`nopal`, `nopalChino`)
- **Visualización diferenciada** por colores
- **Entrenamiento dinámico** con nuevas clases
- **Actualización automática** de datasets via Roboflow API

### 🚀 **Funcionalidades Core**
- **🔄 Actualización Automática**: Sincronización automática con Roboflow
- **🎨 Colores Dinámicos**: Generación automática de colores únicos por clase
- **📊 Estadísticas Avanzadas**: Reportes detallados por clase
- **📷 Tiempo Real**: Detección en cámara con 30 FPS
- **🤖 Entrenamiento Inteligente**: Sistema adaptativo para nuevas clases

## 📊 Métricas del Modelo Actual

- **mAP50 General**: 49.2%
  - `nopal`: 23.0% mAP50 (Precisión: 18.0%, Recall: 100%)
  - `nopalChino`: 75.4% mAP50 (Precisión: 75.9%, Recall: 77.3%)
- **Tiempo de inferencia**: ~110ms por imagen
- **Tamaño del modelo**: 19.2 MB
- **Clases soportadas**: 2 tipos de nopales + personas

## 🎨 Sistema de Visualización

### Códigos de Color por Clase
- 🟢 **Nopal**: Verde (RGB: 0, 255, 0)
- 🟠 **NopalChino**: Naranja (RGB: 255, 165, 0)
- 🔵 **Personas**: Azul (RGB: 255, 0, 0)

## 🎯 ¿Qué hace este proyecto?

Este sistema puede:

- 📹 **Detectar en tiempo real** múltiples tipos de nopales y personas usando tu cámara web
- 🖼️ **Analizar imágenes** para encontrar nopales automáticamente con clasificación
- 🎥 **Procesar videos** completos identificando objetos frame por frame
- 🎓 **Entrenar modelos personalizados** con tus propios datos
- 📊 **Generar estadísticas** y visualizaciones de los resultados
- 🔄 **Actualizar automáticamente** con nuevas clases desde Roboflow

## 🛠️ Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/crbzxy/nopalDetector.git
cd nopalDetector

# Instalar dependencias automáticamente
chmod +x install.sh
./install.sh

# O instalación manual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Uso Rápido

### 1. 📷 Detección Multi-Clase en Tiempo Real
```bash
# Cámara con detección multi-clase
python main.py --mode camera --multi-class --weights runs/detect/train4/weights/best.pt --camera 0

# Controles durante la detección:
# - 'q': Salir
# - 's': Guardar frame
# - SPACE: Pausar/reanudar
# - 'c'/'v': Ajustar confianza
# - 'x'/'z': Ajustar IoU
# - 'f': Activar/desactivar filtros
```

### 2. 🖼️ Análisis de Imágenes Multi-Clase
```bash
# Imagen individual
python main.py --mode predict --multi-class --weights runs/detect/train4/weights/best.pt --input imagen.jpg

# Procesamiento en lote
python main.py --mode batch --multi-class --batch-dir /ruta/imagenes/
```

### 3. 🎓 Entrenamiento Multi-Clase
```bash
# Entrenar con dataset multi-clase
python main.py --mode train --multi-class --data nopal-detector-3/data.yaml

# Entrenar con actualización automática
python main.py --mode train --multi-class --auto-update
```

### 4. 🔄 Actualización Automática de Datasets
```bash
# Verificar y descargar nuevas versiones
python main.py --mode update-labels --auto-update
```

## 📁 Estructura del Proyecto

```
nopalDetector/
├── 📄 main.py                    # Script principal
├── 📁 src/                       # Código fuente
│   ├── 📁 models/               # Detectores de IA
│   ├── 📁 utils/                # Utilidades
│   └── 📁 data/                 # Gestión de datos
├── 📁 config/                   # Configuraciones
├── 📁 models/weights/           # Modelos entrenados
├── 📁 nopal-detector-3/         # Dataset multi-clase actual
├── 📁 outputs/                  # Resultados
│   ├── 📁 predictions/          # Imágenes procesadas
│   ├── 📁 videos/              # Videos procesados
│   └── 📁 visualizations/      # Gráficos y estadísticas
└── 📁 runs/                     # Entrenamientos
    └── 📁 detect/train4/        # Último modelo multi-clase
```

## 🎮 Guía de Comandos Principales

### Detección en Tiempo Real
```bash
# Multi-clase con cámara
python main.py --mode camera --multi-class --weights runs/detect/train4/weights/best.pt --camera 0

# Clásico (solo nopales)
python main.py --mode camera --weights modelo.pt --camera 0 --save-video
```

### Procesamiento de Imágenes
```bash
# Multi-clase
python main.py --mode predict --multi-class --input imagen.jpg --confidence 0.3

# Batch multi-clase
python main.py --mode batch --multi-class --batch-dir fotos/ --output resultados/
```

### Entrenamiento y Datos
```bash
# Entrenar modelo multi-clase
python main.py --mode train --multi-class --data nopal-detector-3/data.yaml

# Listar cámaras disponibles
python main.py --mode list-cameras

# Actualizar datasets desde Roboflow
python main.py --mode update-labels --auto-update
```

## ⚙️ Configuración Avanzada

### Variables de Entorno (.env)
```bash
# Configurar API de Roboflow
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=tu_workspace
ROBOFLOW_PROJECT=tu_proyecto
```

### Parámetros de Detección
```bash
# Ajustar sensibilidad
python main.py --mode camera --multi-class --confidence 0.3  # Más sensible
python main.py --mode camera --multi-class --confidence 0.7  # Menos sensible

# Configurar resolución de cámara
python main.py --mode camera --multi-class --resolution 1280x720
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 🎥 Cámara no funciona
```bash
# Listar cámaras disponibles
python main.py --mode list-cameras

# Probar diferentes índices
python main.py --mode camera --multi-class --camera 0  # o 1, 2, etc.
```

#### 📁 Error de modelo no encontrado
```bash
# Verificar ruta del modelo
ls runs/detect/train4/weights/best.pt

# Usar modelo base si no tienes entrenado
python main.py --mode camera --weights yolo11s.pt
```

#### 🔄 Problemas con Roboflow
```bash
# Verificar configuración
python debug_download.py

# Actualizar manualmente
python update_labels.py
```

## 📈 Rendimiento y Optimización

### Requisitos de Sistema
- **CPU**: Intel i5 o equivalente (mínimo)
- **RAM**: 8GB (recomendado 16GB)
- **GPU**: Opcional (CUDA compatible para mayor velocidad)
- **Cámara**: Cualquier webcam USB o integrada

### Optimización de Velocidad
```bash
# Reducir resolución para mayor FPS
python main.py --mode camera --multi-class --resolution 640x480

# Ajustar confianza para menos procesamiento
python main.py --mode camera --multi-class --confidence 0.5
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Changelog

### v3.0 (Octubre 2025) - Sistema Multi-Clase
- ✅ **Nueva funcionalidad**: Detección multi-clase (nopal, nopalChino)
- ✅ **Nueva funcionalidad**: Cámara multi-clase en tiempo real
- ✅ **Mejora**: Integración completa con Roboflow API
- ✅ **Mejora**: Sistema de colores diferenciados por clase
- ✅ **Mejora**: Actualización automática de datasets
- ✅ **Mejora**: Controles dinámicos en tiempo real
- ✅ **Nuevo**: debug_download.py para troubleshooting
- ✅ **Optimización**: Filtros anti-falsos positivos mejorados

### v2.0 (Previo)
- ✅ Detección básica de nopales y personas
- ✅ Entrenamiento con YOLOv11
- ✅ Interfaz de cámara básica
- ✅ Procesamiento batch

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Carlos Boyzo** - [crbzxy](https://github.com/crbzxy)

## 🙏 Agradecimientos

- [Ultralytics](https://ultralytics.com) por YOLOv11
- [Roboflow](https://roboflow.com) por la plataforma de datos
- Comunidad open source por las librerías utilizadas

---

## 🌵 ¡Detecta nopales como un experto con IA! 🚀

**¿Encontraste útil este proyecto? ¡Dale una ⭐ al repositorio!**