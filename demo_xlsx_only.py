#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DEMONSTRAÇÃO: Funcionalidade --xlsx-only
Como usar a nova opção para gerar apenas arquivos XLSX corrigidos
"""

import os

def show_banner():
    print("=" * 70)
    print("  DEMONSTRAÇÃO: FUNCIONALIDADE --xlsx-only")
    print("=" * 70)
    print("  📄 Gera apenas arquivo XLSX corrigido")
    print("  🚫 Não gera CSV nem SQL")
    print("  🧹 Aplica todas as limpezas de dados")
    print("  ✨ Formatação melhorada com cabeçalhos")
    print("=" * 70)
    print()

def show_examples():
    print("📋 EXEMPLOS DE USO:")
    print("-" * 40)
    print()
    
    print("1️⃣ Conversão básica (apenas XLSX):")
    print("   python3 main_converter.py convert arquivo.xlsx --xlsx-only")
    print()
    
    print("2️⃣ Com schema personalizado:")
    print("   python3 main_converter.py convert arquivo.xlsx --schema schemas/produtos.sql --xlsx-only")
    print()
    
    print("3️⃣ Especificando diretório de saída:")
    print("   python3 main_converter.py convert arquivo.xlsx --xlsx-only -o ./minha_saida")
    print()
    
    print("4️⃣ Modo completo (só XLSX, sem multi-banco):")
    print("   python3 main_converter.py complete arquivo.xlsx --xlsx-only")
    print()
    
    print("5️⃣ Com verbose para ver detalhes:")
    print("   python3 main_converter.py convert arquivo.xlsx --xlsx-only --verbose")
    print()

def show_benefits():
    print("🎯 BENEFÍCIOS DA OPÇÃO --xlsx-only:")
    print("-" * 40)
    print()
    
    print("✅ Limpeza completa de dados:")
    print("   • Remove sufixos .0 indesejados (ex: '11.0' → '11')")
    print("   • Remove valores NaN, None, vazios")
    print("   • Mantém tipos de dados corretos")
    print("   • Trata campos SET/ENUM como strings")
    print()
    
    print("✅ Formatação melhorada:")
    print("   • Cabeçalhos com informações do arquivo original")
    print("   • Contagem de registros")
    print("   • Data/hora de geração")
    print("   • Ajuste automático de largura das colunas")
    print("   • Formatação de cabeçalhos (negrito, cor de fundo)")
    print()
    
    print("✅ Mais rápido:")
    print("   • Não gera CSV nem SQL")
    print("   • Processamento mais rápido")
    print("   • Menor uso de disco")
    print()
    
    print("✅ Ideal para:")
    print("   • Limpeza de dados Excel")
    print("   • Correção de campos com .0")
    print("   • Preparação de dados para outros sistemas")
    print("   • Padronização de planilhas")
    print()

def show_file_structure():
    print("📂 ESTRUTURA DO ARQUIVO GERADO:")
    print("-" * 40)
    print()
    
    print("arquivo_corrigido.xlsx:")
    print("├── Dados Corrigidos (aba)")
    print("│   ├── Linha 1: Arquivo Original: nome_original.xlsx")
    print("│   ├── Linha 2: Registros: 1234")
    print("│   ├── Linha 3: Gerado em: 2024-07-11 16:24:30")
    print("│   ├── Linha 4: (vazia)")
    print("│   ├── Linha 5: CABEÇALHOS (formatados)")
    print("│   └── Linha 6+: DADOS (limpos)")
    print("└── Formatação:")
    print("    ├── Cabeçalhos: negrito, fundo azul")
    print("    ├── Colunas: largura automática")
    print("    └── Dados: tipos corretos, sem .0")
    print()

def show_comparison():
    print("⚖️ COMPARAÇÃO: Normal vs --xlsx-only:")
    print("-" * 40)
    print()
    
    print("🔄 CONVERSÃO NORMAL:")
    print("   Gera: arquivo_convertido.csv + arquivo_inserts.sql")
    print("   Tempo: mais lento")
    print("   Uso: conversão completa para banco")
    print()
    
    print("📄 CONVERSÃO --xlsx-only:")
    print("   Gera: arquivo_corrigido.xlsx")
    print("   Tempo: mais rápido")
    print("   Uso: limpeza e correção de dados")
    print()

def run_demo():
    """Executa demonstração prática"""
    print("🧪 DEMONSTRAÇÃO PRÁTICA:")
    print("-" * 40)
    print()
    
    # Verificar se existe arquivo de teste
    if os.path.exists('examples/teste_limpeza.xlsx'):
        print("✅ Arquivo de teste encontrado: examples/teste_limpeza.xlsx")
        print()
        
        print("🔄 Executando conversão --xlsx-only...")
        print("   Comando: python3 main_converter.py convert examples/teste_limpeza.xlsx --xlsx-only")
        print()
        
        # Executar comando
        os.system("python3 main_converter.py convert examples/teste_limpeza.xlsx --xlsx-only")
        
        print()
        print("✅ Demonstração concluída!")
        print("📁 Verifique o arquivo gerado em: conversao_output/teste_limpeza_corrigido.xlsx")
        
    else:
        print("⚠️  Arquivo de teste não encontrado.")
        print("   Execute primeiro: python3 test_xlsx_only.py")

def main():
    show_banner()
    show_examples()
    show_benefits()
    show_file_structure()
    show_comparison()
    run_demo()

if __name__ == "__main__":
    main()
