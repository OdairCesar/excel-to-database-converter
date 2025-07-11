# Sistema de Conversão Universal - Excel para Banco de Dados

🚀 **Sistema completo de conversão de Excel para múltiplos bancos de dados com validação automática**

## 🔥 Recursos Principais

- 🔄 **Conversão Universal**: Excel → CSV + SQL + XLSX (sempre!)
- 📄 **Modo XLSX-Only**: Apenas arquivo XLSX corrigido (pula CSV/SQL)
- 🗄️ **Multi-Banco**: MySQL, PostgreSQL, SQLite, SQL Server
- 📋 **Schemas Personalizados**: Suporte a CREATE TABLE externos
- ✅ **Validação Automática**: Verificação completa de dados
- 🧹 **Limpeza Automática**: Remove .0 indesejados, NaN, valores vazios
- ✂️ **Truncamento Automático**: Ajusta strings aos limites do schema
- 🌐 **Multiplataforma**: Windows, macOS, Linux
- 💻 **Modo Interativo**: Interface amigável

## 🚀 Instalação Rápida

```bash
# 1. Executar instalação automática
python setup.py

# 2. Teste rápido
python test_final.py

# 3. Conversão personalizada
python main_converter.py convert seu_arquivo.xlsx --schema schemas/seu_schema.sql
```

## 📦 Dependências

```bash
pip install pandas openpyxl sqlalchemy pymysql psycopg2-binary pyodbc
```

## 🎯 Uso Básico

### Conversão Simples
```bash
# Usando schema padrão
python main_converter.py convert dados.xlsx

# Usando schema personalizado
python main_converter.py convert dados.xlsx --schema schemas/produtos.sql
```

### Conversão com Validação
```bash
python main_converter.py validate dados.xlsx --schema schemas/clientes.sql --verbose
```

### Workflow Completo
```bash
python main_converter.py complete dados.xlsx --schema schemas/vendas.sql
```

### Modo Interativo
```bash
python main_converter.py interactive
```

## 🗄️ Schemas Suportados

### MySQL
```sql
CREATE TABLE produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2),
    categoria VARCHAR(100),
    ativo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### PostgreSQL
```sql
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2),
    categoria VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### SQLite
```sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL,
    categoria TEXT,
    ativo INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 📁 Estrutura do Projeto

```
conversao_cadastro/
├── src/                          # Código fonte
│   ├── convert_excel_universal_clean.py  # Conversor principal
│   ├── sql_schema_parser.py              # Parser de schemas SQL
│   ├── validation_system.py              # Sistema de validação
│   └── multi_database_generator.py       # Gerador multi-banco
├── schemas/                      # Schemas SQL de exemplo
│   ├── exemplo_clientes.sql
│   ├── produtos.sql
│   └── default_cadastro.sql
├── examples/                     # Arquivos de exemplo
│   └── exemplo_dados.xlsx
├── scripts/                      # Scripts auxiliares
├── docs/                         # Documentação
├── conversao_output/            # Arquivos gerados
├── main_converter.py            # Script principal
├── test_final.py               # Teste do sistema
├── setup.py                    # Instalação automática
└── README.md                   # Esta documentação
```

## 🔧 Comandos Disponíveis

### Conversão
```bash
# Conversão completa (CSV + SQL + XLSX)
python main_converter.py convert arquivo.xlsx

# Com schema personalizado
python main_converter.py convert arquivo.xlsx --schema schemas/produtos.sql

# Com saída personalizada
python main_converter.py convert arquivo.xlsx -o ./minha_saida --verbose

# Apenas XLSX corrigido (pula CSV/SQL)
python main_converter.py convert arquivo.xlsx --xlsx-only

# XLSX com schema personalizado
python main_converter.py convert arquivo.xlsx --schema schemas/produtos.sql --xlsx-only
```

### Validação
```bash
# Validação completa
python main_converter.py validate arquivo.xlsx --schema schemas/clientes.sql

# Validação verbose
python main_converter.py validate arquivo.xlsx --verbose
```

### Multi-Banco
```bash
# Gerar SQL para todos os bancos
python main_converter.py multi arquivo_inserts.sql

# Com diretório personalizado
python main_converter.py multi arquivo_inserts.sql -o ./multi_outputs
```

### Workflow Completo
```bash
# Conversão + Validação + Multi-Banco (gera CSV + SQL + XLSX)
python main_converter.py complete arquivo.xlsx --schema schemas/vendas.sql

# Workflow apenas XLSX (sem multi-banco)
python main_converter.py complete arquivo.xlsx --xlsx-only
```

## 📊 Exemplos de Saída

### CSV Gerado
```csv
nome,email,telefone,cidade,ativo,created_at
Joao Silva,joao@email.com,11999999999,Sao Paulo,1,2025-07-11 15:27:50
Maria Santos,maria@email.com,11888888888,Rio de Janeiro,1,2025-07-11 15:27:50
```

### SQL Gerado
```sql
-- Conversao de exemplo_dados.xlsx
-- Registros: 4
-- Gerado em: 2025-07-11 15:27:50
-- Tabela: clientes

CREATE TABLE IF NOT EXISTS `clientes` (
  `nome` VARCHAR(255) NOT NULL,
  `email` VARCHAR(100),
  `telefone` VARCHAR(20),
  `cidade` VARCHAR(100),
  `ativo` TINYINT(1) DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO `clientes` (`nome`, `email`, `telefone`, `cidade`, `ativo`, `created_at`) 
VALUES ('Joao Silva', 'joao@email.com', '11999999999', 'Sao Paulo', 1, '2025-07-11 15:27:50');
```

### 🆕 XLSX Corrigido (--xlsx-only)
```
arquivo_corrigido.xlsx
├── Informações do cabeçalho:
│   ├── Arquivo Original: exemplo_dados.xlsx
│   ├── Registros: 4
│   └── Gerado em: 2025-07-11 15:27:50
├── Dados limpos:
│   ├── Campos de texto sem .0 (ex: "11.0" → "11")
│   ├── Valores NaN/None removidos
│   ├── SET/ENUM tratados como strings
│   └── Tipos de dados corretos
└── Formatação:
    ├── Cabeçalhos formatados (negrito, cor)
    ├── Colunas com largura automática
    └── Planilha "Dados Corrigidos"
```

## 🗃️ Bancos Suportados

| Banco | Status | Características |
|-------|--------|----------------|
| **MySQL** | ✅ Completo | AUTO_INCREMENT, ENGINE=InnoDB |
| **PostgreSQL** | ✅ Completo | SERIAL, tipos nativos |
| **SQLite** | ✅ Completo | AUTOINCREMENT, tipos flexíveis |
| **SQL Server** | ✅ Completo | IDENTITY, tipos específicos |

## 🔍 Validação Automática

O sistema inclui validação completa que verifica:

- ✅ Arquivo Excel válido e legível
- ✅ Schema SQL correto e parseável
- ✅ Mapeamento de campos Excel → SQL
- ✅ Tipos de dados compatíveis
- ✅ Geração correta de arquivos
- ✅ Sintaxe SQL válida

## 💻 Modo Interativo

Execute `python main_converter.py interactive` para usar o modo interativo:

```
🚀  MODO INTERATIVO

📊 Arquivo Excel: examples/exemplo_dados.xlsx

📋 Schemas disponíveis:
   0. Schema padrão
   1. schemas/exemplo_clientes.sql
   2. schemas/produtos.sql

Escolha um schema (0-2): 1

🔧 Modos disponíveis:
   1. Conversão simples
   2. Conversão + Validação
   3. Workflow completo

Escolha o modo (1-3): 3
```

## 💡 Casos de Uso

### 1. Migração de Dados
```bash
# Converter planilha de clientes para MySQL
python main_converter.py convert clientes.xlsx --schema schemas/clientes_mysql.sql
```

### 2. Desenvolvimento Multi-Banco
```bash
# Gerar SQL para todos os bancos
python main_converter.py complete produtos.xlsx --schema schemas/produtos.sql
```

### 3. Validação de Dados
```bash
# Validar dados antes da importação
python main_converter.py validate vendas.xlsx --schema schemas/vendas.sql --verbose
```

### 4. Automação de Pipeline
```bash
# Processar múltiplos arquivos
for file in *.xlsx; do
    python main_converter.py convert "$file" --schema schemas/padrao.sql
done
```

## ⚡ Performance

- **Arquivos pequenos** (< 1MB): ~1-2 segundos
- **Arquivos médios** (1-10MB): ~5-15 segundos  
- **Arquivos grandes** (10-100MB): ~30-120 segundos

## 🛠️ Personalização

### Criar Schema Personalizado
```sql
-- schemas/meu_schema.sql
CREATE TABLE minha_tabela (
    id INT PRIMARY KEY AUTO_INCREMENT,
    campo1 VARCHAR(100) NOT NULL,
    campo2 DECIMAL(10,2),
    campo3 TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Usar Schema Personalizado
```bash
python main_converter.py convert meus_dados.xlsx --schema schemas/meu_schema.sql
```

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de dependência**
   ```bash
   pip install pandas openpyxl sqlalchemy
   ```

2. **Arquivo Excel não encontrado**
   ```bash
   # Verificar caminho
   ls -la meu_arquivo.xlsx
   ```

3. **Schema SQL inválido**
   ```bash
   # Validar schema
   python main_converter.py validate arquivo.xlsx --schema schemas/schema.sql --verbose
   ```

4. **Encoding de caracteres**
   ```bash
   # Usar UTF-8
   python main_converter.py convert arquivo.xlsx --verbose
   ```

## 📚 Documentação Adicional

- **Schemas**: Veja `schemas/` para exemplos
- **Testes**: Execute `python test_final.py`
- **Logs**: Use `--verbose` para debug
- **Exemplos**: Veja `examples/` para casos de uso

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/conversao-universal/issues)
- **Wiki**: [GitHub Wiki](https://github.com/seu-usuario/conversao-universal/wiki)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/conversao-universal/discussions)

## 📝 Changelog

### v1.0.0 (2025-07-11)
- ✅ Conversão universal Excel → SQL
- ✅ Suporte a múltiplos bancos de dados
- ✅ Parser de schemas SQL externos
- ✅ Sistema de validação automática
- ✅ Modo interativo
- ✅ Scripts multiplataforma
- ✅ Documentação completa

---

⭐ **Se este projeto te ajudou, considere dar uma estrela no GitHub!**

🚀 **Pronto para converter seus dados? Execute `python main_converter.py --help` para começar!**
