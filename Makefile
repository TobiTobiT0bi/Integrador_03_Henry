.PHONY: help setup generate run clean status

# Forzamos a que todas las ejecuciones usen el cli de uv
PYTHON_RUN = uv run python

help:
	@echo "====================================================================="
	@echo "    SISTEMA MULTIAGENTE ORQUESTADO (RAG + LANGFUSE) - NATIVO UV"
	@echo "====================================================================="
	@echo "Comandos disponibles:"
	@echo "  make setup      - Sincroniza el entorno de forma nativa con 'uv sync'"
	@echo "  make generate   - Genera los documentos masivos con 'uv run'"
	@echo "  make run        - Ejecuta las pruebas del Golden Dataset con 'uv run'"
	@echo "  make status     - Verifica el estado de los archivos de configuracion"
	@echo "  make clean      - Elimina la base de datos local y la cache de Python"
	@echo "====================================================================="

setup:
	@echo "📥 Sincronizando entorno y dependencias con uv sync..."
	uv sync
	
	@echo "⚙️ Verificando archivo de entorno (.env)..."
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			echo "📄 Creando .env desde plantilla .env.example..."; \
			cp .env.example .env; \
		else \
			echo "⚠️ Alerta: No se encontró .env.example para generar el archivo base."; \
		fi; \
	else \
		echo "🔒 Archivo .env ya existente. Conservando configuración actual."; \
	fi
	@echo "✅ Entorno alineado y listo."

generate:
	@echo "📈 Inyectando manuales densos en las carpetas de conocimiento..."
	$(PYTHON_RUN) -m src.generate_knowledge

run:
	@echo "🚀 Iniciando consola interactiva..."
	$(PYTHON_RUN) -m src.multi_agent_system

test:
	@echo "🧪 Ejecutando pruebas del Golden Dataset..."
	$(PYTHON_RUN) -m src.multi_agent_system --test

status:
	@echo "🔍 Verificando estado de la infraestructura..."
	@echo "• Archivo .env:"
	@if [ -f .env ]; then echo "  [OK] Encontrado"; else echo "  [FALTA] No configurado (.env.example detectado)"; fi
	@echo "• Dataset de pruebas (test_queries.json):"
	@if [ -f test_queries.json ]; then echo "  [OK] Encontrado"; else echo "  [FALTA] Modo fallback básico."; fi
	@echo "• Base Vectorial Integrada:"
	@if [ -d data/chroma_db ]; then echo "  [OK] Inicializada localmente"; else echo "  [PENDIENTE] Se creará al iniciar."; fi

clean:
	@echo "🧹 Eliminando base de datos Chroma local..."
	rm -rf data/chroma_db
	@echo "🧹 Limpiando archivos de caché de Python..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✨ Limpieza completada."