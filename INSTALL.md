# 🚀 Guia de Instalação e Setup

Este guia mostra como configurar e começar a usar o MCP Server.

## Pré-requisitos

- Python 3.13 ou superior
- Hatch (instalado globalmente)

## Instalação do Hatch

Se você ainda não tem o Hatch instalado:

```bash
# Usando pip
pip install hatch

# Usando pipx (recomendado)
pipx install hatch

# Verificar instalação
hatch --version
```

## Setup do Projeto

### 1. Navegue até o diretório do projeto

```bash
cd /Users/joao/dev/code_with_ai/claude/claude/python/mcp-server
```

### 2. Crie o ambiente virtual com Hatch

```bash
# Hatch cria automaticamente o ambiente
hatch env create
```

### 3. Instale em modo desenvolvimento

```bash
# Usando Hatch
hatch shell

# Ou usando pip diretamente
pip install -e .
```

### 4. Instale dependências de desenvolvimento (opcional)

```bash
pip install -e ".[dev]"
```

## Verificação da Instalação

### Teste os comandos CLI

```bash
# Comando principal
mcp-server --help

# Demo
mcp-demo

# Análise
mcp-analyze --help
```

### Execute os testes

```bash
# Usando Hatch
hatch run test

# Com cobertura
hatch run test-cov
```

### Execute o exemplo rápido

```bash
cd examples
python quick_start.py
```

## Configuração do Ambiente

### Variáveis de Ambiente (opcional)

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
HUGGINGFACE_TOKEN=your_token_here
POSTGRES_URL=postgresql://localhost/mcp_server
```

### Configuração do IDE

#### VSCode

Crie `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

#### PyCharm

1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing environment
3. Selecione: `.venv/bin/python`

## Uso Básico

### 1. Análise de Projeto

```bash
mcp-server /path/to/your/project
```

### 2. Demo Completa

```bash
mcp-demo
```

### 3. Integração MCP

```bash
mcp-analyze --project /path/to/project --output report.json
```

### 4. Uso Programático

```python
from mcp_server import AIResearchAssistant

assistant = AIResearchAssistant("/path/to/project")
assistant.analyze_project()
report = assistant.generate_report()
print(report)
```

## Desenvolvimento

### Executar testes durante desenvolvimento

```bash
# Watch mode (precisa do pytest-watch)
hatch run pytest-watch

# Ou manualmente
hatch run test
```

### Formatar código antes de commit

```bash
hatch run lint:fmt
```

### Verificar tipos

```bash
hatch run lint:typing
```

### Executar todos os checks

```bash
hatch run lint:all
```

## Build e Distribuição

### Build local

```bash
hatch build
```

Isso cria:
- `dist/mcp_server-1.0.0.tar.gz` (source distribution)
- `dist/mcp_server-1.0.0-py3-none-any.whl` (wheel)

### Instalar localmente a partir do wheel

```bash
pip install dist/mcp_server-1.0.0-py3-none-any.whl
```

## Troubleshooting

### Problema: "Python 3.13 não encontrado"

```bash
# Instale Python 3.13
# macOS com Homebrew
brew install python@3.13

# Ou use pyenv
pyenv install 3.13.0
pyenv local 3.13.0
```

### Problema: "Hatch comando não encontrado"

```bash
# Reinstale o Hatch
pip install --user hatch

# Ou com pipx
pipx install hatch
```

### Problema: "Módulo não encontrado"

```bash
# Reinstale em modo desenvolvimento
pip install -e .

# Ou use hatch shell
hatch shell
```

## Próximos Passos

1. ✅ Execute `mcp-demo` para ver todas as capacidades
2. ✅ Analise seu projeto: `mcp-server /path/to/project`
3. ✅ Leia o README.md para mais detalhes
4. ✅ Explore os exemplos em `examples/`

## Suporte

Se encontrar problemas:

1. Verifique os logs
2. Execute `hatch run test` para validar a instalação
3. Consulte a documentação no README.md

---

**Pronto para começar!** 🚀
