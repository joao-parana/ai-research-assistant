#!/usr/bin/env python3.13
"""
🚀 Quick Start Example
Exemplo rápido de uso do MCP Server
"""

from pathlib import Path
from ai_research_assistant import AIResearchAssistant, ResearchArea


def main():
    """Exemplo de uso básico"""
    
    print("🤖 MCP Server - Quick Start Example\n")
    
    # 1. Analisar projeto atual
    project_path = Path.cwd()
    print(f"📂 Analisando: {project_path}\n")
    
    assistant = AIResearchAssistant(project_path)
    
    # 2. Executar análise
    analysis = assistant.analyze_project()
    
    print(f"\n✅ Análise concluída!")
    print(f"   📁 Arquivos: {analysis.files_analyzed}")
    print(f"   🔧 Tecnologias: {', '.join(analysis.technologies)}")
    
    # 3. Buscar papers relevantes
    print(f"\n📚 Buscando papers sobre Machine Learning...\n")
    papers = assistant.search_relevant_research(ResearchArea.MACHINE_LEARNING, max_papers=3)
    
    for i, paper in enumerate(papers, 1):
        print(f"   {i}. {paper.title}")
        print(f"      Keywords: {', '.join(paper.keywords[:3])}")
    
    # 4. Gerar sugestões
    print(f"\n💡 Gerando sugestões...\n")
    suggestions = assistant.suggest_improvements()
    
    for i, suggestion in enumerate(suggestions[:5], 1):
        print(f"   {i}. {suggestion}")
    
    # 5. Salvar relatório
    print(f"\n📄 Gerando relatório completo...\n")
    report_path = project_path / "mcp_quick_report.txt"
    assistant.generate_report(report_path)
    
    print(f"\n✅ Exemplo concluído!")
    print(f"   Relatório salvo em: {report_path}")


if __name__ == "__main__":
    main()
