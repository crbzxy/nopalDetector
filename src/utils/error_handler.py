"""
Módulo de Manejo de Errores - Nopal Detector
Proporciona decoradores, context managers y retry logic
"""

import logging
import time
from functools import wraps
from typing import Callable, Any, Optional, Type
from contextlib import contextmanager
import cv2

logger = logging.getLogger(__name__)


class ResourceManager:
    """Context manager para OpenCV VideoCapture y VideoWriter"""
    
    def __init__(self, video_path: str, mode: str = 'read'):
        """
        Inicializa el gestor de recursos de video.
        
        Args:
            video_path: Ruta del video
            mode: 'read' para captura, 'write' para escritura
        """
        self.video_path = video_path
        self.mode = mode
        self.cap = None
        self.out = None
        self.frame_width = None
        self.frame_height = None
        self.fps = None
    
    def __enter__(self):
        """Configura el contexto"""
        if self.mode == 'read':
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise RuntimeError(f"❌ No se pudo abrir video: {self.video_path}")
            
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            logger.debug(f"✅ Video abierto para lectura: {self.frame_width}x{self.frame_height} @ {self.fps}fps")
            return self.cap
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Limpia los recursos"""
        if self.cap:
            self.cap.release()
            logger.debug("✅ VideoCapture liberado")
        
        if self.out:
            self.out.release()
            logger.debug("✅ VideoWriter liberado")
        
        if exc_type:
            logger.error(f"❌ Error en context manager: {exc_type.__name__}: {exc_val}")
            return False  # Re-raise la excepción
        
        return True
    
    def create_writer(self, output_path: str, fourcc: str = "mp4v") -> 'ResourceManager':
        """
        Configura el escritor de video.
        
        Args:
            output_path: Ruta del archivo de salida
            fourcc: Código del codec
            
        Returns:
            Self para encadenamiento
        """
        if not self.frame_width or not self.frame_height or not self.fps:
            raise RuntimeError("Primero debe abrir un video para lectura")
        
        fourcc_code = cv2.VideoWriter_fourcc(*fourcc)
        self.out = cv2.VideoWriter(
            output_path,
            fourcc_code,
            self.fps,
            (self.frame_width, self.frame_height)
        )
        
        if not self.out.isOpened():
            raise RuntimeError(f"❌ No se pudo crear VideoWriter: {output_path}")
        
        logger.debug(f"✅ VideoWriter creado: {output_path}")
        return self


@contextmanager
def file_handler(file_path: str, mode: str = 'r'):
    """
    Context manager para manejo seguro de archivos.
    
    Args:
        file_path: Ruta del archivo
        mode: Modo de apertura
        
    Yields:
        Archivo abierto
        
    Example:
        >>> with file_handler("config.yaml", "r") as f:
        ...     data = yaml.safe_load(f)
    """
    file_obj = None
    try:
        file_obj = open(file_path, mode)
        logger.debug(f"✅ Archivo abierto: {file_path}")
        yield file_obj
    except FileNotFoundError:
        logger.error(f"❌ Archivo no encontrado: {file_path}")
        raise
    except IOError as e:
        logger.error(f"❌ Error IO al acceder a {file_path}: {e}")
        raise
    finally:
        if file_obj:
            file_obj.close()
            logger.debug(f"✅ Archivo cerrado: {file_path}")


def retry_on_exception(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorador para reintentar automáticamente.
    
    Args:
        max_retries: Número máximo de intentos
        delay: Delay inicial en segundos
        backoff: Multiplicador de delay entre intentos
        exceptions: Tupla de excepciones a capturar
        
    Returns:
        Función decorada
        
    Example:
        >>> @retry_on_exception(max_retries=3, delay=2)
        ... def download_data():
        ...     # Puede fallar
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    logger.debug(f"[{func.__name__}] Intento {attempt}/{max_retries}")
                    return func(*args, **kwargs)
                
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(
                            f"[{func.__name__}] Falló tras {max_retries} intentos: {e}"
                        )
                        raise
                    
                    logger.warning(
                        f"[{func.__name__}] Intento {attempt} falló: {e}. "
                        f"Reintentando en {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            # Nunca debería llegar aquí
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def handle_validation_errors(func: Callable) -> Callable:
    """
    Decorador para manejar errores de validación.
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada
        
    Example:
        >>> @handle_validation_errors
        ... def process_image(path):
        ...     if not Path(path).exists():
        ...         raise ValueError("Imagen no existe")
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        
        except ValueError as e:
            logger.error(f"[{func.__name__}] Error de validación: {e}")
            raise
        
        except TypeError as e:
            logger.error(f"[{func.__name__}] Error de tipo: {e}")
            raise
        
        except Exception as e:
            logger.error(f"[{func.__name__}] Error inesperado: {type(e).__name__}: {e}")
            raise
    
    return wrapper


def safe_operation(
    operation_name: str,
    default_return: Optional[Any] = None,
    log_level: str = 'error'
):
    """
    Decorador para operaciones que pueden fallar silenciosamente.
    
    Args:
        operation_name: Nombre de la operación (para logs)
        default_return: Valor a retornar en caso de error
        log_level: Nivel de log ('error', 'warning', 'info')
        
    Returns:
        Función decorada
        
    Example:
        >>> @safe_operation("load_config", default_return={})
        ... def load_config(path):
        ...     with open(path) as f:
        ...         return yaml.load(f)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                log_func = getattr(logger, log_level, logger.error)
                log_func(
                    f"[{operation_name}] Falló: {type(e).__name__}: {e}. "
                    f"Retornando valor por defecto: {default_return}"
                )
                return default_return
        
        return wrapper
    return decorator


class ErrorContext:
    """Context manager para manejo granular de errores"""
    
    def __init__(
        self,
        operation_name: str,
        raise_on_error: bool = True,
        default_value: Optional[Any] = None
    ):
        """
        Inicializa el contexto de error.
        
        Args:
            operation_name: Nombre de la operación
            raise_on_error: Si re-lanzar la excepción
            default_value: Valor si no se lanza excepción
        """
        self.operation_name = operation_name
        self.raise_on_error = raise_on_error
        self.default_value = default_value
        self.exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.exception = exc_val
            
            if self.raise_on_error:
                logger.error(
                    f"[{self.operation_name}] Error: {exc_type.__name__}: {exc_val}"
                )
                return False  # Re-raise
            else:
                logger.warning(
                    f"[{self.operation_name}] Error capturado silenciosamente: "
                    f"{exc_type.__name__}: {exc_val}"
                )
                return True  # Suprimir la excepción
        
        return True


def log_execution_time(func: Callable) -> Callable:
    """
    Decorador que registra el tiempo de ejecución.
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"[{func.__name__}] Completado en {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"[{func.__name__}] Falló tras {elapsed:.2f}s: {e}")
            raise
    
    return wrapper
