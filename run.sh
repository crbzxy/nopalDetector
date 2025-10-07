#!/bin/bash

# Script de ejecución rápida para Nopal Detector
# Maneja activación del entorno virtual y ejecución del proyecto

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo "🌵 Nopal Detector - Script de Ejecución"
    echo ""
    echo "Uso: ./run.sh [COMANDO] [OPCIONES]"
    echo ""
    echo "Comandos disponibles:"
    echo "  setup      - Configurar proyecto por primera vez"
    echo "  verify     - Verificar que todo esté configurado"
    echo "  train      - Entrenar modelo"
    echo "  predict    - Hacer predicciones en imágenes"
    echo "  video      - Procesar video"
    echo "  camera     - Detección en tiempo real con cámara"
    echo "  list-cameras - Listar cámaras disponibles"
    echo "  notebook   - Abrir Jupyter Lab"
    echo "  clean      - Limpiar archivos temporales"
    echo ""
    echo "Ejemplos:"
    echo "  ./run.sh setup"
    echo "  ./run.sh train"
    echo "  ./run.sh predict --input /ruta/imagenes"
    echo "  ./run.sh video --input video.mp4"
    echo "  ./run.sh list-cameras"
    echo "  ./run.sh camera --weights models/weights/best_nopal.pt"
    echo "  ./run.sh camera --camera 1 --save-video --resolution 1280x720"
    echo "  ./run.sh notebook"
}

# Función para activar entorno virtual
activate_venv() {
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo -e "${GREEN}✅ Entorno virtual activado${NC}"
    else
        echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
        echo "Ejecuta: ./run.sh setup"
        exit 1
    fi
}

# Función para verificar configuración
check_config() {
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ Archivo .env no encontrado${NC}"
        echo "Ejecuta: ./run.sh setup"
        exit 1
    fi
    
    if grep -q "your_roboflow_api_key_here" .env; then
        echo -e "${YELLOW}⚠️  Necesitas configurar tu API key en .env${NC}"
        exit 1
    fi
}

# Comando: setup
cmd_setup() {
    echo -e "${BLUE}🛠️  Configurando Nopal Detector...${NC}"
    ./setup.sh
}

# Comando: verify
cmd_verify() {
    echo -e "${BLUE}🔍 Verificando configuración...${NC}"
    activate_venv
    python verify_setup.py
}

# Comando: train
cmd_train() {
    echo -e "${BLUE}🤖 Entrenando modelo...${NC}"
    activate_venv
    check_config
    python main.py --mode train "$@"
}

# Comando: predict
cmd_predict() {
    echo -e "${BLUE}🖼️  Realizando predicciones...${NC}"
    activate_venv
    check_config
    python main.py --mode predict "$@"
}

# Comando: video
cmd_video() {
    echo -e "${BLUE}🎥 Procesando video...${NC}"
    activate_venv
    check_config
    python main.py --mode video "$@"
}

# Comando: camera
cmd_camera() {
    echo -e "${BLUE}📹 Iniciando detección en tiempo real...${NC}"
    activate_venv
    check_config
    python main.py --mode camera "$@"
}

# Comando: list-cameras
cmd_list_cameras() {
    echo -e "${BLUE}🎥 Listando cámaras disponibles...${NC}"
    activate_venv
    python main.py --mode list-cameras
}

# Comando: notebook
cmd_notebook() {
    echo -e "${BLUE}📓 Abriendo Jupyter Lab...${NC}"
    activate_venv
    check_config
    
    # Verificar si jupyter está instalado
    if ! command -v jupyter &> /dev/null; then
        echo -e "${YELLOW}⚠️  Jupyter no encontrado, instalando...${NC}"
        pip install jupyterlab
    fi
    
    jupyter lab notebooks/nopal_detector_training.ipynb
}

# Comando: clean
cmd_clean() {
    echo -e "${BLUE}🧹 Limpiando archivos temporales...${NC}"
    
    # Limpiar caches de Python
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Limpiar runs de YOLO
    rm -rf runs/ 2>/dev/null || true
    
    # Limpiar logs
    rm -rf logs/*.log 2>/dev/null || true
    
    # Limpiar checkpoints de Jupyter
    find . -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
    
    echo -e "${GREEN}✅ Limpieza completada${NC}"
}

# Función principal
main() {
    # Si no hay argumentos, mostrar ayuda
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    # Obtener comando
    COMMAND=$1
    shift  # Remover primer argumento
    
    # Ejecutar comando
    case $COMMAND in
        "setup")
            cmd_setup "$@"
            ;;
        "verify")
            cmd_verify "$@"
            ;;
        "train")
            cmd_train "$@"
            ;;
        "predict")
            cmd_predict "$@"
            ;;
        "video")
            cmd_video "$@"
            ;;
        "camera")
            cmd_camera "$@"
            ;;
        "list-cameras")
            cmd_list_cameras "$@"
            ;;
        "notebook")
            cmd_notebook "$@"
            ;;
        "clean")
            cmd_clean "$@"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Comando desconocido: $COMMAND${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"