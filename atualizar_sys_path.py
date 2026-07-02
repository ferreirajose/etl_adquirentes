#!/usr/bin/env python3
"""
Script para atualizar sys.path em todos os arquivos do projeto
"""
import os
import re

# Padrão antigo
PADRAO_ANTIGO = r"sys\.path\.insert\(0, os\.path\.abspath\(os\.path\.join\(os\.path\.dirname\(__file__\), '\.\.', '\.\.'\)\)\)"

# Novo código
CODIGO_NOVO = """# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)"""

def atualizar_arquivo(filepath):
    """Atualiza um arquivo Python substituindo a configuração do sys.path"""
    with open(filepath, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Verificar se tem o padrão antigo
    if not re.search(PADRAO_ANTIGO, conteudo):
        return False
    
    # Substituir
    conteudo_novo = re.sub(PADRAO_ANTIGO, CODIGO_NOVO, conteudo)
    
    # Salvar
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(conteudo_novo)
    
    return True

# Encontrar todos os arquivos .py em scripts/
scripts_dir = '/home/tce8986/dev/etl_adquirentes/scripts'
arquivos_atualizados = []

for root, dirs, files in os.walk(scripts_dir):
    for filename in files:
        if filename.endswith('.py'):
            filepath = os.path.join(root, filename)
            if atualizar_arquivo(filepath):
                arquivos_atualizados.append(filepath)
                print(f"✓ Atualizado: {filepath}")

print(f"\n✅ Total de arquivos atualizados: {len(arquivos_atualizados)}")
