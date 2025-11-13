# 🎯 README.md Estruturado - Guia Completo

## 📋 Resumo

Você agora pode criar um **README.md estruturado** no seu projeto que serve como **4ª fonte de informação** para o MCP Server detectar tecnologias e buscar papers relevantes!

## 🚀 Quick Start

### 1. Criar Template

```bash
cd /path/to/your/project

# Criar template automaticamente
python -c "from mcp_server.readme_parser import create_research_readme_template; from pathlib import Path; create_research_readme_template(Path('README.md'), 'My Project')"
```

### 2. Editar Seções

Edite o `README.md` gerado com suas informações:

```markdown
## Research Focus
- Sua área de pesquisa aqui

## Research Questions
- Suas perguntas aqui

## Technologies
- Suas tecnologias aqui

## Keywords
- Suas keywords aqui
```

### 3. Executar Análise

```bash
mcp-server $(pwd)
```

O sistema irá:
- ✅ Ler o README.md
- ✅ Extrair metadados de pesquisa
- ✅ Detectar tecnologias mencionadas
- ✅ Gerar queries inteligentes
- ✅ Buscar papers relevantes
- ✅ Criar sugestões contextualizadas

## 📊 4 Fontes de Detecção

```
┌─────────────────────────────────────┐
│  1️⃣  pyproject.toml keywords        │
│  2️⃣  Dependencies listadas          │
│  3️⃣  Imports no código              │
│  4️⃣  README.md seções ← NOVO!       │
└─────────────────────────────────────┘
```

## 📝 Seções Reconhecidas

### Obrigatórias (Recomendadas)

#### Research Focus
O que você está pesquisando?

```markdown
## Research Focus

- Machine Learning for Time Series
- Anomaly Detection
- Predictive Maintenance
```

#### Research Questions
Que perguntas você quer responder?

```markdown
## Research Questions

- How can we detect failures earlier?
- Which features are most important?
- Can transfer learning help?
```

#### Keywords
Palavras-chave para busca de papers:

```markdown
## Keywords

- anomaly detection
- time series
- LSTM
- deep learning
```

### Opcionais (Mas Úteis)

#### Technologies
```markdown
## Technologies

- Python 3.13
- TensorFlow
- LSTM Networks
```

#### Goals
```markdown
## Goals

- Achieve 90% accuracy
- Reduce false positives
```

#### Methodology
```markdown
## Methodology

- Data preprocessing
- Model comparison
- Cross-validation
```

#### Datasets
```markdown
## Datasets

- Internal sensor data
- Public benchmarks
```

## 🔍 Como Funciona Internamente

### 1. Parsing

```python
# ReadmeParser extrai seções estruturadas
metadata = ReadmeParser().parse(Path("README.md"))

# Resultado:
ResearchMetadata(
    research_focus=["ML for Time Series"],
    keywords=["anomaly detection", "LSTM"],
    research_questions=["How to detect?"],
    technologies=["Python", "LSTM"],
    ...
)
```

### 2. Detecção de Tecnologias

```python
# Sistema mapeia keywords -> tecnologias
"lstm" → "LSTM Networks"
"transformer" → "Hugging Face Transformers"  
"random forest" → "Random Forest"

# E rastreia a fonte
{
    "LSTM Networks": ["README keywords", "code imports"],
    "Random Forest": ["README technologies", "dependencies"]
}
```

### 3. Geração de Queries

```python
# Combina seções para criar queries
queries = [
    "Machine Learning for Time Series",  # Research Focus
    "anomaly detection LSTM",  # Keywords combinadas
    "LSTM Machine Learning",  # Methodology + Focus
]
```

### 4. Busca de Papers

```python
# Usa queries para buscar papers relevantes
papers = search_papers(queries)
# Retorna papers sobre seus tópicos específicos!
```

## 💡 Exemplo Prático

### Antes (Sem README Estruturado)

```bash
mcp-server $(pwd)

# Output:
🔧 TECNOLOGIAS DETECTADAS:
   • NumPy
   • Pandas

📚 PAPERS:
   • Generic ML papers (não relacionados)
```

### Depois (Com README Estruturado)

```bash
mcp-server $(pwd)

# Output:
📄 Extraindo metadados de pesquisa do README...
   ✓ Research Focus: Anomaly Detection, Time Series
   ✓ Keywords: LSTM, deep learning, transformers
   ✓ 5 perguntas de pesquisa

🔧 TECNOLOGIAS DETECTADAS:
   • LSTM Networks
   • Transformers
   • Random Forest
   • NumPy
   • Pandas

🔍 FONTES:
   • LSTM: README keywords, code imports
   • Transformers: README technologies, dependencies

📚 PAPERS RELEVANTES:
   1. "Deep Learning for Time Series with LSTM"
   2. "Transformer Models for Anomaly Detection"
   3. "Random Forest vs Deep Learning Comparison"

💡 SUGESTÕES:
   1. ❓ 5 perguntas de pesquisa - crie experimentos
   2. 🤖 LSTM detectado - considere attention mechanisms
   3. 📊 Compare Random Forest com deep learning
```

## 🎯 Use Cases

### 1. Projeto de Pesquisa Acadêmica

```markdown
## Research Focus
- Novel approach for X using Y

## Research Questions  
- Can method A outperform B?
- What is the optimal hyperparameter?

## Related Papers
- "Baseline Paper" (2024)
- "State-of-the-art Method" (2025)
```

### 2. Projeto Industrial

```markdown
## Research Focus
- Real-time anomaly detection for production

## Goals
- 99% uptime
- <100ms latency
- Deploy to edge devices

## Datasets
- Factory sensor data
- Historical failure cases
```

### 3. Proof of Concept

```markdown
## Research Focus
- Evaluate feasibility of approach X

## Methodology
- Literature review
- Prototype development
- Performance benchmarking
```

## 🧪 Testing

### Testar Parser

```bash
pytest tests/test_readme_parser.py -v
```

### Testar Integração

```bash
pytest tests/test_metadata_extraction.py::test_detect_mcp_from_keywords -v
```

### Testar Manualmente

```python
from mcp_server.readme_parser import ReadmeParser
from pathlib import Path

parser = ReadmeParser()
metadata = parser.parse(Path("README.md"))

print(f"Focus: {metadata.research_focus}")
print(f"Keywords: {metadata.keywords}")

queries = parser.extract_research_queries(metadata)
print(f"Queries: {queries}")
```

## 📚 API Reference

### ReadmeParser

```python
class ReadmeParser:
    @classmethod
    def parse(cls, readme_path: Path) -> ResearchMetadata | None:
        """Parse README e retorna metadados"""
        
    @classmethod  
    def extract_research_queries(cls, metadata: ResearchMetadata) -> list[str]:
        """Gera queries de pesquisa a partir dos metadados"""
```

### ResearchMetadata

```python
@dataclass
class ResearchMetadata:
    research_focus: list[str]
    research_questions: list[str]
    technologies: list[str]
    keywords: list[str]
    related_papers: list[str]
    goals: list[str]
    methodology: list[str]
    datasets: list[str]
```

### Criar Template

```python
from mcp_server.readme_parser import create_research_readme_template

create_research_readme_template(
    output_path=Path("README.md"),
    project_name="My Research Project"
)
```

## ⚠️ Avisos

### O que o Parser Remove

- Formatação Markdown (`**bold**`, `*italic*`, `` `code` ``)
- Links `[text](url)` → mantém só o texto
- Marcadores de lista (`-`, `*`, `+`, `1.`)
- Headers dentro de conteúdo

### O que Pode Confundir

```markdown
## Research Focus  
Some paragraph text here.  # ❌ Não será detectado
- Item 1  # ✅ Será detectado
```

**Solução:** Use sempre listas (bullets ou números)

## 🎓 Best Practices

### ✅ Faça

- Use listas para itens
- Seja específico e claro
- Inclua keywords técnicas
- Mantenha README atualizado
- Use termos do domínio

### ❌ Evite

- Parágrafos longos sem estrutura
- Termos muito genéricos
- Informações desatualizadas
- Misturar múltiplos tópicos em um item

## 🔄 Workflow Recomendado

1. **Início do Projeto**
   ```bash
   # Criar template
   python -m mcp_server.readme_parser
   ```

2. **Durante Desenvolvimento**
   ```bash
   # Atualizar seções conforme evolui
   # Adicionar novos keywords
   # Refinar research questions
   ```

3. **Revisões Periódicas**
   ```bash
   # Executar análise
   mcp-server $(pwd)
   
   # Revisar papers sugeridos
   # Ajustar README com novos insights
   ```

4. **Antes de Publicar**
   ```bash
   # Garantir README completo
   # Verificar que papers relevantes são encontrados
   # Testar queries geradas
   ```

## 🎉 Próximos Passos

1. ✅ Crie seu README estruturado
2. ✅ Execute `mcp-server $(pwd)`
3. ✅ Veja papers personalizados
4. ✅ Refine baseado nos resultados
5. ✅ Compartilhe com o time!

---

**Documentação:** `docs/README_STRUCTURED.md`  
**Exemplo:** `examples/RESEARCH_README_EXAMPLE.md`  
**Testes:** `tests/test_readme_parser.py`

**Versão:** MCP Server 1.0.0+
