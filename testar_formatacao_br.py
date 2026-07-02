#!/usr/bin/env python3
"""
Script de teste para validar formatação brasileira
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.normalizacao import formatar_data_br, formatar_moeda_br
import pandas as pd


def testar_formatacao_datas():
    """Testa formatação de datas"""
    print("="*60)
    print("TESTE: Formatação de Datas (DD/MM/YYYY)")
    print("="*60)

    testes_data = [
        ('2026-06-04', '04/06/2026'),
        ('2026-01-15', '15/01/2026'),
        ('04/06/2026', '04/06/2026'),
        ('2025-12-31', '31/12/2025'),
        ('', ''),
        (None, ''),
    ]

    sucesso = 0
    falhas = 0

    for entrada, esperado in testes_data:
        resultado = formatar_data_br(entrada)
        status = "✓" if resultado == esperado else "✗"

        if resultado == esperado:
            sucesso += 1
        else:
            falhas += 1

        print(f"{status} '{entrada}' → '{resultado}' (esperado: '{esperado}')")

    print(f"\nResultado: {sucesso} sucessos, {falhas} falhas\n")
    return falhas == 0


def testar_formatacao_moeda():
    """Testa formatação de moeda"""
    print("="*60)
    print("TESTE: Formatação de Moeda (R$ 1.234,56)")
    print("="*60)

    testes_moeda = [
        (1.0, 'R$ 1,00'),
        (10.0, 'R$ 10,00'),
        (100.0, 'R$ 100,00'),
        (1000.0, 'R$ 1.000,00'),
        (1234.56, 'R$ 1.234,56'),
        (10000.99, 'R$ 10.000,99'),
        (123456.78, 'R$ 123.456,78'),
        (0.5, 'R$ 0,50'),
        (0.0, 'R$ 0,00'),
        (None, 'R$ 0,00'),
    ]

    sucesso = 0
    falhas = 0

    for entrada, esperado in testes_moeda:
        resultado = formatar_moeda_br(entrada)
        status = "✓" if resultado == esperado else "✗"

        if resultado == esperado:
            sucesso += 1
        else:
            falhas += 1

        print(f"{status} {entrada} → '{resultado}' (esperado: '{esperado}')")

    print(f"\nResultado: {sucesso} sucessos, {falhas} falhas\n")
    return falhas == 0


def testar_dataframe():
    """Testa formatação em DataFrame"""
    print("="*60)
    print("TESTE: Formatação em DataFrame")
    print("="*60)

    from utils.normalizacao import formatar_colunas_data_br, formatar_colunas_moeda_br

    # Criar DataFrame de teste
    df = pd.DataFrame({
        'Data': ['2026-06-04', '2026-01-15', '2025-12-31'],
        'Valor bruto': [1234.56, 10000.0, 500.50],
        'Valor líquido': [1000.00, 9500.00, 475.00],
        'Status': ['Aprovada', 'Aprovada', 'Estornada']
    })

    print("\nDataFrame ANTES:")
    print(df.to_string(index=False))

    # Aplicar formatações
    df = formatar_colunas_data_br(df, ['Data'])
    df = formatar_colunas_moeda_br(df, ['Valor bruto', 'Valor líquido'])

    print("\nDataFrame DEPOIS:")
    print(df.to_string(index=False))

    # Verificações
    checks = [
        (df['Data'].iloc[0] == '04/06/2026', "Data formatada corretamente"),
        (df['Valor bruto'].iloc[0] == 'R$ 1.234,56', "Valor bruto formatado"),
        (df['Valor líquido'].iloc[1] == 'R$ 9.500,00', "Valor com milhares"),
    ]

    print("\nVerificações:")
    sucesso = 0
    for check, desc in checks:
        status = "✓" if check else "✗"
        if check:
            sucesso += 1
        print(f"{status} {desc}")

    print(f"\nResultado: {sucesso}/{len(checks)} verificações OK\n")
    return sucesso == len(checks)


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   TESTE DE FORMATAÇÃO BRASILEIRA (pt_BR)              ║
    ╚════════════════════════════════════════════════════════╝
    """)

    resultados = []

    resultados.append(("Formatação de Datas", testar_formatacao_datas()))
    resultados.append(("Formatação de Moeda", testar_formatacao_moeda()))
    resultados.append(("Formatação em DataFrame", testar_dataframe()))

    print("="*60)
    print("RESUMO DOS TESTES")
    print("="*60)

    total_sucesso = 0
    for nome, passou in resultados:
        status = "✓ PASSOU" if passou else "✗ FALHOU"
        print(f"{status}: {nome}")
        if passou:
            total_sucesso += 1

    print("="*60)
    print(f"Total: {total_sucesso}/{len(resultados)} testes passaram")
    print("="*60)

    if total_sucesso == len(resultados):
        print("\n🎉 Todos os testes passaram! Formatação brasileira OK.\n")
        return 0
    else:
        print(f"\n⚠️  {len(resultados) - total_sucesso} teste(s) falharam.\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
