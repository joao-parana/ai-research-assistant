#!/usr/bin/env python3.13
"""
🎯 Exemplo: Detecção Inteligente de Tecnologias
Demonstra como o sistema agora detecta tecnologias de múltiplas fontes
"""

from pathlib import Path
from ai_research_assistant import AIResearchAssistant, ProjectMetadataExtractor


def demo_metadata_extraction():
    """Demo de extração de metadados"""
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   🎯 DEMO: Detecção Inteligente de Tecnologias            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Usar o próprio projeto ai-research-assistant como exemplo
    project_path = Path(__file__).parent.parent
    
    print(f"📂 Projeto: {project_path.name}\n")
    
    # 1. Extrair metadados manualmente
    print("=" * 60)
    print("1️⃣  EXTRAÇÃO DE METADADOS")
    print("=" * 60)
    
    extractor = ProjectMetadataExtractor()
    metadata = extractor.extract_from_pyproject(project_path)
    
    if metadata:
        print(f"\n✅ pyproject.toml encontrado!")
        print(f"   Nome: {metadata.name}")
        print(f"   Versão: {metadata.version}")
        print(f"   Descrição: {metadata.description}")
        print(f"\n   📌 Keywords detectadas:")
        for keyword in metadata.keywords:
            print(f"      • {keyword}")
        
        print(f"\n   📦 Dependências ({len(metadata.dependencies)}):")
        for dep in metadata.dependencies[:5]:
            print(f"      • {dep}")
        if len(metadata.dependencies) > 5:
            print(f"      ... e mais {len(metadata.dependencies) - 5}")
    
    # 2. Análise completa do projeto
    print("\n\n" + "=" * 60)
    print("2️⃣  ANÁLISE COMPLETA DO PROJETO")
    print("=" * 60 + "\n")
    
    assistant = AIResearchAssistant(project_path)
    analysis = assistant.analyze_project()
    
    print(f"\n✅ Análise concluída!")
    print(f"\n   📁 Arquivos Python: {analysis.files_analyzed}")
    print(f"\n   🔧 Tecnologias detectadas:")
    for tech in analysis.technologies:
        print(f"      ✓ {tech}")
    
    # 3. Busca automática de papers
    print("\n\n" + "=" * 60)
    print("3️⃣  BUSCA AUTOMÁTICA DE PAPERS")
    print("=" * 60)
    
    print("\n   💡 Sistema detecta keywords e busca automaticamente!\n")
    
    # Busca usando keywords automaticamente
    papers = assistant.search_relevant_research()
    
    print(f"   📚 Papers encontrados ({len(papers)}):\n")
    for i, paper in enumerate(papers, 1):
        print(f"   {i}. {paper.title}")
        print(f"      Keywords: {', '.join(paper.keywords[:3])}")
        print(f"      URL: {paper.url}\n")
    
    # 4. Sugestões específicas
    print("=" * 60)
    print("4️⃣  SUGESTÕES ESPECÍFICAS")
    print("=" * 60 + "\n")
    
    suggestions = assistant.suggest_improvements()
    
    # Filtrar sugestões sobre MCP
    mcp_suggestions = [s for s in suggestions if "MCP" in s or "Model Context Protocol" in s]
    
    print("   🔌 Sugestões relacionadas ao MCP:\n")
    for suggestion in mcp_suggestions:
        print(f"      • {suggestion}\n")
    
    # 5. Comparação: Antes vs Depois
    print("=" * 60)
    print("5️⃣  ANTES vs DEPOIS")
    print("=" * 60 + "\n")
    
    print("   ❌ ANTES (Hard-coded):")
    print("      • Lista fixa de tecnologias")
    print("      • Não detectava 'mcp' do pyproject.toml")
    print("      • Papers genéricos\n")
    
    print("   ✅ DEPOIS (Inteligente):")
    print("      • Lê pyproject.toml, setup.py, requirements.txt")
    print("      • Detecta keywords: 'mcp' → Model Context Protocol")
    print("      • Detecta dependencies automaticamente")
    print("      • Busca papers específicos sobre MCP")
    print("      • Sugestões contextualizadas\n")
    
    # 6. Relatório final
    print("=" * 60)
    print("6️⃣  RELATÓRIO COMPLETO")
    print("=" * 60 + "\n")
    
    report = assistant.generate_report()
    print(report)


def demo_multi_source_detection():
    """Demo de detecção de múltiplas fontes"""
    
    print("\n\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   🎯 DEMO: Detecção Multi-Fonte                           ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    print("O sistema agora detecta tecnologias de 3 fontes:\n")
    
    print("1️⃣  Keywords do pyproject.toml")
    print("   Exemplo: 'mcp' → Model Context Protocol")
    print("   Benefício: Detecta intenção do projeto\n")
    
    print("2️⃣  Dependencies listadas")
    print("   Exemplo: 'numpy>=1.26' → NumPy")
    print("   Benefício: Sabe exatamente o que está instalado\n")
    
    print("3️⃣  Imports no código")
    print("   Exemplo: 'import pandas' → Pandas")
    print("   Benefício: Detecta uso real no código\n")
    
    print("✨ Resultado: Detecção completa e precisa!\n")


def main():
    """Executa todas as demos"""
    
    try:
        demo_metadata_extraction()
        demo_multi_source_detection()
        
        print("\n" + "=" * 60)
        print("✅ DEMO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
        print("""
    🎯 Agora você pode:
    
    1. Executar no seu projeto:
       ai-research-assistant /path/to/your/project
    
    2. Ver detecção automática de MCP e outras tecnologias
    
    3. Receber papers e sugestões relevantes
    
    4. Usar a API programaticamente:
       from ai_research_assistant import AIResearchAssistant
       assistant = AIResearchAssistant("/path")
       assistant.analyze_project()
        """)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
