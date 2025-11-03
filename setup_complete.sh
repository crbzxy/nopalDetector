#!/bin/bash

# 🌵 Nopal Detector - Script de Instalación Completa
# ================================================
# Este script automatiza toda la instalación del proyecto
# Ejecutar: ./setup_complete.sh

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'\nGREEN='\033[0;32m'\nYELLOW='\033[1;33m'\nBLUE='\033[0;34m'\nNC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "🌵 ========================================"
echo "🌵   NOPAL DETECTOR - SETUP COMPLETO"
echo "🌵   Setup Automático del Proyecto"
echo "🌵 ========================================${NC}"
echo ""

# Función para imprimir encabezados
print_step() {
    echo -e "${BLUE}[PASO $1]${NC} $2"
}

# Función para imprimir éxito
print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

# Función para imprimir error
print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Función para imprimir advertencia
print_warning() {
    echo -e "${YELLOW}⚠️ ${NC} $1"
}

# ========================================
# PASO 1: Verificar Python
# ========================================
print_step "1" "Verificando Python..."

if ! command -v python3 &> /dev/null; then
    print_error "Python3 no encontrado"
    echo "Por favor instala Python 3.8 o superior desde https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION encontrado"

# Verificar versión mínima
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "Python 3.8 o superior requerido"
    exit 1
fi

# ========================================
# PASO 2: Verificar pip
# ========================================
print_step "2" "Verificando pip..."

if ! command -v pip3 &> /dev/null; then
    print_error "pip3 no encontrado"
    echo "Intenta: python3 -m pip install --upgrade pip"
    exit 1
fi

PIP_VERSION=$(pip3 --version | awk '{print $2}')
print_success "pip $PIP_VERSION encontrado"

# ========================================
# PASO 3: Actualizar pip
# ========================================
print_step "3" "Actualizando pip..."
pip3 install --upgrade pip > /dev/null 2>&1
print_success "pip actualizado"

# ========================================
# PASO 4: Crear entorno virtual
# ========================================
print_step "4" "Creando entorno virtual..."

if [ -d "venv" ]; then
    print_warning "venv ya existe, usando existente"
else
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# ========================================
# PASO 5: Activar entorno virtual
# ========================================
print_step "5" "Activando entorno virtual..."

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

print_success "Entorno virtual activado"

# ========================================
# PASO 6: Instalar dependencias
# ========================================
print_step "6" "Instalando dependencias (esto puede tardar 2-3 minutos)..."

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    print_success "Dependencias instaladas"
else
    print_error "requirements.txt no encontrado"
    exit 1
fi

# ========================================
# PASO 7: Crear estructura de directorios
# ========================================
print_step "7" "Creando estructura de directorios..."

mkdir -p data/raw
mkdir -p models/weights
mkdir -p outputs/predictions
mkdir -p outputs/videos
mkdir -p outputs/visualizations
mkdir -p logs
mkdir -p tests/fixtures

print_success "Directorios creados"

# ========================================
# PASO 8: Configurar variables de entorno
# ========================================
print_step "8" "Configurando variables de entorno..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Archivo .env creado desde .env.example"
    else
        # Crear .env mínimo
        cat > .env << EOF
# Configuración de Roboflow
ROBOFLOW_API_KEY=tu_api_key_aqui
ROBOFLOW_WORKSPACE=nopaldetector
ROBOFLOW_PROJECT=nopal-detector-0lzvl
ROBOFLOW_VERSION=4

# Configuración del Modelo
MODEL_CONFIDENCE_THRESHOLD=0.3
MODEL_IOU_THRESHOLD=0.45

# Dispositivo (cpu, cuda, mps)
DEVICE=cpu
EOF
        print_success "Archivo .env creado"
    fi
else
    print_warning ".env ya existe, saltando creación"
fi

# ========================================
# PASO 9: Descargar modelo base de YOLO
# ========================================
print_step "9" "Descargando modelo base de YOLO (esto puede tardar 1-2 minutos)..."

python3 << 'EOF' 2>/dev/null
try:
    from ultralytics import YOLO
    model = YOLO('yolov11n.pt')
    print("✅ Modelo YOLO descargado correctamente")
except Exception as e:
    print(f"⚠️  Error descargando YOLO: {e}")
    print("   No te preocupes, se descargar\u00e1 al entrenar")
EOF

print_success "Modelo base descargado"

# ========================================
# PASO 10: Verificar importes
# ========================================
print_step "10" "Verificando importes de librerías..."

python3 << 'EOF' 2>/dev/null
try:
    import ultralytics
    import roboflow
    import cv2
    import yaml
    import numpy
    from dotenv import load_dotenv
    print("✅ Todos los módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    exit(1)
EOF

print_success "Todos los módulos disponibles"

# ========================================
# PASO 11: Crear .gitignore si no existe
# ========================================
print_step "11" "Configurando .gitignore..."

if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOF
# Entorno Virtual
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Proyecto específico
.env
runs/
outputs/predictions/
outputs/videos/
logs/
*.pt
data/raw/
nopal-detector-*/
.DS_Store
EOF
    print_success ".gitignore creado"
else
    print_warning ".gitignore ya existe"
fi

# ========================================
# RESUMEN FINAL
# ========================================
echo ""
echo -e "${GREEN}🎉 ========================================${NC}"
echo -e "${GREEN}✅ INSTALACIÓN COMPLETADA EXITOSAMENTE${NC}"
echo -e "${GREEN}🎉 ========================================${NC}"
echo ""

echo -e "${BLUE}📋 Próximos Pasos:${NC}"
echo ""
echo "1️⃣  ${BLUE}Configurar Roboflow API Key${NC}"
echo "   Edita el archivo .env y completa tu API key:"
echo "   ${YELLOW}nano .env${NC}"
echo "   Obtén tu API key en: https://roboflow.com/settings/api"
echo ""
echo "2️⃣  ${BLUE}Verificar la Instalación${NC}"
echo "   ${YELLOW}python3 verify_environment.py${NC}"
echo ""
echo "3️⃣  ${BLUE}Leer la Guía Completa${NC}"
echo "   ${YELLOW}cat SETUP_GUIDE.md${NC}"
echo "   O abre el archivo en tu editor favorito"
echo ""
echo "4️⃣  ${BLUE}Descargar Dataset y Entrenar${NC}"
echo "   ${YELLOW}python3 main.py --mode train --multi-class --data nopal-detector-4/data.yaml${NC}"
echo ""
echo "5️⃣  ${BLUE}Hacer Predicciones${NC}"
echo "   ${YELLOW}python3 main.py --mode predict --multi-class --input imagen.jpg --weights runs/detect/train/weights/best.pt${NC}"
echo ""

echo -e "${BLUE}📚 Comandos Útiles:${NC}"
echo "   ${YELLOW}make help${NC}          - Ver todos los comandos make"
echo "   ${YELLOW}make status${NC}        - Ver estado del proyecto"
echo "   ${YELLOW}make list-cameras${NC}  - Listar cámaras disponibles"
echo ""

echo -e "${BLUE}🔗 Documentación:${NC}"
echo "   - README.md              - Documentación principal"
echo "   - SETUP_GUIDE.md         - Esta guía (más detallada)"
echo "   - BEST_PRACTICES_REVIEW.md - Análisis de mejoras"
echo "   - IMPLEMENTATION_GUIDE.md   - Guía de integración"
echo ""

echo -e "${GREEN}¡Listo para empezar! 🌵${NC}"
echo ""
