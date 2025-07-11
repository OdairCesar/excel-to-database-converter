#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import sqlite3
import tempfile
from datetime import datetime

class ValidationError(Exception):
    """Excecao para erros de validacao"""
    pass

class SchemaValidator:
    """Validador de schemas SQL"""
    
    def __init__(self):
        self.supported_types = {
            'INT', 'INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT',
            'VARCHAR', 'TEXT', 'LONGTEXT', 'MEDIUMTEXT',
            'DECIMAL', 'FLOAT', 'DOUBLE',
            'DATE', 'DATETIME', 'TIMESTAMP', 'TIME',
            'BOOLEAN', 'BOOL', 'CHAR'
        }
    
    def validate_schema_file(self, schema_file):
        """Valida se o arquivo de schema existe e eh valido"""
        if not os.path.exists(schema_file):
            raise ValidationError(f"Arquivo de schema nao encontrado: {schema_file}")
        
        if not schema_file.endswith('.sql'):
            raise ValidationError(f"Arquivo deve ter extensao .sql: {schema_file}")
        
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                raise ValidationError("Arquivo de schema esta vazio")
            
            if 'CREATE TABLE' not in content.upper():
                raise ValidationError("Schema deve conter CREATE TABLE")
            
            return True
            
        except UnicodeDecodeError:
            raise ValidationError("Erro de encoding no arquivo de schema")
    
    def validate_parsed_schema(self, parsed_schema):
        """Valida schema parseado"""
        if not isinstance(parsed_schema, dict):
            raise ValidationError("Schema deve ser um dicionario")
        
        if 'table_name' not in parsed_schema:
            raise ValidationError("Schema deve ter 'table_name'")
        
        if 'fields' not in parsed_schema:
            raise ValidationError("Schema deve ter 'fields'")
        
        if not parsed_schema['fields']:
            raise ValidationError("Schema deve ter pelo menos um campo")
        
        # Validar campos
        for field_name, field_info in parsed_schema['fields'].items():
            if not isinstance(field_info, dict):
                raise ValidationError(f"Campo {field_name} deve ser um dicionario")
            
            if 'type' not in field_info:
                raise ValidationError(f"Campo {field_name} deve ter 'type'")
            
            field_type = field_info['type'].upper()
            base_type = field_type.split('(')[0]
            
            if base_type not in self.supported_types:
                print(f"Aviso: Tipo {base_type} pode nao ser suportado")
        
        return True
    
    def validate_excel_file(self, excel_file):
        """Valida arquivo Excel"""
        if not os.path.exists(excel_file):
            raise ValidationError(f"Arquivo Excel nao encontrado: {excel_file}")
        
        if not excel_file.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError(f"Arquivo deve ser Excel (.xlsx ou .xls): {excel_file}")
        
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            
            if df.empty:
                raise ValidationError("Arquivo Excel esta vazio")
            
            if len(df.columns) == 0:
                raise ValidationError("Arquivo Excel nao tem colunas")
            
            return True
            
        except Exception as e:
            raise ValidationError(f"Erro ao ler Excel: {e}")

class ConversionValidator:
    """Validador de conversão"""
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
    
    def validate_conversion_result(self, result_df, original_df, schema):
        """Valida resultado da conversão"""
        issues = []
        
        # Verificar se não perdemos registros
        if len(result_df) != len(original_df):
            issues.append(f"Número de registros alterado: {len(original_df)} -> {len(result_df)}")
        
        # Verificar se todos os campos do schema estão presentes
        schema_fields = set(schema['fields'].keys())
        result_fields = set(result_df.columns)
        
        missing_fields = schema_fields - result_fields
        if missing_fields:
            issues.append(f"Campos ausentes: {missing_fields}")
        
        extra_fields = result_fields - schema_fields
        if extra_fields:
            issues.append(f"Campos extras: {extra_fields}")
        
        # Verificar tipos de dados
        for field_name in schema['fields']:
            if field_name in result_df.columns:
                field_type = schema['fields'][field_name]['type'].upper()
                
                if 'INT' in field_type:
                    non_numeric = result_df[field_name].apply(lambda x: not pd.isna(x) and not isinstance(x, (int, float)))
                    if non_numeric.any():
                        issues.append(f"Campo {field_name} deveria ser numérico")
                
                elif 'VARCHAR' in field_type or 'TEXT' in field_type:
                    max_length = None
                    if '(' in field_type and ')' in field_type:
                        try:
                            max_length = int(field_type.split('(')[1].split(')')[0])
                        except:
                            pass
                    
                    if max_length:
                        too_long = result_df[field_name].astype(str).str.len() > max_length
                        if too_long.any():
                            issues.append(f"Campo {field_name} excede tamanho máximo {max_length}")
        
        return issues
    
    def validate_files_generated(self, output_dir, filename):
        """Valida se os arquivos foram gerados"""
        csv_file = os.path.join(output_dir, f"{filename}_convertido.csv")
        sql_file = os.path.join(output_dir, f"{filename}_inserts.sql")
        
        issues = []
        
        if not os.path.exists(csv_file):
            issues.append(f"Arquivo CSV não foi gerado: {csv_file}")
        else:
            try:
                test_df = pd.read_csv(csv_file)
                if test_df.empty:
                    issues.append("Arquivo CSV está vazio")
            except Exception as e:
                issues.append(f"Erro ao ler CSV: {e}")
        
        if not os.path.exists(sql_file):
            issues.append(f"Arquivo SQL não foi gerado: {sql_file}")
        else:
            try:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if not content.strip():
                    issues.append("Arquivo SQL está vazio")
                if 'INSERT INTO' not in content.upper():
                    issues.append("Arquivo SQL não contém INSERTs")
            except Exception as e:
                issues.append(f"Erro ao ler SQL: {e}")
        
        return issues

class DatabaseTester:
    """Testa SQL gerado em banco real"""
    
    def test_sql_syntax(self, sql_file):
        """Testa sintaxe SQL usando SQLite"""
        try:
            # Criar banco temporário
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
                temp_db_path = temp_db.name
            
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            
            # Ler e executar SQL
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Adaptar para SQLite (básico)
            sql_content = sql_content.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
            sql_content = sql_content.replace('`', '"')
            
            # Separar comandos
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]
            
            results = []
            for statement in statements:
                if statement.startswith('--'):
                    continue
                
                try:
                    cursor.execute(statement)
                    results.append(f"✅ {statement[:50]}...")
                except sqlite3.Error as e:
                    results.append(f"❌ {statement[:50]}... - Erro: {e}")
            
            conn.commit()
            conn.close()
            
            # Limpar arquivo temporário
            os.unlink(temp_db_path)
            
            return results
            
        except Exception as e:
            return [f"Erro geral: {e}"]

def run_full_validation(excel_file, schema_file=None, output_dir="./conversao_output", verbose=False):
    """Executa validação completa"""
    print("=" * 60)
    print("VALIDAÇÃO COMPLETA DO SISTEMA DE CONVERSÃO")
    print("=" * 60)
    print()
    
    validator = ConversionValidator()
    db_tester = DatabaseTester()
    
    # Resultados
    validation_results = {
        'schema_validation': [],
        'excel_validation': [],
        'conversion_validation': [],
        'file_validation': [],
        'sql_validation': []
    }
    
    try:
        # 1. Validar arquivo Excel
        print("1. Validando arquivo Excel...")
        try:
            validator.schema_validator.validate_excel_file(excel_file)
            validation_results['excel_validation'].append("✅ Arquivo Excel válido")
            print("   ✅ Arquivo Excel válido")
        except ValidationError as e:
            validation_results['excel_validation'].append(f"❌ {e}")
            print(f"   ❌ {e}")
            return validation_results
        
        # 2. Validar schema (se fornecido)
        if schema_file:
            print("2. Validando schema SQL...")
            try:
                validator.schema_validator.validate_schema_file(schema_file)
                validation_results['schema_validation'].append("✅ Arquivo de schema válido")
                print("   ✅ Arquivo de schema válido")
                
                # Testar parsing
                from sql_schema_parser import SQLSchemaParser
                parser = SQLSchemaParser()
                parsed_schema = parser.parse_file(schema_file)
                
                validator.schema_validator.validate_parsed_schema(parsed_schema)
                validation_results['schema_validation'].append("✅ Schema parseado com sucesso")
                print("   ✅ Schema parseado com sucesso")
                
            except ValidationError as e:
                validation_results['schema_validation'].append(f"❌ {e}")
                print(f"   ❌ {e}")
                return validation_results
        else:
            print("2. Usando schema padrão...")
            validation_results['schema_validation'].append("✅ Schema padrão")
            print("   ✅ Schema padrão")
        
        # 3. Executar conversão
        print("3. Executando conversão...")
        try:
            from convert_excel_universal_clean import convert_excel_to_database
            
            # Ler Excel original
            original_df = pd.read_excel(excel_file, engine='openpyxl')
            
            # Executar conversão
            result_df = convert_excel_to_database(excel_file, output_dir, schema_file, verbose)
            
            validation_results['conversion_validation'].append("✅ Conversão executada")
            print("   ✅ Conversão executada")
            
            # Validar resultado
            if schema_file:
                parser = SQLSchemaParser()
                parsed_schema = parser.parse_file(schema_file)
                from convert_excel_universal_clean import convert_schema_format
                schema = convert_schema_format(parsed_schema)
            else:
                from convert_excel_universal_clean import get_default_schema
                schema = get_default_schema()
            
            issues = validator.validate_conversion_result(result_df, original_df, schema)
            if issues:
                for issue in issues:
                    validation_results['conversion_validation'].append(f"❌ {issue}")
                    print(f"   ❌ {issue}")
            else:
                validation_results['conversion_validation'].append("✅ Conversão válida")
                print("   ✅ Conversão válida")
            
        except Exception as e:
            validation_results['conversion_validation'].append(f"❌ Erro na conversão: {e}")
            print(f"   ❌ Erro na conversão: {e}")
            return validation_results
        
        # 4. Validar arquivos gerados
        print("4. Validando arquivos gerados...")
        filename = os.path.splitext(os.path.basename(excel_file))[0]
        file_issues = validator.validate_files_generated(output_dir, filename)
        
        if file_issues:
            for issue in file_issues:
                validation_results['file_validation'].append(f"❌ {issue}")
                print(f"   ❌ {issue}")
        else:
            validation_results['file_validation'].append("✅ Arquivos gerados corretamente")
            print("   ✅ Arquivos gerados corretamente")
        
        # 5. Testar SQL
        print("5. Testando sintaxe SQL...")
        sql_file = os.path.join(output_dir, f"{filename}_inserts.sql")
        
        if os.path.exists(sql_file):
            sql_results = db_tester.test_sql_syntax(sql_file)
            validation_results['sql_validation'] = sql_results
            
            success_count = sum(1 for r in sql_results if r.startswith('✅'))
            error_count = sum(1 for r in sql_results if r.startswith('❌'))
            
            print(f"   ✅ {success_count} comandos executados com sucesso")
            if error_count > 0:
                print(f"   ❌ {error_count} comandos com erro")
            
            if verbose:
                for result in sql_results:
                    print(f"   {result}")
        else:
            validation_results['sql_validation'].append("❌ Arquivo SQL não encontrado")
            print("   ❌ Arquivo SQL não encontrado")
        
        print()
        print("=" * 60)
        print("RESUMO DA VALIDAÇÃO")
        print("=" * 60)
        
        all_validations = [
            validation_results['excel_validation'],
            validation_results['schema_validation'],
            validation_results['conversion_validation'],
            validation_results['file_validation']
        ]
        
        total_issues = sum(len([v for v in val if v.startswith('❌')]) for val in all_validations)
        total_warnings = sum(len([v for v in val if v.startswith('⚠️')]) for val in all_validations)
        
        if total_issues == 0:
            print("✅ VALIDAÇÃO APROVADA - Sistema funcionando corretamente!")
        else:
            print(f"❌ VALIDAÇÃO REPROVADA - {total_issues} erro(s) encontrado(s)")
        
        if total_warnings > 0:
            print(f"⚠️ {total_warnings} aviso(s) encontrado(s)")
        
        return validation_results
        
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return validation_results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python validation_system.py <excel_file> [schema_file]")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    schema_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    results = run_full_validation(excel_file, schema_file, verbose=True)
