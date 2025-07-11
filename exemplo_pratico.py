#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EXEMPLO PRÁTICO: Comparação entre conversão normal e --xlsx-only
"""

import os
import pandas as pd
from datetime import datetime

def create_sample_data():
    """Cria dados de exemplo com problemas comuns"""
    
    data = {
        'nome': ['João Silva', 'Maria Santos', 'Pedro Oliveira'],
        'celular_ddd': ['11.0', '21.0', '31.0'],  # Problema: .0 no final
        'telefone': ['123456789.0', '987654321.0', '555666777.0'],  # Problema: .0 no final
        'email': ['joao@email.com', 'maria@email.com', 'pedro@email.com'],
        'valor': [100.50, 200.75, 150.25],
        'observacoes': ['Obs 1', None, 'Obs 3'],  # Problema: None
        'categoria': ['A', 'B', 'A']
    }
    
    df = pd.DataFrame(data)
    
    # Salvar arquivo Excel
    sample_file = 'examples/comparacao_exemplo.xlsx'
    os.makedirs(os.path.dirname(sample_file), exist_ok=True)
    df.to_excel(sample_file, index=False)
    
    print(f"✅ Arquivo de exemplo criado: {sample_file}")
    print(f"📊 Dados originais:")
    print(df.to_string(index=False))
    print()
    
    return sample_file

def run_normal_conversion(sample_file):
    """Executa conversão normal"""
    print("🔄 CONVERSÃO NORMAL (CSV + SQL):")
    print("-" * 50)
    
    cmd = f"python3 main_converter.py convert {sample_file} --verbose"
    print(f"Comando: {cmd}")
    print()
    
    os.system(cmd)
    
    # Verificar arquivos gerados
    csv_file = './conversao_output/comparacao_exemplo_convertido.csv'
    sql_file = './conversao_output/comparacao_exemplo_inserts.sql'
    
    if os.path.exists(csv_file):
        print(f"\n📄 CSV gerado: {csv_file}")
        with open(csv_file, 'r', encoding='utf-8') as f:
            print("Conteúdo:")
            print(f.read()[:500] + "...")
    
    if os.path.exists(sql_file):
        print(f"\n📝 SQL gerado: {sql_file}")
        with open(sql_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print("Primeiras linhas:")
            for i, line in enumerate(lines[:10]):
                print(f"{i+1:2d}: {line.strip()}")
    
    print()

def run_xlsx_only_conversion(sample_file):
    """Executa conversão --xlsx-only"""
    print("📄 CONVERSÃO --xlsx-only:")
    print("-" * 50)
    
    cmd = f"python3 main_converter.py convert {sample_file} --xlsx-only --verbose"
    print(f"Comando: {cmd}")
    print()
    
    os.system(cmd)
    
    # Verificar arquivo gerado
    xlsx_file = './conversao_output/comparacao_exemplo_corrigido.xlsx'
    
    if os.path.exists(xlsx_file):
        print(f"\n📊 XLSX corrigido: {xlsx_file}")
        try:
            # Ler dados corrigidos
            df_corrected = pd.read_excel(xlsx_file, sheet_name='Dados Corrigidos')
            print("Dados corrigidos:")
            print(df_corrected.to_string(index=False))
            
            # Mostrar diferenças
            print("\n🔍 DIFERENÇAS IDENTIFICADAS:")
            print("- celular_ddd: '11.0' → '11' (sem .0)")
            print("- telefone: '123456789.0' → '123456789' (sem .0)")
            print("- observacoes: None → '' (limpo)")
            
        except Exception as e:
            print(f"❌ Erro ao ler XLSX: {e}")
    
    print()

def compare_results():
    """Compara os resultados"""
    print("⚖️ COMPARAÇÃO DOS RESULTADOS:")
    print("-" * 50)
    
    # Verificar arquivos
    csv_file = './conversao_output/comparacao_exemplo_convertido.csv'
    sql_file = './conversao_output/comparacao_exemplo_inserts.sql'
    xlsx_file = './conversao_output/comparacao_exemplo_corrigido.xlsx'
    
    print("📁 Arquivos gerados:")
    
    if os.path.exists(csv_file):
        size = os.path.getsize(csv_file)
        print(f"   CSV: {csv_file} ({size} bytes)")
    
    if os.path.exists(sql_file):
        size = os.path.getsize(sql_file)
        print(f"   SQL: {sql_file} ({size} bytes)")
    
    if os.path.exists(xlsx_file):
        size = os.path.getsize(xlsx_file)
        print(f"   XLSX: {xlsx_file} ({size} bytes)")
    
    print()
    print("🎯 QUANDO USAR CADA MODO:")
    print()
    print("🔄 CONVERSÃO NORMAL:")
    print("   ✅ Quando precisar inserir dados no banco")
    print("   ✅ Quando precisar do arquivo CSV")
    print("   ✅ Quando precisar dos comandos SQL")
    print("   ✅ Para workflow completo de migração")
    print()
    print("📄 CONVERSÃO --xlsx-only:")
    print("   ✅ Quando precisar apenas limpar dados")
    print("   ✅ Quando for usar o Excel corrigido em outro sistema")
    print("   ✅ Quando quiser remover .0 indesejados")
    print("   ✅ Para limpeza rápida de planilhas")
    print("   ✅ Quando não precisar de banco de dados")
    print()

def main():
    print("=" * 70)
    print("  EXEMPLO PRÁTICO: CONVERSÃO NORMAL vs --xlsx-only")
    print("=" * 70)
    print()
    
    # 1. Criar dados de exemplo
    sample_file = create_sample_data()
    
    # 2. Conversão normal
    run_normal_conversion(sample_file)
    
    # 3. Conversão --xlsx-only
    run_xlsx_only_conversion(sample_file)
    
    # 4. Comparar resultados
    compare_results()
    
    print("🎉 EXEMPLO CONCLUÍDO!")
    print("📁 Verifique os arquivos gerados em: ./conversao_output/")

if __name__ == "__main__":
    main()
