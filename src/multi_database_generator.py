#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Automação Multi-Banco
Suporte para MySQL, PostgreSQL, SQLite, SQL Server
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Any

class DatabaseAdapter:
    """Adaptador base para bancos de dados"""
    
    def __init__(self, db_type: str):
        self.db_type = db_type.lower()
        self.type_mapping = self.get_type_mapping()
        self.syntax_rules = self.get_syntax_rules()
    
    def get_type_mapping(self) -> Dict[str, str]:
        """Mapeamento de tipos entre bancos"""
        return {}
    
    def get_syntax_rules(self) -> Dict[str, str]:
        """Regras de sintaxe específicas do banco"""
        return {}
    
    def adapt_create_table(self, sql: str) -> str:
        """Adapta CREATE TABLE para o banco específico"""
        return sql
    
    def adapt_insert(self, sql: str) -> str:
        """Adapta INSERT para o banco específico"""
        return sql
    
    def get_connection_string_template(self) -> str:
        """Template de string de conexão"""
        return ""

class MySQLAdapter(DatabaseAdapter):
    """Adaptador MySQL"""
    
    def __init__(self):
        super().__init__('mysql')
    
    def get_type_mapping(self) -> Dict[str, str]:
        return {
            'INTEGER': 'INT',
            'BOOLEAN': 'TINYINT(1)',
            'DATETIME': 'DATETIME',
            'STRING': 'VARCHAR(255)',
            'TEXT': 'TEXT'
        }
    
    def get_syntax_rules(self) -> Dict[str, str]:
        return {
            'quote_char': '`',
            'auto_increment': 'AUTO_INCREMENT',
            'current_timestamp': 'CURRENT_TIMESTAMP',
            'engine': 'ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'
        }
    
    def adapt_create_table(self, sql: str) -> str:
        # Adicionar ENGINE se não existir
        if 'ENGINE=' not in sql.upper():
            sql = sql.rstrip(';\n') + f" {self.syntax_rules['engine']};\n"
        
        # Garantir AUTO_INCREMENT
        sql = sql.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
        
        return sql
    
    def get_connection_string_template(self) -> str:
        return "mysql+pymysql://user:password@host:port/database"

class PostgreSQLAdapter(DatabaseAdapter):
    """Adaptador PostgreSQL"""
    
    def __init__(self):
        super().__init__('postgresql')
    
    def get_type_mapping(self) -> Dict[str, str]:
        return {
            'INT': 'INTEGER',
            'TINYINT': 'SMALLINT',
            'TINYINT(1)': 'BOOLEAN',
            'DATETIME': 'TIMESTAMP',
            'TEXT': 'TEXT',
            'AUTO_INCREMENT': 'SERIAL'
        }
    
    def get_syntax_rules(self) -> Dict[str, str]:
        return {
            'quote_char': '"',
            'auto_increment': 'SERIAL',
            'current_timestamp': 'CURRENT_TIMESTAMP'
        }
    
    def adapt_create_table(self, sql: str) -> str:
        # Converter AUTO_INCREMENT para SERIAL
        sql = re.sub(r'(\w+)\s+INT\s+AUTO_INCREMENT', r'\1 SERIAL', sql, flags=re.IGNORECASE)
        
        # Converter TINYINT(1) para BOOLEAN
        sql = re.sub(r'TINYINT\(1\)', 'BOOLEAN', sql, flags=re.IGNORECASE)
        
        # Converter aspas
        sql = sql.replace('`', '"')
        
        return sql
    
    def adapt_insert(self, sql: str) -> str:
        # Converter aspas
        sql = sql.replace('`', '"')
        return sql
    
    def get_connection_string_template(self) -> str:
        return "postgresql://user:password@host:port/database"

class SQLiteAdapter(DatabaseAdapter):
    """Adaptador SQLite"""
    
    def __init__(self):
        super().__init__('sqlite')
    
    def get_type_mapping(self) -> Dict[str, str]:
        return {
            'VARCHAR': 'TEXT',
            'TINYINT': 'INTEGER',
            'DATETIME': 'TEXT',
            'TIMESTAMP': 'TEXT'
        }
    
    def get_syntax_rules(self) -> Dict[str, str]:
        return {
            'quote_char': '"',
            'auto_increment': 'AUTOINCREMENT',
            'current_timestamp': "datetime('now')"
        }
    
    def adapt_create_table(self, sql: str) -> str:
        # Converter AUTO_INCREMENT para AUTOINCREMENT
        sql = sql.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
        
        # Converter VARCHAR para TEXT
        sql = re.sub(r'VARCHAR\(\d+\)', 'TEXT', sql, flags=re.IGNORECASE)
        
        # Converter DATETIME/TIMESTAMP para TEXT
        sql = re.sub(r'DATETIME|TIMESTAMP', 'TEXT', sql, flags=re.IGNORECASE)
        
        # Converter aspas
        sql = sql.replace('`', '"')
        
        return sql
    
    def adapt_insert(self, sql: str) -> str:
        # Converter aspas
        sql = sql.replace('`', '"')
        return sql
    
    def get_connection_string_template(self) -> str:
        return "sqlite:///database.db"

class SQLServerAdapter(DatabaseAdapter):
    """Adaptador SQL Server"""
    
    def __init__(self):
        super().__init__('sqlserver')
    
    def get_type_mapping(self) -> Dict[str, str]:
        return {
            'AUTO_INCREMENT': 'IDENTITY(1,1)',
            'TINYINT(1)': 'BIT',
            'TEXT': 'NVARCHAR(MAX)',
            'DATETIME': 'DATETIME2'
        }
    
    def get_syntax_rules(self) -> Dict[str, str]:
        return {
            'quote_char': '[',
            'quote_char_end': ']',
            'auto_increment': 'IDENTITY(1,1)',
            'current_timestamp': 'GETDATE()'
        }
    
    def adapt_create_table(self, sql: str) -> str:
        # Converter AUTO_INCREMENT para IDENTITY
        sql = re.sub(r'(\w+)\s+INT\s+AUTO_INCREMENT', r'\1 INT IDENTITY(1,1)', sql, flags=re.IGNORECASE)
        
        # Converter TINYINT(1) para BIT
        sql = re.sub(r'TINYINT\(1\)', 'BIT', sql, flags=re.IGNORECASE)
        
        # Converter aspas para colchetes
        sql = re.sub(r'`([^`]+)`', r'[\1]', sql)
        
        return sql
    
    def adapt_insert(self, sql: str) -> str:
        # Converter aspas para colchetes
        sql = re.sub(r'`([^`]+)`', r'[\1]', sql)
        return sql
    
    def get_connection_string_template(self) -> str:
        return "mssql+pyodbc://user:password@host:port/database?driver=ODBC+Driver+17+for+SQL+Server"

class MultiDatabaseGenerator:
    """Gerador de SQL para múltiplos bancos"""
    
    def __init__(self):
        self.adapters = {
            'mysql': MySQLAdapter(),
            'postgresql': PostgreSQLAdapter(),
            'sqlite': SQLiteAdapter(),
            'sqlserver': SQLServerAdapter()
        }
    
    def generate_for_all_databases(self, source_sql_file: str, output_dir: str, base_filename: str):
        """Gera SQL para todos os bancos suportados"""
        # Ler SQL original
        with open(source_sql_file, 'r', encoding='utf-8') as f:
            original_sql = f.read()
        
        # Separar CREATE TABLE e INSERTs
        create_section = ""
        insert_section = ""
        
        in_create = False
        for line in original_sql.split('\n'):
            if line.strip().upper().startswith('CREATE TABLE'):
                in_create = True
                create_section += line + '\n'
            elif line.strip().upper().startswith('INSERT INTO'):
                in_create = False
                insert_section += line + '\n'
            elif in_create and line.strip():
                create_section += line + '\n'
            elif not in_create and line.strip():
                insert_section += line + '\n'
        
        # Gerar para cada banco
        results = {}
        for db_type, adapter in self.adapters.items():
            try:
                # Adaptar CREATE TABLE
                adapted_create = adapter.adapt_create_table(create_section)
                
                # Adaptar INSERTs
                adapted_insert = adapter.adapt_insert(insert_section)
                
                # Combinar
                full_sql = self._generate_header(db_type, base_filename)
                full_sql += adapted_create + '\n'
                full_sql += adapted_insert
                full_sql += self._generate_footer(db_type)
                
                # Salvar arquivo
                output_file = os.path.join(output_dir, f"{base_filename}_{db_type}.sql")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_sql)
                
                results[db_type] = {
                    'file': output_file,
                    'status': 'success',
                    'connection_template': adapter.get_connection_string_template()
                }
                
            except Exception as e:
                results[db_type] = {
                    'file': None,
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def _generate_header(self, db_type: str, filename: str) -> str:
        """Gera cabeçalho específico do banco"""
        header = f"""-- ===============================================
-- SQL ADAPTADO PARA {db_type.upper()}
-- Arquivo: {filename}
-- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ===============================================

"""
        
        if db_type == 'mysql':
            header += """-- Configurações MySQL
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

"""
        elif db_type == 'postgresql':
            header += """-- Configurações PostgreSQL
SET client_encoding = 'UTF8';

"""
        elif db_type == 'sqlserver':
            header += """-- Configurações SQL Server
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;

"""
        
        return header
    
    def _generate_footer(self, db_type: str) -> str:
        """Gera rodapé específico do banco"""
        footer = f"""
-- ===============================================
-- FIM DO SCRIPT {db_type.upper()}
-- ===============================================
"""
        
        if db_type == 'mysql':
            footer = """
SET FOREIGN_KEY_CHECKS = 1;
""" + footer
        
        return footer
    
    def generate_connection_examples(self, output_dir: str) -> str:
        """Gera arquivo com exemplos de conexão"""
        examples = """# EXEMPLOS DE CONEXÃO COM BANCOS DE DADOS
# Gerado automaticamente pelo sistema de conversão

"""
        
        for db_type, adapter in self.adapters.items():
            examples += f"""
## {db_type.upper()}

### String de Conexão:
{adapter.get_connection_string_template()}

### Exemplo Python:
```python
# {db_type.upper()}
"""
            
            if db_type == 'mysql':
                examples += """import pymysql
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://user:password@host:port/database')
"""
            elif db_type == 'postgresql':
                examples += """import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@host:port/database')
"""
            elif db_type == 'sqlite':
                examples += """import sqlite3
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')
"""
            elif db_type == 'sqlserver':
                examples += """import pyodbc
from sqlalchemy import create_engine

engine = create_engine('mssql+pyodbc://user:password@host:port/database?driver=ODBC+Driver+17+for+SQL+Server')
"""
            
            examples += "```\n"
        
        # Salvar arquivo
        examples_file = os.path.join(output_dir, "DATABASE_CONNECTIONS.md")
        with open(examples_file, 'w', encoding='utf-8') as f:
            f.write(examples)
        
        return examples_file

def main():
    """Fun��o principal para teste"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Gerador Multi-Banco")
    parser.add_argument('sql_file', help='Arquivo SQL source')
    parser.add_argument('-o', '--output', default='./database_outputs', help='Diret�rio de sa�da')
    
    args = parser.parse_args()
    
    # Criar diret�rio de sa�da
    os.makedirs(args.output, exist_ok=True)
    
    # Gerar para todos os bancos
    generator = MultiDatabaseGenerator()
    
    base_filename = os.path.splitext(os.path.basename(args.sql_file))[0]
    results = generator.generate_for_all_databases(args.sql_file, args.output, base_filename)
    
    # Gerar exemplos de conex�o
    examples_file = generator.generate_connection_examples(args.output)
    
    # Mostrar resultados
    print("=" * 60)
    print("GERA��O MULTI-BANCO CONCLU�DA")
    print("=" * 60)
    
    for db_type, result in results.items():
        if result['status'] == 'success':
            print(f"? {db_type.upper()}: {result['file']}")
        else:
            print(f"? {db_type.upper()}: {result['error']}")
    
    print(f"\n?? Exemplos de conex�o: {examples_file}")
    
    return results

if __name__ == "__main__":
    main()
