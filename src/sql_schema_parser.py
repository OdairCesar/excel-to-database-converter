#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL Schema Parser for Conversao Project
Parses CREATE TABLE statements to extract field definitions
"""

import re
import os
import sys
from typing import Dict, List, Optional, Tuple

class SQLSchemaParser:
    """Parser for SQL CREATE TABLE statements"""
    
    def __init__(self):
        self.fields = {}
        self.table_name = None
        self.primary_keys = []
        self.indexes = []
        
    def parse_file(self, sql_file_path: str) -> Dict:
        """Parse SQL file and extract table schema"""
        if not os.path.exists(sql_file_path):
            raise FileNotFoundError(f"SQL schema file not found: {sql_file_path}")
            
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        return self.parse_sql(sql_content)
    
    def parse_sql(self, sql_content: str) -> Dict:
        """Parse SQL content and extract schema information"""
        # Clean up SQL content
        sql_content = self._clean_sql(sql_content)
        
        # Extract table name
        self.table_name = self._extract_table_name(sql_content)
        
        # Extract field definitions
        self.fields = self._extract_fields(sql_content)
        
        # Extract primary keys
        self.primary_keys = self._extract_primary_keys(sql_content)
        
        # Extract indexes
        self.indexes = self._extract_indexes(sql_content)
        
        return {
            'table_name': self.table_name,
            'fields': self.fields,
            'primary_keys': self.primary_keys,
            'indexes': self.indexes
        }
    
    def _clean_sql(self, sql_content: str) -> str:
        """Clean and normalize SQL content"""
        # Remove comments
        sql_content = re.sub(r'--.*?$', '', sql_content, flags=re.MULTILINE)
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        
        # Normalize whitespace
        sql_content = re.sub(r'\s+', ' ', sql_content)
        
        return sql_content.strip()
    
    def _extract_table_name(self, sql_content: str) -> str:
        """Extract table name from CREATE TABLE statement"""
        pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?'
        match = re.search(pattern, sql_content, re.IGNORECASE)
        
        if match:
            return match.group(1)
        
        raise ValueError("Could not find table name in SQL")
    
    def _extract_fields(self, sql_content: str) -> Dict:
        """Extract field definitions from CREATE TABLE statement"""
        fields = {}
        
        # Find the CREATE TABLE section - handle nested parentheses
        # First try to find the complete CREATE TABLE statement
        pattern = r'CREATE\s+TABLE[^(]*\((.*)\)\s*;'
        match = re.search(pattern, sql_content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            # Try alternative pattern without semicolon
            pattern = r'CREATE\s+TABLE[^(]*\((.*)\)'
            match = re.search(pattern, sql_content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            raise ValueError("Could not find field definitions in SQL")
        
        fields_section = match.group(1)
        
        # Split by commas, but be careful with function calls
        field_lines = self._smart_split(fields_section)
        
        for line in field_lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip constraints and keys
            if any(keyword in line.upper() for keyword in ['PRIMARY KEY', 'KEY ', 'INDEX', 'CONSTRAINT', 'FOREIGN KEY']):
                continue
            
            field_info = self._parse_field_definition(line)
            if field_info:
                fields[field_info['name']] = field_info
        
        return fields
    
    def _smart_split(self, text: str) -> List[str]:
        """Split by commas, respecting parentheses and quotes"""
        parts = []
        current = ""
        paren_count = 0
        in_quotes = False
        quote_char = None
        
        for char in text:
            if char in ('"', "'", "`") and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == '(' and not in_quotes:
                paren_count += 1
            elif char == ')' and not in_quotes:
                paren_count -= 1
            elif char == ',' and paren_count == 0 and not in_quotes:
                parts.append(current)
                current = ""
                continue
            
            current += char
        
        if current.strip():
            parts.append(current)
        
        return parts
    
    def _parse_field_definition(self, field_def: str) -> Optional[Dict]:
        """Parse individual field definition"""
        field_def = field_def.strip()
        
        # Extract field name (remove backticks)
        name_match = re.match(r'`?(\w+)`?\s+(.+)', field_def)
        if not name_match:
            return None
        
        field_name = name_match.group(1)
        field_spec = name_match.group(2)
        
        # Parse field type
        type_info = self._parse_field_type(field_spec)
        
        # Parse constraints
        constraints = self._parse_field_constraints(field_spec)
        
        return {
            'name': field_name,
            'type': type_info['type'],
            'size': type_info.get('size'),
            'precision': type_info.get('precision'),
            'scale': type_info.get('scale'),
            'nullable': constraints.get('nullable', True),
            'default': constraints.get('default'),
            'auto_increment': constraints.get('auto_increment', False),
            'enum_values': type_info.get('enum_values'),
            'original_definition': field_def
        }
    
    def _parse_field_type(self, field_spec: str) -> Dict:
        """Parse field type and size information"""
        type_info = {}
        
        # Handle SET and ENUM types specially
        if field_spec.upper().startswith('SET(') or field_spec.upper().startswith('ENUM('):
            # Extract SET/ENUM type and values
            set_enum_match = re.match(r'(SET|ENUM)\(([^)]+)\)', field_spec, re.IGNORECASE)
            if set_enum_match:
                type_info['type'] = set_enum_match.group(1).upper()
                values_str = set_enum_match.group(2)
                # Parse values, handling quotes
                values = []
                current_value = ""
                in_quotes = False
                quote_char = None
                
                for char in values_str:
                    if char in ('"', "'") and not in_quotes:
                        in_quotes = True
                        quote_char = char
                    elif char == quote_char and in_quotes:
                        in_quotes = False
                        quote_char = None
                        values.append(current_value)
                        current_value = ""
                    elif char == ',' and not in_quotes:
                        if current_value:
                            values.append(current_value)
                        current_value = ""
                    elif in_quotes:
                        current_value += char
                
                if current_value:
                    values.append(current_value)
                
                type_info['enum_values'] = values
                return type_info
        
        # Extract base type with size/precision
        type_pattern = r'(\w+)(?:\(([^)]+)\))?'
        match = re.match(type_pattern, field_spec)
        
        if match:
            type_info['type'] = match.group(1).upper()
            size_spec = match.group(2)
            
            if size_spec:
                # Handle ENUM values (fallback)
                if type_info['type'].upper() == 'ENUM':
                    enum_values = [v.strip("'\"") for v in size_spec.split(',')]
                    type_info['enum_values'] = enum_values
                # Handle decimal precision
                elif ',' in size_spec:
                    try:
                        precision, scale = size_spec.split(',', 1)
                        type_info['precision'] = int(precision.strip())
                        type_info['scale'] = int(scale.strip())
                    except ValueError:
                        type_info['size'] = size_spec
                # Handle regular size
                else:
                    try:
                        type_info['size'] = int(size_spec)
                    except ValueError:
                        type_info['size'] = size_spec
        else:
            # Fallback - extract just the type name
            type_name = field_spec.split()[0]
            type_info['type'] = type_name.upper()
        
        return type_info
    
    def _parse_field_constraints(self, field_spec: str) -> Dict:
        """Parse field constraints (NULL, DEFAULT, AUTO_INCREMENT, etc.)"""
        constraints = {}
        
        # Check for NOT NULL
        constraints['nullable'] = 'NOT NULL' not in field_spec.upper()
        
        # Check for AUTO_INCREMENT
        constraints['auto_increment'] = 'AUTO_INCREMENT' in field_spec.upper()
        
        # Extract DEFAULT value
        default_match = re.search(r'DEFAULT\s+([^,\s]+|\'[^\']*\'|"[^"]*")', field_spec, re.IGNORECASE)
        if default_match:
            default_value = default_match.group(1)
            if default_value.upper() == 'NULL':
                constraints['default'] = None
            elif default_value.startswith(("'", '"')):
                constraints['default'] = default_value[1:-1]  # Remove quotes
            else:
                constraints['default'] = default_value
        
        return constraints
    
    def _extract_primary_keys(self, sql_content: str) -> List[str]:
        """Extract primary key fields"""
        primary_keys = []
        
        # Look for PRIMARY KEY definition
        pk_pattern = r'PRIMARY\s+KEY\s*\(([^)]+)\)'
        match = re.search(pk_pattern, sql_content, re.IGNORECASE)
        
        if match:
            pk_fields = match.group(1)
            # Split and clean field names
            for field in pk_fields.split(','):
                field = field.strip().strip('`"\'')
                primary_keys.append(field)
        
        return primary_keys
    
    def _extract_indexes(self, sql_content: str) -> List[Dict]:
        """Extract index definitions"""
        indexes = []
        
        # Look for KEY/INDEX definitions
        index_pattern = r'(?:KEY|INDEX)\s+`?(\w+)`?\s*\(([^)]+)\)'
        matches = re.finditer(index_pattern, sql_content, re.IGNORECASE)
        
        for match in matches:
            index_name = match.group(1)
            index_fields = [f.strip().strip('`"\'') for f in match.group(2).split(',')]
            
            indexes.append({
                'name': index_name,
                'fields': index_fields
            })
        
        return indexes
    
    def get_field_names(self) -> List[str]:
        """Get list of field names"""
        return list(self.fields.keys())
    
    def get_field_info(self, field_name: str) -> Optional[Dict]:
        """Get information for specific field"""
        return self.fields.get(field_name)
    
    def is_required_field(self, field_name: str) -> bool:
        """Check if field is required (NOT NULL and no default)"""
        field_info = self.get_field_info(field_name)
        if not field_info:
            return False
        
        return not field_info['nullable'] and field_info.get('default') is None
    
    def get_field_type(self, field_name: str) -> Optional[str]:
        """Get field type"""
        field_info = self.get_field_info(field_name)
        return field_info['type'] if field_info else None
    
    def export_summary(self) -> str:
        """Export schema summary"""
        summary = []
        summary.append(f"Table: {self.table_name}")
        summary.append(f"Fields: {len(self.fields)}")
        summary.append(f"Primary Keys: {', '.join(self.primary_keys)}")
        summary.append("")
        
        for field_name, field_info in self.fields.items():
            type_str = field_info['type']
            if field_info.get('size'):
                type_str += f"({field_info['size']})"
            elif field_info.get('precision'):
                type_str += f"({field_info['precision']},{field_info['scale']})"
            
            null_str = "NOT NULL" if not field_info['nullable'] else "NULL"
            default_str = f"DEFAULT {field_info['default']}" if field_info.get('default') else ""
            
            summary.append(f"  {field_name}: {type_str} {null_str} {default_str}".strip())
        
        return "\n".join(summary)

def main():
    """Test the parser with a SQL file"""
    if len(sys.argv) != 2:
        print("Usage: python sql_schema_parser.py <sql_file>")
        sys.exit(1)
    
    sql_file = sys.argv[1]
    parser = SQLSchemaParser()
    
    try:
        schema = parser.parse_file(sql_file)
        print(parser.export_summary())
    except Exception as e:
        print(f"Error parsing SQL file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
