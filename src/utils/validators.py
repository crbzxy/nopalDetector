"""
Módulo de Validación de Entrada - Nopal Detector
Valida rutas, formatos, y disponibilidad de recursos
"""

import os
import logging
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)


class InputValidator:
    """Validador centralizado para todas las entradas del usuario"""
    
    # Extensiones soportadas
    SUPPORTED_IMAGES = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    SUPPORTED_VIDEOS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
    
    @staticmethod
    def validate_image_path(path: str, allow_dir: bool = False) -> tuple[bool, str]:
        """
        Valida que sea una imagen soportada.
        
        Args:
            path: Ruta del archivo o directorio
            allow_dir: Si True, permite directorios con imágenes
            
        Returns:
            tuple: (es_válido, mensaje_error)
            
        Example:
            >>> valid, msg = InputValidator.validate_image_path("foto.jpg")
            >>> if not valid:
            ...     logger.error(msg)
        """
        try:
            p = Path(path)
            
            if not p.exists():
                return False, f"❌ La ruta no existe: {path}"
            
            if p.is_dir():
                if not allow_dir:
                    return False, f"❌ Se esperaba un archivo, se recibió un directorio: {path}"
                
                # Verificar que hay imágenes en el directorio
                images = list(p.glob("*"))
                images = [f for f in images if f.suffix.lower() in InputValidator.SUPPORTED_IMAGES]
                
                if not images:
                    return False, f"❌ No se encontraron imágenes en: {path}"
                
                return True, f"✅ Directorio con {len(images)} imagen(es) detectada(s)"
            
            # Es un archivo
            if p.suffix.lower() not in InputValidator.SUPPORTED_IMAGES:
                supported = ", ".join(InputValidator.SUPPORTED_IMAGES)
                return False, f"❌ Formato no soportado: {p.suffix}. Soportados: {supported}"
            
            return True, f"✅ Imagen válida: {p.name}"
            
        except Exception as e:
            return False, f"❌ Error validando imagen: {e}"
    
    @staticmethod
    def validate_video_path(path: str) -> tuple[bool, str]:
        """
        Valida que sea un video soportado.
        
        Args:
            path: Ruta del archivo de video
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        try:
            p = Path(path)
            
            if not p.exists():
                return False, f"❌ El video no existe: {path}"
            
            if p.is_dir():
                return False, f"❌ Se esperaba un archivo de video, se recibió un directorio: {path}"
            
            if p.suffix.lower() not in InputValidator.SUPPORTED_VIDEOS:
                supported = ", ".join(InputValidator.SUPPORTED_VIDEOS)
                return False, f"❌ Formato de video no soportado: {p.suffix}. Soportados: {supported}"
            
            # Verificar tamaño mínimo (al menos 1KB)
            file_size = p.stat().st_size
            if file_size < 1024:
                return False, f"❌ Archivo de video muy pequeño ({file_size} bytes): {path}"
            
            return True, f"✅ Video válido: {p.name} ({file_size / (1024*1024):.1f} MB)"
            
        except Exception as e:
            return False, f"❌ Error validando video: {e}"
    
    @staticmethod
    def validate_weights_path(path: str) -> tuple[bool, str]:
        """
        Valida que el archivo de pesos sea accesible y válido.
        
        Args:
            path: Ruta del archivo de pesos (.pt)
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        try:
            p = Path(path)
            
            if not p.exists():
                return False, f"❌ Archivo de pesos no encontrado: {path}"
            
            if p.is_dir():
                return False, f"❌ Se esperaba un archivo .pt, se recibió un directorio: {path}"
            
            if p.suffix != '.pt':
                return False, f"❌ Formato incorrecto. Se esperaba .pt, se recibió: {p.suffix}"
            
            # Verificar tamaño (modelos suelen ser > 10MB)
            file_size = p.stat().st_size
            if file_size < 1024 * 100:  # 100KB mínimo
                return False, f"❌ Archivo sospechosamente pequeño ({file_size / 1024:.1f} KB): {path}"
            
            # Verificar permisos de lectura
            if not os.access(p, os.R_OK):
                return False, f"❌ No hay permisos de lectura para: {path}"
            
            return True, f"✅ Pesos válidos: {p.name} ({file_size / (1024*1024):.1f} MB)"
            
        except Exception as e:
            return False, f"❌ Error validando pesos: {e}"
    
    @staticmethod
    def validate_directory(path: str, must_exist: bool = True, 
                         must_contain: Optional[str] = None) -> tuple[bool, str]:
        """
        Valida un directorio.
        
        Args:
            path: Ruta del directorio
            must_exist: Si False, permite crear el directorio
            must_contain: Si especificado, verifica que contenga archivos con esa extensión
            
        Returns:
            tuple: (es_válido, mensaje_error)
            
        Example:
            >>> valid, msg = InputValidator.validate_directory(
            ...     "my_dir", 
            ...     must_contain="*.jpg"
            ... )
        """
        try:
            p = Path(path)
            
            if not p.exists():
                if must_exist:
                    return False, f"❌ Directorio no existe: {path}"
                else:
                    # Crear el directorio
                    try:
                        p.mkdir(parents=True, exist_ok=True)
                        return True, f"✅ Directorio creado: {path}"
                    except Exception as e:
                        return False, f"❌ No se pudo crear directorio: {e}"
            
            if not p.is_dir():
                return False, f"❌ No es un directorio: {path}"
            
            # Verificar contenido si se especificó
            if must_contain:
                items = list(p.glob(must_contain))
                if not items:
                    return False, f"❌ Directorio no contiene {must_contain}: {path}"
                return True, f"✅ Directorio válido con {len(items)} elementos coincidentes"
            
            return True, f"✅ Directorio válido: {path}"
            
        except Exception as e:
            return False, f"❌ Error validando directorio: {e}"
    
    @staticmethod
    def validate_yaml_path(path: str) -> tuple[bool, str]:
        """
        Valida un archivo YAML de configuración.
        
        Args:
            path: Ruta del archivo YAML
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        try:
            p = Path(path)
            
            if not p.exists():
                return False, f"❌ Archivo YAML no encontrado: {path}"
            
            if p.suffix not in ['.yaml', '.yml']:
                return False, f"❌ Formato incorrecto, se esperaba .yaml o .yml: {p.suffix}"
            
            # Intentar parsear el YAML
            import yaml
            try:
                with open(p, 'r') as f:
                    yaml.safe_load(f)
                return True, f"✅ YAML válido: {p.name}"
            except yaml.YAMLError as e:
                return False, f"❌ Error en YAML: {e}"
            
        except Exception as e:
            return False, f"❌ Error validando YAML: {e}"
    
    @staticmethod
    def validate_model_data_pair(weights_path: str, data_yaml_path: str) -> tuple[bool, str]:
        """
        Valida que el modelo y los datos sean compatibles.
        
        Args:
            weights_path: Ruta de los pesos
            data_yaml_path: Ruta del archivo data.yaml
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        # Validar cada uno
        weights_valid, weights_msg = InputValidator.validate_weights_path(weights_path)
        if not weights_valid:
            return False, weights_msg
        
        yaml_valid, yaml_msg = InputValidator.validate_yaml_path(data_yaml_path)
        if not yaml_valid:
            return False, yaml_msg
        
        return True, "✅ Modelo y datos son compatibles"
    
    @staticmethod
    def validate_confidence(value: float) -> tuple[bool, str]:
        """
        Valida que el umbral de confianza sea válido.
        
        Args:
            value: Valor de confianza (0-1)
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        if not isinstance(value, (int, float)):
            return False, f"❌ Confianza debe ser un número, se recibió: {type(value)}"
        
        if not 0 <= value <= 1:
            return False, f"❌ Confianza debe estar entre 0 y 1, se recibió: {value}"
        
        return True, f"✅ Confianza válida: {value}"
    
    @staticmethod
    def validate_batch_inputs(batch_dir: str) -> tuple[bool, str]:
        """
        Valida que un directorio sea válido para procesamiento batch.
        
        Args:
            batch_dir: Ruta del directorio batch
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        dir_valid, dir_msg = InputValidator.validate_directory(batch_dir, must_exist=True)
        if not dir_valid:
            return False, dir_msg
        
        # Verificar que contiene imágenes
        p = Path(batch_dir)
        images = [f for f in p.glob("*") 
                 if f.is_file() and f.suffix.lower() in InputValidator.SUPPORTED_IMAGES]
        
        if not images:
            return False, f"❌ No se encontraron imágenes soportadas en: {batch_dir}"
        
        return True, f"✅ Directorio batch válido con {len(images)} imagen(es)"
