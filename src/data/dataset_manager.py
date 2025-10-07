"""
Dataset Manager para Nopal Detector
Maneja la descarga, preparación y organización del dataset desde Roboflow
"""

import os
import yaml
import shutil
import random
from typing import Dict, Any, Optional
from roboflow import Roboflow


class DatasetManager:
    """Gestor del dataset para el proyecto de detección de nopales"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el gestor del dataset
        
        Args:
            config: Configuración del proyecto
        """
        self.config = config
        self.rf_config = config['roboflow']
        self.data_config = config['data']
        self.dataset = None
        self.dataset_location = None
        
        # Validar que tengamos API key
        if not self.rf_config.get('api_key'):
            raise ValueError(
                "❌ API key de Roboflow no encontrada en la configuración. "
                "Asegúrate de configurar la variable de entorno ROBOFLOW_API_KEY"
            )
        
    def download_dataset(self) -> str:
        """
        Descarga el dataset desde Roboflow
        
        Returns:
            str: Ruta del dataset descargado
        """
        print("🗂️ Descargando dataset desde Roboflow...")
        
        rf = Roboflow(api_key=self.rf_config['api_key'])
        project = rf.workspace(self.rf_config['workspace']).project(self.rf_config['project'])
        version = project.version(self.rf_config['version'])
        self.dataset = version.download(self.rf_config['format'])
        self.dataset_location = self.dataset.location
        
        print(f"✅ Dataset descargado en: {self.dataset_location}")
        return self.dataset_location
    
    def prepare_dataset(self) -> Dict[str, str]:
        """
        Prepara y organiza el dataset creando las carpetas necesarias
        
        Returns:
            Dict[str, str]: Rutas de las carpetas del dataset
        """
        if not self.dataset_location:
            raise ValueError("Primero debe descargar el dataset")
            
        print("📂 Preparando estructura del dataset...")
        
        base_dir = self.dataset_location
        
        # Definir rutas
        paths = {
            'train_img': os.path.join(base_dir, "train/images"),
            'train_lbl': os.path.join(base_dir, "train/labels"),
            'valid_img': os.path.join(base_dir, "valid/images"),
            'valid_lbl': os.path.join(base_dir, "valid/labels"),
            'test_img': os.path.join(base_dir, "test/images"),
            'test_lbl': os.path.join(base_dir, "test/labels")
        }
        
        # Crear todas las carpetas
        for path in paths.values():
            os.makedirs(path, exist_ok=True)
            
        # Crear validación si no existe
        self._create_validation_split(paths)
        
        # Actualizar data.yaml
        self._update_data_yaml(base_dir, paths)
        
        print("✅ Dataset preparado correctamente")
        return paths
    
    def _create_validation_split(self, paths: Dict[str, str]) -> None:
        """
        Crea un split de validación si no existe
        
        Args:
            paths: Diccionario con las rutas del dataset
        """
        train_img_dir = paths['train_img']
        train_lbl_dir = paths['train_lbl']
        valid_img_dir = paths['valid_img']
        valid_lbl_dir = paths['valid_lbl']
        
        if not os.listdir(valid_img_dir):
            print("⚠️ No se encontró carpeta de validación, creando split...")
            
            all_imgs = [f for f in os.listdir(train_img_dir) 
                       if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            
            if all_imgs:
                random.seed(self.data_config['random_seed'])
                split_size = max(1, int(len(all_imgs) * self.data_config['validation_split']))
                sampled = random.sample(all_imgs, split_size)
                
                for img in sampled:
                    lbl = os.path.splitext(img)[0] + ".txt"
                    
                    # Mover imagen
                    shutil.move(
                        os.path.join(train_img_dir, img),
                        os.path.join(valid_img_dir, img)
                    )
                    
                    # Mover label si existe
                    lbl_path = os.path.join(train_lbl_dir, lbl)
                    if os.path.exists(lbl_path):
                        shutil.move(
                            lbl_path,
                            os.path.join(valid_lbl_dir, lbl)
                        )
                
                print(f"✅ Movidas {len(sampled)} imágenes a validación")
            else:
                print("⚠️ No hay imágenes en train para dividir")
    
    def _update_data_yaml(self, base_dir: str, paths: Dict[str, str]) -> None:
        """
        Actualiza el archivo data.yaml con las rutas correctas
        
        Args:
            base_dir: Directorio base del dataset
            paths: Diccionario con las rutas del dataset
        """
        data_yaml_path = os.path.join(base_dir, "data.yaml")
        
        with open(data_yaml_path, "r") as f:
            data_yaml = yaml.safe_load(f)
        
        # Actualizar rutas
        data_yaml["train"] = paths['train_img']
        data_yaml["val"] = paths['valid_img']
        
        # Solo incluir test si hay imágenes
        test_img_dir = paths['test_img']
        if any(f.lower().endswith((".jpg", ".jpeg", ".png")) 
               for f in os.listdir(test_img_dir)):
            data_yaml["test"] = test_img_dir
        else:
            if "test" in data_yaml:
                del data_yaml["test"]
            print("⚠️ No hay imágenes de test, omitiendo del data.yaml")
        
        # Guardar archivo actualizado
        with open(data_yaml_path, "w") as f:
            yaml.dump(data_yaml, f)
        
        print(f"✅ data.yaml actualizado: {data_yaml_path}")
    
    def get_data_yaml_path(self) -> Optional[str]:
        """
        Obtiene la ruta del archivo data.yaml
        
        Returns:
            str: Ruta del archivo data.yaml o None si no existe
        """
        if self.dataset_location:
            return os.path.join(self.dataset_location, "data.yaml")
        return None