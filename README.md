# Nopal Detector con YOLOv11 🌵

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-orange)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Sistema inteligente de detección de nopales y personas en tiempo real usando inteligencia artificial**

Un proyecto completo que utiliza la tecnología más avanzada (YOLOv11) para identificar nopales y personas en imágenes, videos y cámara en vivo. Diseñado para ser fácil de usar, incluso sin conocimientos técnicos previos.

## 🎯 ¿Qué hace este proyecto?

Este sistema puede:
- 📹 **Detectar en tiempo real** nopales y personas usando tu cámara web
- 🖼️ **Analizar imágenes** para encontrar nopales automáticamente
- 🎥 **Procesar videos** completos identificando objetos frame por frame
- 🎓 **Entrenar modelos personalizados** con tus propios datos
- 📊 **Generar estadísticas** y visualizaciones de los resultados

## 🚀 Características Principales

- ✅ **Detección Dual Inteligente:** Distingue entre nopales y personas con alta precisión
- ✅ **Interfaz Fácil de Usar:** Controles simples con teclas durante la detección
- ✅ **Filtros Avanzados:** Sistema anti-falsos positivos incorporado
- ✅ **Cámara en Tiempo Real:** Procesamiento de video en vivo con 30 FPS
- ✅ **Configuración Automática:** Scripts que instalan todo por ti
- ✅ **Arquitectura Profesional:** Código organizado y bien documentado
- ✅ **Multiplataforma:** Funciona en Windows, Mac y Linux
- ✅ **Seguro:** Protección de claves API y datos sensibles

## � Instalación Súper Fácil

### 🎯 Para Usuarios sin Experiencia Técnica

**¡Solo sigue estos 3 pasos!**

#### Paso 1: Descargar el Proyecto
```bash
# Copia y pega esto en tu terminal:
git clone https://github.com/crbzxy/nopalDetector.git
cd nopalDetector
```

#### Paso 2: Instalación Automática
```bash
# Este script instala todo automáticamente:
./setup.sh
```

#### Paso 3: Verificar que Todo Funciona
```bash
# Este comando prueba que la instalación fue exitosa:
python verify_setup.py
```

**¡Ya está listo! Ahora puedes usar el detector.**

### 🔧 Para Usuarios Avanzados (Instalación Manual)

<details>
<summary>Haz clic aquí para ver instalación manual</summary>

```bash
# 1. Clonar repositorio
git clone https://github.com/crbzxy/nopalDetector.git
cd nopalDetector

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (opcional para dataset)
cp .env.example .env
# Editar .env con tu API key de Roboflow si la tienes
```
</details>

## � Requisitos del Sistema

### 📱 Requisitos Mínimos (Para usar el detector básico)
- **Sistema Operativo:** Windows 10, macOS 10.14+, o Linux Ubuntu 18.04+
- **Python:** Versión 3.8 o más nueva ([Descargar aquí](https://python.org))
- **RAM:** 4GB mínimo (8GB recomendado)
- **Espacio en Disco:** 3GB libres
- **Cámara Web:** Cualquier cámara USB o integrada

### 🚀 Requisitos Recomendados (Para entrenamiento)
- **RAM:** 16GB o más
- **GPU:** NVIDIA con CUDA (opcional pero acelera mucho el proceso)
- **Espacio en Disco:** 10GB libres
- **Internet:** Conexión estable para descargar modelos

### 📦 ¿Qué se Instala Automáticamente?
El script de instalación descarga e instala:
- **YOLOv11:** La inteligencia artificial para detectar objetos
- **OpenCV:** Para procesar imágenes y video
- **Roboflow:** Para gestionar datasets (opcional)
- **Otras librerías:** Herramientas de apoyo necesarias

<details>
<summary>🔍 Lista completa de dependencias técnicas</summary>

```bash
ultralytics>=8.0.0     # YOLOv11 - Motor de inteligencia artificial
roboflow>=1.1.0        # Gestión de datasets
opencv-python>=4.8.0   # Procesamiento de imágenes
python-dotenv>=1.0.0   # Variables de entorno seguras
matplotlib>=3.5.0      # Gráficos y visualizaciones
pyyaml>=6.0            # Archivos de configuración
pillow>=9.0.0          # Manejo de imágenes
numpy>=1.21.0          # Cálculos matemáticos
```
</details>

## 🎮 Cómo Usar el Detector (Guía Paso a Paso)

### 🚀 Opción 1: Detección con tu Cámara (¡Lo Más Divertido!)

**Paso 1:** Abre tu terminal y navega al proyecto
```bash
cd nopalDetector
```

**Paso 2:** Activa el entorno (esto prepara el sistema)
```bash
source venv/bin/activate
# En Windows: venv\Scripts\activate
```

**Paso 3:** ¡Inicia la detección en tiempo real!
```bash
python main.py --mode camera
```

**🎮 Controles durante la detección:**
- **Q** = Salir del programa
- **S** = Guardar la imagen actual
- **ESPACIO** = Pausar/reanudar el video
- **C** = Hacer la detección más estricta (menos falsos positivos)
- **V** = Hacer la detección más permisiva (detecta más objetos)
- **F** = Activar/desactivar filtros inteligentes de tamaño

### 📸 Opción 2: Analizar una Imagen

```bash
# Detectar nopales en una imagen específica
python main.py --mode predict --source "ruta/a/tu/imagen.jpg"
```

### 🎥 Opción 3: Procesar un Video Completo

```bash
# Procesar un video y guardar resultado
python main.py --mode video --source "ruta/a/tu/video.mp4"
```

### 🎓 Opción 4: Entrenar tu Propio Modelo (Avanzado)

```bash
# Entrenar con tus propias imágenes de nopales
python main.py --mode train
```

## ⚙️ Configuración Opcional

### 🔑 API Key de Roboflow (Solo si quieres usar datasets online)

<details>
<summary>🤔 ¿Necesito esto? (Haz clic para leer)</summary>

**NO es obligatorio para usar el detector básico.** Solo necesitas esto si:
- Quieres descargar datasets adicionales de internet
- Planeas entrenar modelos con datos de Roboflow

Si solo quieres usar el detector con tu cámara, ¡puedes saltar esta sección!
</details>

**Si decides configurarlo:**

1. Ve a [Roboflow.com](https://roboflow.com/) y crea una cuenta gratuita
2. Ve a **Settings → API Keys** 
3. Copia tu API key
4. Crea el archivo de configuración:
   ```bash
   cp .env.example .env
   ```
5. Edita el archivo `.env` y pega tu API key:
   ```bash
   ROBOFLOW_API_KEY=tu_api_key_aqui
   ```

### 🎛️ Ajustes de Detección

Puedes cambiar qué tan sensible es el detector editando `config/model_config.yaml`:

```yaml
# Más estricto = menos falsos positivos
confidence_threshold: 0.90  # Valores: 0.1 (permisivo) a 0.95 (estricto)

# Control de detecciones duplicadas  
iou_threshold: 0.60        # Valores: 0.1 a 0.9
```

## 📁 ¿Qué Hay en Cada Carpeta?

```
nopalDetector/                    📂 Proyecto principal
├── 📋 README.md                  → Esta documentación
├── 🚀 main.py                    → Programa principal (ejecuta desde aquí)
├── ⚙️ setup.sh                   → Instalador automático  
├── 🔍 verify_setup.py            → Verificador de instalación
├── 📦 requirements.txt           → Lista de programas necesarios
├── 🏃‍♂️ run.sh                     → Script rápido para ejecutar
│
├── config/                       📂 Configuraciones
│   ├── model_config.yaml         → Ajustes del detector
│   └── training_config.yaml      → Ajustes de entrenamiento
│
├── src/                          📂 Código fuente (cerebro del programa)
│   ├── data/                     → Gestión de imágenes y datos
│   ├── models/                   → Lógica de detección IA
│   └── utils/                    → Herramientas auxiliares
│
├── data/                         📂 Tus imágenes y datasets
│   ├── raw/                      → Imágenes originales
│   └── processed/                → Imágenes procesadas
│
├── outputs/                      📂 Resultados generados
│   ├── predictions/              → Imágenes con detecciones
│   ├── videos/                   → Videos procesados
│   └── visualizations/           → Gráficos y estadísticas
│
├── models/                       📂 Modelos de IA entrenados
│   └── weights/                  → Archivos de pesos del modelo
│
└── logs/                         📂 Registros de actividad
    └── training_logs/            → Historial de entrenamientos
```

## 🆘 Solución de Problemas Comunes

### ❌ "Command not found: python"
**Problema:** Python no está instalado o no está en el PATH
**Solución:**
1. Instala Python desde [python.org](https://python.org)
2. En macOS/Linux, prueba usar `python3` en lugar de `python`
3. Reinicia tu terminal después de instalar

### ❌ "No module named 'cv2'"
**Problema:** OpenCV no se instaló correctamente
**Solución:**
```bash
pip install opencv-python
# O reinstala todo:
pip install -r requirements.txt
```

### ❌ "No camera detected"
**Problema:** La cámara no se detecta
**Solución:**
1. Verifica que tu cámara funcione en otras aplicaciones
2. Prueba con diferentes índices de cámara:
   ```bash
   python main.py --mode camera --camera 0  # Cámara principal
   python main.py --mode camera --camera 1  # Cámara secundaria
   ```
3. En macOS: Da permisos de cámara a la Terminal

### ❌ "ModuleNotFoundError: No module named 'ultralytics'"
**Problema:** Las dependencias no se instalaron
**Solución:**
```bash
# Activa el entorno virtual primero
source venv/bin/activate
# Luego instala las dependencias
pip install -r requirements.txt
```

### ❌ Detecciones incorrectas (personas detectadas como nopales)
**Problema:** El modelo necesita ajuste de sensibilidad
**Solución:**
1. **Durante la detección:** Presiona **C** varias veces para aumentar la precisión
2. **Permanente:** Edita `config/model_config.yaml` y cambia:
   ```yaml
   confidence_threshold: 0.90  # Más estricto
   ```
3. **Usar filtros:** Presiona **F** durante la detección para activar filtros de tamaño

### ❌ "Permission denied" en macOS/Linux
**Problema:** Permisos de ejecución faltantes
**Solución:**
```bash
chmod +x setup.sh
chmod +x run.sh
```

### 🤔 ¿Nada de esto me ayuda?

1. **Verifica tu instalación:**
   ```bash
   python verify_setup.py
   ```

2. **Busca en los logs:**
   ```bash
   ls logs/  # Revisa archivos de error
   ```

3. **Reinstalación completa:**
   ```bash
   rm -rf venv/
   ./setup.sh
   ```

## 🔬 Características Técnicas Avanzadas

### 🧠 Inteligencia Artificial Implementada
- **YOLOv11:** Última versión de la familia YOLO, optimizada para velocidad y precisión
- **Detección Dual:** Modelo combinado que distingue entre nopales y personas
- **Filtros Inteligentes:** Sistema anti-falsos positivos basado en tamaño y forma
- **Procesamiento en Tiempo Real:** 30 FPS en hardware moderno

### 🎯 Sistema de Filtros Avanzado
```python
# Filtros implementados automáticamente:
✅ Filtro de confianza: 0.90 (configurable)
✅ Filtro de área: Rechaza objetos >12% del frame
✅ Filtro de aspecto: Elimina formas extremas (ratio 4:1)
✅ Filtro de tamaño mínimo: Descarta objetos <30px
✅ Control IoU: Elimina detecciones duplicadas
```

### 📊 Métricas de Rendimiento
- **Velocidad:** 30 FPS en tiempo real
- **Precisión:** >90% en condiciones ideales
- **Memoria:** ~2GB RAM durante operación
- **Compatibilidad:** CPU y GPU (CUDA)

### 🔄 Arquitectura Modular
```
Núcleo del Sistema:
├── DatasetManager     → Gestión automática de datos
├── NopalDetector      → Motor de IA YOLOv11
├── CameraDetector     → Interfaz de cámara en tiempo real
├── VideoProcessor     → Procesamiento batch de videos
└── Visualization      → Generación de gráficos y estadísticas
```

## 📈 Casos de Uso Reales

### 🌱 Agricultura de Precisión
- **Monitoreo de Cultivos:** Conteo automático de nopales en plantaciones
- **Control de Calidad:** Identificación de nopales maduros vs. jóvenes
- **Inventario Automatizado:** Estadísticas de producción en tiempo real

### 🔬 Investigación Científica  
- **Estudios de Biodiversidad:** Conteo de especies en ecosistemas
- **Monitoreo Ambiental:** Seguimiento de poblaciones de cactáceas
- **Análisis de Comportamiento:** Interacciones humano-planta

### 🎓 Educación y Demostración
- **Enseñanza de IA:** Ejemplo práctico de visión computacional
- **Workshops:** Demostración de tecnologías YOLO
- **Proyectos Estudiantiles:** Base para proyectos de ML/CV

## 🛠️ Para Desarrolladores

### 🔧 Extensión del Sistema
```python
# Ejemplo: Añadir nuevas clases de detección
from src.models.detector import NopalPersonDetector

detector = NopalPersonDetector()
# Añadir nuevas categorías es tan simple como:
# 1. Actualizar el dataset
# 2. Re-entrenar el modelo
# 3. Actualizar las configuraciones
```

### 📚 API Interna
```python
# Uso programático del detector
from src.utils.camera_detector import CameraDetector

camera = CameraDetector("path/to/weights.pt")
camera.start_detection(camera_index=0)
```

### 🧪 Testing y Validación
```bash
# Suite de pruebas incluida
python verify_setup.py           # Verificación del entorno
python -m pytest tests/         # Tests unitarios (si existen)
python main.py --mode validate  # Validación del modelo
```

## 🤝 Cómo Contribuir

### 🎯 Formas de Ayudar
1. **Reportar Bugs:** Usa GitHub Issues para reportar problemas
2. **Mejoras de Código:** Pull requests son bienvenidos
3. **Documentación:** Ayuda a mejorar esta documentación
4. **Datasets:** Contribuye con imágenes de nopales de calidad
5. **Testing:** Prueba en diferentes plataformas y reporta resultados

### 📝 Guía de Contribución
1. **Fork** el repositorio
2. **Crea** una rama para tu feature: `git checkout -b feature/amazing-feature`
3. **Commit** tus cambios: `git commit -m 'Add amazing feature'`
4. **Push** a la rama: `git push origin feature/amazing-feature`
5. **Abre** un Pull Request

### 🏆 Reconocimientos
Agradecemos a todos los contribuidores que hacen posible este proyecto:
- Dataset original: Roboflow Community
- Base YOLOv11: Ultralytics
- Inspiración: Comunidad open-source de visión computacional

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 📞 Soporte y Contacto

### 🆘 ¿Necesitas Ayuda?
1. **Documentación:** Lee este README completo
2. **Issues:** [GitHub Issues](https://github.com/crbzxy/nopalDetector/issues)
3. **Discusiones:** [GitHub Discussions](https://github.com/crbzxy/nopalDetector/discussions)

### 🚀 Próximas Características
- [ ] Interfaz web para usar sin terminal
- [ ] App móvil para detección en campo
- [ ] Modelo mejorado con más especies de cactáceas
- [ ] Integración con drones para monitoreo aéreo
- [ ] Dashboard de estadísticas en tiempo real

---

**¡Gracias por usar Nopal Detector! 🌵✨**

Si este proyecto te fue útil, ¡considera darle una estrella ⭐ en GitHub!