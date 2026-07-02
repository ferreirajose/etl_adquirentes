#!/usr/bin/env python3
"""
Script para verificar se as correções foram aplicadas corretamente
Executa verificações estáticas nos arquivos Python modificados
"""
import os
import re

def verificar_arquivo(filepath, pattern, descricao):
    """Verifica se um arquivo contém um padrão específico"""
    with open(filepath, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    encontrado = bool(re.search(pattern, conteudo, re.MULTILINE | re.DOTALL))

    status = "✅" if encontrado else "❌"
    print(f"{status} {descricao}")
    print(f"   Arquivo: {os.path.relpath(filepath, '/home/tce8986/dev/etl_adquirentes')}")

    return encontrado

def main():
    base_dir = '/home/tce8986/dev/etl_adquirentes'

    print("="*70)
    print("VERIFICAÇÃO DAS CORREÇÕES IMPLEMENTADAS")
    print("="*70)

    # Contadores
    total_verificacoes = 0
    verificacoes_ok = 0

    # 1. Verificar configuração sys.path em alguns arquivos de amostra
    print("\n1. VERIFICANDO CONFIGURAÇÃO DO SYS.PATH")
    print("-"*70)

    arquivos_amostra = [
        'scripts/cielo/01_transforma_vendas.py',
        'scripts/pagarme/12_agrega_vendas.py',
        'scripts/final/19_consolida_final.py'
    ]

    pattern_syspath = r"project_root_path = '/content/etl_adquirentes'"

    for arquivo in arquivos_amostra:
        filepath = os.path.join(base_dir, arquivo)
        total_verificacoes += 1
        if verificar_arquivo(filepath, pattern_syspath, "Configuração sys.path atualizada"):
            verificacoes_ok += 1

    # 2. Verificar rename de "Número de Parcelas" para "Quantidade de parcelas"
    print("\n2. VERIFICANDO RENAME 'Número de Parcelas' → 'Quantidade de parcelas'")
    print("-"*70)

    arquivos_rename = [
        ('scripts/pagarme/12_agrega_vendas.py', "Vendas Pagar.me"),
        ('scripts/pagarme/15_agrega_estornos.py', "Estornos Pagar.me"),
        ('scripts/pagarme/18_agrega_chargebacks.py', "Chargebacks Pagar.me")
    ]

    pattern_rename = r"'Número de Parcelas':\s*'Quantidade de parcelas'"

    for arquivo, descricao in arquivos_rename:
        filepath = os.path.join(base_dir, arquivo)
        total_verificacoes += 1
        if verificar_arquivo(filepath, pattern_rename, f"Rename em {descricao}"):
            verificacoes_ok += 1

    # 3. Verificar criação da coluna Adquirente
    print("\n3. VERIFICANDO CRIAÇÃO DA COLUNA 'Adquirente'")
    print("-"*70)

    arquivos_adquirente = [
        ('scripts/cielo/05_consolida_estornos.py', "Estornos Cielo", "Cielo"),
        ('scripts/cielo/08_consolida_chargebacks.py', "Chargebacks Cielo", "Cielo"),
        ('scripts/pagarme/14_consolida_estornos.py', "Estornos Pagar.me", "Pagar.me"),
        ('scripts/pagarme/17_consolida_chargebacks.py', "Chargebacks Pagar.me", "Pagar.me")
    ]

    for arquivo, descricao, adquirente in arquivos_adquirente:
        filepath = os.path.join(base_dir, arquivo)
        pattern = rf"merged_df\['Adquirente'\]\s*=\s*'{adquirente}'"
        total_verificacoes += 1
        if verificar_arquivo(filepath, pattern, f"Coluna Adquirente em {descricao}"):
            verificacoes_ok += 1

    # Resumo
    print("\n" + "="*70)
    print("RESUMO DA VERIFICAÇÃO")
    print("="*70)
    print(f"Total de verificações: {total_verificacoes}")
    print(f"Verificações OK: {verificacoes_ok}")
    print(f"Verificações FALHAS: {total_verificacoes - verificacoes_ok}")

    if verificacoes_ok == total_verificacoes:
        print("\n✅ TODAS AS CORREÇÕES FORAM APLICADAS CORRETAMENTE!")
        return 0
    else:
        print(f"\n❌ {total_verificacoes - verificacoes_ok} CORREÇÃO(ÕES) NÃO ENCONTRADA(S)")
        return 1

if __name__ == '__main__':
    exit(main())
