#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SISTEMA DE CONVERSAO UNIVERSAL - SCRIPT PRINCIPAL
Conversao de Excel para multiplos bancos de dados com validacao automatica
"""

import os
import sys
import argparse
import platform
from datetime import datetime
from pathlib import Path

def show_main_banner():
    print("=" * 70)
    print("  SISTEMA DE CONVERSÃO UNIVERSAL DE EXCEL PARA BANCO DE DADOS")
    print("=" * 70)
    print("  🔄 Excel → CSV + SQL (MySQL, PostgreSQL, SQLite, SQL Server)")
    print("  📋 Schemas SQL personalizados")
    print("  ✅ Validação automática completa")
    print("  🌐 Scripts multiplataforma")
    print("=" * 70)
    print()

def check_dependencies():
    """Verifica dependências necessárias"""
    required_modules = [
        'pandas', 'openpyxl', 'sqlalchemy'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌  DEPENDÊNCIAS FALTANDO:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n📦 Instale com: pip install " + " ".join(missing_modules))
        return False
    
    return True

def get_available_schemas(schemas_dir="schemas"):
    """Lista schemas disponíveis"""
    schemas = []
    if os.path.exists(schemas_dir):
        for file in os.listdir(schemas_dir):
            if file.endswith('.sql'):
                schemas.append(os.path.join(schemas_dir, file))
    return schemas

def show_schema_info(schema_file):
    """Mostra informações do schema"""
    try:
        from src.sql_schema_parser import SQLSchemaParser
        parser = SQLSchemaParser()
        schema = parser.parse_file(schema_file)
        
        print(f"📋 Schema: {schema['table_name']}")
        print(f"📊 Campos: {len(schema['fields'])}")
        for field_name, field_info in schema['fields'].items():
            print(f"   - {field_name}: {field_info['type']}")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao ler schema: {e}")

def convert_excel_mode(args):
    """Modo de conversão de Excel"""
    from src.convert_excel_universal_clean import convert_excel_to_database
    
    print("🔄 MODO: Conversão de Excel")
    print(f"📊 Arquivo: {args.excel_file}")
    if args.schema:
        print(f"📋 Schema: {args.schema}")
        show_schema_info(args.schema)
    print(f"💾 Saída: {args.output}")
    if getattr(args, 'xlsx_only', False):
        print("📄 Modo: Apenas XLSX corrigido (pular CSV/SQL)")
    else:
        print("📄 Modo: Gerar CSV + SQL + XLSX")
    print()
    
    try:
        result = convert_excel_to_database(
            args.excel_file, 
            args.output, 
            args.schema, 
            args.verbose,
            xlsx_only=getattr(args, 'xlsx_only', False)
        )
        print(f"✅ Conversão concluída! ({len(result)} registros)")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        return False

def multi_database_mode(args):
    """Modo multi-banco"""
    from src.multi_database_generator import MultiDatabaseGenerator
    
    print("🗄️ MODO: Geração Multi-Banco")
    print(f"📄 Arquivo SQL: {args.sql_file}")
    print(f"💾 Saída: {args.output}")
    print()
    
    try:
        # Criar diretório multi-banco
        multi_db_dir = os.path.join(args.output, "multi_database")
        os.makedirs(multi_db_dir, exist_ok=True)
        
        generator = MultiDatabaseGenerator()
        base_filename = os.path.splitext(os.path.basename(args.sql_file))[0]
        
        results = generator.generate_for_all_databases(
            args.sql_file, 
            multi_db_dir, 
            base_filename
        )
        
        # Gerar exemplos de conexão
        examples_file = generator.generate_connection_examples(multi_db_dir)
        
        print("✅ Geração multi-banco concluída!")
        print("\n📊 Resultados:")
        for db_type, result in results.items():
            if result['status'] == 'success':
                print(f"   ✅ {db_type.upper()}: {result['file']}")
            else:
                print(f"   ❌ {db_type.upper()}: {result['error']}")
        
        print(f"\n📋 Exemplos de conexão: {examples_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na geração multi-banco: {e}")
        return False

def validation_mode(args):
    """Modo validação"""
    from src.validation_system import run_full_validation
    
    print("🔍 MODO: Validação Completa")
    print(f"📊 Arquivo: {args.excel_file}")
    if args.schema:
        print(f"📋 Schema: {args.schema}")
    print()
    
    try:
        results = run_full_validation(
            args.excel_file,
            args.schema,
            args.output,
            args.verbose
        )
        
        # Contar resultados
        total_errors = 0
        total_warnings = 0
        
        for category, validations in results.items():
            if category == 'sql_validation':
                continue
            
            errors = len([v for v in validations if v.startswith('❌')])
            warnings = len([v for v in validations if v.startswith('⚠️')])
            
            total_errors += errors
            total_warnings += warnings
        
        if total_errors == 0:
            print("✅ Validação aprovada!")
            return True
        else:
            print(f"❌ Validação reprovada ({total_errors} erros, {total_warnings} avisos)")
            return False
        
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False

def complete_workflow_mode(args):
    """Modo workflow completo"""
    print("🚀 MODO: Workflow Completo")
    if getattr(args, 'xlsx_only', False):
        print("   1. Conversão de Excel (apenas XLSX)")
        print("   2. Validação")
        print("   (Geração Multi-Banco será pulada)")
    else:
        print("   1. Conversão de Excel (CSV + SQL + XLSX)")
        print("   2. Validação")
        print("   3. Geração Multi-Banco")
    print()
    
    success = True
    
    # 1. Conversão
    print("🔄 ETAPA 1: Conversão...")
    if not convert_excel_mode(args):
        success = False
    print()
    
    # 2. Validação
    print("🔍 ETAPA 2: Validação...")
    if not validation_mode(args):
        success = False
    print()
    
    # 3. Multi-banco (apenas se não for xlsx_only e se existe arquivo SQL)
    if not getattr(args, 'xlsx_only', False):
        filename = os.path.splitext(os.path.basename(args.excel_file))[0]
        sql_file = os.path.join(args.output, f"{filename}_inserts.sql")
        
        if os.path.exists(sql_file):
            print("🗄️ ETAPA 3: Geração Multi-Banco...")
            args.sql_file = sql_file
            if not multi_database_mode(args):
                success = False
        else:
            print("⚠️  ETAPA 3: Pulada (arquivo SQL não encontrado)")
    else:
        print("⚠️  ETAPA 3: Pulada (modo xlsx-only ativado)")
    
    print()
    if success:
        print("✅ WORKFLOW COMPLETO CONCLUÍDO!")
    else:
        print("❌ WORKFLOW INCOMPLETO (verifique erros acima)")
    
    return success

def interactive_mode():
    """Modo interativo"""
    print("💻  MODO INTERATIVO")
    print()
    
    # Escolher arquivo Excel
    while True:
        excel_file = input("📊 Arquivo Excel: ").strip()
        if os.path.exists(excel_file):
            break
        print("❌ Arquivo não encontrado!")
    
    # Escolher schema
    schemas = get_available_schemas()
    if schemas:
        print("\n📋 Schemas disponíveis:")
        print("   0. Schema padrão")
        for i, schema in enumerate(schemas, 1):
            print(f"   {i}. {schema}")
        
        while True:
            try:
                choice = int(input("\nEscolha um schema (0-{}): ".format(len(schemas))))
                if choice == 0:
                    schema_file = None
                    break
                elif 1 <= choice <= len(schemas):
                    schema_file = schemas[choice - 1]
                    break
                else:
                    print("❌ Escolha inválida!")
            except ValueError:
                print("❌ Digite um número!")
    else:
        schema_file = None
        print("📋 Usando schema padrão")
    
    # Escolher modo
    print("\n🔧 Modos disponíveis:")
    print("   1. Conversão simples")
    print("   2. Conversão + Validação")
    print("   3. Workflow completo")
    
    while True:
        try:
            mode = int(input("Escolha o modo (1-3): "))
            if 1 <= mode <= 3:
                break
            else:
                print("❌ Escolha inválida!")
        except ValueError:
            print("❌ Digite um número!")
    
    # Configurar argumentos
    class Args:
        def __init__(self):
            self.excel_file = excel_file
            self.schema = schema_file
            self.output = "./conversao_output"
            self.verbose = True
    
    args = Args()
    
    # Executar modo escolhido
    print("\n" + "=" * 50)
    if mode == 1:
        return convert_excel_mode(args)
    elif mode == 2:
        success = convert_excel_mode(args)
        if success:
            return validation_mode(args)
        return False
    elif mode == 3:
        return complete_workflow_mode(args)

def main():
    parser = argparse.ArgumentParser(
        description="Sistema de Conversao Universal de Excel para Banco de Dados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
MODOS DE OPERACAO:

1. CONVERSAO SIMPLES:
   python main_converter.py convert arquivo.xlsx

2. CONVERSAO COM SCHEMA:
   python main_converter.py convert arquivo.xlsx --schema schemas/produtos.sql

3. VALIDACAO:
   python main_converter.py validate arquivo.xlsx

4. GERACAO MULTI-BANCO:
   python main_converter.py multi arquivo_inserts.sql

5. WORKFLOW COMPLETO:
   python main_converter.py complete arquivo.xlsx

6. MODO INTERATIVO:
   python main_converter.py interactive

EXEMPLOS:
  python main_converter.py convert vendas.xlsx --schema schemas/vendas.sql -v
  python main_converter.py validate produtos.xlsx --schema schemas/produtos.sql
  python main_converter.py complete dados.xlsx --output ./resultados
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponiveis')
    
    # Comando convert
    convert_parser = subparsers.add_parser('convert', help='Converter Excel')
    convert_parser.add_argument('excel_file', help='Arquivo Excel')
    convert_parser.add_argument('--schema', help='Schema SQL')
    convert_parser.add_argument('-o', '--output', default='./conversao_output', help='Diretorio de saida')
    convert_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    convert_parser.add_argument('--xlsx-only', action='store_true', help='Gerar apenas XLSX corrigido (pular CSV/SQL)')
    
    # Comando validate
    validate_parser = subparsers.add_parser('validate', help='Validar conversao')
    validate_parser.add_argument('excel_file', help='Arquivo Excel')
    validate_parser.add_argument('--schema', help='Schema SQL')
    validate_parser.add_argument('-o', '--output', default='./conversao_output', help='Diretorio de saida')
    validate_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    
    # Comando multi
    multi_parser = subparsers.add_parser('multi', help='Gerar multi-banco')
    multi_parser.add_argument('sql_file', help='Arquivo SQL')
    multi_parser.add_argument('-o', '--output', default='./conversao_output', help='Diretório de saída')
    multi_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    
    # Comando complete
    complete_parser = subparsers.add_parser('complete', help='Workflow completo')
    complete_parser.add_argument('excel_file', help='Arquivo Excel')
    complete_parser.add_argument('--schema', help='Schema SQL')
    complete_parser.add_argument('-o', '--output', default='./conversao_output', help='Diretório de saída')
    complete_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    complete_parser.add_argument('--xlsx-only', action='store_true', help='Gerar apenas XLSX corrigido (pular CSV/SQL)')
    
    # Comando interactive
    interactive_parser = subparsers.add_parser('interactive', help='Modo interativo')
    
    args = parser.parse_args()
    
    # Mostrar banner
    show_main_banner()
    
    # Informações do sistema
    print(f"💻  Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Diretório: {os.getcwd()}")
    print()
    
    # Verificar dependências
    if not check_dependencies():
        return 1
    
    # Executar comando
    if args.command == 'convert':
        success = convert_excel_mode(args)
    elif args.command == 'validate':
        success = validation_mode(args)
    elif args.command == 'multi':
        success = multi_database_mode(args)
    elif args.command == 'complete':
        success = complete_workflow_mode(args)
    elif args.command == 'interactive':
        success = interactive_mode()
    else:
        parser.print_help()
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
