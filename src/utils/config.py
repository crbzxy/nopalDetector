"""
Utilidades para cargar configuración y variables de entorno
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


def load_env_vars():
    """
    Carga variables de entorno desde archivo .env si existe
    """
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            print("✅ Variables de entorno cargadas desde .env")
        else:
            print("⚠️ Archivo .env no encontrado, usando variables del sistema")
    except ImportError:
        print("⚠️ python-dotenv no instalado, usando variables del sistema")


def get_roboflow_config() -> Dict[str, Any]:
    """
    Obtiene la configuración de Roboflow desde variables de entorno
    
    Returns:
        Dict con configuración de Roboflow
        
    Raises:
        ValueError: Si no se encuentra la API key
    """
    load_env_vars()
    
    api_key = os.getenv('ROBOFLOW_API_KEY')
    if not api_key:
        raise ValueError(
            "❌ ROBOFLOW_API_KEY no encontrada. "
            "Por favor:\n"
            "1. Copia .env.example como .env\n"
            "2. Completa ROBOFLOW_API_KEY con tu API key real\n"
            "3. O exporta la variable: export ROBOFLOW_API_KEY=tu_api_key"
        )
    
    return {
        'api_key': api_key,
        'workspace': os.getenv('ROBOFLOW_WORKSPACE', 'nopaldetector'),
        'project': os.getenv('ROBOFLOW_PROJECT', 'nopal-detector-0lzvl'),
        'version': int(os.getenv('ROBOFLOW_VERSION', '2')),
        'format': 'yolov11'
    }


def load_config_with_env(config_path: str) -> Dict[str, Any]:
    """
    Carga configuración desde YAML y combina con variables de entorno
    
    Args:
        config_path: Ruta al archivo de configuración YAML
        
    Returns:
        Dict con configuración completa
    """
    # Cargar configuración base
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Sobrescribir configuración de Roboflow con variables de entorno
    try:
        config['roboflow'] = get_roboflow_config()
    except ValueError as e:
        print(f"⚠️ Error cargando configuración de Roboflow: {e}")
        # Mantener configuración del archivo YAML como fallback
        pass
    
    # Sobrescribir otros parámetros si están en variables de entorno
    if os.getenv('MODEL_CONFIDENCE_THRESHOLD'):
        config['model']['prediction']['confidence_threshold'] = float(
            os.getenv('MODEL_CONFIDENCE_THRESHOLD')
        )
    
    if os.getenv('MODEL_IOU_THRESHOLD'):
        config['model']['prediction']['iou_threshold'] = float(
            os.getenv('MODEL_IOU_THRESHOLD')
        )
    
    return config


def validate_api_key():
    """
    Valida que la API key de Roboflow esté configurada
    
    Returns:
        bool: True si está configurada correctamente
    """
    try:
        config = get_roboflow_config()
        return len(config['api_key']) > 10  # Validación básica
    except ValueError:
        return False


def setup_environment():
    """
    Configura el entorno inicial del proyecto
    """
    print("🔧 Configurando entorno...")
    
    # Cargar variables de entorno
    load_env_vars()
    
    # Verificar API key
    if validate_api_key():
        print("✅ API key de Roboflow configurada correctamente")
    else:
        print("⚠️ API key de Roboflow no configurada")
        print("   Copia .env.example como .env y completa tus credenciales")
    
    # Crear directorios necesarios
    directories = [
        'data/raw',
        'models/weights', 
        'outputs/predictions',
        'outputs/videos',
        'outputs/visualizations'
    ]
    
    project_root = Path(__file__).parent.parent.parent
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✅ Entorno configurado correctamente")