"""
Utilidades para visualización de resultados
"""

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict, Any
from PIL import Image


class ResultVisualizer:
    """Clase para visualizar resultados de detección"""
    
    def __init__(self, output_dir: str = "outputs/visualizations"):
        """
        Inicializa el visualizador
        
        Args:
            output_dir: Directorio para guardar visualizaciones
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_training_results(self, results_dir: str = "runs/detect/train") -> str:
        """
        Grafica los resultados del entrenamiento
        
        Args:
            results_dir: Directorio con los resultados del entrenamiento
            
        Returns:
            str: Ruta del archivo de gráficos guardado
        """
        print("📊 Generando gráficos de entrenamiento...")
        
        results_path = os.path.join(results_dir, "results.csv")
        if not os.path.exists(results_path):
            print(f"⚠️ No se encontró {results_path}")
            return None
        
        # Leer resultados
        import pandas as pd
        df = pd.read_csv(results_path)
        df.columns = df.columns.str.strip()  # Limpiar espacios
        
        # Crear subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Resultados del Entrenamiento YOLOv11 - Nopal Detector', fontsize=16)
        
        # Loss curves
        if 'train/box_loss' in df.columns:
            ax1.plot(df.index, df['train/box_loss'], label='Train Box Loss', color='blue')
            ax1.plot(df.index, df['val/box_loss'], label='Val Box Loss', color='red')
            ax1.set_title('Box Loss')
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Loss')
            ax1.legend()
            ax1.grid(True)
        
        # mAP curves
        if 'metrics/mAP50(B)' in df.columns:
            ax2.plot(df.index, df['metrics/mAP50(B)'], label='mAP@0.5', color='green')
            ax2.plot(df.index, df['metrics/mAP50-95(B)'], label='mAP@0.5:0.95', color='orange')
            ax2.set_title('Mean Average Precision')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('mAP')
            ax2.legend()
            ax2.grid(True)
        
        # Precision and Recall
        if 'metrics/precision(B)' in df.columns:
            ax3.plot(df.index, df['metrics/precision(B)'], label='Precision', color='purple')
            ax3.plot(df.index, df['metrics/recall(B)'], label='Recall', color='brown')
            ax3.set_title('Precision & Recall')
            ax3.set_xlabel('Epoch')
            ax3.set_ylabel('Score')
            ax3.legend()
            ax3.grid(True)
        
        # Learning rate
        if 'lr/pg0' in df.columns:
            ax4.plot(df.index, df['lr/pg0'], label='Learning Rate', color='red')
            ax4.set_title('Learning Rate')
            ax4.set_xlabel('Epoch')
            ax4.set_ylabel('LR')
            ax4.legend()
            ax4.grid(True)
        
        plt.tight_layout()
        
        # Guardar gráfico
        output_path = os.path.join(self.output_dir, "training_results.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráficos guardados en: {output_path}")
        return output_path
    
    def create_detection_grid(self, predictions_dir: str, max_images: int = 9) -> str:
        """
        Crea una grilla con las mejores detecciones
        
        Args:
            predictions_dir: Directorio con las predicciones
            max_images: Número máximo de imágenes en la grilla
            
        Returns:
            str: Ruta del archivo de grilla guardado
        """
        print("🖼️ Creando grilla de detecciones...")
        
        # Obtener imágenes
        image_files = [f for f in os.listdir(predictions_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            print("⚠️ No se encontraron imágenes en el directorio de predicciones")
            return None
        
        # Limitar número de imágenes
        image_files = image_files[:max_images]
        
        # Calcular dimensiones de la grilla
        cols = int(np.ceil(np.sqrt(len(image_files))))
        rows = int(np.ceil(len(image_files) / cols))
        
        # Crear figura
        fig, axes = plt.subplots(rows, cols, figsize=(20, 20))
        fig.suptitle('Detecciones de Nopales y Personas', fontsize=16)
        
        # Si solo hay una imagen, convertir axes a array
        if len(image_files) == 1:
            axes = [axes]
        elif rows == 1 or cols == 1:
            axes = axes.flatten()
        else:
            axes = axes.flatten()
        
        # Mostrar imágenes
        for i, img_file in enumerate(image_files):
            img_path = os.path.join(predictions_dir, img_file)
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            axes[i].imshow(img_rgb)
            axes[i].set_title(img_file, fontsize=10)
            axes[i].axis('off')
        
        # Ocultar axes vacíos
        for i in range(len(image_files), len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        
        # Guardar grilla
        output_path = os.path.join(self.output_dir, "detection_grid.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Grilla guardada en: {output_path}")
        return output_path
    
    def plot_detection_stats(self, stats: Dict[str, int]) -> str:
        """
        Grafica estadísticas de detección
        
        Args:
            stats: Diccionario con estadísticas
            
        Returns:
            str: Ruta del archivo de estadísticas guardado
        """
        print("📈 Generando gráfico de estadísticas...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Estadísticas de Detección', fontsize=16)
        
        # Gráfico de barras
        categories = ['Nopales', 'Personas']
        counts = [stats['total_nopales'], stats['total_persons']]
        colors = ['green', 'blue']
        
        ax1.bar(categories, counts, color=colors, alpha=0.7)
        ax1.set_title('Detecciones Totales')
        ax1.set_ylabel('Número de Detecciones')
        
        # Agregar valores en las barras
        for i, count in enumerate(counts):
            ax1.text(i, count + max(counts) * 0.01, str(count), 
                    ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de pastel
        if sum(counts) > 0:
            ax2.pie(counts, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Distribución de Detecciones')
        
        plt.tight_layout()
        
        # Guardar gráfico
        output_path = os.path.join(self.output_dir, "detection_stats.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Estadísticas guardadas en: {output_path}")
        return output_path
    
    def create_comparison_view(self, original_dir: str, predictions_dir: str, 
                             max_pairs: int = 6) -> str:
        """
        Crea una vista de comparación antes/después
        
        Args:
            original_dir: Directorio con imágenes originales
            predictions_dir: Directorio con predicciones
            max_pairs: Número máximo de pares a mostrar
            
        Returns:
            str: Ruta del archivo de comparación guardado
        """
        print("🔄 Creando vista de comparación...")
        
        # Encontrar imágenes comunes
        orig_files = set(os.listdir(original_dir))
        pred_files = set(os.listdir(predictions_dir))
        common_files = list(orig_files.intersection(pred_files))
        
        if not common_files:
            print("⚠️ No se encontraron imágenes comunes")
            return None
        
        # Limitar número de comparaciones
        common_files = common_files[:max_pairs]
        
        # Crear figura
        fig, axes = plt.subplots(len(common_files), 2, figsize=(16, 6 * len(common_files)))
        fig.suptitle('Comparación: Original vs Detecciones', fontsize=16)
        
        if len(common_files) == 1:
            axes = axes.reshape(1, -1)
        
        for i, img_file in enumerate(common_files):
            # Imagen original
            orig_path = os.path.join(original_dir, img_file)
            orig_img = cv2.imread(orig_path)
            orig_rgb = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
            
            # Imagen con detecciones
            pred_path = os.path.join(predictions_dir, img_file)
            pred_img = cv2.imread(pred_path)
            pred_rgb = cv2.cvtColor(pred_img, cv2.COLOR_BGR2RGB)
            
            axes[i, 0].imshow(orig_rgb)
            axes[i, 0].set_title(f'Original: {img_file}', fontsize=10)
            axes[i, 0].axis('off')
            
            axes[i, 1].imshow(pred_rgb)
            axes[i, 1].set_title(f'Con Detecciones: {img_file}', fontsize=10)
            axes[i, 1].axis('off')
        
        plt.tight_layout()
        
        # Guardar comparación
        output_path = os.path.join(self.output_dir, "comparison_view.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Comparación guardada en: {output_path}")
        return output_path