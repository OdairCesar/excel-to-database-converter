#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup Script - Excel to Database Conversion System
"""

import os
import sys
import platform
import subprocess
import json

def show_banner():
    print("=" * 70)
    print("  EXCEL TO DATABASE CONVERSION SYSTEM - SETUP")
    print("=" * 70)
    print("  ?? Automatic configuration")
    print("  ?? Install dependencies")
    print("  ?? Environment setup")
    print("=" * 70)
    print()

def check_python():
    version = sys.version_info
    print(f"?? Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("? Python 3.7+ required!")
        return False
    
    print("? Python version OK")
    return True

def install_deps():
    deps = [
        'pandas>=1.3.0',
        'openpyxl>=3.0.0',
        'sqlalchemy>=1.4.0'
    ]
    
    print("?? Installing dependencies...")
    
    for dep in deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          capture_output=True, check=True)
            print(f"   ? {dep}")
        except subprocess.CalledProcessError:
            print(f"   ??  {dep} - Error")
    
    print("? Dependencies installed")

def create_structure():
    print("?? Creating directories...")
    
    dirs = [
        'src', 'schemas', 'scripts', 'docs', 'examples', 
        'tests', 'output', 'conversao_output', 'temp'
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"   ? {directory}/")
    
    print("? Structure created")

def create_config():
    print("??  Creating config file...")
    
    config = {
        "version": "1.0.0",
        "default_output_dir": "./conversao_output",
        "encoding": "utf-8",
        "supported_databases": ["mysql", "postgresql", "sqlite", "sqlserver"]
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print("? Config created: config.json")

def create_examples():
    print("?? Creating example files...")
    
    # Example data
    example_data = """nome,email,telefone,cidade
Joao Silva,joao@email.com,11999999999,Sao Paulo
Maria Santos,maria@email.com,11888888888,Rio de Janeiro
Pedro Oliveira,pedro@email.com,11777777777,Belo Horizonte
Ana Costa,ana@email.com,11666666666,Salvador
"""
    
    with open('examples/exemplo_dados.csv', 'w', encoding='utf-8') as f:
        f.write(example_data)
    
    # Convert to Excel
    try:
        import pandas as pd
        df = pd.read_csv('examples/exemplo_dados.csv')
        df.to_excel('examples/exemplo_dados.xlsx', index=False)
        print("? Example Excel: examples/exemplo_dados.xlsx")
    except ImportError:
        print("??  Pandas not available for Excel example")
    
    # Example schema
    example_schema = """-- Example schema for clients
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20),
    cidade VARCHAR(100),
    ativo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
    
    with open('schemas/exemplo_clientes.sql', 'w', encoding='utf-8') as f:
        f.write(example_schema)
    
    print("? Example schema: schemas/exemplo_clientes.sql")

def run_tests():
    print("?? Running basic tests...")
    
    try:
        import pandas as pd
        import openpyxl
        print("? Imports OK")
        
        df = pd.DataFrame({'nome': ['Test'], 'valor': [123]})
        print("? DataFrame OK")
        
        df.to_excel('temp/test.xlsx', index=False)
        print("? Excel write OK")
        
        df2 = pd.read_excel('temp/test.xlsx')
        print("? Excel read OK")
        
        os.remove('temp/test.xlsx')
        print("? Basic tests passed")
        return True
        
    except Exception as e:
        print(f"? Test error: {e}")
        return False

def show_final():
    print()
    print("=" * 70)
    print("  ? SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("?? NEXT STEPS:")
    print()
    print("1. Quick test:")
    print("   python main_converter.py convert examples/exemplo_dados.xlsx")
    print()
    print("2. Interactive mode:")
    print("   python main_converter.py interactive")
    print()
    print("3. Full help:")
    print("   python main_converter.py --help")
    print()
    print("?? Documentation: README.md")
    print("?? Examples: examples/")
    print("?? Config: config.json")
    print()
    print("=" * 70)

def main():
    show_banner()
    
    print(f"???  System: {platform.system()} {platform.release()}")
    print(f"?? Directory: {os.getcwd()}")
    print()
    
    if not check_python():
        return 1
    
    try:
        install_deps()
        create_structure()
        create_config()
        create_examples()
        
        if run_tests():
            show_final()
            return 0
        else:
            print("??  Setup complete but with test errors")
            return 1
            
    except Exception as e:
        print(f"? Setup error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
