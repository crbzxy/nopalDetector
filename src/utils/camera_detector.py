"""
Procesador de cámara en tiempo real para detección de nopales y personas
"""

import cv2
import numpy as np
import threading
import queue
import time
from typing import Optional, Callable, Dict, Any, List, Tuple, Union
from ultralytics import YOLO


class CameraDetector:
    """Detector de nopales y personas usando cámara en tiempo real"""
    
    def __init__(self, config_or_weights: Union[Dict[str, Any], str]):
        """
        Inicializa el detector de cámara
        
        Args:
            config_or_weights: Configuración del modelo o ruta a los pesos
        """
        if isinstance(config_or_weights, str):
            # Si es una ruta de archivo, crear configuración básica
            self.weights_path = config_or_weights
            self.config = {
                'model': {
                    'nopal_model_path': config_or_weights,
                    'person_model_path': 'yolo11s.pt'  # Modelo base para personas
                },
                'prediction': {
                    'confidence_threshold': 0.90,  # Muy estricto para evitar falsos positivos
                    'iou_threshold': 0.7,          # Supresión muy agresiva
                    'max_detections': 3             # Máximo 3 nopales por frame
                }
            }
            self.model_config = self.config['model']
            self._apply_basic_settings = False  # No aplicar configuraciones automáticas
        else:
            # Si es configuración completa
            self.config = config_or_weights
            self.model_config = config_or_weights['model']
            self.weights_path = self.model_config.get('nopal_model_path', 'yolo11s.pt')
            self._apply_basic_settings = False
        
        self.nopal_model = None
        self.person_model = None
        self.cap = None
        self.is_running = False
        self.frame_queue = queue.Queue(maxsize=2)
        self.result_queue = queue.Queue(maxsize=2)
        
        # Configuración de filtros
        self.use_size_filters = True  # Activar filtros de tamaño por defecto
        
        # Estadísticas en tiempo real
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Configuración de ventana
        self.window_name = "Nopal Detector - Cámara en Tiempo Real"
        
    @staticmethod
    def list_available_cameras() -> Dict[int, str]:
        """
        Lista todas las cámaras disponibles de forma estática
        
        Returns:
            Diccionario con índice y nombre de cámaras disponibles
        """
        import cv2
        
        cameras = {}
        
        # Probar hasta 10 índices de cámara
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Verificar que realmente puede capturar frames
                ret, frame = cap.read()
                if ret:
                    cameras[i] = f"Cámara {i}"
                cap.release()
        
        return cameras
    
    def list_cameras(self) -> List[Dict[str, Any]]:
        """
        Lista todas las cámaras disponibles en el sistema
        
        Returns:
            Lista de diccionarios con información de cámaras
        """
        cameras = []
        
        # Probar hasta 10 índices de cámara
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Obtener propiedades de la cámara
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                cameras.append({
                    'index': i,
                    'name': f"Cámara {i}",
                    'resolution': f"{width}x{height}",
                    'fps': fps,
                    'available': True
                })
                cap.release()
            else:
                # Intentar con diferentes backends
                for backend in [cv2.CAP_DSHOW, cv2.CAP_V4L2, cv2.CAP_AVFOUNDATION]:
                    cap = cv2.VideoCapture(i, backend)
                    if cap.isOpened():
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        
                        cameras.append({
                            'index': i,
                            'name': f"Cámara {i} ({backend})",
                            'resolution': f"{width}x{height}",
                            'fps': fps,
                            'available': True,
                            'backend': backend
                        })
                        cap.release()
                        break
        
        return cameras
    
    def load_models(self, nopal_model_path: Optional[str] = None):
        """
        Carga los modelos para detección
        
        Args:
            nopal_model_path: Ruta del modelo entrenado de nopales
        """
        print("📥 Cargando modelos para detección en tiempo real...")
        
        # Cargar modelo de nopales
        if nopal_model_path and cv2.os.path.exists(nopal_model_path):
            self.nopal_model = YOLO(nopal_model_path)
            print(f"✅ Modelo de nopales cargado: {nopal_model_path}")
        else:
            print("⚠️ Modelo de nopales no encontrado, usando modelo base")
            self.nopal_model = YOLO(self.model_config['base_model'])
            
        # Cargar modelo de personas
        self.person_model = YOLO(self.model_config['person_model'])
        print("✅ Modelo de personas cargado")
    
    def setup_camera(self, camera_index: int = 0, resolution: Tuple[int, int] = None) -> bool:
        """
        Configura la cámara y carga los modelos
        
        Args:
            camera_index: Índice de la cámara a usar
            resolution: Resolución deseada (width, height)
            
        Returns:
            bool: True si la cámara se configuró correctamente
        """
        try:
            # Cargar modelos si no están cargados
            if not self.nopal_model or not self.person_model:
                print("🤖 Cargando modelos...")
                self._load_models()
            
            # Guardar índice de cámara para reconexión
            self._current_camera_index = camera_index
            
            # Liberar cámara anterior si existe
            if self.cap:
                self.cap.release()
            
            # Abrir nueva cámara
            self.cap = cv2.VideoCapture(camera_index)
            
            if not self.cap.isOpened():
                # Intentar con diferentes backends
                for backend in [cv2.CAP_DSHOW, cv2.CAP_V4L2, cv2.CAP_AVFOUNDATION]:
                    self.cap = cv2.VideoCapture(camera_index, backend)
                    if self.cap.isOpened():
                        break
            
            if not self.cap.isOpened():
                print(f"❌ No se pudo abrir la cámara {camera_index}")
                return False
            
            # Configurar resolución si se especifica
            if resolution:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
            
            # Configurar FPS
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Solo configuraciones básicas sin automáticos
            # No aplicar configuraciones que puedan causar inestabilidad
            
            # Verificar configuración
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            print(f"✅ Cámara {camera_index} configurada:")
            print(f"   Resolución: {actual_width}x{actual_height}")
            print(f"   FPS: {actual_fps}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error configurando cámara: {e}")
            return False
    
    def _load_models(self):
        """Carga los modelos de forma privada"""
        try:
            # Cargar modelo de nopales usando la ruta especificada
            print(f"📥 Cargando modelo de nopales: {self.weights_path}")
            self.nopal_model = YOLO(self.weights_path)
            print("✅ Modelo de nopales cargado")
            
            # Cargar modelo de personas (usar modelo base)
            person_model_path = self.model_config.get('person_model_path', 'yolo11s.pt')
            print(f"📥 Cargando modelo de personas: {person_model_path}")
            self.person_model = YOLO(person_model_path)
            print("✅ Modelo de personas cargado")
            
        except Exception as e:
            print(f"❌ Error cargando modelos: {e}")
            # Usar modelo base como fallback
            print("🔄 Usando modelo base como fallback...")
            self.nopal_model = YOLO('yolo11s.pt')
            self.person_model = YOLO('yolo11s.pt')
    
    def _configure_camera_settings(self):
        """Configura ajustes avanzados de la cámara para mejor calidad"""
        try:
            print("🔧 Configurando ajustes de cámara...")
            
            # Configurar exposición para mejor iluminación
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Exposición manual
            self.cap.set(cv2.CAP_PROP_EXPOSURE, -4)         # Exposición más alta
            print("   ✅ Exposición configurada para mejor iluminación")
            
            # Configurar brillo y contraste mejorados
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.6)      # Más brillo
            self.cap.set(cv2.CAP_PROP_CONTRAST, 0.7)        # Más contraste
            self.cap.set(cv2.CAP_PROP_SATURATION, 0.6)      # Saturación moderada
            print("   ✅ Brillo, contraste y saturación optimizados")
            
            # Enfoque automático
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            print("   ✅ Enfoque automático activado")
            
            # Configurar balance de blancos automático
            self.cap.set(cv2.CAP_PROP_AUTO_WB, 1)
            print("   ✅ Balance de blancos automático activado")
            
            # Configurar ganancia para mejor imagen en poca luz
            self.cap.set(cv2.CAP_PROP_GAIN, 10)
            print("   ✅ Ganancia configurada para mejor imagen")
            
            # Esperar un momento para que la cámara se ajuste
            time.sleep(2)
            print("   ⏳ Esperando ajuste automático de la cámara...")
            
            # Capturar algunos frames para que la cámara se estabilice
            for _ in range(10):
                ret, frame = self.cap.read()
                if not ret:
                    break
                time.sleep(0.1)
            
            print("   ✅ Cámara configurada y estabilizada")
            
        except Exception as e:
            print(f"   ⚠️  Algunos ajustes no están disponibles: {e}")
    
    def enable_advanced_settings(self):
        """Activar configuraciones avanzadas de cámara"""
        self._apply_basic_settings = True
        if self.cap and self.cap.isOpened():
            print("🔧 Aplicando configuraciones avanzadas...")
            self._configure_camera_settings()
    
    def disable_advanced_settings(self):
        """Desactivar configuraciones avanzadas para mayor estabilidad"""
        self._apply_basic_settings = False
        print("✅ Usando configuración básica y estable")
    
    def _check_camera_health(self) -> bool:
        """Verificar si la cámara está funcionando correctamente"""
        if not self.cap or not self.cap.isOpened():
            return False
        
        # Intentar leer un frame de prueba
        ret, frame = self.cap.read()
        return ret and frame is not None
    
    def _reconnect_camera(self, camera_index: int) -> bool:
        """Intentar reconectar la cámara"""
        try:
            print("🔄 Intentando reconectar cámara...")
            if self.cap:
                self.cap.release()
            
            self.cap = cv2.VideoCapture(camera_index)
            
            if self.cap.isOpened() and self._check_camera_health():
                print("✅ Cámara reconectada exitosamente")
                return True
            else:
                print("❌ No se pudo reconectar la cámara")
                return False
        except Exception as e:
            print(f"❌ Error reconectando cámara: {e}")
            return False
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Procesa un frame con detecciones
        
        Args:
            frame: Frame de la cámara
            
        Returns:
            Frame anotado con detecciones
        """
        if not self.nopal_model or not self.person_model:
            return frame
            
        # Obtener umbral de confianza de la configuración
        conf_thresh = self.config.get('prediction', {}).get('confidence_threshold', 0.5)
        
        # Realizar predicciones
        try:
            # Usar umbrales más estrictos para reducir falsos positivos
            conf_thresh = self.config.get('prediction', {}).get('confidence_threshold', 0.7)
            iou_thresh = self.config.get('prediction', {}).get('iou_threshold', 0.5)
            
            res_nopal = self.nopal_model(frame, conf=conf_thresh, iou=iou_thresh, verbose=False)
            res_person = self.person_model(frame, conf=conf_thresh, iou=iou_thresh, verbose=False)
            
            annotated_frame = frame.copy()
            
            # Contadores para estadísticas por clase
            class_counts = {}
            person_count = 0
            
            # Dibujar detecciones de nopales (multi-clase)
            if res_nopal and len(res_nopal) > 0 and res_nopal[0].boxes is not None:
                for box in res_nopal[0].boxes:
                    x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                    
                    # Filtros para reducir falsos positivos (solo si están activados)
                    if self.use_size_filters:
                        box_width = x2 - x1
                        box_height = y2 - y1
                        box_area = box_width * box_height
                        frame_area = frame.shape[0] * frame.shape[1]
                        area_ratio = box_area / frame_area
                        
                        # Filtro 1: Rechazar detecciones muy grandes (probablemente personas)
                        if area_ratio > 0.12:  # Más del 12% del frame
                            continue
                        
                        # Filtro 2: Filtro por tamaño mínimo (evitar ruido)
                        if box_width < 30 or box_height < 30:  # Muy pequeño
                            continue
                        
                        # Filtro 3: Aspecto ratio - nopales no son extremadamente alargados
                        aspect_ratio = box_width / box_height if box_height > 0 else 0
                        if aspect_ratio > 4.0 or aspect_ratio < 0.25:  # Muy alargado o muy alto
                            continue
                    
                    # Obtener la clase antes de incrementar contador
                    class_id = int(box.cls) if box.cls is not None else 0
                    class_names = self.nopal_model.names if hasattr(self.nopal_model, 'names') else {0: 'nopal'}
                    class_name = class_names.get(class_id, 'nopal')
                    
                    # Incrementar contador de esta clase
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
                    
                    # Colores para diferentes clases
                    colors = {
                        'nopal': (0, 255, 0),        # Verde
                        'nopalChino': (255, 165, 0),  # Naranja
                        0: (0, 255, 0),              # Verde por defecto
                        1: (255, 165, 0)             # Naranja para clase 1
                    }
                    
                    # Seleccionar color
                    if class_name in colors:
                        color = colors[class_name]
                    elif class_id in colors:
                        color = colors[class_id]
                    else:
                        color = (0, 255, 0)  # Verde por defecto
                    
                    # Dibujar rectángulo
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Dibujar etiqueta
                    if box.conf is not None:
                        confidence = box.conf.item()
                        label = f"{class_name}: {confidence:.2f}"
                        
                        # Fondo para el texto
                        (text_width, text_height), _ = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                        )
                        cv2.rectangle(
                            annotated_frame, 
                            (x1, y1 - text_height - 10), 
                            (x1 + text_width, y1), 
                            color, -1
                        )
                        
                        # Texto
                        text_color = (255, 255, 255) if class_name == 'nopalChino' else (0, 0, 0)
                        cv2.putText(
                            annotated_frame, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2
                        )
            
            # Dibujar detecciones de personas (azul)
            if res_person and len(res_person) > 0 and res_person[0].boxes is not None:
                for box in res_person[0].boxes:
                    if int(box.cls) == 0:  # Solo personas (clase 0 en COCO)
                        person_count += 1
                        x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                        
                        # Dibujar rectángulo
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        
                        # Dibujar etiqueta
                        if box.conf is not None:
                            confidence = box.conf.item()
                            label = f"Persona: {confidence:.2f}"
                            
                            # Fondo para el texto
                            (text_width, text_height), _ = cv2.getTextSize(
                                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                            )
                            cv2.rectangle(
                                annotated_frame, 
                                (x1, y1 - text_height - 10), 
                                (x1 + text_width, y1), 
                                (255, 0, 0), -1
                            )
                            
                            # Texto
                            cv2.putText(
                                annotated_frame, label, (x1, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
                            )
            
            # Agregar información en pantalla
            self._draw_info_overlay(annotated_frame, class_counts, person_count)
            
            return annotated_frame
            
        except Exception as e:
            print(f"⚠️ Error procesando frame: {e}")
            return frame
    
    def _draw_info_overlay(self, frame: np.ndarray, class_counts: Dict[str, int], person_count: int):
        """
        Dibuja información superpuesta en el frame con contadores por clase
        
        Args:
            frame: Frame a anotar
            class_counts: Diccionario con contadores por clase
            person_count: Número de personas detectadas
        """
        height, width = frame.shape[:2]
        
        # Obtener todas las clases disponibles del modelo
        all_classes = []
        if self.nopal_model and hasattr(self.nopal_model, 'names'):
            all_classes = list(self.nopal_model.names.values())
        else:
            all_classes = ['nopal']  # Fallback
        
        # Calcular altura del overlay según número de clases totales
        num_classes = len(all_classes)
        overlay_height = 90 + (num_classes * 25)  # Base + 25px por cada clase
        
        # Fondo semi-transparente para la información
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, overlay_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Información del proyecto
        cv2.putText(frame, "Nopal Detector", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Estadísticas de detección por clase
        y_offset = 60
        
        # Colores para cada clase
        colors = {
            'nopal': (0, 255, 0),        # Verde
            'nopalChino': (255, 165, 0)  # Naranja
        }
        
        # Mostrar contador de todas las clases (incluso si el conteo es 0)
        for class_name in sorted(all_classes):
            count = class_counts.get(class_name, 0)  # 0 si no se detectó
            color = colors.get(class_name, (0, 255, 0))
            cv2.putText(frame, f"{class_name}: {count}", (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            y_offset += 25
        
        # Personas
        cv2.putText(frame, f"Personas: {person_count}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        y_offset += 25
        
        # FPS
        cv2.putText(frame, f"FPS: {self.current_fps:.1f}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Controles
        controls_text = "Controles: [Q]uit [S]ave [Space]Pause"
        cv2.putText(frame, controls_text, (10, height - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def _update_fps(self):
        """Actualiza el contador de FPS"""
        self.fps_counter += 1
        if time.time() - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_start_time = time.time()
    
    def start_detection(self, camera_index: int = 0, save_video: bool = False, 
                       output_path: str = None) -> bool:
        """
        Inicia la detección en tiempo real
        
        Args:
            camera_index: Índice de la cámara a usar
            save_video: Si guardar el video con detecciones
            output_path: Ruta donde guardar el video
            
        Returns:
            bool: True si se ejecutó correctamente
        """
        if not self.nopal_model or not self.person_model:
            print("❌ Modelos no cargados. Ejecuta load_models() primero")
            return False
        
        if not self.setup_camera(camera_index):
            return False
        
        # Configurar grabación si se solicita
        video_writer = None
        if save_video:
            if not output_path:
                output_path = f"outputs/videos/camera_detection_{int(time.time())}.mp4"
            
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = 20  # FPS fijo para grabación
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"📹 Grabando video en: {output_path}")
        
        print("🎥 Iniciando detección en tiempo real...")
        print("   Presiona 'q' para salir")
        print("   Presiona 's' para guardar frame actual")
        print("   Presiona 'space' para pausar/reanudar")
        print("   Controles de detección:")
        print("     'c' - Aumentar confianza (menos detecciones)")
        print("     'v' - Disminuir confianza (más detecciones)")
        print("     'x' - Aumentar IoU (menos duplicados)")
        print("     'z' - Disminuir IoU (más detecciones)")
        print("     'f' - Activar/desactivar filtros de tamaño")
        
        # Mostrar configuración inicial
        conf_thresh = self.config.get('prediction', {}).get('confidence_threshold', 0.85)
        iou_thresh = self.config.get('prediction', {}).get('iou_threshold', 0.6)
        print(f"   📊 Configuración inicial: Confianza={conf_thresh:.2f}, IoU={iou_thresh:.2f}")
        
        self.is_running = True
        paused = False
        frame_counter = 0
        error_counter = 0
        max_errors = 5  # Máximo de errores consecutivos antes de salir
        
        try:
            while self.is_running:
                if not paused:
                    ret, frame = self.cap.read()
                    if not ret:
                        error_counter += 1
                        print(f"⚠️ Error leyendo frame de la cámara (intento {error_counter}/{max_errors})")
                        
                        if error_counter >= max_errors:
                            print("❌ Demasiados errores consecutivos. Cerrando...")
                            break
                        
                        # Intentar reconectar la cámara cada 3 errores
                        if error_counter % 3 == 0:
                            camera_index = getattr(self, '_current_camera_index', 0)
                            if not self._reconnect_camera(camera_index):
                                print("❌ No se pudo recuperar la conexión de la cámara")
                                break
                        
                        # Pausa breve antes del siguiente intento
                        time.sleep(0.1)
                        continue
                    
                    # Reset contador de errores si el frame se lee correctamente
                    error_counter = 0
                    
                    # Procesar frame
                    annotated_frame = self.process_frame(frame)
                    
                    # Actualizar FPS
                    self._update_fps()
                    
                    # Guardar frame si se está grabando
                    if video_writer:
                        video_writer.write(annotated_frame)
                    
                    frame_counter += 1
                else:
                    # Si está pausado, seguir mostrando el último frame
                    pass
                
                # Mostrar frame
                cv2.imshow(self.window_name, annotated_frame)
                
                # Manejar teclas
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):  # Salir
                    break
                elif key == ord('s'):  # Guardar frame
                    timestamp = int(time.time())
                    save_path = f"outputs/predictions/camera_frame_{timestamp}.jpg"
                    cv2.imwrite(save_path, annotated_frame)
                    print(f"📸 Frame guardado: {save_path}")
                elif key == ord(' '):  # Pausar/reanudar
                    paused = not paused
                    status = "pausado" if paused else "reanudado"
                    print(f"⏸️ Video {status}")
                elif key == ord('c'):  # Aumentar umbral de confianza
                    current_conf = self.config['prediction']['confidence_threshold']
                    new_conf = min(0.95, current_conf + 0.05)
                    self.config['prediction']['confidence_threshold'] = new_conf
                    print(f"🎯 Umbral de confianza: {new_conf:.2f}")
                elif key == ord('v'):  # Disminuir umbral de confianza
                    current_conf = self.config['prediction']['confidence_threshold']
                    new_conf = max(0.1, current_conf - 0.05)
                    self.config['prediction']['confidence_threshold'] = new_conf
                    print(f"🎯 Umbral de confianza: {new_conf:.2f}")
                elif key == ord('x'):  # Aumentar umbral IoU
                    current_iou = self.config['prediction']['iou_threshold']
                    new_iou = min(0.9, current_iou + 0.05)
                    self.config['prediction']['iou_threshold'] = new_iou
                    print(f"🔧 Umbral IoU: {new_iou:.2f}")
                elif key == ord('z'):  # Disminuir umbral IoU
                    current_iou = self.config['prediction']['iou_threshold']
                    new_iou = max(0.1, current_iou - 0.05)
                    self.config['prediction']['iou_threshold'] = new_iou
                    print(f"🔧 Umbral IoU: {new_iou:.2f}")
                elif key == ord('f'):  # Activar/desactivar filtros de tamaño
                    self.use_size_filters = not self.use_size_filters
                    status = "activados" if self.use_size_filters else "desactivados"
                    print(f"🔍 Filtros de tamaño: {status}")
        
        except KeyboardInterrupt:
            print("\n⚠️ Interrumpido por usuario")
        
        finally:
            # Limpiar recursos
            self.is_running = False
            
            if self.cap:
                self.cap.release()
            
            if video_writer:
                video_writer.release()
                print(f"✅ Video guardado: {output_path}")
            
            cv2.destroyAllWindows()
            print(f"✅ Detección completada. Frames procesados: {frame_counter}")
        
        return True
    
    def stop_detection(self):
        """Detiene la detección en tiempo real"""
        self.is_running = False