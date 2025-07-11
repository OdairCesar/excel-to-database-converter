#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE FINAL - Sistema de Conversão Universal Excel para Banco de Dados
Sistema completo de testes para verificar funcionalidades
"""

import os
import sys
import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def show_test_banner():
    """Mostra banner dos testes"""
    print("=" * 70)
    print("  TESTE FINAL - SISTEMA DE CONVERSÃO UNIVERSAL")
    print("=" * 70)
    print("  🧪 Testes automatizados completos")
    print("  📊 Verificação de funcionalidades")
    print("  🔧 Diagnóstico de problemas")
    print("=" * 70)
    print()

def test_dependencies():
    """Testa dependências do sistema"""
    print("🔍 Testando dependências...")
    
    required_modules = [
        'pandas', 'openpyxl', 'sqlalchemy'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"   ❌ {module} - FALTANDO")
    
    if missing_modules:
        print(f"\n❌ Dependências faltando: {', '.join(missing_modules)}")
        print("📦 Instale com: pip install " + " ".join(missing_modules))
        return False
    
    print("✅ Todas as dependências estão instaladas")
    return True

def test_structure():
    """Testa estrutura do projeto"""
    print("\n🏗️  Testando estrutura do projeto...")
    
    required_files = [
        'main_converter.py',
        'config.json',
        'README.md',
        'src/convert_excel_universal_clean.py',
        'src/sql_schema_parser.py',
        'src/validation_system.py',
        'src/multi_database_generator.py'
    ]
    
    required_dirs = [
        'src',
        'schemas',
        'conversao_output'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            missing_files.append(file)
            print(f"   ❌ {file} - FALTANDO")
    
    missing_dirs = []
    for dir in required_dirs:
        if os.path.exists(dir):
            print(f"   ✅ {dir}/")
        else:
            missing_dirs.append(dir)
            print(f"   ❌ {dir}/ - FALTANDO")
    
    if missing_files or missing_dirs:
        print(f"\n❌ Arquivos/diretórios faltando:")
        for item in missing_files + missing_dirs:
            print(f"   - {item}")
        return False
    
    print("✅ Estrutura do projeto OK")
    return True

def test_config():
    """Testa arquivo de configuração"""
    print("\n⚙️  Testando configuração...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_keys = ['version', 'default_output_dir', 'encoding', 'supported_databases']
        for key in required_keys:
            if key in config:
                print(f"   ✅ {key}: {config[key]}")
            else:
                print(f"   ❌ {key} - FALTANDO")
                return False
        
        print("✅ Configuração OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler config.json: {e}")
        return False

def test_modules():
    """Testa importação dos módulos"""
    print("\n📦 Testando módulos do sistema...")
    
    modules_to_test = [
        ('sql_schema_parser', 'SQLSchemaParser'),
        ('validation_system', 'ValidationError'),
        ('multi_database_generator', 'MultiDatabaseGenerator'),
        ('convert_excel_universal_clean', 'convert_excel_to_database')
    ]
    
    for module_name, class_or_function in modules_to_test:
        try:
            module = __import__(module_name)
            if hasattr(module, class_or_function):
                print(f"   ✅ {module_name}.{class_or_function}")
            else:
                print(f"   ❌ {module_name}.{class_or_function} - FUNÇÃO/CLASSE NÃO ENCONTRADA")
                return False
        except ImportError as e:
            print(f"   ❌ {module_name} - ERRO DE IMPORTAÇÃO: {e}")
            return False
    
    print("✅ Todos os módulos carregados")
    return True

def test_schema_parser():
    """Testa o parser de schemas SQL"""
    print("\n🔍 Testando parser de schemas...")
    
    try:
        from sql_schema_parser import SQLSchemaParser
        
        # Criar schema de teste
        test_schema = """
        CREATE TABLE test_table (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE,
            idade INT DEFAULT 0,
            ativo BOOLEAN DEFAULT TRUE
        );
        """
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(test_schema)
            temp_file = f.name
        
        # Testar parser
        parser = SQLSchemaParser()
        result = parser.parse_file(temp_file)
        
        # Verificar resultado
        if result and 'table_name' in result and 'fields' in result:
            print(f"   ✅ Tabela: {result['table_name']}")
            print(f"   ✅ Campos: {len(result['fields'])}")
            for field, info in result['fields'].items():
                print(f"      - {field}: {info['type']}")
        else:
            print("   ❌ Resultado inválido do parser")
            return False
        
        # Limpar arquivo temporário
        os.unlink(temp_file)
        
        print("✅ Parser de schemas OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do parser: {e}")
        return False

def test_validation():
    """Testa sistema de validação"""
    print("\n✅ Testando sistema de validação...")
    
    try:
        from validation_system import SchemaValidator, ValidationError
        
        validator = SchemaValidator()
        
        # Testar validação de arquivo inexistente
        try:
            validator.validate_schema_file('arquivo_inexistente.sql')
            print("   ❌ Deveria ter falhado com arquivo inexistente")
            return False
        except ValidationError:
            print("   ✅ Validação de arquivo inexistente OK")
        
        # Criar arquivo válido temporário
        valid_schema = """
        CREATE TABLE usuarios (
            id INT PRIMARY KEY,
            nome VARCHAR(255)
        );
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(valid_schema)
            temp_file = f.name
        
        # Testar validação de arquivo válido
        try:
            validator.validate_schema_file(temp_file)
            print("   ✅ Validação de arquivo válido OK")
        except ValidationError as e:
            print(f"   ❌ Arquivo válido rejeitado: {e}")
            return False
        
        # Limpar arquivo temporário
        os.unlink(temp_file)
        
        print("✅ Sistema de validação OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de validação: {e}")
        return False

def test_excel_conversion():
    """Testa conversão de Excel"""
    print("\n🔄 Testando conversão de Excel...")
    
    try:
        import pandas as pd
        from convert_excel_universal_clean import convert_excel_to_database
        
        # Criar dados de teste
        test_data = {
            'nome': ['João Silva', 'Maria Santos', 'Pedro Oliveira'],
            'email': ['joao@email.com', 'maria@email.com', 'pedro@email.com'],
            'idade': [25, 30, 35],
            'ativo': [True, True, False]
        }
        
        df = pd.DataFrame(test_data)
        
        # Criar arquivo Excel temporário
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            excel_file = f.name
        
        df.to_excel(excel_file, index=False)
        print(f"   ✅ Arquivo Excel criado: {len(df)} registros")
        
        # Criar diretório de saída temporário
        temp_output_dir = tempfile.mkdtemp()
        
        # Testar conversão
        result = convert_excel_to_database(
            excel_file=excel_file,
            output_dir=temp_output_dir,
            schema_file=None,
            verbose=False,
            xlsx_only=False
        )
        
        if result is not None and not result.empty:
            print(f"   ✅ Conversão realizada: {len(result)} registros processados")
            
            # Verificar arquivos gerados
            expected_files = ['csv', 'sql', 'xlsx']
            generated_files = []
            
            for file in os.listdir(temp_output_dir):
                for ext in expected_files:
                    if file.endswith(f'.{ext}'):
                        generated_files.append(ext)
                        print(f"   ✅ Arquivo gerado: {file}")
            
            if len(generated_files) >= 2:  # Pelo menos 2 formatos
                print("✅ Conversão de Excel OK")
                success = True
            else:
                print("❌ Poucos arquivos gerados")
                success = False
        else:
            print("❌ Conversão falhou")
            success = False
        
        # Limpar arquivos temporários
        os.unlink(excel_file)
        shutil.rmtree(temp_output_dir)
        
        return success
        
    except Exception as e:
        print(f"❌ Erro no teste de conversão: {e}")
        return False

def test_database_generation():
    """Testa geração de múltiplos bancos de dados"""
    print("\n🗄️  Testando geração de bancos de dados...")
    
    try:
        from multi_database_generator import MultiDatabaseGenerator
        import tempfile
        
        # Criar SQL de teste
        test_sql = """
        CREATE TABLE usuarios (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE,
            idade INT DEFAULT 0
        );
        
        INSERT INTO usuarios (nome, email, idade) VALUES ('João', 'joao@email.com', 25);
        INSERT INTO usuarios (nome, email, idade) VALUES ('Maria', 'maria@email.com', 30);
        """
        
        # Criar arquivo SQL temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(test_sql)
            temp_sql_file = f.name
        
        # Criar diretório de saída temporário
        temp_output_dir = tempfile.mkdtemp()
        
        generator = MultiDatabaseGenerator()
        
        # Testar geração para todos os bancos
        results = generator.generate_for_all_databases(
            source_sql_file=temp_sql_file,
            output_dir=temp_output_dir,
            base_filename='test_usuarios'
        )
        
        # Verificar resultados
        success_count = 0
        for db_type, result in results.items():
            if result['status'] == 'success':
                print(f"   ✅ {db_type.upper()}: {result['file']}")
                success_count += 1
            else:
                print(f"   ❌ {db_type.upper()}: {result.get('error', 'Unknown error')}")
        
        # Limpar arquivos temporários
        os.unlink(temp_sql_file)
        import shutil
        shutil.rmtree(temp_output_dir)
        
        if success_count >= 2:  # Pelo menos 2 bancos funcionando
            print("✅ Geração de bancos de dados OK")
            return True
        else:
            print("❌ Poucos bancos funcionando")
            return False
        
    except Exception as e:
        print(f"❌ Erro no teste de geração: {e}")
        return False

def test_main_converter():
    """Testa o conversor principal"""
    print("\n🎯 Testando conversor principal...")
    
    try:
        # Importar e testar o módulo principal
        sys.path.insert(0, '.')
        import main_converter
        
        # Verificar se as funções principais existem
        required_functions = [
            'show_main_banner',
            'check_dependencies',
            'get_available_schemas',
            'convert_excel_mode'
        ]
        
        for func_name in required_functions:
            if hasattr(main_converter, func_name):
                print(f"   ✅ {func_name}")
            else:
                print(f"   ❌ {func_name} - FUNÇÃO NÃO ENCONTRADA")
                return False
        
        # Testar verificação de dependências
        deps_ok = main_converter.check_dependencies()
        if deps_ok:
            print("   ✅ Verificação de dependências OK")
        else:
            print("   ❌ Verificação de dependências falhou")
            return False
        
        # Testar listagem de schemas
        schemas = main_converter.get_available_schemas()
        print(f"   ✅ Schemas disponíveis: {len(schemas)}")
        
        print("✅ Conversor principal OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do conversor principal: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("🚀 Iniciando testes completos...")
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Diretório: {os.getcwd()}")
    print()
    
    tests = [
        ("Dependências", test_dependencies),
        ("Estrutura", test_structure),
        ("Configuração", test_config),
        ("Módulos", test_modules),
        ("Parser de Schemas", test_schema_parser),
        ("Sistema de Validação", test_validation),
        ("Conversão Excel", test_excel_conversion),
        ("Geração de Bancos", test_database_generation),
        ("Conversor Principal", test_main_converter)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Erro crítico em {test_name}: {e}")
            failed += 1
    
    # Resultados finais
    print("\n" + "=" * 70)
    print("  RESULTADOS DOS TESTES")
    print("=" * 70)
    print(f"✅ Testes aprovados: {passed}")
    print(f"❌ Testes falharam: {failed}")
    print(f"📊 Total de testes: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema está funcionando corretamente")
        print("\n🚀 Pronto para uso!")
    else:
        print(f"\n⚠️  {failed} TESTE(S) FALHARAM")
        print("❌ Sistema pode ter problemas")
        print("\n🔧 Verifique os erros acima e execute:")
        print("   python setup.py")
    
    print("=" * 70)
    
    return failed == 0

def main():
    """Função principal"""
    show_test_banner()
    
    success = run_all_tests()
    
    if success:
        print("\n💡 PRÓXIMOS PASSOS:")
        print("1. Execute: python main_converter.py --help")
        print("2. Teste com: python main_converter.py interactive")
        print("3. Veja exemplos em: README.md")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
