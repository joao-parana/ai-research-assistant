"""
🤖 MCP Server - AI Research Assistant

Integração completa de MCPs (Model Context Protocol) com Python 3.13
para análise inteligente de projetos e pesquisa científica.

Features:
- 📊 Análise de código e detecção de tecnologias
- 📚 Busca de papers no Hugging Face
- 🤖 Recomendações de ML/DL
- 💡 Sugestões inteligentes de melhorias
- 📦 Leitura automática de metadados (pyproject.toml, setup.py, requirements.txt)
- 📄 Leitura e interpretação de README.md estruturado (4ª fonte!)
"""

__version__ = "0.5.0"
__author__ = "João"

from ai_research_assistant.ai_research_assistant import (
    AIResearchAssistant,
    Model,
    Paper,
    ProjectAnalysis,
    ProjectMetadata,
    ProjectMetadataExtractor,
    ResearchArea,
)
from ai_research_assistant.readme_parser import (
    ReadmeParser,
    ResearchMetadata,
    create_research_readme_template,
)

__all__ = [
    "AIResearchAssistant",
    "Paper",
    "Model",
    "ProjectAnalysis",
    "ProjectMetadata",
    "ProjectMetadataExtractor",
    "ResearchArea",
    "ReadmeParser",
    "ResearchMetadata",
    "create_research_readme_template",
]
