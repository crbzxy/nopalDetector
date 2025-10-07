"""
Detector para Nopales y Personas usando YOLOv11
Maneja el entrenamiento y las predicciones
"""

import os
import cv2
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from ultralytics import YOLO


class NopalPersonDetector:
    """Detector dual para nopales y personas"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el detector
        
        Args:
            config: Configuración del modelo
        """
        self.config = config
        self.model_config = config['model']
        self.output_config = config['output']
        
        self.nopal_model = None
        self.person_model = None
        self.best_model_path = None
        
    def train_nopal_model(self, data_yaml_path: str) -> Dict[str, Any]:
        """
        Entrena el modelo para detección de nopales
        
        Args:
            data_yaml_path: Ruta del archivo data.yaml
            
        Returns:
            Dict: Resultados del entrenamiento
        """
        print("🤖 Iniciando entrenamiento del modelo de nopales...")
        
        # Cargar modelo base
        model = YOLO(self.model_config['base_model'])
        
        # Configuración de entrenamiento
        train_config = self.model_config['training']
        
        # Entrenar
        results = model.train(
            data=data_yaml_path,
            epochs=train_config['epochs'],
            imgsz=train_config['image_size'],
            batch=train_config['batch_size'],
            patience=train_config['patience']
        )
        
        # Guardar ruta del mejor modelo
        self.best_model_path = os.path.join("runs/detect/train/weights/best.pt")
        
        print(f"✅ Entrenamiento completado. Mejor modelo: {self.best_model_path}")
        return results
    
    def load_models(self, nopal_model_path: Optional[str] = None) -> None:
        """
        Carga los modelos para predicción
        
        Args:
            nopal_model_path: Ruta del modelo entrenado de nopales
        """
        print("📥 Cargando modelos...")
        
        # Cargar modelo de nopales
        if nopal_model_path and os.path.exists(nopal_model_path):
            self.nopal_model = YOLO(nopal_model_path)
            print(f"✅ Modelo de nopales cargado: {nopal_model_path}")
        elif self.best_model_path and os.path.exists(self.best_model_path):
            self.nopal_model = YOLO(self.best_model_path)
            print(f"✅ Modelo de nopales cargado: {self.best_model_path}")
        else:
            print("⚠️ No se encontró modelo entrenado de nopales")
            
        # Cargar modelo de personas
        self.person_model = YOLO(self.model_config['person_model'])
        print("✅ Modelo de personas cargado")
    
    def predict_images(self, test_img_dir: str) -> str:
        """
        Realiza predicciones en imágenes de test
        
        Args:
            test_img_dir: Directorio con imágenes de test
            
        Returns:
            str: Directorio con las predicciones
        """
        if not self.nopal_model or not self.person_model:
            raise ValueError("Primero debe cargar los modelos")
            
        print(f"🖼️ Procesando imágenes en: {test_img_dir}")
        
        # Crear directorio de salida
        predictions_dir = self.output_config['predictions_dir']
        os.makedirs(predictions_dir, exist_ok=True)
        
        # Configuración de predicción
        conf_thresh = self.model_config['prediction']['confidence_threshold']
        
        # Realizar predicciones
        res_nopal = self.nopal_model(test_img_dir, save=False, conf=conf_thresh)
        res_person = self.person_model(test_img_dir, save=False, conf=conf_thresh)
        
        # Anotar imágenes
        for idx, r_nopal in enumerate(res_nopal):
            img_path = r_nopal.path
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            annotated_img = self._annotate_image(img, r_nopal, res_person[idx])
            
            # Guardar imagen anotada
            out_path = os.path.join(predictions_dir, os.path.basename(img_path))
            cv2.imwrite(out_path, annotated_img)
            
        print(f"✅ Predicciones guardadas en: {predictions_dir}")
        return predictions_dir
    
    def process_video(self, video_path: str, output_filename: str = "output_video.mp4") -> str:
        """
        Procesa un video aplicando detecciones
        
        Args:
            video_path: Ruta del video de entrada
            output_filename: Nombre del archivo de salida
            
        Returns:
            str: Ruta del video procesado
        """
        if not self.nopal_model or not self.person_model:
            raise ValueError("Primero debe cargar los modelos")
            
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video no encontrado: {video_path}")
            
        print(f"🎥 Procesando video: {video_path}")
        
        # Crear directorio de salida
        videos_dir = self.output_config['videos_dir']
        os.makedirs(videos_dir, exist_ok=True)
        
        output_path = os.path.join(videos_dir, output_filename)
        
        # Configurar captura de video
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # Configurar escritor de video
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        conf_thresh = self.model_config['prediction']['confidence_threshold']
        frame_count = 0
        
        print("🎬 Procesando frames...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Realizar predicciones
            res_nopal = self.nopal_model(frame, conf=conf_thresh, verbose=False)
            res_person = self.person_model(frame, conf=conf_thresh, verbose=False)
            
            # Anotar frame
            annotated_frame = self._annotate_image(frame, res_nopal[0], res_person[0])
            
            # Escribir frame
            out.write(annotated_frame)
            frame_count += 1
            
            # Progreso cada 100 frames
            if frame_count % 100 == 0:
                print(f"📹 Procesados {frame_count} frames...")
        
        cap.release()
        out.release()
        
        print(f"✅ Video procesado guardado en: {output_path}")
        return output_path
    
    def _annotate_image(self, img: np.ndarray, nopal_results, person_results) -> np.ndarray:
        """
        Anota una imagen con las detecciones de nopales y personas
        
        Args:
            img: Imagen original
            nopal_results: Resultados de detección de nopales
            person_results: Resultados de detección de personas
            
        Returns:
            np.ndarray: Imagen anotada
        """
        annotated_img = img.copy()
        
        # Anotar detecciones de nopales (verde)
        if nopal_results.boxes is not None:
            for box in nopal_results.boxes:
                x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                if box.conf is not None:
                    confidence = box.conf.item()
                    label = f"nopal: {confidence:.2f}"
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