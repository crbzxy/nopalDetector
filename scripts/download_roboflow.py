#!/usr/bin/env python3
"""
🌵 Nopal Detector - Roboflow Dataset Downloader
Descarga el dataset desde Roboflow con configuración automática
"""

import os
import sys
from pathlib import Path
import yaml

def download_dataset(api_key=None, workspace=None, project=None, version=None):
    """
    Descarga el dataset desde Roboflow
    
    Args:
        api_key: API key de Roboflow (opcional, se puede usar variable de entorno)
        workspace: Nombre del workspace
        project: Nombre del proyecto
        version: Versión del dataset
    """
    try:
        from roboflow import Roboflow
    except ImportError:
        print("❌ Error: roboflow no está instalado")
        print("💡 Ejecuta: pip install roboflow")
        sys.exit(1)
    
    # Cargar configuración desde model_config.yaml si existe
    config_path = Path(__file__).parent.parent / "config" / "model_config.yaml"
    
    if config_path.exists():
        print(f"📄 Cargando configuración desde {config_path}")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            rf_config = config.get('roboflow', {})
            
            workspace = workspace or rf_config.get('workspace')
            project = project or rf_config.get('project')
            version = version or rf_config.get('version')
    
    # Obtener API key
    api_key = api_key or os.getenv('ROBOFLOW_API_KEY')
    
    if not api_key:
        print("❌ Error: API key no proporcionada")
        print("💡 Opciones:")
        print("   1. Exporta: export ROBOFLOW_API_KEY='tu_api_key'")
        print("   2. Pásala como argumento: --api-key tu_api_key")
        sys.exit(1)
    
    if not all([workspace, project, version]):
        print("❌ Error: Faltan parámetros de Roboflow")
        print("💡 Asegúrate de que config/model_config.yaml está configurado correctamente")
        sys.exit(1)
    
    print("🌵 =======================================")
    print("🌵   ROBOFLOW DATASET DOWNLOADER")
    print("🌵 =======================================")
    print(f"📦 Workspace: {workspace}")
    print(f"📂 Proyecto: {project}")
    print(f"🔢 Versión: {version}")
    print()
    
    # Inicializar Roboflow
    print("🔐 Conectando a Roboflow...")
    rf = Roboflow(api_key=api_key)
    
    # Obtener proyecto
    print(f"📥 Descargando proyecto...")
    project_obj = rf.workspace(workspace).project(project)
    version_obj = project_obj.version(version)
    
    # Descargar dataset
    print("⬇️ Descargando dataset (esto puede tardar unos minutos)...")
    dataset = version_obj.download("yolov11")
    
    print()
    print(f"✅ Dataset descargado exitosamente!")
    print(f"📁 Ubicación: {dataset.location}")
    print()
    print("🎯 Próximos pasos:")
    print(f"   1. Entrenar: python3 main.py --mode train --multi-class --data {dataset.location}/data.yaml")
    print(f"   2. O usar scripts/train.sh {dataset.location}/data.yaml")
    
    return dataset.location

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Descargar dataset desde Roboflow')
    parser.add_argument('--api-key', help='API key de Roboflow')
    parser.add_argument('--workspace', help='Nombre del workspace')
    parser.add_argument('--project', help='Nombre del proyecto')
    parser.add_argument('--version', type=int, help='Versión del dataset')
    
    args = parser.parse_args()
    
    try:
        download_dataset(
            api_key=args.api_key,
            workspace=args.workspace,
            project=args.project,
            version=args.version
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
