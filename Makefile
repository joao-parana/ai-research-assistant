.PHONY: help install test test-cov lint fmt clean build docs run-demo

# Cores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)MCP Server - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala o projeto em modo desenvolvimento
	@echo "$(BLUE)Instalando projeto...$(NC)"
	hatch env create
	@echo "$(GREEN)✓ Instalação completa!$(NC)"

install-dev: ## Instala com dependências de desenvolvimento
	@echo "$(BLUE)Instalando com dev dependencies...$(NC)"
	pip install -e ".[dev]"
	@echo "$(GREEN)✓ Instalação completa!$(NC)"

test: ## Executa todos os testes
	@echo "$(BLUE)Executando testes...$(NC)"
	hatch run test

test-cov: ## Executa testes com cobertura
	@echo "$(BLUE)Executando testes com cobertura...$(NC)"
	hatch run test-cov

test-html: ## Gera relatório HTML de cobertura
	@echo "$(BLUE)Gerando relatório HTML...$(NC)"
	hatch run cov-report
	@echo "$(GREEN)✓ Relatório em htmlcov/index.html$(NC)"

lint: ## Verifica estilo e tipos
	@echo "$(BLUE)Verificando código...$(NC)"
	hatch run lint:all

fmt: ## Formata o código
	@echo "$(BLUE)Formatando código...$(NC)"
	hatch run lint:fmt
	@echo "$(GREEN)✓ Código formatado!$(NC)"

typing: ## Verifica tipos com mypy
	@echo "$(BLUE)Verificando tipos...$(NC)"
	hatch run lint:typing

clean: ## Remove arquivos gerados
	@echo "$(BLUE)Limpando projeto...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf dist/ build/ 2>/dev/null || true
	@echo "$(GREEN)✓ Projeto limpo!$(NC)"

build: clean ## Build do pacote
	@echo "$(BLUE)Building pacote...$(NC)"
	hatch build
	@echo "$(GREEN)✓ Build completo em dist/$(NC)"

run-demo: ## Executa a demo
	@echo "$(BLUE)Executando demo...$(NC)"
	mcp-demo

run-example: ## Executa exemplo rápido
	@echo "$(BLUE)Executando exemplo...$(NC)"
	python examples/quick_start.py

analyze: ## Analisa o projeto atual
	@echo "$(BLUE)Analisando projeto atual...$(NC)"
	mcp-analyze --project . --output analysis_report.json

shell: ## Abre shell do Hatch
	@echo "$(BLUE)Abrindo shell...$(NC)"
	hatch shell

version: ## Mostra versão
	@echo "$(BLUE)MCP Server$(NC)"
	@python -c "from mcp_server import __version__; print(f'Version: {__version__}')"

deps: ## Lista dependências
	@echo "$(BLUE)Dependências instaladas:$(NC)"
	pip list

check-python: ## Verifica versão do Python
	@echo "$(BLUE)Versão do Python:$(NC)"
	@python --version

setup: install test ## Setup completo (install + test)
	@echo "$(GREEN)✓ Setup completo!$(NC)"

ci: lint test ## Simula CI pipeline
	@echo "$(GREEN)✓ CI pipeline completo!$(NC)"

all: clean fmt lint test build ## Executa tudo
	@echo "$(GREEN)✓ Todos os passos completos!$(NC)"

dev: ## Inicia desenvolvimento (instala + shell)
	@echo "$(BLUE)Preparando ambiente de desenvolvimento...$(NC)"
	$(MAKE) install-dev
	@echo "$(GREEN)✓ Pronto! Use 'make shell' para ativar o ambiente$(NC)"

.DEFAULT_GOAL := help
