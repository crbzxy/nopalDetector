"""
Script principal para ejecutar el detector de nopales desde línea de comandos
"""

import argparse
import sys
import os
import yaml
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

from data.dataset_manager import DatasetManager
from models.detector import NopalPersonDetector
from utils.visualization import ResultVisualizer
from utils.config import load_config_with_env, setup_environment


def main():
    parser = argparse.ArgumentParser(description='Nopal Detector con YOLOv11')
    parser.add_argument('--config', default='config/model_config.yaml', 
                       help='Ruta al archivo de configuración')
    parser.add_argument('--mode', choices=['train', 'predict', 'video'], 
                       required=True, help='Modo de operación')
    parser.add_argument('--input', help='Ruta de entrada (imagen, video o directorio)')
    parser.add_argument('--output', help='Ruta de salida')
    parser.add_argument('--weights', help='Ruta a los pesos del modelo entrenado')
    
    args = parser.parse_args()
    
    # Configurar entorno
    setup_environment()
    
    # Cargar configuración con variables de entorno
    config = load_config_with_env(args.config)
    
    if args.mode == 'train':
        print("🚀 Iniciando entrenamiento...")
        
        # Inicializar dataset manager
        dataset_manager = DatasetManager(config)
        
        # Descargar y preparar dataset
        dataset_location = dataset_manager.download_dataset()
        dataset_manager.prepare_dataset()
        data_yaml_path = dataset_manager.get_data_yaml_path()
        
        # Entrenar modelo
        detector = NopalPersonDetector(config)
        results = detector.train_nopal_model(data_yaml_path)
        
        print("✅ Entrenamiento completado")
        
    elif args.mode == 'predict':
        if not args.input:
            print("❌ Error: Se requiere --input para modo predict")
            return
            
        print("🔍 Realizando predicciones...")
        
        detector = NopalPersonDetector(config)
        detector.load_models(args.weights)
        
        predictions_dir = detector.predict_images(args.input)
        stats = detector.get_detection_stats(args.input)
        
        print(f"📊 Estadísticas: {stats}")
        print(f"✅ Predicciones guardadas en: {predictions_dir}")
        
    elif args.mode == 'video':
        if not args.input:
            print("❌ Error: Se requiere --input para modo video")
            return
            
        print("🎥 Procesando video...")
        
        detector = NopalPersonDetector(config)
        detector.load_models(args.weights)
        
        output_filename = args.output or "output_video.mp4"
        output_path = detector.process_video(args.input, output_filename)
        
        print(f"✅ Video procesado guardado en: {output_path}")


if __name__ == "__main__":
    main()