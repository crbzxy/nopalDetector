#!/bin/bash

# Script de configuración inicial para Nopal Detector
echo "🌵 Configurando Nopal Detector..."

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar Python
if ! command_exists python3; then
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.8 o superior."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verificar pip
if ! command_exists pip3; then
    echo "❌ pip3 no encontrado. Por favor instala pip."
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env desde plantilla..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Debes editar el archivo .env con tu API key de Roboflow"
else
    echo "✅ Archivo .env ya existe"
fi

# Verificar si ya existe API key en .env
if grep -q "your_roboflow_api_key_here" .env 2>/dev/null; then
    echo "⚠️  Tu archivo .env aún contiene valores de ejemplo"
    echo "   Por favor edita .env y configura tu ROBOFLOW_API_KEY real"
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Crear directorios necesarios
echo "📁 Creando estructura de directorios..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models/weights
mkdir -p outputs/predictions
mkdir -p outputs/videos
mkdir -p outputs/visualizations
mkdir -p logs

# Verificar instalación de dependencias clave
echo "🔍 Verificando instalación..."
python3 -c "import ultralytics; print('✅ Ultralytics instalado')" 2>/dev/null || echo "❌ Error con Ultralytics"
python3 -c "import roboflow; print('✅ Roboflow instalado')" 2>/dev/null || echo "❌ Error con Roboflow"
python3 -c "import cv2; print('✅ OpenCV instalado')" 2>/dev/null || echo "❌ Error con OpenCV"
python3 -c "import dotenv; print('✅ python-dotenv instalado')" 2>/dev/null || echo "❌ Error con python-dotenv"

echo ""
echo "🎉 Configuración completada!"
echo ""
echo "📋 PASOS SIGUIENTES:"
echo "1. 🔑 Configurar API key:"
echo "   - Edita el archivo .env"
echo "   - Cambia 'your_roboflow_api_key_here' por tu API key real"
echo "   - Obtén tu API key en: https://roboflow.com/"
echo ""
echo "2. 🚀 Activar entorno y usar:"
echo "   source venv/bin/activate"
echo "   python main.py --mode train"
echo ""
echo "3. 📓 O usar el notebook:"
echo "   jupyter lab notebooks/nopal_detector_training.ipynb"
echo ""
echo "📖 Para más información, consulta el README.md"