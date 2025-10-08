"""
🏷️ Detector Multi-Clase Dinámico - Nopal Detector
Maneja detección de múltiples clases configuradas dinámicamente desde Roboflow
"""

import os
import yaml
import cv2
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from ultralytics import YOLO
from pathlib import Path

class MultiClassDetector:
    """Detector que maneja múltiples clases dinámicamente"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el detector multi-clase
        
        Args:
            config: Configuración del modelo
        """
        self.config = config
        self.model_config = config['model']
        self.output_config = config['output']
        
        self.custom_model = None
        self.person_model = None
        self.class_names = []
        self.class_colors = {}
        self.best_model_path = None
        
        # Cargar información de clases desde dataset
        self.load_class_info()
        
    def load_class_info(self):
        """Cargar información de clases desde el dataset actual"""
        try:
            # Intentar múltiples fuentes para las clases
            classes_loaded = False
            
            # 1. Intentar cargar desde el modelo entrenado si existe
            trained_model_path = self.model_config.get('nopal_model_path')
            if trained_model_path and os.path.exists(trained_model_path):
                try:
                    temp_model = YOLO(trained_model_path)
                    if hasattr(temp_model, 'names') and temp_model.names:
                        self.class_names = list(temp_model.names.values())
                        print(f"✅ Clases cargadas desde modelo entrenado: {self.class_names}")
                        classes_loaded = True
                except Exception as e:
                    print(f"⚠️ No se pudieron cargar clases del modelo: {e}")
            
            # 2. Si no se cargaron, buscar en datasets disponibles
            if not classes_loaded:
                # Buscar todos los datasets disponibles
                for version in [3, 2, 1]:  # Probar versiones en orden descendente
                    data_yaml_path = f"nopal-detector-{version}/data.yaml"
                    
                    if os.path.exists(data_yaml_path):
                        with open(data_yaml_path, 'r') as f:
                            data = yaml.safe_load(f)
                            self.class_names = data.get('names', [])
                            
                        print(f"✅ Clases cargadas desde {data_yaml_path}: {self.class_names}")
                        classes_loaded = True
                        break
            
            # 3. Fallback si no se encontró nada
            if not classes_loaded:
                print(f"⚠️ No se encontró información de clases, usando fallback")
                self.class_names = ['nopal']  # Fallback
                
            # Generar colores únicos para cada clase
            self.generate_class_colors()
                
        except Exception as e:
            print(f"❌ Error cargando información de clases: {e}")
            self.class_names = ['nopal']  # Fallback
            
    def generate_class_colors(self):
        """Generar colores únicos para cada clase"""
        np.random.seed(42)  # Para colores consistentes
        colors = []
        
        for i in range(len(self.class_names)):
            # Generar colores distintivos
            hue = (i * 137.508) % 360  # Usar ratio áureo para buena distribución
            color = self.hsv_to_rgb(hue, 0.8, 0.9)
            colors.append(color)
            
        # Asignar colores a nombres de clases
        for i, class_name in enumerate(self.class_names):
            self.class_colors[class_name] = colors[i]
            
        print(f"🎨 Colores generados para {len(self.class_names)} clases")
        
    def hsv_to_rgb(self, h, s, v):
        """Convertir HSV a RGB"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
        return (int(r*255), int(g*255), int(b*255))
        
    def train_custom_model(self, data_yaml_path: str) -> Dict[str, Any]:
        """
        Entrena el modelo para detección de clases personalizadas
        
        Args:
            data_yaml_path: Ruta del archivo data.yaml
            
        Returns:
            Dict: Resultados del entrenamiento
        """
        print(f"🤖 Iniciando entrenamiento del modelo multi-clase...")
        print(f"📊 Clases a entrenar: {self.class_names}")
        
        # Cargar modelo base
        model = YOLO(self.model_config['base_model'])
        
        # Configuración de entrenamiento
        train_config = self.model_config['training']
        
        # Entrenar
        results = model.train(
            data=data_yaml_path,
            epochs=train_config['epochs'],
            batch=train_config['batch_size'],
            imgsz=train_config['image_size'],
            patience=train_config.get('patience', 10),
            save=True,
            verbose=True,
            plots=True,
            val=True
        )
        
        # Guardar ruta del mejor modelo
        self.best_model_path = results.save_dir / 'weights' / 'best.pt'
        
        print(f"✅ Entrenamiento completado!")
        print(f"📄 Mejor modelo guardado en: {self.best_model_path}")
        
        return {
            'model_path': str(self.best_model_path),
            'results': results,
            'classes': self.class_names,
            'num_classes': len(self.class_names)
        }
    
    def load_models(self, custom_weights_path: str = None):
        """
        Cargar modelos entrenados
        
        Args:
            custom_weights_path: Ruta a pesos del modelo personalizado
        """
        try:
            # Cargar modelo personalizado
            if custom_weights_path and os.path.exists(custom_weights_path):
                self.custom_model = YOLO(custom_weights_path)
                print(f"✅ Modelo personalizado cargado: {custom_weights_path}")
            else:
                # Buscar último modelo entrenado
                runs_dir = Path("runs/detect")
                if runs_dir.exists():
                    train_dirs = [d for d in runs_dir.iterdir() if d.is_dir() and d.name.startswith('train')]
                    if train_dirs:
                        latest_train = max(train_dirs, key=lambda x: x.stat().st_mtime)
                        best_path = latest_train / 'weights' / 'best.pt'
                        if best_path.exists():
                            self.custom_model = YOLO(str(best_path))
                            print(f"✅ Último modelo entrenado cargado: {best_path}")
                        else:
                            print("⚠️ No se encontró modelo entrenado, usando modelo base")
                            self.custom_model = YOLO(self.model_config['base_model'])
                    else:
                        print("⚠️ No se encontraron entrenamientos previos")
                        self.custom_model = YOLO(self.model_config['base_model'])
                else:
                    print("⚠️ Directorio de entrenamientos no existe")
                    self.custom_model = YOLO(self.model_config['base_model'])
            
            # Cargar modelo de personas
            self.person_model = YOLO(self.model_config['person_model'])
            print(f"✅ Modelo de personas cargado")
            
        except Exception as e:
            print(f"❌ Error cargando modelos: {e}")
            
    def predict_image(self, image_path: str, conf_threshold: float = None, 
                     save_result: bool = True) -> Dict[str, Any]:
        """
        Realizar predicción en una imagen
        
        Args:
            image_path: Ruta de la imagen
            conf_threshold: Umbral de confianza
            save_result: Si guardar el resultado
            
        Returns:
            Dict: Resultados de la predicción
        """
        if not self.custom_model:
            print("❌ Modelo no cargado")
            return {}
            
        conf = conf_threshold or self.model_config['prediction']['confidence_threshold']
        
        try:
            # Realizar predicción con modelo personalizado
            results = self.custom_model(image_path, conf=conf, save=save_result)
            
            # Procesar resultados
            processed_results = self.process_results(results[0])
            
            return {
                'image_path': image_path,
                'detections': processed_results,
                'confidence_threshold': conf,
                'classes_detected': list(set([det['class'] for det in processed_results]))
            }
            
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
            return {}
    
    def process_results(self, result):
        """
        Procesar resultados de YOLO para múltiples clases
        
        Args:
            result: Resultado de YOLO
            
        Returns:
            List: Lista de detecciones procesadas
        """
        detections = []
        
        if result.boxes is not None:
            boxes = result.boxes.cpu().numpy()
            
            for box in boxes:
                # Obtener información de la detección
                x1, y1, x2, y2 = box.xyxy[0]
                confidence = box.conf[0]
                class_id = int(box.cls[0])
                
                # Obtener nombre de la clase
                if class_id < len(self.class_names):
                    class_name = self.class_names[class_id]
                else:
                    class_name = f"clase_{class_id}"
                
                detection = {
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': float(confidence),
                    'class': class_name,
                    'class_id': class_id,
                    'color': self.class_colors.get(class_name, (0, 255, 0))
                }
                
                detections.append(detection)
        
        return detections
    
    def annotate_image(self, image: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """
        Anotar imagen con detecciones de múltiples clases
        
        Args:
            image: Imagen original
            detections: Lista de detecciones
            
        Returns:
            np.ndarray: Imagen anotada
        """
        annotated_image = image.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class']
            color = detection['color']
            
            # Dibujar bounding box
            cv2.rectangle(annotated_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            
            # Preparar texto
            label = f"{class_name}: {confidence:.2f}"
            
            # Calcular tamaño del texto
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
            )
            
            # Dibujar fondo del texto
            cv2.rectangle(
                annotated_image,
                (bbox[0], bbox[1] - text_height - baseline - 5),
                (bbox[0] + text_width, bbox[1]),
                color,
                -1
            )
            
            # Dibujar texto
            cv2.putText(
                annotated_image,
                label,
                (bbox[0], bbox[1] - baseline - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
        
        return annotated_image
    
    def get_class_statistics(self, detections: List[Dict]) -> Dict[str, int]:
        """
        Obtener estadísticas de clases detectadas
        
        Args:
            detections: Lista de detecciones
            
        Returns:
            Dict: Conteo por clase
        """
        stats = {}
        for detection in detections:
            class_name = detection['class']
            stats[class_name] = stats.get(class_name, 0) + 1
        
        return stats
    
    def print_detection_summary(self, detections: List[Dict]):
        """
        Imprimir resumen de detecciones
        
        Args:
            detections: Lista de detecciones
        """
        if not detections:
            print("🔍 No se detectaron objetos")
            return
            
        stats = self.get_class_statistics(detections)
        
        print(f"🎯 DETECCIONES ENCONTRADAS:")
        for class_name, count in stats.items():
            color_info = self.class_colors.get(class_name, (0, 255, 0))
            print(f"   {class_name}: {count} objetos (Color: RGB{color_info})")
        
        total = sum(stats.values())
        print(f"   Total: {total} objetos detectados")