"""
Detector para Nopales y Personas usando YOLOv11
Maneja el entrenamiento y las predicciones
"""

import os
import cv2
import numpy as np
import logging
from typing import Dict, Any, Optional
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class YOLODetector:
    """Detector YOLO genérico para entrenamiento y predicción"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el detector
        
        Args:
            config: Configuración del modelo
        """
        self.config = config
        self.model_config = config['model']
        self.output_config = config['output']
        self.model = None
        self.best_model_path = None
        
    def train_custom_model(self, data_yaml_path: str) -> Dict[str, Any]:
        """
        Entrena un modelo personalizado con YOLO
        
        Args:
            data_yaml_path: Ruta del archivo data.yaml
            
        Returns:
            Dict: Resultados del entrenamiento
        """
        logger.info("🤖 Iniciando entrenamiento...")
        
        # Cargar modelo base
        self.model = YOLO(self.model_config['base_model'])
        
        # Configuración de entrenamiento
        train_config = self.model_config['training']
        
        # Entrenar
        results = self.model.train(
            data=data_yaml_path,
            epochs=train_config['epochs'],
            imgsz=train_config['image_size'],
            batch=train_config['batch_size'],
            patience=train_config['patience']
        )
        
        # Guardar ruta del mejor modelo
        self.best_model_path = os.path.join("runs/detect/train/weights/best.pt")
        
        logger.info(f"✅ Modelo guardado: {self.best_model_path}")
        return results
    
    def load_model(self, model_path: Optional[str] = None) -> None:
        """
        Carga el modelo para predicción
        
        Args:
            model_path: Ruta del modelo entrenado
        """
        logger.info("📥 Cargando modelo...")
        
        if model_path and os.path.exists(model_path):
            self.model = YOLO(model_path)
            logger.info(f"✅ Modelo cargado: {model_path}")
        elif self.best_model_path and os.path.exists(self.best_model_path):
            self.model = YOLO(self.best_model_path)
            logger.info(f"✅ Modelo cargado: {self.best_model_path}")
        else:
            logger.warning("⚠️ No se encontró el modelo")
    
    def predict_image(self, image_path: str, conf_threshold: float = 0.5, save_result: bool = True) -> Dict[str, Any]:
        """
        Realiza predicción en una imagen
        
        Args:
            image_path: Ruta de la imagen
            conf_threshold: Umbral de confianza
            save_result: Si guardar o no el resultado
            
        Returns:
            Dict: Resultados de la predicción
        """
        if not self.model:
            raise ValueError("Primero debe cargar el modelo")
            
        logger.info("🖼️ Procesando imagen: %s", image_path)
        
        # Crear directorio de salida
        predictions_dir = self.output_config['predictions_dir']
        os.makedirs(predictions_dir, exist_ok=True)
        
        # Realizar predicción
        results = self.model(image_path, conf=conf_threshold, save=save_result)
        
        # Procesar resultados
        detections = []
        if len(results) > 0:
            result = results[0]  # tomar primer resultado
            boxes = result.boxes
            
            for box in boxes:
                detection = {
                    'bbox': box.xyxy[0].tolist(),
                    'confidence': float(box.conf),
                    'class_id': int(box.cls),
                    'class_name': result.names[int(box.cls)]
                }
                detections.append(detection)
        
        # Si se guardó el resultado, incluir la ruta
        output_path = None
        if save_result:
            output_path = os.path.join(predictions_dir, 
                                     os.path.basename(image_path))
        
        return {
            'detections': detections,
            'output_path': output_path
        }
    
    def process_video(self, video_path: str, output_filename: str = "output_video.mp4") -> str:
        """
        Procesa un video aplicando detecciones
        
        Args:
            video_path: Ruta del video de entrada
            output_filename: Nombre del archivo de salida
            
        Returns:
            str: Ruta del video procesado
        """
        if not self.model:
            raise ValueError("Primero debe cargar el modelo")
            
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video no encontrado: {video_path}")
            
        logger.info("🎥 Procesando: %s", video_path)
        
        # Crear directorio de salida
        videos_dir = self.output_config['videos_dir']
        os.makedirs(videos_dir, exist_ok=True)
        
        output_path = os.path.join(videos_dir, output_filename)
        conf_thresh = self.model_config['prediction']['confidence_threshold']
        
        # Usar YOLO para procesar video
        self.model.predict(
            source=video_path,
            conf=conf_thresh,
            save=True,
            project=videos_dir,
            name=output_filename
        )
        
        logger.info("✅ Video procesado")
        
        return output_path
        
    def print_detection_summary(self, detections: list) -> None:
        """
        Imprime un resumen de las detecciones realizadas
        
        Args:
            detections: Lista de detecciones
        """
        if not detections:
            logger.info("❌ No se encontraron objetos")
            return
            
        # Contabilizar detecciones por clase
        class_counts = {}
        for det in detections:
            class_name = det['class_name']
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
        # Imprimir resumen
        logger.info("\n🎯 Detecciones:")
        for class_name, count in class_counts.items():
            logger.info(f"  {class_name}: {count}")
        
        """
        """
        annotated_img = img.copy()
        
        # Anotar detecciones de nopales (verde)
        if nopal_results.boxes is not None:
            for box in nopal_results.boxes:
                x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                if box.conf is not None:
                    confidence = box.conf.item()
                    class_name = nopal_results.names[int(box.cls)]
                    label = f"{class_name}: {confidence:.2f}"
                    cv2.putText(
                        annotated_img, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                    )
        
        # Anotar detecciones de personas (azul)
        if person_results.boxes is not None:
            for box in person_results.boxes:
                # Solo personas (clase 0 en COCO)
                if int(box.cls) == 0:
                    x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                    cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    
                    if box.conf is not None:
                        confidence = box.conf.item()
                        label = f"person: {confidence:.2f}"
                        cv2.putText(
                            annotated_img, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2
                        )
        
        return annotated_img
    
    def get_detection_stats(self, test_img_dir: str) -> Dict[str, int]:
        """
        Obtiene estadísticas de detección
        
        Args:
            test_img_dir: Directorio con imágenes de test
            
        Returns:
            Dict: Estadísticas de detección
        """
        if not self.nopal_model or not self.person_model:
            raise ValueError("Primero debe cargar los modelos")
        
        conf_thresh = self.model_config['prediction']['confidence_threshold']
        
        res_nopal = self.nopal_model(test_img_dir, save=False, conf=conf_thresh)
        res_person = self.person_model(test_img_dir, save=False, conf=conf_thresh)
        
        total_nopales = 0
        total_persons = 0
        
        for r_nopal in res_nopal:
            if r_nopal.boxes is not None:
                total_nopales += len(r_nopal.boxes)
        
        for r_person in res_person:
            if r_person.boxes is not None:
                # Solo contar personas (clase 0)
                total_persons += sum(1 for box in r_person.boxes if int(box.cls) == 0)
        
        return {
            'total_images': len(res_nopal),
            'total_nopales': total_nopales,
            'total_persons': total_persons
        }