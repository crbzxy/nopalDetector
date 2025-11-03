.PHONY: help install clean test train predict camera list-cameras validate

# Variables
PYTHON := venv/bin/python
PIP := venv/bin/pip
VENV := venv

help: ## Mostrar ayuda
	@echo "🌵 Nopal Detector - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias y configurar entorno
	@echo "🌵 Instalando Nopal Detector..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "📦 Creando entorno virtual..."; \
		python3 -m venv venv; \
	fi
	@echo "⬆️  Actualizando pip..."
	@$(PIP) install --upgrade pip
	@echo "📚 Instalando dependencias..."
	@$(PIP) install -r requirements.txt
	@echo "📁 Creando directorios..."
	@mkdir -p data/raw models/weights outputs/predictions outputs/videos outputs/visualizations
	@if [ ! -f ".env" ]; then \
		echo "⚙️  Creando archivo .env..."; \
		cp .env.example .env; \
		echo "⚠️  IMPORTANTE: Edita el archivo .env con tu API key de Roboflow"; \
	fi
	@echo "✅ Instalación completada!"

clean: ## Limpiar archivos temporales y cache
	@echo "🧹 Limpiando archivos temporales..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.log" -delete
	@echo "✅ Limpieza completada!"

clean-all: clean ## Limpiar todo incluyendo venv y runs
	@echo "🧹 Limpiando entorno virtual y runs..."
	@rm -rf venv/
	@rm -rf runs/
	@rm -rf outputs/predictions/*
	@rm -rf outputs/videos/*
	@echo "✅ Limpieza total completada!"

list-cameras: ## Listar cámaras disponibles
	@$(PYTHON) main.py --mode list-cameras

train: ## Entrenar modelo (requiere data.yaml)
	@if [ -z "$(DATA)" ]; then \
		echo "❌ Error: Especifica DATA=path/to/data.yaml"; \
		echo "Ejemplo: make train DATA=nopal-detector-4/data.yaml"; \
		exit 1; \
	fi
	@$(PYTHON) main.py --mode train --multi-class --data $(DATA)

predict-image: ## Predecir sobre imagen (requiere WEIGHTS e INPUT)
	@if [ -z "$(WEIGHTS)" ] || [ -z "$(INPUT)" ]; then \
		echo "❌ Error: Especifica WEIGHTS y INPUT"; \
		echo "Ejemplo: make predict-image WEIGHTS=runs/detect/train6/weights/best.pt INPUT=imagen.jpg"; \
		exit 1; \
	fi
	@$(PYTHON) main.py --mode predict --multi-class --weights $(WEIGHTS) --input $(INPUT)

predict-dir: ## Predecir sobre directorio (requiere WEIGHTS y SOURCE)
	@if [ -z "$(WEIGHTS)" ] || [ -z "$(SOURCE)" ]; then \
		echo "❌ Error: Especifica WEIGHTS y SOURCE"; \
		echo "Ejemplo: make predict-dir WEIGHTS=runs/detect/train6/weights/best.pt SOURCE=nopal-detector-4/images/val"; \
		exit 1; \
	fi
	@$(PYTHON) main.py --mode predict --source $(SOURCE) --weights $(WEIGHTS)

camera: ## Ejecutar detección en tiempo real (requiere WEIGHTS)
	@if [ -z "$(WEIGHTS)" ]; then \
		echo "❌ Error: Especifica WEIGHTS"; \
		echo "Ejemplo: make camera WEIGHTS=runs/detect/train6/weights/best.pt CAMERA=0"; \
		exit 1; \
	fi
	@$(PYTHON) main.py --mode camera --multi-class --weights $(WEIGHTS) --camera $(or $(CAMERA),0)

validate: ## Validar modelo (requiere WEIGHTS y DATA)
	@if [ -z "$(WEIGHTS)" ] || [ -z "$(DATA)" ]; then \
		echo "❌ Error: Especifica WEIGHTS y DATA"; \
		echo "Ejemplo: make validate WEIGHTS=runs/detect/train6/weights/best.pt DATA=nopal-detector-4/data.yaml"; \
		exit 1; \
	fi
	@$(PYTHON) main.py --mode validate --weights $(WEIGHTS) --data $(DATA)

update-labels: ## Actualizar etiquetas desde Roboflow
	@$(PYTHON) main.py --mode update-labels --auto-update

check-env: ## Verificar configuración del entorno
	@echo "🔍 Verificando configuración..."
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Pip: $$($(PIP) --version)"
	@if [ -f ".env" ]; then \
		echo "✅ Archivo .env encontrado"; \
	else \
		echo "⚠️  Archivo .env no encontrado (usa 'make install')"; \
	fi
	@if [ -d "$(VENV)" ]; then \
		echo "✅ Entorno virtual encontrado"; \
	else \
		echo "⚠️  Entorno virtual no encontrado (usa 'make install')"; \
	fi
	@echo ""
	@echo "📦 Paquetes instalados:"
	@$(PIP) list | grep -E "(ultralytics|roboflow|opencv|supervision)"

setup-test: ## Crear directorio de test con imágenes de ejemplo
	@echo "📁 Creando directorio de test..."
	@if [ -z "$(DATASET)" ]; then \
		echo "❌ Error: Especifica DATASET"; \
		echo "Ejemplo: make setup-test DATASET=nopal-detector-4"; \
		exit 1; \
	fi
	@mkdir -p $(DATASET)/images/test
	@if [ -d "$(DATASET)/images/val" ]; then \
		cp $(DATASET)/images/val/* $(DATASET)/images/test/ 2>/dev/null || true; \
		echo "✅ Directorio de test creado con imágenes de validación"; \
	else \
		echo "⚠️  Directorio de validación no encontrado"; \
	fi

status: ## Mostrar estado del proyecto
	@echo "🌵 Estado del proyecto Nopal Detector"
	@echo "======================================"
	@echo ""
	@echo "📊 Estructura:"
	@ls -lh runs/detect/ 2>/dev/null | tail -n +2 || echo "  No hay entrenamientos aún"
	@echo ""
	@echo "🏋️  Último entrenamiento:"
	@ls -lt runs/detect/*/weights/best.pt 2>/dev/null | head -1 || echo "  No hay pesos entrenados"
	@echo ""
	@echo "📁 Datasets:"
	@ls -d nopal-detector-*/ 2>/dev/null || echo "  No hay datasets descargados"
