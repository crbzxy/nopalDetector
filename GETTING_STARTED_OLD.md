# 🚀 Guía de Inicio Rápido - Nopal Detector

¡Bienvenido a Nopal Detector! Esta guía te ayudará a configurar y usar el proyecto en menos de 5 minutos.

## ⚡ Inicio Ultra-Rápido

```bash
# 1. Configurar proyecto
./run.sh setup

# 2. Verificar que todo esté bien
./run.sh verify

# 3. Entrenar modelo
./run.sh train

# 4. O usar notebook interactivo
./run.sh notebook
```

## 🎯 Lo Esencial

### ✅ Lo que SÍ necesitas hacer:

1. **Obtener API Key de Roboflow:**
   - Ve a [roboflow.com](https://roboflow.com)
   - Registrate/inicia sesión
   - Ve a Settings → API Keys
   - Copia tu API key

2. **Configurar archivo .env:**
   ```bash
   cp .env.example .env
   nano .env  # Pegar tu API key aquí
   ```

3. **Ejecutar setup:**
   ```bash
   ./run.sh setup
   ```

### ❌ Lo que NO necesitas hacer:

- ❌ Instalar YOLO manualmente
- ❌ Descargar datasets manualmente
- ❌ Configurar directorios manualmente
- ❌ Instalar dependencias una por una

## 🛠️ Comandos Útiles

| Comando | Descripción |
|---------|-------------|
| `./run.sh setup` | Configuración inicial completa |
| `./run.sh verify` | Verificar que todo esté bien |
| `./run.sh train` | Entrenar modelo |
| `./run.sh predict --input /ruta/imagenes` | Procesar imágenes |
| `./run.sh video --input video.mp4` | Procesar video |
| `./run.sh list-cameras` | Ver cámaras disponibles |
| `./run.sh camera --weights modelo.pt` | Detección en tiempo real |
| `./run.sh notebook` | Abrir Jupyter Lab |
| `./run.sh clean` | Limpiar archivos temporales |

## 📹 Detección en Tiempo Real con Cámara

### Configuración Inicial
```bash
# 1. Verificar cámaras disponibles
./run.sh list-cameras

# 2. Tener un modelo entrenado
./run.sh train  # Si no tienes modelo aún

# 3. Iniciar detección
./run.sh camera --weights models/weights/best_nopal.pt
```

### Opciones de Cámara
```bash
# Cámara específica
./run.sh camera --camera 1 --weights models/weights/best_nopal.pt

# Resolución personalizada
./run.sh camera --resolution 1280x720 --weights models/weights/best_nopal.pt

# Guardar video de la sesión
./run.sh camera --save-video --weights models/weights/best_nopal.pt

# Todas las opciones combinadas
./run.sh camera --camera 1 --resolution 1920x1080 --save-video --weights models/weights/best_nopal.pt
```

### Controles en Vivo
- **`q`**: Salir de la aplicación
- **`r`**: Iniciar/pausar grabación
- **Info en pantalla**: FPS, detecciones, tiempo

## 🎨 Configuraciones Rápidas

### Para Pruebas Rápidas (5 min):
```bash
# Editar config/model_config.yaml
training:
  epochs: 5
  batch_size: 4
  image_size: 416
```

### Para Resultados Buenos (30 min):
```bash
# Usar configuración por defecto
training:
  epochs: 50
  batch_size: 16
  image_size: 640
```

### Para Máxima Calidad (2-3 horas):
```bash
# Editar config/model_config.yaml
training:
  epochs: 100
  batch_size: 8
  image_size: 832
```

## 🐛 Problemas Comunes

### "ROBOFLOW_API_KEY not found"
```bash
# Solución:
cp .env.example .env
nano .env  # Agregar tu API key real
```

### "No module named 'ultralytics'"
```bash
# Solución:
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied: ./run.sh"
```bash
# Solución:
chmod +x run.sh setup.sh
```

### Video no se procesa
```bash
# Solución: Verificar formato
# Formatos soportados: .mp4, .avi, .mov
ffmpeg -i tu_video.mov tu_video.mp4
```

## 📁 ¿Qué Archivos Modificar?

### Para Personalizar Dataset:
- `config/model_config.yaml` → sección `roboflow`

### Para Ajustar Entrenamiento:
- `config/model_config.yaml` → sección `training`
- `config/training_config.yaml` → diferentes perfiles

### Para Cambiar Detección:
- `config/model_config.yaml` → sección `prediction`

## 🎯 Flujo Típico de Trabajo

1. **Primera vez:**
   ```bash
   ./run.sh setup
   ./run.sh verify
   ```

2. **Entrenar modelo:**
   ```bash
   ./run.sh train
   ```

3. **Probar con imágenes:**
   ```bash
   ./run.sh predict --input data/test_images/
   ```

4. **Procesar video:**
   ```bash
   ./run.sh video --input mi_video.mp4
   ```

5. **Detección en tiempo real:**
   ```bash
   # Ver cámaras disponibles
   ./run.sh list-cameras
   
   # Usar cámara
   ./run.sh camera --weights models/weights/best_nopal.pt
   ```

6. **Ver resultados:**
   - Imágenes: `outputs/predictions/`
   - Videos: `outputs/videos/`
   - Gráficos: `outputs/visualizations/`
   - Videos de cámara: `outputs/videos/camera_YYYYMMDD_HHMMSS.mp4`

## 🔧 Modo Desarrollo

Si quieres modificar el código:

```bash
# Activar entorno
source venv/bin/activate

# Modificar código en src/

# Probar cambios
python main.py --mode train

# O usar notebook para experimentar
jupyter lab notebooks/nopal_detector_training.ipynb
```

## 🆘 ¿Necesitas Ayuda?

1. **Verificar configuración:**
   ```bash
   ./run.sh verify
   ```

2. **Ver logs detallados:**
   ```bash
   python main.py --mode train --verbose
   ```

3. **Limpiar y empezar de nuevo:**
   ```bash
   ./run.sh clean
   rm -rf venv/
   ./run.sh setup
   ```

## 🎉 ¡Ya Estás Listo!

Una vez que tengas tu API key configurada, el proyecto se maneja solo. 

**¿Todo configurado?** → Ejecuta `./run.sh train` y ¡a detectar nopales! 🌵