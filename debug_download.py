#!/usr/bin/env python3
"""
🔧 Debug y Descarga Manual de Dataset v3
"""

import os
import yaml
from roboflow import Roboflow
from dotenv import load_dotenv

def manual_download():
    """Descarga manual del dataset v3 con debug detallado"""
    load_dotenv()
    
    api_key = os.getenv('ROBOFLOW_API_KEY')
    
    if not api_key:
        print("❌ Error: ROBOFLOW_API_KEY no configurado")
        return
    
    # Configuración
    workspace_id = "nopaldetector"
    project_name = "nopal-detector-0lzvl"
    version_num = 3
    
    try:
        print(f"🔗 Conectando a Roboflow...")
        rf = Roboflow(api_key=api_key)
        project = rf.workspace(workspace_id).project(project_name)
        
        print(f"📥 Obteniendo versión {version_num}...")
        version = project.version(version_num)
        
        print(f"📊 Información de la versión:")
        print(f"   - Versión: {version.version}")
        print(f"   - ID: {version.id}")
        
        # Intentar obtener más información
        try:
            print(f"📋 Intentando obtener clases...")
            
            # Múltiples métodos para obtener clases
            if hasattr(version, 'classes'):
                print(f"   Clases (method 1): {version.classes}")
            
            if hasattr(version, 'model') and hasattr(version.model, 'classes'):
                print(f"   Clases (method 2): {version.model.classes}")
                
            # También ver qué otros atributos tiene
            print(f"🔍 Atributos de version: {[attr for attr in dir(version) if not attr.startswith('_')]}")
            
        except Exception as e:
            print(f"⚠️ Error obteniendo clases: {e}")
        
        # Descargar dataset con nombre específico
        print(f"📥 Descargando dataset versión {version_num}...")
        download_location = f"./nopal-detector-{version_num}"
        dataset = version.download("yolov11", location=download_location)
        
        print(f"✅ Dataset descargado en: {dataset.location}")
        
        # Buscar el archivo data.yaml en varias ubicaciones posibles
        possible_paths = [
            os.path.join(dataset.location, 'data.yaml'),
            os.path.join(download_location, 'data.yaml'),
            f"./nopal-detector-{version_num}/data.yaml",
            "./data.yaml"
        ]
        
        found_data_yaml = False
        for data_yaml_path in possible_paths:
            if os.path.exists(data_yaml_path):
                print(f"📄 Encontrado data.yaml en: {data_yaml_path}")
                with open(data_yaml_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    print(f"🏷️ Clases en data.yaml: {data.get('names', [])}")
                    print(f"📊 Número de clases: {data.get('nc', 'No especificado')}")
                    found_data_yaml = True
                break
        
        if not found_data_yaml:
            print("⚠️ No se encontró data.yaml en ninguna ubicación")
            # Listar contenido del directorio descargado
            if hasattr(dataset, 'location') and os.path.exists(dataset.location):
                print(f"📁 Contenido de {dataset.location}:")
                for item in os.listdir(dataset.location):
                    print(f"   - {item}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manual_download()