#!/usr/bin/env python3.13
"""
Parser de README.md para extração de metadados de pesquisa
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ResearchMetadata:
    """Metadados de pesquisa extraídos do README"""

    research_focus: list[str] = field(default_factory=list)
    research_questions: list[str] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    related_papers: list[str] = field(default_factory=list)
    goals: list[str] = field(default_factory=list)
    methodology: list[str] = field(default_factory=list)
    datasets: list[str] = field(default_factory=list)


class ReadmeParser:
    """
    Parser inteligente de README.md que extrai informações estruturadas.

    Reconhece seções especiais:
    - ## Research Focus
    - ## Research Questions
    - ## Technologies / Tech Stack
    - ## Keywords
    - ## Related Papers
    - ## Goals / Objectives
    - ## Methodology / Approach
    - ## Datasets
    """

    # Mapeamento de seções reconhecidas
    SECTION_MAPPING = {
        "research focus": "research_focus",
        "research area": "research_focus",
        "research domain": "research_focus",
        "focus area": "research_focus",
        "research questions": "research_questions",
        "research problem": "research_questions",
        "key questions": "research_questions",
        "questions": "research_questions",
        "technologies": "technologies",
        "tech stack": "technologies",
        "tools": "technologies",
        "frameworks": "technologies",
        "keywords": "keywords",
        "tags": "keywords",
        "topics": "keywords",
        "related papers": "related_papers",
        "references": "related_papers",
        "papers": "related_papers",
        "literature": "related_papers",
        "goals": "goals",
        "objectives": "goals",
        "aims": "goals",
        "methodology": "methodology",
        "approach": "methodology",
        "methods": "methodology",
        "datasets": "datasets",
        "data sources": "datasets",
        "data": "datasets",
    }

    @classmethod
    def parse(cls, readme_path: Path) -> ResearchMetadata | None:
        """
        Parse README.md e extrai metadados de pesquisa.

        Args:
            readme_path: Caminho para o README.md

        Returns:
            ResearchMetadata com informações extraídas ou None
        """
        if not readme_path.exists():
            return None

        try:
            content = readme_path.read_text(encoding="utf-8")
            return cls._parse_content(content)
        except Exception as e:
            print(f"⚠️  Erro ao ler README.md: {e}")
            return None

    @classmethod
    def _parse_content(cls, content: str) -> ResearchMetadata:
        """Parse do conteúdo do README"""
        metadata = ResearchMetadata()

        # Dividir por seções (headers H2 e H3)
        sections = cls._extract_sections(content)

        # Processar cada seção
        for header, section_content in sections.items():
            cls._process_section(header, section_content, metadata)

        return metadata

    @classmethod
    def _extract_sections(cls, content: str) -> dict[str, str]:
        """Extrai seções do markdown (## e ###)"""
        sections = {}
        current_header = None
        current_content = []

        for line in content.split("\n"):
            # Detectar headers
            header_match = re.match(r"^(#{2,3})\s+(.+)$", line)

            if header_match:
                # Salvar seção anterior
                if current_header:
                    sections[current_header] = "\n".join(current_content).strip()

                # Iniciar nova seção
                current_header = header_match.group(2).strip()
                current_content = []
            elif current_header:
                current_content.append(line)

        # Salvar última seção
        if current_header:
            sections[current_header] = "\n".join(current_content).strip()

        return sections

    @classmethod
    def _process_section(cls, header: str, content: str, metadata: ResearchMetadata):
        """Processa uma seção específica"""
        header_lower = header.lower()

        # Encontrar qual campo corresponde a este header
        field_name = None
        for section_key, field in cls.SECTION_MAPPING.items():
            if section_key in header_lower:
                field_name = field
                break

        if not field_name:
            return

        # Extrair itens da seção
        items = cls._extract_items(content)

        # Atualizar metadata
        current_items = getattr(metadata, field_name)
        current_items.extend(items)

    @classmethod
    def _extract_items(cls, content: str) -> list[str]:
        """Extrai itens de uma seção (bullets, números, ou linhas)"""
        items = []

        for line in content.split("\n"):
            line = line.strip()

            if not line:
                continue

            # Remover marcadores de lista
            line = re.sub(r"^[-*+]\s+", "", line)  # bullets
            line = re.sub(r"^\d+\.\s+", "", line)  # numbered
            line = re.sub(r"^>\s+", "", line)  # quotes

            # Remover markdown links mas manter o texto
            line = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", line)

            # Remover código inline
            line = re.sub(r"`([^`]+)`", r"\1", line)

            # Remover bold/italic
            line = re.sub(r"\*\*([^\*]+)\*\*", r"\1", line)
            line = re.sub(r"\*([^\*]+)\*", r"\1", line)

            line = line.strip()

            if line and not line.startswith("#"):
                items.append(line)

        return items

    @classmethod
    def extract_research_queries(cls, metadata: ResearchMetadata) -> list[str]:
        """
        Gera queries de pesquisa a partir dos metadados.

        Combina research focus, questions, e keywords para criar
        queries efetivas para busca de papers.
        """
        queries = []

        # 1. Research Focus direto
        queries.extend(metadata.research_focus)

        # 2. Research Questions como queries
        for question in metadata.research_questions:
            # Remover pontuação de pergunta
            query = question.rstrip("?").strip()
            queries.append(query)

        # 3. Combinar keywords principais
        if len(metadata.keywords) >= 2:
            # Pegar top 3 keywords e combinar
            top_keywords = metadata.keywords[:3]
            combined = " ".join(top_keywords)
            queries.append(combined)

        # 4. Metodologia + Focus
        if metadata.methodology and metadata.research_focus:
            for method in metadata.methodology[:2]:
                for focus in metadata.research_focus[:2]:
                    queries.append(f"{method} {focus}")

        return queries


def create_research_readme_template(output_path: Path, project_name: str = "Your Project"):
    """
    Cria um template de README.md estruturado para pesquisa.

    Args:
        output_path: Onde salvar o template
        project_name: Nome do projeto
    """
    template = f"""# {project_name}

> Brief description of your research project

## Research Focus

List your main research areas (one per line):

- Machine Learning for Time Series Analysis
- Anomaly Detection in Industrial Systems
- Predictive Maintenance using Deep Learning

## Research Questions

Key questions you're trying to answer:

- How can we improve early detection of equipment failures?
- What features are most predictive of anomalies?
- Can transfer learning improve model performance with limited data?

## Technologies

Technologies and frameworks used:

- Python 3.13
- TensorFlow / PyTorch
- Pandas & NumPy
- Scikit-learn

## Keywords

Research keywords for paper discovery:

- partial discharge
- time series
- anomaly detection
- predictive maintenance
- deep learning
- transformer models

## Goals

Project objectives:

- Develop real-time anomaly detection system
- Achieve >95% accuracy in fault prediction
- Reduce false positives by 50%

## Methodology

Research approach:

- Data preprocessing and feature engineering
- Model comparison (Random Forest, LSTM, Transformer)
- Cross-validation and hyperparameter tuning
- Deployment with monitoring

## Datasets

Data sources being used:

- Internal sensor data (2020-2025)
- Public benchmark datasets
- Simulated fault scenarios

## Related Papers

Papers that influenced this work:

- "Benchmarking ML for Fault Detection" (2025)
- "Transformer Models for Time Series" (2024)

---

**Note:** This README structure is optimized for the MCP Server AI Research Assistant.
The tool will automatically extract research metadata to find relevant papers and suggest improvements.
"""

    output_path.write_text(template, encoding="utf-8")
    print(f"✅ Template criado em: {output_path}")


if __name__ == "__main__":
    # Teste do parser
    from pathlib import Path

    # Criar template
    test_path = Path("RESEARCH_README_TEMPLATE.md")
    create_research_readme_template(test_path)

    # Testar parse
    parser = ReadmeParser()
    metadata = parser.parse(test_path)

    if metadata:
        print("\n📊 Metadados extraídos:")
        print(f"Research Focus: {metadata.research_focus}")
        print(f"Questions: {metadata.research_questions}")
        print(f"Keywords: {metadata.keywords}")
        print(f"Technologies: {metadata.technologies}")

        print("\n🔍 Queries geradas:")
        queries = parser.extract_research_queries(metadata)
        for i, query in enumerate(queries[:5], 1):
            print(f"   {i}. {query}")
