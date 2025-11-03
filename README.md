
# 🌵 Nopal Detector — guía práctica y rápida

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-orange)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Un detector multi-clase para nopales y personas basado en YOLO (Ultralytics). Esta README se centra en que puedas ejecutar el proyecto localmente de forma rápida y reproducible.

TL;DR — 3 comandos para empezar
```bash
git clone https://github.com/crbzxy/nopalDetector.git
cd nopalDetector
make install   # o: ./install.sh
```

💡 **Comandos `make` disponibles:**
```bash
make help          # Ver todos los comandos
make check-env     # Verificar instalación  
make status        # Estado del proyecto
make train         # Entrenar modelo
make predict-dir   # Predicciones en directorio
make camera        # Detección en tiempo real
```
📊 Ver [tabla completa de comandos](#comandos-make-disponibles) más abajo

Por qué usarlo
- Detección multi-clase (p. ej. `nopal`, `nopalChino`, `person`).
- Modo cámara en tiempo real, procesamiento de imágenes/video y entrenamiento personalizado.
- Integración con Roboflow para actualizar datasets.

Primeros pasos (recomendado)
1. Clona el repositorio y accede al directorio (ya mostrado en TL;DR).
2. Crea/activa un entorno virtual y asegúrate de usar el Python del `venv`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. (Opcional) Permite ejecución de scripts y genera datos de ejemplo:

```bash
chmod +x scripts/*.sh
./scripts/init_dataset.sh nopal-detector-3 "nopal,nopalChino,person"
./venv/bin/python scripts/generate_sample_dataset.py nopal-detector-3
```

Comandos principales (copiar/pegar)

### 1️⃣ Listar cámaras disponibles
```bash
python3 main.py --mode list-cameras
```

### 2️⃣ Entrenar el modelo (usar `data.yaml` creado por `init_dataset.sh` o Roboflow)
```bash
python3 main.py --mode train --multi-class --data nopal-detector-3/data.yaml
```

**Resultado:** Los pesos entrenados se guardarán en `runs/detect/trainX/weights/best.pt` (donde X es el número del run).

### 3️⃣ Realizar predicciones

#### Sobre una imagen individual:
```bash
python3 main.py --mode predict --multi-class \
  --weights runs/detect/train6/weights/best.pt \
  --input imagen.jpg
```

#### Sobre un directorio de imágenes:
```bash
# ⚠️ IMPORTANTE: La estructura del dataset debe ser:
# nopal-detector-4/
# ├── images/
# │   ├── train/
# │   ├── val/
# │   └── test/     # <-- Crea este directorio si no existe

# Opción 1: Usar el directorio de validación
python3 main.py --mode predict \
  --source nopal-detector-4/images/val \
  --weights runs/detect/train6/weights/best.pt

# Opción 2: Crear y usar directorio de test
mkdir -p nopal-detector-4/images/test
cp nopal-detector-4/images/val/* nopal-detector-4/images/test/  # Copia imágenes de ejemplo
python3 main.py --mode predict \
  --source nopal-detector-4/images/test \
  --weights runs/detect/train6/weights/best.pt
```

**Nota:** El parámetro `--source` debe apuntar a:
- Una imagen individual: `imagen.jpg`
- Un directorio existente con imágenes: `nopal-detector-4/images/val/`
- ❌ **NO** usar rutas que no existan como `nopal-detector-4/test/images`

### 4️⃣ Cámara en tiempo real (multi-clase)
```bash
python3 main.py --mode camera --multi-class \
  --weights runs/detect/train6/weights/best.pt \
  --camera 0
```

### 5️⃣ Actualizar etiquetas desde Roboflow
```bash
python3 main.py --mode update-labels --auto-update
```

Notas sobre rutas de pesos
- Los pesos de ejemplo se guardan en `runs/detect/<run>/weights/best.pt` después del entrenamiento.
- Si `runs/detect/<run>/weights/best.pt` no existe, ejecuta primero un entrenamiento de prueba o apunta a un checkpoint válido.

Comandos Make Disponibles

Puedes usar `make` para operaciones comunes. Lista completa:

| Comando | Descripción | Ejemplo |
|---------|-------------|----------|
| `make help` | Mostrar ayuda | `make help` |
| `make install` | Instalar dependencias y configurar entorno | `make install` |
| `make check-env` | Verificar configuración del entorno | `make check-env` |
| `make status` | Mostrar estado del proyecto | `make status` |
| **ENTRENAMIENTO** |
| `make train` | Entrenar modelo (requiere DATA) | `make train DATA=nopal-detector-4/data.yaml` |
| **PREDICCIÓN** |
| `make predict-image` | Predecir sobre imagen | `make predict-image WEIGHTS=runs/detect/train6/weights/best.pt INPUT=imagen.jpg` |
| `make predict-dir` | Predecir sobre directorio | `make predict-dir WEIGHTS=runs/detect/train6/weights/best.pt SOURCE=nopal-detector-4/images/val` |
| **CÁMARA** |
| `make list-cameras` | Listar cámaras disponibles | `make list-cameras` |
| `make camera` | Detección en tiempo real | `make camera WEIGHTS=runs/detect/train6/weights/best.pt CAMERA=0` |
| **UTILIDADES** |
| `make setup-test` | Crear directorio de test | `make setup-test DATASET=nopal-detector-4` |
| `make update-labels` | Actualizar etiquetas desde Roboflow | `make update-labels` |
| `make validate` | Validar modelo | `make validate WEIGHTS=runs/detect/train6/weights/best.pt DATA=nopal-detector-4/data.yaml` |
| `make clean` | Limpiar archivos temporales | `make clean` |
| `make clean-all` | Limpiar todo (venv, runs, outputs) | `make clean-all` |

**Ejemplos rápidos:**
```bash
# Setup inicial
make install
make check-env

# Ver estado
make status
make list-cameras

# Entrenar y predecir
make train DATA=nopal-detector-4/data.yaml
make predict-dir WEIGHTS=runs/detect/train6/weights/best.pt SOURCE=nopal-detector-4/images/val
```

Scripts útiles (en `scripts/`)
- `scripts/init_dataset.sh <dir> "clase1,clase2,..."` — crea la estructura YOLO y escribe `data.yaml`.
- `scripts/generate_sample_dataset.py <dir>` — genera imágenes/labels de ejemplo para pruebas rápidas.
- `scripts/train.sh <ruta/data.yaml> [ruta/pesos]` — wrapper amigable que usa el Python del venv.
- `scripts/eval.sh <ruta/data.yaml> <checkpoint>` — evalúa un checkpoint.

Configuración (.env)

**Paso 1:** Copia el archivo de ejemplo
```bash
cp .env.example .env
```

**Paso 2:** Edita `.env` y completa tu API key de Roboflow  
Obtén tu API key en: https://roboflow.com/settings/api

```bash
# MÍNIMO REQUERIDO
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4  # ⚠️ Usa versión 4 (la más reciente)

# OPCIONAL
MODEL_CONFIDENCE_THRESHOLD=0.3  # 0.3=más detecciones | 0.7=más preciso
DEVICE=cpu  # cpu | cuda (NVIDIA) | mps (Mac M1/M2/M3)
```

**Verificar configuración:**
```bash
make check-env
```

📚 **Documentación completa:** [docs/ENV_VARIABLES.md](docs/ENV_VARIABLES.md)

Solución de problemas rápida
- ModuleNotFoundError: No module named 'yaml' — activa el `venv` y ejecuta:
```bash
source venv/bin/activate
pip install -r requirements.txt
```
- `python` no encontrado en zsh: usa `python3` o activa el venv (`source venv/bin/activate`).
- Peso no encontrado (`best.pt`): comprueba `ls runs/detect/*/weights/` o entrena con `./scripts/train.sh`.

Estructura del proyecto (relevante)
```
nopalDetector/
├─ main.py                 # Entrada CLI
├─ install.sh              # Instalador rápido
├─ scripts/                # Scripts de ayuda (init, train, eval, generar muestras)
├─ src/                    # Código fuente: models, utils, data
├─ config/                 # Configs YAML
└─ runs/                   # Salidas de entrenamiento (weights, logs)
```

Métricas y clases (ejemplo)
- mAP50 (ejemplo): 49.2% — resultados varían por dataset y run.
- Clases: `['nopal', 'nopalChino', 'person']`

Contribuir
- Haz fork, crea una rama, añade tests/ejemplos y abre un PR. Sigue buenas prácticas de commits.

Contacto
- Autor: Carlos Boyzo — [crbzxy](https://github.com/crbzxy)
- GitHub: [nopalDetector](https://github.com/crbzxy/nopalDetector)
