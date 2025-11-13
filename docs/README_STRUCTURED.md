# 📄 README.md Estruturado para Pesquisa

## O que é?

O MCP Server agora suporta **README.md estruturado** como **4ª fonte de detecção** de tecnologias e metadados de pesquisa!

## Como Funciona?

O sistema lê seções específicas do seu README.md e as usa para:

1. 🔍 **Detectar tecnologias** mencionadas
2. 📚 **Buscar papers relevantes** baseado no foco de pesquisa
3. 💡 **Gerar sugestões** contextualizadas
4. 🎯 **Criar queries inteligentes** para busca

## Seções Reconhecidas

### Research Focus
Define as áreas principais de pesquisa.

**Exemplo:**
```markdown
## Research Focus
- Machine Learning for Time Series
- Anomaly Detection
```

### Research Questions
Perguntas de pesquisa.

**Exemplo:**
```markdown
## Research Questions
- How can we detect failures earlier?
- Which features are most important?
```

### Technologies
Tecnologias usadas.

**Exemplo:**
```markdown
## Technologies
- Python 3.13
- TensorFlow
- LSTM
```

### Keywords
Keywords para papers.

**Exemplo:**
```markdown
## Keywords
- anomaly detection
- time series
- LSTM
```

## Template Completo

```markdown
# Your Project Name

## Research Focus
- Your research area

## Research Questions
- Your questions

## Technologies
- Your tech stack

## Keywords
- Your keywords

## Goals
- Your objectives

## Methodology
- Your approach
```

## Como Usar

```bash
# 1. Criar README estruturado
mcp-server $(pwd)

# 2. Sistema detecta automaticamente!
```

## API

```python
from mcp_server.readme_parser import ReadmeParser

parser = ReadmeParser()
metadata = parser.parse(Path("README.md"))
queries = parser.extract_research_queries(metadata)
```

---

Veja mais em: [Documentação Completa]
