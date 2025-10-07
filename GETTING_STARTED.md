# 🚀 Guía de Inicio Rápido - Nopal Detector

**¡Bienvenido! Esta guía te ayudará a usar el detector de nopales en menos de 5 minutos.**

## 🎯 ¿Qué Vas a Lograr?

Al final de esta guía podrás:
- ✅ Detectar nopales usando tu cámara web en tiempo real
- ✅ Procesar imágenes para encontrar nopales automáticamente  
- ✅ Entender cómo funciona el sistema sin conocimientos técnicos

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

### Paso 3: ¡Probar que Funciona!
```bash
# Verifica que todo esté bien:
python verify_setup.py
```

**¡Si ves "✅ Todo configurado correctamente", ya puedes empezar!**

## 🎮 Usar el Detector

### 🎥 Opción 1: Cámara en Tiempo Real (¡Recomendado!)

```bash
# Activa el entorno:
source venv/bin/activate

# ¡Inicia la detección!
python main.py --mode camera
```

**🎮 Controles mientras usas la cámara:**
- **Q** = Salir
- **S** = Guardar la imagen actual
- **ESPACIO** = Pausar/reanudar
- **C** = Hacer detección más estricta (menos falsos positivos)
- **V** = Hacer detección más permisiva (detecta más objetos)
- **F** = Activar/desactivar filtros inteligentes

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

### 🚨 Problemas Comunes:

**"No se encuentra la cámara"**
```bash
# Prueba con diferentes cámaras:
python main.py --mode camera --camera 0  # Cámara principal
python main.py --mode camera --camera 1  # Cámara secundaria
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

# USO DIARIO
source venv/bin/activate              # Activar entorno
python main.py --mode camera          # Cámara en tiempo real
python main.py --mode predict --source imagen.jpg  # Analizar imagen
python main.py --mode video --source video.mp4     # Procesar video

# SOLUCIÓN DE PROBLEMAS
python verify_setup.py               # Verificar instalación
./setup.sh                          # Reinstalar si hay problemas
```

## 📞 ¿Necesitas Ayuda?

1. **Primero:** Lee esta guía completa
2. **Segundo:** Ejecuta `python verify_setup.py` para diagnósticos
3. **Tercero:** Revisa las secciones de problemas comunes
4. **Último recurso:** Abre un issue en GitHub

---

**¡Disfruta detectando nopales! 🌵✨**

*Esta guía te debe haber tomado menos de 5 minutos. Si algo no está claro, ¡mejoremos la documentación juntos!*