#!/usr/bin/env python3
"""
Script de verificación para Nopal Detector
Verifica que todo esté configurado correctamente antes de usar el proyecto
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requerido. Versión actual:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_virtual_env():
    """Verificar entorno virtual"""
    if sys.prefix == sys.base_prefix:
        print("⚠️  No estás en un entorno virtual")
        print("   Ejecuta: source venv/bin/activate")
        return False
    print("✅ Entorno virtual activo")
    return True

def check_dependencies():
    """Verificar dependencias instaladas"""
    required_packages = [
        'ultralytics',
        'roboflow', 
        'opencv-python',
        'PyYAML',
        'numpy',
        'matplotlib',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'dotenv':
                import dotenv
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing)}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Verificar archivo .env"""
    if not os.path.exists('.env'):
        print("❌ Archivo .env no encontrado")
        print("   Ejecuta: cp .env.example .env")
        print("   Luego edita .env con tu API key")
        return False
    
    # Verificar contenido
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'your_roboflow_api_key_here' in content:
        print("⚠️  Archivo .env contiene valores de ejemplo")
        print("   Edita .env con tu API key real de Roboflow")
        return False
    
    if 'ROBOFLOW_API_KEY=' not in content:
        print("❌ ROBOFLOW_API_KEY no encontrada en .env")
        return False
    
    print("✅ Archivo .env configurado")
    return True

def check_directories():
    """Verificar estructura de directorios"""
    required_dirs = [
        'src',
        'config', 
        'notebooks',
        'data/raw',
        'data/processed',
        'models/weights',
        'outputs/predictions',
        'outputs/videos',
        'outputs/visualizations',
        'logs'
    ]
    
    missing = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing.append(directory)
        else:
            print(f"✅ {directory}/")
    
    if missing:
        print(f"\n⚠️  Directorios faltantes: {', '.join(missing)}")
        for dir_path in missing:
            os.makedirs(dir_path, exist_ok=True)
        print("✅ Directorios creados automáticamente")
    
    return True

def check_config_files():
    """Verificar archivos de configuración"""
    config_files = [
        'config/model_config.yaml',
        'config/training_config.yaml'
    ]
    
    for config_file in config_files:
        if not os.path.exists(config_file):
            print(f"❌ {config_file} no encontrado")
            return False
        print(f"✅ {config_file}")
    
    return True

def check_notebook():
    """Verificar notebook"""
    notebook_path = 'notebooks/nopal_detector_training.ipynb'
    if not os.path.exists(notebook_path):
        print(f"❌ {notebook_path} no encontrado")
        return False
    print(f"✅ {notebook_path}")
    return True

def check_api_key():
    """Verificar API key de Roboflow"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('ROBOFLOW_API_KEY')
        if not api_key or api_key == 'your_roboflow_api_key_here':
            print("❌ API key de Roboflow no configurada")
            print("   1. Ve a https://roboflow.com/")
            print("   2. Obtén tu API key")
            print("   3. Edita .env: ROBOFLOW_API_KEY=tu_api_key")
            return False
        
        if len(api_key) < 20:
            print("⚠️  API key parece inválida (muy corta)")
            return False
            
        print("✅ API key de Roboflow configurada")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando API key: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificando configuración de Nopal Detector...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_env),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Directory Structure", check_directories),
        ("Config Files", check_config_files),
        ("Notebook", check_notebook),
        ("API Key", check_api_key),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        result = check_func()
        results.append(result)
    
    print("\n" + "="*50)
    
    if all(results):
        print("🎉 ¡Todo configurado correctamente!")
        print("\n🚀 Puedes empezar a usar el proyecto:")
        print("   python main.py --mode train")
        print("   jupyter lab notebooks/nopal_detector_training.ipynb")
    else:
        failed = sum(1 for r in results if not r)
        print(f"❌ {failed} verificaciones fallaron")
        print("\n🔧 Sigue las instrucciones arriba para corregir los problemas")
        print("   Luego ejecuta este script nuevamente")
        sys.exit(1)

if __name__ == "__main__":
    main()