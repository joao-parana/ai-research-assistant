# 🤖 MCP Server - AI Research Assistant

> **Integração completa de MCPs com Python 3.13**
>
> Sistema inteligente que analisa projetos, busca research papers, e sugere melhorias baseadas em ML/DL

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Built with Hatch](https://img.shields.io/badge/built%20with-hatch-4051b5)](https://hatch.pypa.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

### 🎯 O que o sistema faz:

- **📊 Análise de Projeto**: Escaneia código, detecta tecnologias, conta linhas
- **📚 Research Papers**: Busca papers relevantes no Hugging Face
- **🤖 Recomendações ML/DL**: Sugere modelos baseados em research recente
- **💡 Sugestões Inteligentes**: Propõe melhorias específicas para seu código
- **📈 Comparação de Modelos**: Benchmark de diferentes abordagens
- **📄 Relatórios**: Gera relatórios detalhados em texto e JSON

---

## 🚀 Quick Start

### Instalação

```bash
pip install ai-research-assistant
```

OU se desejar contribuir via Fork

```bash
git clone git@github.com:your_github_account/ai-research-assistant.git
cd $HOME/dev/NIE/ai-research-assistant

# Usando Hatch (recomendado)
hatch env create

# Ou usando pip
pip install -e .
```

### Building Pinning files

```bash
pip-compile -o requirements.txt pyproject.toml
pip-compile --extra dev -o dev-requirements.txt pyproject.toml
```

### Uso Básico

#### 1️⃣ Análise Básica

```bash
# Usando script instalado
ai-research-assistant /path/to/your/research/project

# Ou diretamente
python -m ai_research_assistant.ai_research_assistant /path/to/your/research/project
```

#### 2️⃣ Demo Interativa

```bash
mcp-demo
```

#### 3️⃣ Integração MCP

```bash
# Analisar projeto específico
cd ..
mcp-analyze --project ./gamma-pd-analytics

# Exportar relatório JSON
mcp-analyze --project ./meu-projeto --output relatorio.json
```

---

## 📦 Estrutura do Projeto

```
ai-research-assistant/
├── pyproject.toml              # Configuração Hatch
├── README.md                   # Este arquivo
├── LICENSE                     # Licença MIT
├── src/
│   └── ai_research_assistant/
│       ├── __init__.py         # Package init
│       ├── ai_research_assistant.py  # 🧠 Assistente principal
│       ├── demo_usage.py       # 🎯 Demonstração
│       ├── integrate_mcps.py   # 🔌 Integração MCP
│       └── cli.py              # CLI entry point
└── tests/
    └── __init__.py
```

---

## 🎓 Python 3.13 Features Usadas

### ✨ Novidades do Python 3.13:

```python
# 1. Type Aliases com 'type'
type ProjectPath = str | Path
type PaperQuery = str

# 2. StrEnum para enums de string
class ResearchArea(StrEnum):
    MACHINE_LEARNING = "machine_learning"
    DEEP_LEARNING = "deep_learning"

# 3. Dataclasses com slots e frozen
@dataclass(slots=True, frozen=True)
class Paper:
    title: str
    authors: list[str]

# 4. Protocols para structural subtyping
class MCPClient(Protocol):
    def search_papers(self, query: str) -> list[Paper]: ...
```

---

## 🔌 MCPs Integrados

### Disponíveis:

| MCP                   | Status | Uso                       |
| --------------------- | ------ | ------------------------- |
| 🤗 **Hugging Face**   | ✅     | Busca papers e modelos    |
| 🌐 **Web Search**     | ✅     | Informações atualizadas   |
| 📁 **Filesystem**     | ✅     | Análise de código         |
| 🗄️ **PostgreSQL**     | ⚙️     | Armazenamento de análises |
| 🎨 **Flux Image Gen** | ⚙️     | Visualizações             |

---

## 📊 Exemplo de Output

```
╔══════════════════════════════════════════════════════════════╗
║          🤖 AI RESEARCH ASSISTANT - REPORT                  ║
╚══════════════════════════════════════════════════════════════╝

📦 PROJETO: gamma-pd-analytics
📁 Arquivos analisados: 15

🔧 TECNOLOGIAS DETECTADAS:
   • NumPy
   • Pandas
   • Matplotlib
   • SciPy
   • Pydantic

📚 PAPERS RELEVANTES ENCONTRADOS:

   1. Benchmarking ML and DL for Fault Detection
      Autores: Bhuvan Saravanan, Pasanth Kumar M D
      Keywords: SVM, KNN, Random Forest, LSTM, 1D-CNN
      Accuracy: 86.82%

💡 SUGESTÕES DE MELHORIA:

   1. 🤖 Random Forest alcançou 86.82% accuracy
   2. 🧠 Testar 1D-CNN (86.30%) para séries temporais
   3. ⚡ Transformers podem melhorar classificação
```

---

## 🛠️ Desenvolvimento com Hatch

### Comandos Úteis

```bash
# Criar ambiente
hatch env create

# Executar testes
hatch run test

# Executar testes com cobertura
hatch run test-cov

# Gerar relatório HTML de cobertura
hatch run cov-report

# Verificar tipos (mypy)
hatch run lint:typing

# Formatar código
hatch run lint:fmt

# Verificar estilo
hatch run lint:style

# Executar todos os lints
hatch run lint:all
```

### Build e Publicação

```bash
# Build do pacote
hatch build

# Publicar no PyPI (quando pronto)
hatch publish
```

---

## 🎯 Use Cases

### 1. Análise de Partial Discharge

```python
from ai_research_assistant import AIResearchAssistant, ResearchArea

# Analisar projeto
assistant = AIResearchAssistant("/path/to/gamma-pd-analytics")
assistant.analyze_project()

# Buscar research relevante
papers = assistant.search_relevant_research(ResearchArea.PARTIAL_DISCHARGE)

# Gerar recomendações
suggestions = assistant.suggest_improvements()

# Relatório completo
report = assistant.generate_report()
```

### 2. Integração Programática

```python
from ai_research_assistant.integrate_mcps import MCPIntegrator, MCPConfig
from pathlib import Path

# Configurar
config = MCPConfig(
    huggingface_enabled=True,
    brave_enabled=True,
    filesystem_enabled=True
)

# Criar integrador
integrator = MCPIntegrator(config)

# Analisar projeto
results = integrator.analyze_partial_discharge_project(
    Path("/path/to/project")
)

# Exportar relatório
integrator.export_report(Path("report.json"))
```

---

## 🔬 Research Papers Incluídos

### Top Papers para Partial Discharge:

1. **Benchmarking ML/DL for Fault Detection** (86.82%)
   - Random Forest, XGBoost, 1D-CNN
   - [https://hf.co/papers/2505.06295](https://hf.co/papers/2505.06295)

2. **AI Transformers for Power Quality** (99.81%)
   - Attention Transformers
   - [https://hf.co/papers/2402.14949](https://hf.co/papers/2402.14949)

---

## 🧪 Testes

```bash
# Executar todos os testes
hatch run test

# Com cobertura
hatch run test-cov

# Gerar HTML
hatch run cov-report
```

---

## 🎨 Roadmap

### Próximas Features:

- [ ] 🎨 Geração de visualizações com Flux
- [ ] 🗄️ Integração com PostgreSQL para histórico
- [ ] 🌐 Web UI com Streamlit
- [ ] 🤖 Auto-aplicação de sugestões
- [ ] 📊 Dashboard interativo com métricas
- [ ] 🔄 CI/CD para análise contínua
- [ ] 🧪 Testes A/B de modelos sugeridos

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Algumas ideias:

1. **Novos MCPs**: Adicione integração com outros serviços
2. **Modelos**: Teste novos algoritmos de ML/DL
3. **Visualizações**: Crie dashboards interativos
4. **Papers**: Expanda a base de research

### Workflow

```bash
# Fork e clone o repositório
git clone https://github.com/your-username/ai-research-assistant.git

# Crie um branch
git checkout -b feature/nova-feature

# Desenvolva e teste
hatch run test

# Commit e push
git commit -m "Add: nova feature"
git push origin feature/nova-feature

# Abra um Pull Request
```

---

## 📝 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- **Hugging Face** - Papers e modelos
- **Python 3.13** - Features modernas
- **Hatch** - Build system excelente
- **MCP** - Arquitetura de integração

---

## 📞 Suporte

Encontrou um bug? Tem uma sugestão?

- 🐛 Issues: [GitHub Issues]
- 💬 Discussões: [GitHub Discussions]

---

**Feito com ❤️ usando Python 3.13 e Hatch**
