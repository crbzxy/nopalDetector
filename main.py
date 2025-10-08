"""
🌵 Nopal Detector - Sistema Multi-Clase Inteligente
Sistema de detección avanzado con actualización automática de etiquetas
"""

import argparse
import sys
import os
import yaml
import logging
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

from src.data.dataset_manager import DatasetManager
from src.models.detector import YOLODetector
from src.models.multi_class_detector import MultiClassDetector
from utils.visualization import ResultVisualizer
from utils.config import load_config_with_env, setup_environment
from utils.camera_detector import CameraDetector
from update_labels import LabelUpdater

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

def check_for_label_updates(config, quiet=False):
    """Verificar si hay nuevas etiquetas disponibles en Roboflow"""
    if not quiet:
        logger.info("🔄 Verificando actualizaciones de etiquetas...")
    
    try:
        updater = LabelUpdater(config)
        has_updates = updater.check_for_updates()
        
        if has_updates:
            logger.info("🆕 ¡Nuevas etiquetas disponibles!")
            response = input("¿Deseas actualizar automáticamente? (s/N): ").lower().strip()
            
            if response in ['s', 'si', 'sí', 'y', 'yes']:
                if updater.update_dataset():
                    logger.info("✅ Dataset actualizado exitosamente!")
                    logger.info("💡 Se recomienda entrenar el modelo con las nuevas etiquetas")
                    return True
                else:
                    logger.error("❌ Error actualizando dataset")
            else:
                logger.info("⏭️ Actualización omitida")
        elif not quiet:
            logger.info("✅ Sin cambios en las etiquetas")
            
    except Exception as e:
        logger.warning(f"⚠️ Error verificando actualizaciones: {e}")
    
    return False

def main():
    parser = argparse.ArgumentParser(description='Nopal Detector - Sistema Multi-Clase Inteligente')
    
    # Configuración básica
    parser.add_argument('--config', default='config/model_config.yaml', 
                       help='Ruta al archivo de configuración')
    
    # Modo de operación
    parser.add_argument('--mode', 
                       choices=['train', 'predict', 'video', 'camera', 'list-cameras', 'batch', 'update-labels'], 
                       required=True, 
                       help='Modo de operación')
    
    # Argumentos de entrada/salida
    parser.add_argument('--input', '-i',
                       help='Ruta de entrada (imagen, video o directorio)')
    parser.add_argument('--output', '-o',
                       help='Ruta de salida')
    parser.add_argument('--weights', '-w',
                       help='Ruta a los pesos del modelo entrenado')
    
    # Configuración de cámara
    parser.add_argument('--camera', type=int, default=0, 
                       help='Índice de cámara a usar (default: 0)')
    parser.add_argument('--save-video', action='store_true', 
                       help='Guardar video de la detección en cámara')
    parser.add_argument('--resolution', 
                       help='Resolución de cámara (ej: 640x480)')
    parser.add_argument('--auto-focus', action='store_true', 
                       help='Forzar enfoque automático al inicio')
    
    # Configuración de detección
    parser.add_argument('--confidence', '-c', type=float, default=0.5,
                       help='Umbral de confianza (default: 0.5)')
    
    # Argumentos para procesamiento batch
    parser.add_argument('--batch-dir',
                       type=str,
                       help='Directorio con imágenes para procesar en batch')
    
    # Nuevas funcionalidades v3.0
    parser.add_argument('--multi-class', action='store_true',
                       help='Usar detector multi-clase dinámico')
    parser.add_argument('--auto-update', action='store_true',
                       help='Verificar automáticamente actualizaciones de etiquetas')
    parser.add_argument('--skip-update-check', action='store_true',
                       help='Saltar verificación de actualizaciones')
    parser.add_argument('--data', type=str,
                       help='Ruta al archivo data.yaml para entrenamiento')
    
    args = parser.parse_args()
    
    # Configurar entorno
    setup_environment()
    
    # Cargar configuración con variables de entorno
    config = load_config_with_env(args.config)
    
    # Banner de bienvenida
    logger.info("🌵 =======================================")
    logger.info("🌵    NOPAL DETECTOR")
    logger.info("🌵    Sistema Multi-Clase Inteligente")
    logger.info("🌵 =======================================")
    logger.info(f"🎯 Modo: {args.mode.upper()}")
    
    # Verificar actualizaciones de etiquetas
    labels_updated = False
    if not args.skip_update_check and args.mode not in ['update-labels', 'list-cameras']:
        if args.auto_update:
            labels_updated = check_for_label_updates(config)
        elif args.mode == 'train':
            logger.info("💡 Tip: Usa --auto-update para verificar nuevas etiquetas")
    
    try:
        if args.mode == 'update-labels':
            logger.info("🏷️ Actualizando etiquetas desde Roboflow...")
            updater = LabelUpdater(config)
            
            if updater.check_for_updates():
                if updater.update_dataset():
                    logger.info("✅ Etiquetas actualizadas exitosamente!")
                else:
                    logger.error("❌ Error actualizando etiquetas")
            else:
                logger.info("ℹ️ No hay actualizaciones disponibles")
                
        elif args.mode == 'train':
            logger.info("🚀 Iniciando entrenamiento...")
            
            if args.multi_class:
                logger.info("🎯 Modo: Multi-clase")
                
                # Verificar que se proporcionó el archivo data.yaml
                if not args.data:
                    # Buscar el dataset más reciente en el directorio
                    import glob
                    # Descargar dataset desde Roboflow
                    from src.data.dataset_manager import DatasetManager
                    dataset_manager = DatasetManager(config)
                    dataset_location = dataset_manager.download_dataset()
                    data_yaml_path = dataset_manager.get_data_yaml_path()
                    
                    if data_yaml_path and os.path.exists(data_yaml_path):
                        args.data = data_yaml_path
                        logger.info("🔍 Dataset descargado y configurado: %s", args.data)
                    else:
                        logger.error("❌ Error al descargar el dataset")
                        return
                
                if not os.path.exists(args.data):
                    logger.error(f"❌ No se encontró: {args.data}")
                    return
                
                # Entrenar con detector multi-clase
                detector = MultiClassDetector(config)
                results = detector.train_custom_model(args.data)
                
                logger.info("✅ Entrenamiento completado!")
                logger.info(f"📊 Modelo: {results.get('model_path', 'N/A')}")
                logger.info(f"🏷️ Clases: {results.get('classes', [])}")
                
            else:
                logger.info("🌵 Modo: Clásico")
                
                # Inicializar y preparar dataset
                dataset_manager = DatasetManager(config)
                dataset_manager.download_dataset()
                dataset_manager.prepare_dataset()
                data_yaml_path = dataset_manager.get_data_yaml_path()
                
                # Entrenar modelo
                detector = YOLODetector(config)
                results = detector.train_custom_model(data_yaml_path)
                
                logger.info("✅ Entrenamiento completado")
            
        elif args.mode == 'predict':
            if not args.input:
                logger.error("❌ Falta --input")
                logger.info("💡 Ejemplo: python main.py --mode predict --input imagen.jpg")
                return
                
            logger.info("🔍 Realizando predicciones...")
            
            if args.multi_class:
                detector = MultiClassDetector(config)
                detector.load_models(args.weights)
                
                results = detector.predict_image(
                    args.input, 
                    conf_threshold=args.confidence,
                    save_result=True
                )
                
                if results:
                    logger.info("✅ Predicción completada!")
                    detector.print_detection_summary(results.get('detections', []))
                else:
                    logger.error("❌ Error en la predicción")
            else:
                detector = YOLODetector(config)
                detector.load_model(args.weights)
                
                results = detector.predict_image(
                    args.input,
                    conf_threshold=args.confidence,
                    save_result=True
                )
                
                if results:
                    logger.info("✅ Predicción completada!")
                    detector.print_detection_summary(results.get('detections', []))
                else:
                    logger.error("❌ Error en la predicción")
                
                if 'output_path' in results:
                    logger.info(f"✅ Guardado en: {results['output_path']}")
            
        elif args.mode == 'video':
            if not args.input:
                logger.error("❌ Falta --input")
                logger.info("💡 Ejemplo: python main.py --mode video --input video.mp4")
                return
                
            logger.info("🎥 Procesando video...")
            
            if args.multi_class:
                logger.warning("⚠️ Video multi-clase en desarrollo")
                logger.info("💡 Usa: --mode video (sin --multi-class)")
            else:
                detector = YOLODetector(config)
                detector.load_model(args.weights)
                
                output_filename = args.output or "output_video.mp4"
                output_path = detector.process_video(args.input, output_filename)
                
                logger.info(f"✅ Video guardado: {output_path}")
        
        elif args.mode == 'list-cameras':
            logger.info("🎥 Cámaras disponibles:")
            cameras = CameraDetector.list_available_cameras()
            for i, name in cameras.items():
                logger.info(f"  {i}: {name}")
        
        elif args.mode == 'camera':
            if not args.weights:
                logger.error("❌ Faltan --weights")
                logger.info("💡 Ejemplo: python main.py --mode camera --weights runs/detect/train4/weights/best.pt")
                return
            
            logger.info(f"🎥 Cámara {args.camera}")
            
            if args.multi_class:
                logger.info("🎯 Modo: Multi-clase")
                
                # Configurar resolución
                resolution = None
                if args.resolution:
                    try:
                        width, height = map(int, args.resolution.split('x'))
                        resolution = (width, height)
                    except ValueError:
                        logger.error(f"❌ Resolución inválida: {args.resolution}")
                        logger.info("💡 Formato: 640x480")
                        return
                
                # Inicializar detector multi-clase
                camera_detector = CameraDetector(args.weights)
                
                if camera_detector.setup_camera(args.camera, resolution):
                    if args.auto_focus:
                        logger.info("🎯 Configuración avanzada activada")
                        camera_detector.enable_advanced_settings()
                        import time
                        time.sleep(3)
                    
                    logger.info("📹 Controles: [Q]uit [S]ave [Space]Pause [C/V]Conf [X/Z]IoU [F]iltros")
                    logger.info("🌵 Clases: Nopal (Verde), NopalChino (Naranja)")
                    
                    camera_detector.start_detection(save_video=args.save_video)
                else:
                    logger.error(f"❌ No se pudo acceder a la cámara {args.camera}")
                return
            
            # Configurar resolución (modo clásico)
            resolution = None
            if args.resolution:
                try:
                    width, height = map(int, args.resolution.split('x'))
                    resolution = (width, height)
                except ValueError:
                    logger.error(f"❌ Resolución inválida: {args.resolution}")
                    return
            
            camera_detector = CameraDetector(args.weights)
            
            if camera_detector.setup_camera(args.camera, resolution):
                if args.auto_focus:
                    camera_detector.enable_advanced_settings()
                    import time
                    time.sleep(3)
                
                logger.info("📹 Controles: [Q]uit [R]ecord [Space]Capture")
                camera_detector.start_detection(save_video=args.save_video)
            else:
                logger.error(f"❌ No se pudo acceder a la cámara {args.camera}")
                
        elif args.mode == 'batch':
            print("📁 Procesamiento en lote...")
            
            if not args.batch_dir:
                print("❌ Error: Se requiere --batch-dir para procesamiento batch")
                print("💡 Ejemplo: python main.py --mode batch --batch-dir ./imagenes/")
                return
            
            if not os.path.exists(args.batch_dir):
                print(f"❌ Error: No se encontró el directorio {args.batch_dir}")
                return
            
            if args.multi_class:
                print("🎯 Procesamiento batch con detector multi-clase")
                detector = MultiClassDetector(config)
                detector.load_models(args.weights)
                
                # Buscar todas las imágenes
                image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
                images = []
                
                for ext in image_extensions:
                    images.extend(Path(args.batch_dir).glob(f"*{ext}"))
                    images.extend(Path(args.batch_dir).glob(f"*{ext.upper()}"))
                
                print(f"📊 Encontradas {len(images)} imágenes para procesar")
                
                successful = 0
                total_detections_by_class = {}
                
                for i, image_path in enumerate(images, 1):
                    print(f"🔄 Procesando {i}/{len(images)}: {image_path.name}")
                    
                    results = detector.predict_image(
                        str(image_path),
                        conf_threshold=args.confidence,
                        save_result=True
                    )
                    
                    if results:
                        successful += 1
                        detections = results.get('detections', [])
                        
                        stats = detector.get_class_statistics(detections)
                        for class_name, count in stats.items():
                            total_detections_by_class[class_name] = total_detections_by_class.get(class_name, 0) + count
                        print(f"   ✅ {len(detections)} detecciones: {stats}")
                    else:
                        print(f"   ❌ Error procesando imagen")
                
                print(f"🎯 Procesamiento completado: {successful}/{len(images)} exitosas")
                
                if total_detections_by_class:
                    print("\n📊 RESUMEN TOTAL POR CLASE:")
                    for class_name, total in total_detections_by_class.items():
                        print(f"   {class_name}: {total} detecciones")
            else:
                print("🌵 Procesamiento batch con detector clásico")
                print("⚠️ Funcionalidad batch clásica en desarrollo")
                print("💡 Usa el modo multi-clase: --batch-dir ./imagenes/ --multi-class")
        
    except KeyboardInterrupt:
        print("\n⏹️ Proceso interrumpido por el usuario")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        logger.info("🌵 ¡Gracias por usar Nopal Detector!")

if __name__ == "__main__":
    main()