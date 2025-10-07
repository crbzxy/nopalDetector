"""
Utilidades para procesamiento de video
"""

import cv2
import numpy as np
from typing import Callable, Optional, Tuple


class VideoProcessor:
    """Clase para procesamiento avanzado de video"""
    
    def __init__(self, input_path: str, output_path: str):
        """
        Inicializa el procesador de video
        
        Args:
            input_path: Ruta del video de entrada
            output_path: Ruta del video de salida
        """
        self.input_path = input_path
        self.output_path = output_path
        self.cap = None
        self.writer = None
        
    def __enter__(self):
        """Context manager entry"""
        self.cap = cv2.VideoCapture(self.input_path)
        
        # Obtener propiedades del video
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Configurar escritor
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(
            self.output_path, fourcc, self.fps, (self.width, self.height)
        )
        
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.cap:
            self.cap.release()
        if self.writer:
            self.writer.release()
    
    def process_frames(self, 
                      frame_processor: Callable[[np.ndarray], np.ndarray],
                      progress_callback: Optional[Callable[[int, int], None]] = None) -> None:
        """
        Procesa todos los frames del video
        
        Args:
            frame_processor: Función que procesa cada frame
            progress_callback: Callback para mostrar progreso
        """
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Procesar frame
            processed_frame = frame_processor(frame)
            
            # Escribir frame procesado
            self.writer.write(processed_frame)
            
            frame_count += 1
            
            # Callback de progreso
            if progress_callback and frame_count % 30 == 0:  # Cada segundo aprox
                progress_callback(frame_count, self.total_frames)
    
    @staticmethod
    def resize_frame(frame: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """
        Redimensiona un frame manteniendo la proporción
        
        Args:
            frame: Frame a redimensionar
            target_size: Tamaño objetivo (width, height)
            
        Returns:
            Frame redimensionado
        """
        h, w = frame.shape[:2]
        target_w, target_h = target_size
        
        # Calcular ratio manteniendo proporción
        ratio = min(target_w / w, target_h / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        
        # Redimensionar
        resized = cv2.resize(frame, (new_w, new_h))
        
        # Crear frame con padding si es necesario
        if new_w != target_w or new_h != target_h:
            # Crear frame negro del tamaño objetivo
            padded = np.zeros((target_h, target_w, 3), dtype=np.uint8)
            
            # Calcular posición para centrar
            y_offset = (target_h - new_h) // 2
            x_offset = (target_w - new_w) // 2
            
            # Colocar frame redimensionado en el centro
            padded[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized
            
            return padded
        
        return resized
    
    @staticmethod
    def add_watermark(frame: np.ndarray, text: str, 
                     position: Tuple[int, int] = (10, 30)) -> np.ndarray:
        """
        Agrega una marca de agua al frame
        
        Args:
            frame: Frame al que agregar la marca
            text: Texto de la marca de agua
            position: Posición (x, y) del texto
            
        Returns:
            Frame con marca de agua
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        color = (255, 255, 255)  # Blanco
        thickness = 2
        
        # Agregar sombra
        cv2.putText(frame, text, (position[0] + 2, position[1] + 2), 
                   font, font_scale, (0, 0, 0), thickness + 1)
        
        # Agregar texto principal
        cv2.putText(frame, text, position, font, font_scale, color, thickness)
        
        return frame


class FrameBuffer:
    """Buffer para almacenar frames temporalmente"""
    
    def __init__(self, max_size: int = 30):
        """
        Inicializa el buffer
        
        Args:
            max_size: Número máximo de frames en buffer
        """
        self.max_size = max_size
        self.frames = []
        self.current_index = 0
    
    def add_frame(self, frame: np.ndarray) -> None:
        """Agrega un frame al buffer"""
        if len(self.frames) >= self.max_size:
            # Reemplazar frame más antiguo
            self.frames[self.current_index] = frame.copy()
            self.current_index = (self.current_index + 1) % self.max_size
        else:
            self.frames.append(frame.copy())
    
    def get_frame(self, offset: int = 0) -> Optional[np.ndarray]:
        """
        Obtiene un frame del buffer
        
        Args:
            offset: Offset desde el frame actual (negativo para frames anteriores)
            
        Returns:
            Frame o None si no está disponible
        """
        if not self.frames:
            return None
            
        index = (self.current_index - 1 - offset) % len(self.frames)
        if 0 <= index < len(self.frames):
            return self.frames[index]
        
        return None
    
    def clear(self) -> None:
        """Limpia el buffer"""
        self.frames.clear()
        self.current_index = 0