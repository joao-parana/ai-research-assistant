"""
Testes para o AI Research Assistant
"""

import pytest
from pathlib import Path
from mcp_server import AIResearchAssistant, ResearchArea, Paper


def test_research_area_enum():
    """Testa o enum ResearchArea"""
    assert ResearchArea.MACHINE_LEARNING == "machine_learning"
    assert ResearchArea.PARTIAL_DISCHARGE == "partial_discharge"


def test_paper_dataclass():
    """Testa a criação de Paper"""
    paper = Paper(
        title="Test Paper",
        authors=["Author 1", "Author 2"],
        abstract="Test abstract",
        keywords=["ML", "DL"],
        url="https://test.com",
        upvotes=5
    )
    
    assert paper.title == "Test Paper"
    assert len(paper.authors) == 2
    assert paper.upvotes == 5


def test_assistant_initialization(tmp_path):
    """Testa inicialização do assistente"""
    assistant = AIResearchAssistant(tmp_path)
    assert assistant.project_path == tmp_path
    assert assistant.analysis is None


def test_detect_technologies(tmp_path):
    """Testa detecção de tecnologias"""
    # Criar arquivo Python de teste
    test_file = tmp_path / "test.py"
    test_file.write_text("import numpy as np\nimport pandas as pd\n")
    
    assistant = AIResearchAssistant(tmp_path)
    technologies = assistant._detect_technologies()
    
    assert "NumPy" in technologies
    assert "Pandas" in technologies


def test_analyze_project(tmp_path):
    """Testa análise de projeto"""
    # Criar alguns arquivos Python
    (tmp_path / "file1.py").write_text("import numpy\n")
    (tmp_path / "file2.py").write_text("import pandas\n")
    
    assistant = AIResearchAssistant(tmp_path)
    analysis = assistant.analyze_project()
    
    assert analysis.project_name == tmp_path.name
    assert analysis.files_analyzed == 2
    assert len(analysis.technologies) > 0


def test_search_relevant_research(tmp_path):
    """Testa busca de papers"""
    assistant = AIResearchAssistant(tmp_path)
    assistant.analyze_project()
    
    papers = assistant.search_relevant_research(ResearchArea.PARTIAL_DISCHARGE)
    
    assert isinstance(papers, list)
    assert len(papers) > 0
    assert all(isinstance(p, Paper) for p in papers)


def test_suggest_improvements_without_analysis(tmp_path):
    """Testa que suggest_improvements requer análise prévia"""
    assistant = AIResearchAssistant(tmp_path)
    
    with pytest.raises(ValueError, match="Execute analyze_project"):
        assistant.suggest_improvements()


def test_suggest_improvements_with_analysis(tmp_path):
    """Testa geração de sugestões"""
    # Criar arquivo com NumPy
    (tmp_path / "test.py").write_text("import numpy as np\n")
    
    assistant = AIResearchAssistant(tmp_path)
    assistant.analyze_project()
    suggestions = assistant.suggest_improvements()
    
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0


def test_generate_report(tmp_path):
    """Testa geração de relatório"""
    (tmp_path / "test.py").write_text("import numpy\n")
    
    assistant = AIResearchAssistant(tmp_path)
    assistant.analyze_project()
    report = assistant.generate_report()
    
    assert isinstance(report, str)
    assert "AI RESEARCH ASSISTANT" in report
    assert tmp_path.name in report


def test_generate_report_with_output_file(tmp_path):
    """Testa salvamento de relatório em arquivo"""
    (tmp_path / "test.py").write_text("import pandas\n")
    output_file = tmp_path / "report.txt"
    
    assistant = AIResearchAssistant(tmp_path)
    assistant.analyze_project()
    report = assistant.generate_report(output_file)
    
    assert output_file.exists()
    content = output_file.read_text()
    assert "AI RESEARCH ASSISTANT" in content
