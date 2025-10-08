#!/usr/bin/env python3
"""
"""
🧪 Script de Prueba Integral - Nopal Detector
Verifica todas las funcionalidades principales del sistema
"""
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path

def print_header(title):
    """Imprimi        print("💡 PRÓXIMOS PASOS:")
        print("   1. Probar actualización: python update_labels.py")
        print("   2. Entrenar modelo: python main.py --mode train --multi-class")
        print("   3. Probar detección: python main.py --mode predict --input imagen.jpg --multi-class")cabezado de sección"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔄 {description}")
    print(f"📝 Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Éxito!")
            if result.stdout.strip():
                print(f"📄 Salida:\n{result.stdout}")
        else:
            print("❌ Error!")
            print(f"🚨 Error: {result.stderr}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def check_file_exists(file_path, description):
    """Verificar que un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description} no encontrado: {file_path}")
        return False

def test_label_updater():
    """Probar el sistema de actualización de etiquetas"""
    print_header("PRUEBA DE ACTUALIZACIÓN DE ETIQUETAS")
    
    # Verificar que existe el archivo update_labels.py
    if not check_file_exists("update_labels.py", "Script de actualización"):
        return False
    
    # Probar la clase LabelUpdater
    print("\n🔍 Probando LabelUpdater...")
    
    test_code = """
import sys
sys.path.append('.')
from update_labels import LabelUpdater
import yaml

# Cargar configuración
with open('config/model_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Crear updater
updater = LabelUpdater(config)
print("✅ LabelUpdater creado exitosamente")

# Verificar configuración actual
print(f"📊 Dataset actual: nopal-detector-{updater.current_version}")
print(f"🔗 Workspace: {updater.workspace_id}")
print(f"📋 Proyecto: {updater.project_name}")
"""
    
    try:
        exec(test_code)
        return True
    except Exception as e:
        print(f"❌ Error probando LabelUpdater: {e}")
        return False

def test_multi_class_detector():
    """Probar el detector multi-clase"""
    print_header("PRUEBA DE DETECTOR MULTI-CLASE")
    
    # Verificar que existe el archivo
    if not check_file_exists("src/models/multi_class_detector.py", "Detector multi-clase"):
        return False
    
    # Probar la clase MultiClassDetector
    print("\n🔍 Probando MultiClassDetector...")
    
    test_code = """
import sys
sys.path.append('src')
from models.multi_class_detector import MultiClassDetector
import yaml

# Cargar configuración
with open('config/model_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Crear detector
detector = MultiClassDetector(config)
print("✅ MultiClassDetector creado exitosamente")
print(f"🏷️ Clases cargadas: {detector.class_names}")
print(f"🎨 Colores generados: {len(detector.class_colors)} colores")
"""
    
    try:
        exec(test_code)
        return True
    except Exception as e:
        print(f"❌ Error probando MultiClassDetector: {e}")
        return False

def test_config_files():
    """Verificar archivos de configuración"""
    print_header("VERIFICACIÓN DE CONFIGURACIÓN")
    
    config_files = [
        ("config/model_config.yaml", "Configuración del modelo"),
        ("config/training_config.yaml", "Configuración de entrenamiento"),
        ("nopal-detector-2/data.yaml", "Dataset configuration")
    ]
    
    all_good = True
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            all_good = False
        else:
            # Verificar que se puede cargar
            try:
                with open(file_path, 'r') as f:
                    data = yaml.safe_load(f)
                print(f"   📋 Contenido válido YAML")
            except Exception as e:
                print(f"   ❌ Error leyendo YAML: {e}")
                all_good = False
    
    return all_good

def test_dataset_structure():
    """Verificar estructura del dataset"""
    print_header("VERIFICACIÓN DE DATASET")
    
    dataset_dirs = [
        "nopal-detector-2/train/images",
        "nopal-detector-2/train/labels", 
        "nopal-detector-2/valid/images",
        "nopal-detector-2/valid/labels",
        "nopal-detector-2/test/images",
        "nopal-detector-2/test/labels"
    ]
    
    all_good = True
    for dir_path in dataset_dirs:
        if os.path.exists(dir_path):
            count = len([f for f in os.listdir(dir_path) if not f.startswith('.')])
            print(f"✅ {dir_path}: {count} archivos")
        else:
            print(f"❌ {dir_path}: no encontrado")
            all_good = False
    
    return all_good

def test_model_weights():
    """Verificar pesos del modelo"""
    print_header("VERIFICACIÓN DE MODELOS")
    
    model_paths = [
        "yolo11s.pt",
        "runs/detect/train2/weights/best.pt",
        "runs/detect/train2/weights/last.pt"
    ]
    
    weights_found = 0
    for model_path in model_paths:
        if check_file_exists(model_path, f"Modelo {model_path}"):
            weights_found += 1
            
            # Verificar tamaño del archivo
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"   📏 Tamaño: {size_mb:.1f} MB")
    
    return weights_found > 0

def test_integration():
    """Prueba de integración básica"""
    print_header("PRUEBA DE INTEGRACIÓN")
    
    # Verificar que se puede importar todo
    print("\n🔍 Probando imports...")
    
    try:
        # Test import de update_labels
        from update_labels import LabelUpdater
        print("✅ update_labels importado")
        
        # Test import básico de configuración
        import yaml
        with open('config/model_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✅ Configuración cargada")
        
        # Test de creación de objetos principales
        updater = LabelUpdater(config)
        print("✅ LabelUpdater instanciado")
        
        print("✅ Todos los imports y instanciaciones exitosas")
        return True
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    print("🌵 =======================================")
    print("🌵   NOPAL DETECTOR - TESTS")
    print("🌵   Prueba Integral del Sistema")
    print("🌵 =======================================")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        return False
    
    # Lista de pruebas
    tests = [
        ("Configuración", test_config_files),
        ("Dataset", test_dataset_structure),
        ("Modelos", test_model_weights),
        ("Actualización de Etiquetas", test_label_updater),
        ("Detector Multi-Clase", test_multi_class_detector),
        ("Integración", test_integration)
    ]
    
    # Ejecutar pruebas
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Error en prueba {test_name}: {e}")
            results[test_name] = False
    
    # Mostrar resumen
    print_header("RESUMEN DE PRUEBAS")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Sistema listo para usar.")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Probar actualización: python update_labels.py")
        print("   2. Entrenar modelo: python main_v3.py --mode train --multi-class")
        print("   3. Probar detección: python main_v3.py --mode predict --input imagen.jpg --multi-class")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)