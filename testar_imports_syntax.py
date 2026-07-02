#!/usr/bin/env python3
"""
Script de teste para validar SINTAXE dos imports (não executa código que usa pandas)
"""

import sys
import os
import ast

# Adicionar raiz do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

print("="*60)
print("TESTE DE SINTAXE DE IMPORTS")
print("="*60)

def testar_syntax_arquivo(arquivo):
    """Testa se um arquivo Python tem sintaxe válida"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        ast.parse(codigo)
        return True, None
    except SyntaxError as e:
        return False, str(e)

# Teste 1: Arquivos utils
print("\n1. Testando sintaxe dos arquivos utils...")
arquivos_utils = [
    'utils/__init__.py',
    'utils/mappings.py',
    'utils/transformacoes.py',
    'utils/normalizacao.py',
    'utils/agregacao.py',
    'utils/leitura_arquivos.py'
]

todos_ok = True
for arquivo in arquivos_utils:
    ok, erro = testar_syntax_arquivo(arquivo)
    status = "✓" if ok else "✗"
    print(f"   {status} {arquivo}")
    if not ok:
        print(f"      Erro: {erro}")
        todos_ok = False

if not todos_ok:
    print("\n✗ Erros de sintaxe encontrados!")
    sys.exit(1)

# Teste 2: Verificar exports no __init__.py
print("\n2. Verificando exports em utils/__init__.py...")
try:
    with open('utils/__init__.py', 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Verificar imports
    imports_esperados = [
        'from .mappings import',
        'from .transformacoes import',
        'from .normalizacao import',
        'from .agregacao import',
        'from .leitura_arquivos import'
    ]

    for imp in imports_esperados:
        if imp in conteudo:
            print(f"   ✓ {imp}")
        else:
            print(f"   ✗ Faltando: {imp}")
            todos_ok = False

    # Verificar __all__
    if '__all__' in conteudo:
        print("   ✓ __all__ definido")
    else:
        print("   ✗ __all__ não encontrado")
        todos_ok = False

except Exception as e:
    print(f"   ✗ Erro ao ler arquivo: {e}")
    todos_ok = False

# Teste 3: Verificar imports nos scripts
print("\n3. Testando imports nos scripts de transformação...")
scripts = [
    'scripts/cielo/01_transforma_vendas.py',
    'scripts/cielo/04_transforma_estornos.py',
    'scripts/cielo/07_transforma_chargebacks.py',
    'scripts/pagarme/10_transforma_vendas.py',
    'scripts/pagarme/13_transforma_estornos.py',
    'scripts/pagarme/16_transforma_chargebacks.py'
]

for script in scripts:
    try:
        with open(script, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Verificar imports necessários
        tem_leitura = 'from utils.leitura_arquivos import' in conteudo
        tem_sys_path = 'sys.path.insert' in conteudo

        if tem_leitura and tem_sys_path:
            print(f"   ✓ {os.path.basename(script)}")
        else:
            print(f"   ⚠ {os.path.basename(script)}")
            if not tem_leitura:
                print(f"      Faltando: import de leitura_arquivos")
            if not tem_sys_path:
                print(f"      Faltando: sys.path.insert")

    except Exception as e:
        print(f"   ✗ {os.path.basename(script)}: {e}")
        todos_ok = False

# Teste 4: Arquivos de configuração
print("\n4. Verificando arquivos de configuração...")
configs = [
    ('pyrightconfig.json', 'Pyright'),
    ('.vscode/settings.json', 'VS Code')
]

for arquivo, nome in configs:
    if os.path.exists(arquivo):
        print(f"   ✓ {nome} ({arquivo})")
    else:
        print(f"   ✗ {nome} ({arquivo}) não encontrado")

# Resumo
print("\n" + "="*60)
print("RESULTADO")
print("="*60)

if todos_ok:
    print("✅ Sintaxe de todos os arquivos está correta!")
    print("\nPróximos passos:")
    print("  1. Recarregar VS Code: Ctrl+Shift+P > 'Developer: Reload Window'")
    print("  2. Verificar se os erros de import sumiram")
    print("  3. Testar autocomplete: digite 'from utils.mappings import'")
    print("\nNota: O erro 'No module named pandas' é normal neste ambiente.")
    print("      Os imports funcionarão corretamente no Colab ou em produção.")
else:
    print("⚠️ Alguns problemas foram encontrados")
    print("\nVerifique os itens marcados com ✗ acima")

print("="*60)

sys.exit(0 if todos_ok else 1)
