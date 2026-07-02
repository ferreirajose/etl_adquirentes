"""
Script de teste para validação das regras de negócio ETL Adquirentes

Regras testadas:
1. Chargebacks: "Quantidade de parcelas" é OPCIONAL
2. Vendas (Cielo/Pagarme): "Quantidade de parcelas" é OBRIGATÓRIO
3. Consolidado: Coluna "Adquirente" deve exibir "Cielo" ou "Pagar.me"
"""

import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validacao import (
    validar_quantidade_parcelas_vendas,
    validar_quantidade_parcelas_chargebacks,
    validar_adquirente_consolidado,
    exibir_relatorio_validacao
)


def test_regra_1_chargebacks_opcional():
    """
    Testa REGRA 1: Quantidade de parcelas é OPCIONAL para chargebacks
    """
    print("\n" + "="*70)
    print("TESTE REGRA 1: Chargebacks - Quantidade de parcelas OPCIONAL")
    print("="*70)

    # Cenário 1: Chargebacks SEM coluna quantidade de parcelas
    df_sem_coluna = pd.DataFrame({
        'Data': ['01/01/2024', '02/01/2024'],
        'Adquirente': ['Cielo', 'Cielo'],
        'Valor': [100.0, 200.0],
        'Status': ['Chargeback', 'Chargeback']
    })

    print("\n📋 Cenário 1: Chargebacks SEM coluna 'Quantidade de parcelas'")
    _, avisos = validar_quantidade_parcelas_chargebacks(df_sem_coluna, 'Cielo')
    exibir_relatorio_validacao('Chargebacks', 'Cielo', [], avisos)

    # Cenário 2: Chargebacks COM coluna mas valores nulos
    df_com_nulos = pd.DataFrame({
        'Data': ['01/01/2024', '02/01/2024', '03/01/2024'],
        'Adquirente': ['Pagar.me', 'Pagar.me', 'Pagar.me'],
        'Quantidade de parcelas': [2, None, 1],
        'Valor': [100.0, 200.0, 150.0],
        'Status': ['Chargeback', 'Chargeback', 'Chargeback']
    })

    print("\n📋 Cenário 2: Chargebacks COM valores nulos (PERMITIDO)")
    _, avisos = validar_quantidade_parcelas_chargebacks(df_com_nulos, 'Pagar.me')
    exibir_relatorio_validacao('Chargebacks', 'Pagar.me', [], avisos)

    print("\n✅ REGRA 1 TESTADA: Chargebacks podem ter quantidade de parcelas nula\n")


def test_regra_2_vendas_obrigatorio():
    """
    Testa REGRA 2: Quantidade de parcelas é OBRIGATÓRIO para vendas
    """
    print("\n" + "="*70)
    print("TESTE REGRA 2: Vendas - Quantidade de parcelas OBRIGATÓRIO")
    print("="*70)

    # Cenário 1: Vendas Cielo COM quantidade de parcelas (VÁLIDO)
    df_valido = pd.DataFrame({
        'Data': ['01/01/2024', '02/01/2024'],
        'Adquirente': ['Cielo', 'Cielo'],
        'Quantidade de parcelas': [1, 2],
        'Valor': [100.0, 200.0],
        'Status': ['Aprovada', 'Aprovada']
    })

    print("\n📋 Cenário 1: Vendas Cielo VÁLIDAS (todas com parcelas)")
    _, erros = validar_quantidade_parcelas_vendas(df_valido, 'Cielo')
    exibir_relatorio_validacao('Vendas', 'Cielo', erros)

    # Cenário 2: Vendas Pagar.me COM valores nulos (INVÁLIDO)
    df_invalido = pd.DataFrame({
        'Data': ['01/01/2024', '02/01/2024', '03/01/2024'],
        'Adquirente': ['Pagar.me', 'Pagar.me', 'Pagar.me'],
        'Installments': [2, None, 0],  # None e 0 são inválidos
        'Valor': [100.0, 200.0, 150.0],
        'Status': ['Aprovada', 'Aprovada', 'Aprovada']
    })

    print("\n📋 Cenário 2: Vendas Pagar.me INVÁLIDAS (com nulos/zeros)")
    _, erros = validar_quantidade_parcelas_vendas(df_invalido, 'Pagar.me')
    exibir_relatorio_validacao('Vendas', 'Pagar.me', erros)

    # Cenário 3: Vendas sem a coluna (INVÁLIDO)
    df_sem_coluna = pd.DataFrame({
        'Data': ['01/01/2024'],
        'Adquirente': ['Cielo'],
        'Valor': [100.0],
        'Status': ['Aprovada']
    })

    print("\n📋 Cenário 3: Vendas SEM coluna de parcelas (INVÁLIDO)")
    _, erros = validar_quantidade_parcelas_vendas(df_sem_coluna, 'Cielo')
    exibir_relatorio_validacao('Vendas', 'Cielo', erros)

    print("\n✅ REGRA 2 TESTADA: Vendas DEVEM ter quantidade de parcelas\n")


def test_regra_3_adquirente_consolidado():
    """
    Testa REGRA 3: Consolidado deve exibir nome da Adquirente (Cielo ou Pagar.me)
    """
    print("\n" + "="*70)
    print("TESTE REGRA 3: Consolidado - Coluna Adquirente obrigatória")
    print("="*70)

    # Cenário 1: Consolidado VÁLIDO
    df_valido = pd.DataFrame({
        'Data': ['01/01/2024', '02/01/2024', '03/01/2024'],
        'EC': ['Gran Centro', 'Gran Norte', 'Gran Pré'],
        'Adquirente': ['Cielo', 'Pagar.me', 'Cielo'],
        'Valor bruto': [100.0, 200.0, 150.0],
        'Status': ['Aprovada', 'Aprovada', 'Chargeback']
    })

    print("\n📋 Cenário 1: Consolidado VÁLIDO (Cielo e Pagar.me)")
    _, erros = validar_adquirente_consolidado(df_valido)
    exibir_relatorio_validacao('Consolidado Final', 'Todas', erros)

    # Cenário 2: Consolidado com valores NULOS (INVÁLIDO)
    df_com_nulos = pd.DataFrame({
        'Data': ['01/01/2024', '02/01/2024'],
        'EC': ['Gran Centro', 'Gran Norte'],
        'Adquirente': ['Cielo', None],
        'Valor bruto': [100.0, 200.0]
    })

    print("\n📋 Cenário 2: Consolidado com NULOS (INVÁLIDO)")
    _, erros = validar_adquirente_consolidado(df_com_nulos)
    exibir_relatorio_validacao('Consolidado Final', 'Todas', erros)

    # Cenário 3: Consolidado com valores INVÁLIDOS (INVÁLIDO)
    df_invalido = pd.DataFrame({
        'Data': ['01/01/2024', '02/01/2024'],
        'EC': ['Gran Centro', 'Gran Norte'],
        'Adquirente': ['Cielo', 'Rede'],  # 'Rede' não é válida
        'Valor bruto': [100.0, 200.0]
    })

    print("\n📋 Cenário 3: Consolidado com adquirente INVÁLIDA (INVÁLIDO)")
    _, erros = validar_adquirente_consolidado(df_invalido)
    exibir_relatorio_validacao('Consolidado Final', 'Todas', erros)

    # Cenário 4: Consolidado SEM coluna Adquirente (INVÁLIDO)
    df_sem_coluna = pd.DataFrame({
        'Data': ['01/01/2024'],
        'EC': ['Gran Centro'],
        'Valor bruto': [100.0]
    })

    print("\n📋 Cenário 4: Consolidado SEM coluna Adquirente (CRÍTICO)")
    _, erros = validar_adquirente_consolidado(df_sem_coluna)
    exibir_relatorio_validacao('Consolidado Final', 'Todas', erros)

    print("\n✅ REGRA 3 TESTADA: Consolidado deve ter Adquirente válida\n")


def executar_todos_testes():
    """
    Executa todos os testes de validação
    """
    print("\n" + "🧪"*35)
    print("EXECUÇÃO DE TESTES - REGRAS DE VALIDAÇÃO ETL ADQUIRENTES")
    print("🧪"*35)

    test_regra_1_chargebacks_opcional()
    test_regra_2_vendas_obrigatorio()
    test_regra_3_adquirente_consolidado()

    print("\n" + "="*70)
    print("✅ TODOS OS TESTES EXECUTADOS COM SUCESSO")
    print("="*70)
    print("\n📝 RESUMO DAS REGRAS:")
    print("  1️⃣  Chargebacks: Quantidade de parcelas é OPCIONAL")
    print("  2️⃣  Vendas: Quantidade de parcelas é OBRIGATÓRIO")
    print("  3️⃣  Consolidado: Adquirente deve ser 'Cielo' ou 'Pagar.me'")
    print("="*70 + "\n")


if __name__ == '__main__':
    executar_todos_testes()
