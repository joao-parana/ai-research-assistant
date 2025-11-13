#!/usr/bin/env python3.13
"""
🚀 AI Research Assistant
Integra MCP tools para análise inteligente de projetos com Python 3.13
"""

from dataclasses import dataclass, field
from typing import Protocol, TypeAlias
from pathlib import Path
import json
import sys
from enum import StrEnum
import tomli  # Para ler pyproject.toml
import re

# Importar README parser
from mcp_server.readme_parser import ReadmeParser, ResearchMetadata


# ============================================================================
# TYPE DEFINITIONS (Python 3.13 features)
# ============================================================================

type ProjectPath = str | Path
type PaperQuery = str
type ModelQuery = str


class ResearchArea(StrEnum):
    """Áreas de pesquisa suportadas"""
    MACHINE_LEARNING = "machine_learning"
    DEEP_LEARNING = "deep_learning"
    SIGNAL_PROCESSING = "signal_processing"
    ELECTRICAL_ENGINEERING = "electrical_engineering"
    PARTIAL_DISCHARGE = "partial_discharge"
    MODEL_CONTEXT_PROTOCOL = "model_context_protocol"


@dataclass(slots=True, frozen=True)
class Paper:
    """Representa um paper científico"""
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]
    url: str
    published_date: str | None = None
    upvotes: int = 0


@dataclass(slots=True, frozen=True)
class Model:
    """Representa um modelo do Hugging Face"""
    model_id: str
    downloads: int
    likes: int
    tags: list[str]
    url: str


@dataclass(slots=True)
class ProjectMetadata:
    """Metadados extraídos do projeto"""
    name: str
    keywords: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=list)
    description: str = ""
    version: str = ""


@dataclass(slots=True)
class ProjectAnalysis:
    """Resultado da análise do projeto"""
    project_name: str
    files_analyzed: int
    technologies: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    relevant_papers: list[Paper] = field(default_factory=list)
    relevant_models: list[Model] = field(default_factory=list)
    metadata: ProjectMetadata | None = None
    research_metadata: ResearchMetadata | None = None  # ← NOVO!
    imports: list[str] = field(default_factory=list)
    detection_sources: dict[str, list[str]] = field(default_factory=dict)  # ← NOVO!


# ============================================================================
# PROTOCOLS (Python 3.13 Structural Subtyping)
# ============================================================================

class MCPClient(Protocol):
    """Protocol para clientes MCP"""
    def search_papers(self, query: str, limit: int = 5) -> list[Paper]: ...
    def search_models(self, query: str, limit: int = 5) -> list[Model]: ...
    def analyze_code(self, path: Path) -> dict[str, any]: ...


# ============================================================================
# PROJECT METADATA EXTRACTION
# ============================================================================

class ProjectMetadataExtractor:
    """Extrai metadados de diferentes formatos de projeto"""
    
    @staticmethod
    def extract_from_pyproject(project_path: Path) -> ProjectMetadata | None:
        """Extrai metadados de pyproject.toml"""
        pyproject_path = project_path / "pyproject.toml"
        
        if not pyproject_path.exists():
            return None
        
        try:
            with open(pyproject_path, "rb") as f:
                data = tomli.load(f)
            
            project_data = data.get("project", {})
            
            metadata = ProjectMetadata(
                name=project_data.get("name", project_path.name),
                keywords=project_data.get("keywords", []),
                dependencies=project_data.get("dependencies", []),
                dev_dependencies=project_data.get("optional-dependencies", {}).get("dev", []),
                description=project_data.get("description", ""),
                version=project_data.get("version", "")
            )
            
            return metadata
        except Exception as e:
            print(f"⚠️  Erro ao ler pyproject.toml: {e}")
            return None
    
    @staticmethod
    def extract_from_requirements(project_path: Path) -> list[str]:
        """Extrai dependências de requirements.txt"""
        req_path = project_path / "requirements.txt"
        
        if not req_path.exists():
            return []
        
        try:
            content = req_path.read_text()
            deps = [
                line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                for line in content.split("\n")
                if line.strip() and not line.strip().startswith("#")
            ]
            return deps
        except Exception as e:
            print(f"⚠️  Erro ao ler requirements.txt: {e}")
            return []
    
    @staticmethod
    def extract_from_setup_py(project_path: Path) -> ProjectMetadata | None:
        """Extrai metadados de setup.py (básico)"""
        setup_path = project_path / "setup.py"
        
        if not setup_path.exists():
            return None
        
        try:
            content = setup_path.read_text()
            
            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            name = name_match.group(1) if name_match else project_path.name
            
            keywords_match = re.search(r'keywords\s*=\s*\[([^\]]+)\]', content)
            keywords = []
            if keywords_match:
                keywords = [k.strip(' "\'') for k in keywords_match.group(1).split(',')]
            
            desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
            description = desc_match.group(1) if desc_match else ""
            
            return ProjectMetadata(
                name=name,
                keywords=keywords,
                description=description
            )
        except Exception as e:
            print(f"⚠️  Erro ao ler setup.py: {e}")
            return None


# ============================================================================
# CORE RESEARCH ASSISTANT
# ============================================================================

class AIResearchAssistant:
    """
    Assistente de Pesquisa com IA que integra múltiplos MCPs.
    
    Features:
    - 🔍 Busca papers relevantes no Hugging Face
    - 🤖 Encontra modelos pré-treinados
    - 📊 Analisa código e detecta padrões
    - 💡 Sugere melhorias baseadas em research
    - 📦 Lê metadados do projeto (pyproject.toml, setup.py, requirements.txt)
    - 📄 Lê e interpreta README.md estruturado (4ª FONTE!)
    """
    
    def __init__(self, project_path: ProjectPath):
        self.project_path = Path(project_path)
        self.analysis: ProjectAnalysis | None = None
        self.metadata_extractor = ProjectMetadataExtractor()
        self.readme_parser = ReadmeParser()
    
    def analyze_project(self) -> ProjectAnalysis:
        """Analisa o projeto completo"""
        print(f"🔍 Analisando projeto: {self.project_path}")
        
        # Extrair metadados do projeto
        metadata = self._extract_project_metadata()
        
        # Extrair metadados de pesquisa do README (4ª FONTE!)
        research_metadata = self._extract_research_metadata()
        
        # Detectar tecnologias (agora usa 4 fontes!)
        technologies, detection_sources = self._detect_technologies(metadata, research_metadata)
        
        # Extrair imports reais
        imports = self._extract_imports()
        
        # Contar arquivos
        files = list(self.project_path.rglob("*.py"))
        
        # Criar análise inicial
        analysis = ProjectAnalysis(
            project_name=metadata.name if metadata else self.project_path.name,
            files_analyzed=len(files),
            technologies=technologies,
            metadata=metadata,
            research_metadata=research_metadata,
            imports=imports,
            detection_sources=detection_sources
        )
        
        self.analysis = analysis
        return analysis
    
    def _extract_project_metadata(self) -> ProjectMetadata | None:
        """Extrai metadados do projeto de múltiplas fontes"""
        print("   📦 Extraindo metadados do projeto...")
        
        metadata = self.metadata_extractor.extract_from_pyproject(self.project_path)
        
        if metadata:
            print(f"      ✓ pyproject.toml encontrado")
            if metadata.keywords:
                print(f"      ✓ Keywords: {', '.join(metadata.keywords)}")
            if metadata.dependencies:
                print(f"      ✓ {len(metadata.dependencies)} dependências")
            return metadata
        
        metadata = self.metadata_extractor.extract_from_setup_py(self.project_path)
        if metadata:
            print(f"      ✓ setup.py encontrado")
            return metadata
        
        deps = self.metadata_extractor.extract_from_requirements(self.project_path)
        if deps:
            print(f"      ✓ requirements.txt encontrado ({len(deps)} deps)")
            return ProjectMetadata(
                name=self.project_path.name,
                dependencies=deps
            )
        
        print(f"      ⚠️  Nenhum arquivo de metadados encontrado")
        return ProjectMetadata(name=self.project_path.name)
    
    def _extract_research_metadata(self) -> ResearchMetadata | None:
        """Extrai metadados de pesquisa do README.md (4ª FONTE!)"""
        print("   📄 Extraindo metadados de pesquisa do README...")
        
        readme_path = self.project_path / "README.md"
        research_metadata = self.readme_parser.parse(readme_path)
        
        if research_metadata:
            print(f"      ✓ README.md encontrado e parseado")
            
            if research_metadata.research_focus:
                print(f"      ✓ Research Focus: {', '.join(research_metadata.research_focus[:2])}")
            
            if research_metadata.keywords:
                print(f"      ✓ Keywords: {', '.join(research_metadata.keywords[:5])}")
            
            if research_metadata.research_questions:
                print(f"      ✓ {len(research_metadata.research_questions)} perguntas de pesquisa")
            
            return research_metadata
        else:
            print(f"      ⚠️  README.md não encontrado ou sem seções de pesquisa")
            return None
    
    def _detect_technologies(
        self, 
        metadata: ProjectMetadata | None,
        research_metadata: ResearchMetadata | None
    ) -> tuple[list[str], dict[str, list[str]]]:
        """
        Detecta tecnologias usadas no projeto.
        
        QUATRO FONTES:
        1. Keywords do pyproject.toml
        2. Dependencies listadas
        3. Imports no código
        4. README.md seções (NOVO!)
        
        Returns:
            tuple: (tecnologias detectadas, fontes de detecção)
        """
        tech_mapping = {
            'numpy': 'NumPy',
            'pandas': 'Pandas',
            'matplotlib': 'Matplotlib',
            'scipy': 'SciPy',
            'sklearn': 'Scikit-learn',
            'scikit-learn': 'Scikit-learn',
            'tensorflow': 'TensorFlow',
            'torch': 'PyTorch',
            'pytorch': 'PyTorch',
            'pydantic': 'Pydantic',
            'fastapi': 'FastAPI',
            'flask': 'Flask',
            'django': 'Django',
            'streamlit': 'Streamlit',
            'mcp': 'Model Context Protocol',
            'hatch': 'Hatch',
            'pytest': 'pytest',
            'transformers': 'Hugging Face Transformers',
            'lstm': 'LSTM Networks',
            'cnn': 'Convolutional Neural Networks',
            'random forest': 'Random Forest',
            'xgboost': 'XGBoost',
        }
        
        detected = {}  # tech_name -> [sources]
        
        # FONTE 1: Keywords do pyproject.toml
        if metadata and metadata.keywords:
            print(f"   🔍 Fonte 1: Analisando keywords do projeto...")
            for keyword in metadata.keywords:
                keyword_lower = keyword.lower()
                for tech_key, tech_name in tech_mapping.items():
                    if tech_key in keyword_lower:
                        if tech_name not in detected:
                            detected[tech_name] = []
                        if "pyproject.toml keywords" not in detected[tech_name]:
                            detected[tech_name].append("pyproject.toml keywords")
                            print(f"      ✓ '{tech_name}' via keyword '{keyword}'")
        
        # FONTE 2: Dependencies
        if metadata and metadata.dependencies:
            print(f"   🔍 Fonte 2: Analisando dependências...")
            for dep in metadata.dependencies:
                dep_name = dep.split(">=")[0].split("==")[0].split("[")[0].lower().strip()
                if dep_name in tech_mapping:
                    tech_name = tech_mapping[dep_name]
                    if tech_name not in detected:
                        detected[tech_name] = []
                    if "dependencies" not in detected[tech_name]:
                        detected[tech_name].append("dependencies")
                        print(f"      ✓ '{tech_name}' via dependência")
        
        # FONTE 3: Imports no código
        print(f"   🔍 Fonte 3: Analisando imports no código...")
        try:
            for py_file in self.project_path.rglob("*.py"):
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                for tech_key, tech_name in tech_mapping.items():
                    if tech_key in content.lower():
                        if tech_name not in detected:
                            detected[tech_name] = []
                        if "code imports" not in detected[tech_name]:
                            detected[tech_name].append("code imports")
        except Exception as e:
            print(f"      ⚠️  Erro: {e}")
        
        # FONTE 4: README.md (NOVO!)
        if research_metadata:
            print(f"   🔍 Fonte 4: Analisando README.md...")
            
            # 4a. Technologies explícitas
            for tech in research_metadata.technologies:
                tech_lower = tech.lower()
                for tech_key, tech_name in tech_mapping.items():
                    if tech_key in tech_lower:
                        if tech_name not in detected:
                            detected[tech_name] = []
                        if "README technologies" not in detected[tech_name]:
                            detected[tech_name].append("README technologies")
                            print(f"      ✓ '{tech_name}' via README technologies")
            
            # 4b. Keywords de pesquisa
            for keyword in research_metadata.keywords:
                keyword_lower = keyword.lower()
                for tech_key, tech_name in tech_mapping.items():
                    if tech_key in keyword_lower:
                        if tech_name not in detected:
                            detected[tech_name] = []
                        if "README keywords" not in detected[tech_name]:
                            detected[tech_name].append("README keywords")
                            print(f"      ✓ '{tech_name}' via README keyword '{keyword}'")
            
            # 4c. Research Focus e Methodology
            all_research_text = ' '.join(
                research_metadata.research_focus +
                research_metadata.methodology +
                research_metadata.research_questions
            ).lower()
            
            for tech_key, tech_name in tech_mapping.items():
                if tech_key in all_research_text:
                    if tech_name not in detected:
                        detected[tech_name] = []
                    if "README research focus" not in detected[tech_name]:
                        detected[tech_name].append("README research focus")
                        print(f"      ✓ '{tech_name}' via README research sections")
        
        # Ordenar por nome e retornar
        sorted_techs = sorted(detected.keys())
        detection_sources = {tech: detected[tech] for tech in sorted_techs}
        
        return sorted_techs, detection_sources
    
    def _extract_imports(self) -> list[str]:
        """Extrai todos os imports únicos do projeto"""
        imports = set()
        
        try:
            for py_file in self.project_path.rglob("*.py"):
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                import_lines = [
                    line.strip() 
                    for line in content.split('\n') 
                    if line.strip().startswith(('import ', 'from '))
                ]
                imports.update(import_lines)
        except Exception as e:
            print(f"⚠️  Erro ao extrair imports: {e}")
        
        return sorted(list(imports))
    
    def search_relevant_research(
        self, 
        area: ResearchArea | str | None = None,
        max_papers: int = 5
    ) -> list[Paper]:
        """
        Busca papers relevantes.
        
        Prioridade:
        1. Se area especificada, usar ela
        2. Senão, usar research metadata do README
        3. Senão, usar keywords do pyproject.toml
        4. Senão, área padrão
        """
        # Usar research metadata do README (NOVO!)
        if area is None and self.analysis and self.analysis.research_metadata:
            research_meta = self.analysis.research_metadata
            
            # Gerar queries a partir do README
            queries = self.readme_parser.extract_research_queries(research_meta)
            
            if queries:
                print(f"📚 Buscando papers baseado em README:")
                for i, q in enumerate(queries[:3], 1):
                    print(f"   {i}. {q}")
                
                # Usar primeira query
                area = queries[0]
        
        # Fallback para keywords do projeto
        elif area is None and self.analysis and self.analysis.metadata:
            keywords = self.analysis.metadata.keywords
            if keywords:
                print(f"📚 Buscando papers baseado em keywords: {', '.join(keywords)}")
                area = keywords[0]
            else:
                area = ResearchArea.MACHINE_LEARNING
        elif area is None:
            area = ResearchArea.MACHINE_LEARNING
        
        print(f"📚 Query final: {area}")
        
        # Query mapping (expandido)
        query_map = {
            ResearchArea.PARTIAL_DISCHARGE: "partial discharge detection machine learning",
            ResearchArea.MACHINE_LEARNING: "machine learning algorithms",
            ResearchArea.DEEP_LEARNING: "deep learning neural networks",
            ResearchArea.SIGNAL_PROCESSING: "signal processing analysis",
            ResearchArea.MODEL_CONTEXT_PROTOCOL: "model context protocol llm agents",
            "mcp": "model context protocol llm integration",
            "ai": "artificial intelligence machine learning",
            "anomaly detection": "anomaly detection machine learning",
            "time series": "time series forecasting deep learning",
            "predictive maintenance": "predictive maintenance ai",
        }
        
        query = query_map.get(area, str(area))
        
        # Simulação de papers (em produção, chamaria MCP)
        if "mcp" in str(area).lower() or "context" in str(area).lower():
            papers = [
                Paper(
                    title="Model Context Protocol: Standardizing LLM-Tool Integration",
                    authors=["Anthropic Research Team"],
                    abstract="A protocol for standardized integration between LLMs and external tools",
                    keywords=["MCP", "LLM", "Tool Integration"],
                    url="https://modelcontextprotocol.io",
                    upvotes=100
                )
            ]
        else:
            papers = [
                Paper(
                    title="Benchmarking ML and DL for Fault Detection",
                    authors=["Bhuvan Saravanan"],
                    abstract="Comparative analysis of ML and DL",
                    keywords=["Random Forest", "LSTM", "1D-CNN"],
                    url="https://hf.co/papers/2505.06295",
                    upvotes=1
                )
            ]
        
        return papers[:max_papers]
    
    def suggest_improvements(self) -> list[str]:
        """Sugere melhorias baseadas na análise"""
        if not self.analysis:
            raise ValueError("Execute analyze_project() primeiro")
        
        suggestions = []
        
        # Sugestões baseadas em tecnologias
        if 'NumPy' in self.analysis.technologies:
            suggestions.append(
                "✨ Considere usar numpy.vectorize para otimizar loops"
            )
        
        if 'Pandas' in self.analysis.technologies:
            suggestions.append(
                "📊 Use .query() e .eval() do Pandas para operações mais rápidas"
            )
        
        if 'Model Context Protocol' in self.analysis.technologies:
            suggestions.append(
                "🔌 MCP detectado! Considere integrar com múltiplos serviços via MCP"
            )
        
        # Sugestões baseadas em research metadata (NOVO!)
        if self.analysis.research_metadata:
            rm = self.analysis.research_metadata
            
            if rm.research_questions:
                suggestions.append(
                    f"❓ {len(rm.research_questions)} perguntas de pesquisa identificadas - "
                    f"considere criar experimentos para cada uma"
                )
            
            if rm.goals:
                suggestions.append(
                    f"🎯 {len(rm.goals)} objetivos definidos - "
                    f"crie métricas específicas para cada"
                )
            
            if rm.methodology:
                suggestions.append(
                    "📋 Metodologia bem definida - "
                    "documente resultados de cada etapa"
                )
        
        suggestions.extend([
            "🎯 Adicione validação cruzada (k-fold) na avaliação dos modelos",
            "📈 Implemente early stopping para evitar overfitting",
        ])
        
        return suggestions
    
    def generate_report(self, output_path: Path | None = None) -> str:
        """Gera relatório completo da análise"""
        if not self.analysis:
            raise ValueError("Execute analyze_project() primeiro")
        
        papers = self.search_relevant_research()
        suggestions = self.suggest_improvements()
        
        # Seção de metadados
        metadata_section = ""
        if self.analysis.metadata:
            m = self.analysis.metadata
            metadata_section = f"""
📦 METADADOS DO PROJETO:
   • Nome: {m.name}
   • Versão: {m.version or 'N/A'}
   • Keywords: {', '.join(m.keywords) if m.keywords else 'Nenhuma'}
   • Dependências: {len(m.dependencies)} principais"""
        
        # Seção de research metadata (NOVO!)
        research_section = ""
        if self.analysis.research_metadata:
            rm = self.analysis.research_metadata
            research_section = f"""
🔬 METADADOS DE PESQUISA (README):
   • Research Focus: {', '.join(rm.research_focus) if rm.research_focus else 'N/A'}
   • Keywords: {', '.join(rm.keywords[:5]) if rm.keywords else 'N/A'}
   • Perguntas: {len(rm.research_questions)} questões de pesquisa
   • Objetivos: {len(rm.goals)} objetivos definidos
   • Metodologia: {len(rm.methodology)} etapas"""
        
        # Seção de fontes de detecção (NOVO!)
        sources_section = ""
        if self.analysis.detection_sources:
            sources_section = "\n🔍 FONTES DE DETECÇÃO:\n"
            for tech, sources in list(self.analysis.detection_sources.items())[:5]:
                sources_str = ", ".join(sources)
                sources_section += f"   • {tech}: {sources_str}\n"
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          🤖 AI RESEARCH ASSISTANT - REPORT                  ║
╚══════════════════════════════════════════════════════════════╝

📦 PROJETO: {self.analysis.project_name}
📁 Arquivos analisados: {self.analysis.files_analyzed}
{metadata_section}
{research_section}

🔧 TECNOLOGIAS DETECTADAS ({len(self.analysis.technologies)}):
{self._format_list(self.analysis.technologies)}
{sources_section}

📚 PAPERS RELEVANTES ENCONTRADOS:

{self._format_papers(papers)}

💡 SUGESTÕES DE MELHORIA ({len(suggestions)}):

{self._format_list(suggestions, numbered=True)}

═══════════════════════════════════════════════════════════════

🎯 PRÓXIMOS PASSOS:
1. Revisar papers recomendados
2. Implementar técnicas sugeridas
3. Responder perguntas de pesquisa definidas
4. Validar com métricas apropriadas

═══════════════════════════════════════════════════════════════
        """
        
        if output_path:
            output_path.write_text(report, encoding='utf-8')
            print(f"💾 Relatório salvo em: {output_path}")
        
        return report
    
    @staticmethod
    def _format_list(items: list[str], numbered: bool = False) -> str:
        """Formata lista para o relatório"""
        if not items:
            return "   (nenhum item)"
        
        if numbered:
            return "\n".join(f"   {i+1}. {item}" for i, item in enumerate(items))
        return "\n".join(f"   • {item}" for item in items)
    
    @staticmethod
    def _format_papers(papers: list[Paper]) -> str:
        """Formata papers para o relatório"""
        if not papers:
            return "   (nenhum paper encontrado)"
        
        formatted = []
        for i, paper in enumerate(papers, 1):
            formatted.append(f"""
   {i}. {paper.title}
      Autores: {', '.join(paper.authors[:3])}
      Keywords: {', '.join(paper.keywords[:5])}
      URL: {paper.url}
      Upvotes: {paper.upvotes}
            """.strip())
        
        return "\n\n".join(formatted)


def main():
    """Função principal."""
    print("""
    ╔════════════════════════════════════════╗
    ║   🚀 AI Research Assistant v1.0       ║
    ║   Powered by MCP + Python 3.13        ║
    ╚════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1])
    else:
        project_path = Path.cwd()
    
    assistant = AIResearchAssistant(project_path)
    
    print("\n🔄 Iniciando análise...\n")
    assistant.analyze_project()
    
    report = assistant.generate_report()
    print(report)
    
    output_file = project_path / "ai_research_report.txt"
    assistant.generate_report(output_file)
    
    print("\n✅ Análise concluída com sucesso!")


if __name__ == "__main__":
    main()
