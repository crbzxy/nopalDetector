#!/usr/bin/env python3
"""
🏷️ Actualizador de Etiquetas - Nopal Detector
Detecta automáticamente nuevas etiquetas en Roboflow y actualiza el modelo
"""

import os
import yaml
import json
from roboflow import Roboflow
from dotenv import load_dotenv
from pathlib import Path

class LabelUpdater:
    def __init__(self, config=None):
        """Inicializar el actualizador de etiquetas"""
        load_dotenv()
        self.api_key = os.getenv('ROBOFLOW_API_KEY')
        self.workspace = None
        self.project = None
        self.current_version = None
        self.config = config
        self.load_config()
        
    def load_config(self):
        """Cargar configuración desde model_config.yaml o usar la proporcionada"""
        try:
            if self.config:
                # Usar configuración proporcionada
                roboflow_config = self.config.get('roboflow', {})
            else:
                # Cargar desde archivo
                with open('config/model_config.yaml', 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    roboflow_config = config.get('roboflow', {})
                    
            self.workspace_id = roboflow_config.get('workspace')
            self.project_name = roboflow_config.get('project')
            self.current_version = roboflow_config.get('version', 1)
            
            print("✅ Configuración cargada:")
            print(f"   🔗 Workspace: {self.workspace_id}")
            print(f"   📋 Proyecto: {self.project_name}")
            print(f"   📊 Versión actual: {self.current_version}")
            
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            raise
            
    def get_current_labels(self):
        """Obtener etiquetas actuales del dataset local"""
        try:
            data_yaml_path = f"nopal-detector-{self.current_version}/data.yaml"
            
            if not os.path.exists(data_yaml_path):
                print(f"⚠️ No se encontró {data_yaml_path}")
                return []
            
            with open(data_yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                current_labels = data.get('names', [])
                
            print(f"📋 Etiquetas actuales: {current_labels}")
            return current_labels
            
        except Exception as e:
            print(f"❌ Error obteniendo etiquetas actuales: {e}")
            return []
            
    def get_roboflow_info(self):
        """Obtener información actual del proyecto en Roboflow"""
        try:
            if not self.api_key:
                print("❌ Error: ROBOFLOW_API_KEY no configurado")
                return None, None
                
            rf = Roboflow(api_key=self.api_key)
            project = rf.workspace(self.workspace_id).project(self.project_name)
            
            # Obtener todas las versiones disponibles
            versions_list = project.versions()
            print(f"🔍 Debug: Encontradas {len(versions_list)} versiones")
            
            if not versions_list:
                print("❌ No se encontraron versiones en el proyecto")
                return None, None
            
            # Obtener la última versión (la de mayor número)
            latest_version_num = 0
            latest_version_obj = None
            
            for version_obj in versions_list:
                version_num = version_obj.version
                print(f"🔍 Debug: Versión encontrada: {version_num}")
                
                # Convertir a entero para comparar
                try:
                    version_int = int(version_num)
                except (ValueError, TypeError):
                    print(f"⚠️ Warning: No se pudo convertir versión {version_num} a entero")
                    continue
                
                if version_int > latest_version_num:
                    latest_version_num = version_int
                    latest_version_obj = version_obj
            
            print(f"🔍 Debug: Última versión seleccionada: {latest_version_num}")
            
            # Usar el objeto de la última versión
            latest_version = latest_version_obj
            
            # Obtener clases de la última versión - acceder al model
            try:
                # Intentar obtener clases del modelo
                model_classes = latest_version.model.classes if hasattr(latest_version, 'model') else None
                if model_classes:
                    latest_classes = [{'name': cls} for cls in model_classes]
                else:
                    # Alternativa: obtener desde el dataset
                    latest_classes = [{'name': 'nopal'}]  # Fallback temporal
                    print("⚠️ Usando clases por defecto - no se pudieron obtener desde Roboflow")
            except Exception as class_error:
                print(f"⚠️ Error obteniendo clases: {class_error}")
                latest_classes = [{'name': 'nopal'}]  # Fallback
            
            print(f"🔗 Última versión en Roboflow: {latest_version_num}")
            print(f"🏷️ Clases disponibles: {latest_classes}")
            
            return latest_version_num, latest_classes
            
        except Exception as e:
            print(f"❌ Error conectando con Roboflow: {e}")
            print(f"🔍 Debug: Tipo de error: {type(e)}")
            import traceback
            traceback.print_exc()
            return None, None
            
    def compare_labels(self, current_labels, roboflow_classes):
        """Comparar etiquetas locales vs Roboflow"""
        if not roboflow_classes:
            return False
            
        # Convertir classes de Roboflow a lista de nombres
        roboflow_labels = [cls['name'] for cls in roboflow_classes]
        
        print("\\n📊 COMPARACIÓN DE ETIQUETAS:")
        print(f"   📁 Local: {current_labels}")
        print(f"   ☁️ Roboflow: {roboflow_labels}")
        
        # Verificar si hay diferencias
        if set(current_labels) == set(roboflow_labels):
            print("   ✅ Sin cambios en etiquetas")
            return False
        else:
            print("   🆕 ¡Nuevas etiquetas detectadas!")
            new_labels = set(roboflow_labels) - set(current_labels)
            removed_labels = set(current_labels) - set(roboflow_labels)
            
            if new_labels:
                print(f"   ➕ Nuevas: {list(new_labels)}")
            if removed_labels:
                print(f"   ➖ Removidas: {list(removed_labels)}")
                
            return True
            
    def download_latest_dataset(self, version_num):
        """Descargar la última versión del dataset desde Roboflow"""
        try:
            print(f"📥 Descargando dataset versión {version_num}...")
            
            rf = Roboflow(api_key=self.api_key)
            project = rf.workspace(self.workspace_id).project(self.project_name)
            version = project.version(version_num)
            
            dataset = version.download("yolov11", location=".")
            
            print(f"✅ Dataset descargado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error descargando dataset: {e}")
            return False
            
    def update_config(self, new_version, new_labels):
        """Actualizar configuración con nueva versión"""
        try:
            # Leer configuración actual
            with open('config/model_config.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Actualizar versión
            config['roboflow']['version'] = new_version
            
            # Guardar configuración actualizada
            with open('config/model_config.yaml', 'w', encoding='utf-8') as f:
                yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
            
            # Crear backup de configuración anterior
            backup_file = f"config/model_config_v{self.current_version}_backup.yaml"
            with open(backup_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
            
            print(f"✅ Configuración actualizada a versión {new_version}")
            print(f"💾 Backup guardado en: {backup_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error actualizando configuración: {e}")
            return False
            
    def check_for_updates(self):
        """Verificar si hay actualizaciones disponibles"""
        print("🔍 Verificando actualizaciones en Roboflow...")
        
        # Obtener etiquetas actuales
        current_labels = self.get_current_labels()
        
        # Obtener información de Roboflow
        latest_version, roboflow_classes = self.get_roboflow_info()
        
        if not latest_version or not roboflow_classes:
            print("❌ No se pudo verificar actualizaciones")
            return False
        
        # Verificar si hay nueva versión
        if latest_version > self.current_version:
            print("\\n🚀 ¡ACTUALIZACIÓN DISPONIBLE!")
            print(f"   📊 Versión actual: {self.current_version}")
            print(f"   🆕 Versión disponible: {latest_version}")
            return True
        
        # Verificar si hay cambios en etiquetas (misma versión)
        has_label_changes = self.compare_labels(current_labels, roboflow_classes)
        
        if has_label_changes:
            print("\\n🏷️ ¡CAMBIOS EN ETIQUETAS DETECTADOS!")
            return True
        
        print("\\n✅ Dataset actualizado - sin cambios")
        return False
        
    def update_dataset(self):
        """Actualizar dataset completo"""
        try:
            print("\\n🔄 Iniciando actualización del dataset...")
            
            # Obtener información actual de Roboflow
            latest_version, roboflow_classes = self.get_roboflow_info()
            
            if not latest_version:
                print("❌ No se pudo obtener información de Roboflow")
                return False
            
            # Descargar dataset más reciente
            if not self.download_latest_dataset(latest_version):
                return False
            
            # Actualizar configuración si es una nueva versión
            if latest_version > self.current_version:
                roboflow_labels = [cls['name'] for cls in roboflow_classes]
                if not self.update_config(latest_version, roboflow_labels):
                    return False
            
            print("\\n🎉 ¡ACTUALIZACIÓN COMPLETADA!")
            print(f"📊 Dataset actualizado a versión {latest_version}")
            
            if roboflow_classes:
                labels = [cls['name'] for cls in roboflow_classes]
                print(f"🏷️ Etiquetas disponibles: {labels}")
            
            print("\\n💡 PRÓXIMOS PASOS:")
            print("   1. Revisar el nuevo dataset")
            print("   2. Entrenar modelo con nuevas etiquetas:")
            print(f"      python main.py --mode train --multi-class --data nopal-detector-{latest_version}/data.yaml")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en actualización: {e}")
            return False

def main():
    """Función principal para ejecución directa"""
    print("🏷️ =======================================")
    print("🏷️   Nopal Detector")
    print("🏷️   Actualizador de Labels")
    print("🏷️ =======================================")
    
    try:
        # Crear actualizador
        updater = LabelUpdater()
        
        # Verificar actualizaciones
        if updater.check_for_updates():
            response = input("\\n¿Deseas actualizar el dataset? (s/N): ").lower().strip()
            
            if response in ['s', 'si', 'sí', 'y', 'yes']:
                updater.update_dataset()
            else:
                print("⏭️ Actualización cancelada")
        else:
            print("\\n✅ No hay actualizaciones disponibles")
            
    except KeyboardInterrupt:
        print("\\n⏹️ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()