"""
Testes para o ReadmeParser
"""

import pytest
from pathlib import Path
from ai_research_assistant.readme_parser import ReadmeParser, ResearchMetadata, create_research_readme_template


def test_parse_research_focus(tmp_path):
    """Testa parsing de Research Focus"""
    readme_content = """
# Test Project

## Research Focus

- Machine Learning
- Deep Learning
- Time Series Analysis
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert metadata is not None
    assert len(metadata.research_focus) == 3
    assert "Machine Learning" in metadata.research_focus
    assert "Deep Learning" in metadata.research_focus
    assert "Time Series Analysis" in metadata.research_focus


def test_parse_research_questions(tmp_path):
    """Testa parsing de Research Questions"""
    readme_content = """
## Research Questions

- How can we improve accuracy?
- Which model is best?
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert len(metadata.research_questions) == 2
    assert any("accuracy" in q.lower() for q in metadata.research_questions)


def test_parse_technologies(tmp_path):
    """Testa parsing de Technologies"""
    readme_content = """
## Technologies

- Python 3.13
- TensorFlow
- PyTorch
- LSTM
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert len(metadata.technologies) == 4
    assert "Python 3.13" in metadata.technologies
    assert "TensorFlow" in metadata.technologies


def test_parse_keywords(tmp_path):
    """Testa parsing de Keywords"""
    readme_content = """
## Keywords

- machine learning
- deep learning
- anomaly detection
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert len(metadata.keywords) == 3
    assert "machine learning" in metadata.keywords


def test_parse_all_sections(tmp_path):
    """Testa parsing de todas as seções"""
    readme_content = """
# Complete Project

## Research Focus
- AI Research

## Research Questions
- Can we do better?

## Technologies
- Python
- LSTM

## Keywords
- ml
- dl

## Goals
- Achieve 90% accuracy

## Methodology
- Data preprocessing
- Model training

## Datasets
- Internal data
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert len(metadata.research_focus) > 0
    assert len(metadata.research_questions) > 0
    assert len(metadata.technologies) > 0
    assert len(metadata.keywords) > 0
    assert len(metadata.goals) > 0
    assert len(metadata.methodology) > 0
    assert len(metadata.datasets) > 0


def test_extract_research_queries(tmp_path):
    """Testa geração de queries de pesquisa"""
    readme_content = """
## Research Focus
- Anomaly Detection

## Research Questions
- How to detect outliers?

## Keywords
- anomaly
- detection
- ml
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    queries = parser.extract_research_queries(metadata)
    
    assert len(queries) > 0
    # Deve incluir research focus
    assert any("Anomaly Detection" in q for q in queries)
    # Deve incluir keywords combinadas
    assert any("anomaly" in q.lower() for q in queries)


def test_parse_nonexistent_file(tmp_path):
    """Testa comportamento com arquivo inexistente"""
    parser = ReadmeParser()
    metadata = parser.parse(tmp_path / "NONEXISTENT.md")
    
    assert metadata is None


def test_parse_empty_readme(tmp_path):
    """Testa parsing de README vazio"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text("")
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert metadata is not None
    assert len(metadata.research_focus) == 0


def test_parse_with_markdown_formatting(tmp_path):
    """Testa remoção de formatação Markdown"""
    readme_content = """
## Technologies

- **Python** 3.13
- *TensorFlow*
- `PyTorch`
- [NumPy](https://numpy.org)
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    # Deve remover formatação mas manter texto
    assert any("Python" in tech for tech in metadata.technologies)
    assert any("TensorFlow" in tech for tech in metadata.technologies)
    assert any("PyTorch" in tech for tech in metadata.technologies)
    assert any("NumPy" in tech for tech in metadata.technologies)


def test_case_insensitive_headers(tmp_path):
    """Testa que headers são case-insensitive"""
    readme_content = """
## research focus
- ML

## RESEARCH QUESTIONS
- Question?

## Research Area
- AI
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    # Deve detectar todas variações
    assert len(metadata.research_focus) >= 2  # ML e AI


def test_create_template(tmp_path):
    """Testa criação de template"""
    output_path = tmp_path / "TEMPLATE.md"
    
    create_research_readme_template(output_path, "Test Project")
    
    assert output_path.exists()
    content = output_path.read_text()
    
    # Deve conter seções principais
    assert "## Research Focus" in content
    assert "## Research Questions" in content
    assert "## Technologies" in content
    assert "## Keywords" in content


def test_numbered_lists(tmp_path):
    """Testa parsing de listas numeradas"""
    readme_content = """
## Methodology

1. Data preprocessing
2. Model training
3. Evaluation
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert len(metadata.methodology) == 3
    assert "Data preprocessing" in metadata.methodology


def test_mixed_list_styles(tmp_path):
    """Testa diferentes estilos de lista"""
    readme_content = """
## Keywords

- keyword1
* keyword2
+ keyword3
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    assert len(metadata.keywords) == 3


def test_query_generation_priority(tmp_path):
    """Testa prioridade na geração de queries"""
    readme_content = """
## Research Focus
- Primary Focus

## Keywords
- key1
- key2
- key3

## Methodology
- Method A

## Research Questions
- Question A?
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    queries = parser.extract_research_queries(metadata)
    
    # Deve incluir research focus (prioridade alta)
    assert any("Primary Focus" in q for q in queries)
    
    # Deve incluir combinação de keywords
    assert any("key1" in q or "key2" in q for q in queries)


def test_section_aliases(tmp_path):
    """Testa aliases de seções"""
    readme_content = """
## Tech Stack
- Python

## Key Questions
- What?

## Objectives
- Goal 1
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content)
    
    parser = ReadmeParser()
    metadata = parser.parse(readme_path)
    
    # Tech Stack -> Technologies
    assert len(metadata.technologies) > 0
    
    # Key Questions -> Research Questions
    assert len(metadata.research_questions) > 0
    
    # Objectives -> Goals
    assert len(metadata.goals) > 0
