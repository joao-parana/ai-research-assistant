#!/bin/bash
# Script para corrigir formatação do projeto

cd /Users/joao/dev/NIE/ai-research-assistant

echo "🔧 Formatando código com Ruff..."
hatch run lint:fmt

echo ""
echo "✅ Formatação concluída!"
echo ""
echo "Agora execute: make lint"
