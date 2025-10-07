#!/bin/bash

# Script de instalación para Nopal Detector
echo "🌵 Instalando Nopal Detector..."

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p data/raw
mkdir -p models/weights
mkdir -p outputs/predictions
mkdir -p outputs/videos
mkdir -p outputs/visualizations

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tu API key de Roboflow"
fi

echo "✅ Instalación completada!"
echo ""
echo "⚠️  CONFIGURACIÓN REQUERIDA:"
echo "   1. Edita el archivo .env con tu API key de Roboflow"
echo "   2. ROBOFLOW_API_KEY=tu_api_key_aqui"
echo ""
echo "🚀 Para usar el proyecto:"
echo "   source venv/bin/activate"
echo "   python main.py --mode train"
echo ""
echo "📓 O abrir el notebook:"
echo "   jupyter lab notebooks/nopal_detector_training.ipynb"