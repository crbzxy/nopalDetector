#!/usr/bin/env python3
"""
🔍 Verificador de Configuración - Nopal Detector
Diagnóstica y verifica que todo esté listo para usar el detector de nopales
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Mostrar header bonito"""
    print("🌵" * 20)
    print("🔍 VERIFICADOR DE CONFIGURACIÓN")
    print("   Nopal Detector v1.0")
    print("🌵" * 20)
    print()

def check_python_version():
    """Verificar versión de Python"""
    print("📋 Verificando Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ requerido. Versión actual: {version.major}.{version.minor}")
        print("   💡 Solución: Instala Python 3.8+ desde python.org")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - ¡Perfecto!")
    return True

def check_virtual_env():
    """Verificar entorno virtual"""
    print("\n📦 Verificando entorno virtual...")
    if sys.prefix == sys.base_prefix:
        print("⚠️  No estás en un entorno virtual")
        print("   💡 Solución: Ejecuta 'source venv/bin/activate'")
        print("   💡 Si no existe: Ejecuta './setup.sh' primero")
        return False
    print("✅ Entorno virtual activo - ¡Correcto!")
    return True

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("\n📚 Verificando librerías necesarias...")
    required_packages = [
        ('ultralytics', 'ultralytics', 'Motor de inteligencia artificial YOLOv11'),
        ('roboflow', 'roboflow', 'Gestión de datasets'), 
        ('opencv-python', 'cv2', 'Procesamiento de imágenes y cámara'),
        ('PyYAML', 'yaml', 'Archivos de configuración'),
        ('numpy', 'numpy', 'Cálculos matemáticos'),
        ('matplotlib', 'matplotlib', 'Gráficos y visualizaciones'),
        ('python-dotenv', 'dotenv', 'Variables de entorno seguras')
    ]
    
    missing = []
    for package_name, import_name, description in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} ({description})")
        except ImportError:
            print(f"❌ {package_name} - {description}")
            missing.append(package_name)
    
    if missing:
        print(f"\n⚠️  Librerías faltantes: {', '.join(missing)}")
        print("   💡 Solución: pip install -r requirements.txt")
        print("   💡 O ejecuta: ./setup.sh")
        return False
    
    print("✅ Todas las librerías están instaladas")
    return True

def check_env_file():
    """Verificar archivo .env"""
    print("\n🔑 Verificando configuración de API...")
    
    if not os.path.exists('.env'):
        print("⚠️  Archivo .env no encontrado")
        print("   💡 Esto es OPCIONAL si solo usas la cámara")
        print("   💡 Para datasets: cp .env.example .env")
        return True  # No es crítico para uso básico
    
    # Verificar contenido
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'your_roboflow_api_key_here' in content:
        print("⚠️  Archivo .env contiene valores de ejemplo")
        print("   💡 Para datasets: Edita .env con tu API key real")
        return True  # No es crítico
    
    if 'ROBOFLOW_API_KEY=' in content:
        print("✅ API key configurada (para datasets online)")
    else:
        print("ℹ️  Sin API key (solo cámara local disponible)")
    
    return True

def check_directories():
    """Verificar estructura de directorios"""
    print("\n📁 Verificando estructura de carpetas...")
    required_dirs = [
        ('src', 'Código fuente del proyecto'),
        ('config', 'Archivos de configuración'), 
        ('notebooks', 'Cuadernos interactivos'),
        ('data/raw', 'Datos originales'),
        ('data/processed', 'Datos procesados'),
        ('models/weights', 'Modelos entrenados'),
        ('outputs/predictions', 'Resultados de detecciones'),
        ('outputs/videos', 'Videos procesados'),
        ('outputs/visualizations', 'Gráficos y estadísticas'),
        ('logs', 'Registros del sistema')
    ]
    
    missing = []
    for directory, description in required_dirs:
        if not os.path.exists(directory):
            missing.append(directory)
            print(f"⚠️  {directory}/ - {description}")
        else:
            print(f"✅ {directory}/ - {description}")
    
    if missing:
        print(f"\n🔧 Creando carpetas faltantes...")
        for dir_path in missing:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Creada: {dir_path}/")
    
    return True

def check_config_files():
    """Verificar archivos de configuración"""
    print("\n⚙️ Verificando archivos de configuración...")
    config_files = [
        ('config/model_config.yaml', 'Configuración del modelo IA'),
        ('config/training_config.yaml', 'Configuración de entrenamiento')
    ]
    
    all_good = True
    for config_file, description in config_files:
        if not os.path.exists(config_file):
            print(f"❌ {config_file} - {description}")
            all_good = False
        else:
            print(f"✅ {config_file} - {description}")
    
    return all_good

def check_main_files():
    """Verificar archivos principales"""
    print("\n📄 Verificando archivos principales...")
    main_files = [
        ('main.py', 'Programa principal'),
        ('notebooks/nopal_detector_training.ipynb', 'Cuaderno interactivo'),
        ('requirements.txt', 'Lista de dependencias'),
        ('setup.sh', 'Script de instalación'),
        ('.env.example', 'Plantilla de configuración')
    ]
    
    all_good = True
    for file_path, description in main_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} - {description}")
            all_good = False
        else:
            print(f"✅ {file_path} - {description}")
    
    return all_good

def check_camera():
    """Verificar acceso a cámara"""
    print("\n📹 Verificando acceso a cámara...")
    try:
        import cv2
        # Intentar abrir cámara 0
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Cámara 0 detectada y accesible")
            cap.release()
            
            # Probar cámara 1 también
            cap1 = cv2.VideoCapture(1)
            if cap1.isOpened():
                print("✅ Cámara 1 también disponible")
                cap1.release()
            else:
                print("ℹ️  Solo cámara 0 disponible")
        else:
            print("⚠️  No se puede acceder a la cámara")
            print("   💡 Verifica permisos de cámara en Configuración del Sistema")
            return False
    except Exception as e:
        print(f"❌ Error verificando cámara: {e}")
        return False
    
    return True

def check_models():
    """Verificar modelos disponibles"""
    print("\n🤖 Verificando modelos de IA...")
    
    # Verificar modelo base YOLOv11
    base_model = 'yolo11s.pt'
    if os.path.exists(base_model):
        print(f"✅ {base_model} - Modelo base YOLOv11")
    else:
        print(f"ℹ️  {base_model} se descargará automáticamente al usar")
    
    # Verificar modelo entrenado
    trained_model = 'runs/detect/train/weights/best.pt'
    if os.path.exists(trained_model):
        print(f"✅ {trained_model} - Modelo personalizado entrenado")
    else:
        print(f"ℹ️  {trained_model} se creará después del entrenamiento")
    
    return True

def check_api_key():
    """Verificar API key de Roboflow (opcional)"""
    print("\n🔑 Verificando API key de Roboflow...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('ROBOFLOW_API_KEY')
        if not api_key or api_key == 'your_roboflow_api_key_here':
            print("ℹ️  API key de Roboflow no configurada")
            print("   💡 Esto es OPCIONAL para uso con cámara")
            print("   💡 Para datasets online: Ve a https://roboflow.com/")
            return True  # No crítico
        
        if len(api_key) < 20:
            print("⚠️  API key parece inválida (muy corta)")
            return True  # No crítico
            
        print("✅ API key de Roboflow configurada")
        return True
        
    except Exception as e:
        print(f"ℹ️  No se pudo verificar API key: {e}")
        return True  # No crítico
    
    # Verificar modelo entrenado
    trained_model = 'runs/detect/train/weights/best.pt'
    if os.path.exists(trained_model):
        print(f"✅ {trained_model} - Modelo personalizado entrenado")
    else:
        print(f"ℹ️  {trained_model} se creará después del entrenamiento")
    
    return True

def check_api_key():
    """Verificar API key de Roboflow (opcional)"""
    print("\n🔑 Verificando API key de Roboflow...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('ROBOFLOW_API_KEY')
        if not api_key or api_key == 'your_roboflow_api_key_here':
            print("ℹ️  API key de Roboflow no configurada")
            print("   💡 Esto es OPCIONAL para uso con cámara")
            print("   💡 Para datasets online: Ve a https://roboflow.com/")
            return True  # No crítico
        
        if len(api_key) < 20:
            print("⚠️  API key parece inválida (muy corta)")
            return True  # No crítico
            
        print("✅ API key de Roboflow configurada")
        return True
        
    except Exception as e:
        print(f"ℹ️  No se pudo verificar API key: {e}")
        return True  # No crítico

def print_usage_guide():
    """Mostrar guía de uso"""
    print("\n" + "🌵" * 30)
    print("🚀 GUÍA DE USO RÁPIDO")
    print("🌵" * 30)
    
    print("\n📹 Para detección con cámara en tiempo real:")
    print("   source venv/bin/activate")
    print("   python main.py --mode camera")
    
    print("\n📸 Para analizar una imagen:")
    print("   python main.py --mode predict --source imagen.jpg")
    
    print("\n🎬 Para procesar un video:")
    print("   python main.py --mode video --source video.mp4")
    
    print("\n🎓 Para entrenar tu propio modelo:")
    print("   python main.py --mode train")
    
    print("\n📔 Para usar el cuaderno interactivo:")
    print("   jupyter lab notebooks/nopal_detector_training.ipynb")
    
    print("\n🆘 Si algo no funciona:")
    print("   1. Lee GETTING_STARTED.md")
    print("   2. Ejecuta ./setup.sh")
    print("   3. Ejecuta este verificador nuevamente")

def main():
    """Función principal mejorada"""
    print_header()
    
    checks = [
        ("Python Version", check_python_version, True),
        ("Virtual Environment", check_virtual_env, True),
        ("Dependencies", check_dependencies, True),
        ("Directory Structure", check_directories, False),
        ("Config Files", check_config_files, True),
        ("Main Files", check_main_files, True),
        ("Camera Access", check_camera, False),
        ("Models", check_models, False),
        ("API Key", check_api_key, False),
    ]
    
    results = []
    critical_failed = False
    
    for name, check_func, is_critical in checks:
        result = check_func()
        results.append(result)
        
        if not result and is_critical:
            critical_failed = True
    
    print("\n" + "🌵" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("🌵" * 50)
    
    if not critical_failed:
        print("🎉 ¡CONFIGURACIÓN EXITOSA!")
        print("✅ Todos los componentes críticos están listos")
        
        if not all(results):
            warnings = sum(1 for r in results if not r)
            print(f"⚠️  {warnings} advertencias no críticas")
        
        print_usage_guide()
        
    else:
        failed = sum(1 for i, r in enumerate(results) if not r and checks[i][2])
        print(f"❌ {failed} VERIFICACIONES CRÍTICAS FALLARON")
        print("\n🔧 ACCIONES REQUERIDAS:")
        print("   1. Sigue las instrucciones de arriba ☝️")
        print("   2. Ejecuta: ./setup.sh")
        print("   3. Ejecuta: python verify_setup.py")
        print("\n💡 Lee GETTING_STARTED.md para ayuda detallada")
        sys.exit(1)

if __name__ == "__main__":
    main()