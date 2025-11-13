"""
Testes para extração de metadados do projeto
"""

import pytest
from pathlib import Path
from ai_research_assistant import (
    ProjectMetadataExtractor,
    AIResearchAssistant,
    ResearchArea,
    ProjectMetadata
)


def test_extract_from_pyproject(tmp_path):
    """Testa extração de metadados do pyproject.toml"""
    # Criar pyproject.toml de teste
    pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"
description = "A test project"
keywords = ["mcp", "ai", "research"]
dependencies = [
    "numpy>=1.26.0",
    "pandas>=2.1.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.4.0"]
"""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)
    
    # Extrair metadados
    extractor = ProjectMetadataExtractor()
    metadata = extractor.extract_from_pyproject(tmp_path)
    
    assert metadata is not None
    assert metadata.name == "test-project"
    assert metadata.version == "1.0.0"
    assert metadata.description == "A test project"
    assert "mcp" in metadata.keywords
    assert "ai" in metadata.keywords
    assert len(metadata.dependencies) == 2


def test_extract_from_requirements(tmp_path):
    """Testa extração de requirements.txt"""
    req_content = """
numpy>=1.26.0
pandas>=2.1.0
# Comentário
matplotlib==3.8.0
    """
    req_path = tmp_path / "requirements.txt"
    req_path.write_text(req_content)
    
    extractor = ProjectMetadataExtractor()
    deps = extractor.extract_from_requirements(tmp_path)
    
    assert "numpy" in deps
    assert "pandas" in deps
    assert "matplotlib" in deps
    assert len(deps) == 3


def test_detect_mcp_from_keywords(tmp_path):
    """Testa detecção de MCP a partir de keywords"""
    # Criar pyproject.toml com keyword MCP
    pyproject_content = """
[project]
name = "mcp-test"
keywords = ["mcp", "Model Context Protocol"]
dependencies = []
"""
    (tmp_path / "pyproject.toml").write_text(pyproject_content)
    
    # Criar arquivo Python vazio
    (tmp_path / "test.py").write_text("")
    
    assistant = AIResearchAssistant(tmp_path)
    analysis = assistant.analyze_project()
    
    assert "Model Context Protocol" in analysis.technologies


def test_detect_technologies_from_dependencies(tmp_path):
    """Testa detecção a partir de dependências"""
    pyproject_content = """
[project]
name = "test-deps"
keywords = []
dependencies = [
    "numpy>=1.26.0",
    "pydantic>=2.5.0",
]
"""
    (tmp_path / "pyproject.toml").write_text(pyproject_content)
    (tmp_path / "test.py").write_text("")
    
    assistant = AIResearchAssistant(tmp_path)
    analysis = assistant.analyze_project()
    
    assert "NumPy" in analysis.technologies
    assert "Pydantic" in analysis.technologies


def test_detect_technologies_from_imports(tmp_path):
    """Testa detecção a partir de imports no código"""
    # Criar arquivo Python com imports
    (tmp_path / "test.py").write_text("import numpy as np\nimport pandas as pd\n")
    
    assistant = AIResearchAssistant(tmp_path)
    analysis = assistant.analyze_project()
    
    assert "NumPy" in analysis.technologies
    assert "Pandas" in analysis.technologies


def test_search_papers_with_mcp_keyword(tmp_path):
    """Testa que MCP keyword resulta em papers sobre MCP"""
    pyproject_content = """
[project]
name = "mcp-project"
keywords = ["mcp"]
dependencies = []
"""
    (tmp_path / "pyproject.toml").write_text(pyproject_content)
    (tmp_path / "test.py").write_text("")
    
    assistant = AIResearchAssistant(tmp_path)
    assistant.analyze_project()
    
    # Buscar papers (deve usar keywords automaticamente)
    papers = assistant.search_relevant_research()
    
    assert len(papers) > 0
    # Verificar que algum paper é sobre MCP
    mcp_papers = [p for p in papers if "MCP" in str(p.keywords) or "Protocol" in str(p.keywords)]
    assert len(mcp_papers) > 0


def test_metadata_in_analysis(tmp_path):
    """Testa que metadados são incluídos na análise"""
    pyproject_content = """
[project]
name = "meta-test"
version = "2.0.0"
description = "Test metadata"
keywords = ["test"]
dependencies = ["numpy>=1.0"]
"""
    (tmp_path / "pyproject.toml").write_text(pyproject_content)
    (tmp_path / "test.py").write_text("")
    
    assistant = AIResearchAssistant(tmp_path)
    analysis = assistant.analyze_project()
    
    assert analysis.metadata is not None
    assert analysis.metadata.name == "meta-test"
    assert analysis.metadata.version == "2.0.0"
    assert analysis.metadata.description == "Test metadata"
    assert "test" in analysis.metadata.keywords


def test_suggestions_for_mcp_project(tmp_path):
    """Testa sugestões específicas para projetos MCP"""
    pyproject_content = """
[project]
name = "mcp-app"
keywords = ["mcp"]
dependencies = []
"""
    (tmp_path / "pyproject.toml").write_text(pyproject_content)
    (tmp_path / "test.py").write_text("")
    
    assistant = AIResearchAssistant(tmp_path)
    assistant.analyze_project()
    suggestions = assistant.suggest_improvements()
    
    # Deve ter sugestões específicas sobre MCP
    mcp_suggestions = [s for s in suggestions if "MCP" in s or "Model Context Protocol" in s]
    assert len(mcp_suggestions) > 0


def test_fallback_to_requirements(tmp_path):
    """Testa fallback para requirements.txt quando não há pyproject.toml"""
    # Sem pyproject.toml, apenas requirements.txt
    (tmp_path / "requirements.txt").write_text("numpy>=1.0\npandas>=2.0\n")
    (tmp_path / "test.py").write_text("")
    
    assistant = AIResearchAssistant(tmp_path)
    analysis = assistant.analyze_project()
    
    assert analysis.metadata is not None
    assert len(analysis.metadata.dependencies) == 2


def test_no_metadata_files(tmp_path):
    """Testa comportamento quando não há arquivos de metadados"""
    (tmp_path / "test.py").write_text("import numpy\n")
    
    assistant = AIResearchAssistant(tmp_path)
    analysis = assistant.analyze_project()
    
    # Deve criar metadata básico
    assert analysis.metadata is not None
    assert analysis.metadata.name == tmp_path.name
    
    # Mas ainda detecta tecnologias do código
    assert "NumPy" in analysis.technologies
