"""
Módulo de validação de dados ETL Adquirentes

Contém validações para garantir qualidade dos dados processados
"""

import pandas as pd


def validar_quantidade_parcelas_vendas(df, adquirente):
    """
    Valida se a coluna 'Quantidade de parcelas' está preenchida em vendas

    Regra: Para vendas (Cielo e Pagarme), quantidade de parcelas é OBRIGATÓRIA

    Args:
        df: DataFrame com os dados
        adquirente: Nome da adquirente ('Cielo' ou 'Pagarme')

    Returns:
        tuple: (df_validado, erros_encontrados)
    """
    erros = []

    # Colunas possíveis para quantidade de parcelas
    colunas_parcelas = [
        'Quantidade de parcelas',
        'Número de Parcelas',
        'Installments'
    ]

    # Encontrar a coluna existente
    coluna_encontrada = None
    for col in colunas_parcelas:
        if col in df.columns:
            coluna_encontrada = col
            break

    if not coluna_encontrada:
        erros.append(f"⚠ ERRO: Coluna de quantidade de parcelas não encontrada")
        return df, erros

    # Verificar valores nulos, zerados ou inválidos
    # Nota: Valores < 1 são inválidos (venda deve ter pelo menos 1 parcela)
    mask_nulos = df[coluna_encontrada].isna()
    mask_zero = df[coluna_encontrada] == 0
    mask_negativo = df[coluna_encontrada] < 0
    mask_vazio = df[coluna_encontrada].astype(str).str.strip() == ''

    registros_invalidos = mask_nulos | mask_zero | mask_negativo | mask_vazio
    total_invalidos = registros_invalidos.sum()

    if total_invalidos > 0:
        erros.append(
            f"⚠ VALIDAÇÃO FALHOU [{adquirente}]: "
            f"{total_invalidos} registro(s) de VENDAS com quantidade de parcelas inválida"
        )
        erros.append(f"   → Campo obrigatório e deve ser >= 1")

        # Exibir amostra dos registros com problema
        if total_invalidos <= 5:
            indices = df[registros_invalidos].index.tolist()
            valores = df.loc[registros_invalidos, coluna_encontrada].tolist()
            erros.append(f"   → Linhas com problema: {list(zip(indices, valores))}")
    else:
        print(f"✓ VALIDAÇÃO OK [{adquirente}]: Todas as vendas têm quantidade de parcelas válida")

    return df, erros


def validar_quantidade_parcelas_chargebacks(df, adquirente):
    """
    Valida se a coluna 'Quantidade de parcelas' existe em chargebacks

    Regra: Para chargebacks, quantidade de parcelas é OPCIONAL

    Args:
        df: DataFrame com os dados
        adquirente: Nome da adquirente ('Cielo' ou 'Pagarme')

    Returns:
        tuple: (df_validado, avisos)
    """
    avisos = []

    colunas_parcelas = [
        'Quantidade de parcelas',
        'Número de Parcelas',
        'Installments'
    ]

    coluna_encontrada = None
    for col in colunas_parcelas:
        if col in df.columns:
            coluna_encontrada = col
            break

    if coluna_encontrada:
        mask_nulos = df[coluna_encontrada].isna()
        total_nulos = mask_nulos.sum()

        if total_nulos > 0:
            avisos.append(
                f"ℹ INFO [{adquirente}]: {total_nulos} chargeback(s) sem quantidade de parcelas (OPCIONAL)"
            )
    else:
        avisos.append(f"ℹ INFO [{adquirente}]: Coluna 'Quantidade de parcelas' não existe em chargebacks (OPCIONAL)")

    return df, avisos


def validar_adquirente_consolidado(df):
    """
    Valida se a coluna 'Adquirente' está preenchida no consolidado

    Regra: Consolidado deve exibir o nome da Adquirente (Cielo ou Pagarme)

    Args:
        df: DataFrame consolidado

    Returns:
        tuple: (df_validado, erros_encontrados)
    """
    erros = []

    if 'Adquirente' not in df.columns:
        erros.append("⚠ ERRO CRÍTICO: Coluna 'Adquirente' não encontrada no consolidado")
        return df, erros

    # Verificar valores nulos
    mask_nulos = df['Adquirente'].isna()
    total_nulos = mask_nulos.sum()

    if total_nulos > 0:
        erros.append(
            f"⚠ VALIDAÇÃO FALHOU: {total_nulos} registro(s) sem adquirente no consolidado"
        )

    # Verificar valores válidos
    adquirentes_validos = ['Cielo', 'Pagar.me']
    mask_invalidos = ~df['Adquirente'].isin(adquirentes_validos)
    total_invalidos = mask_invalidos.sum()

    if total_invalidos > 0:
        valores_invalidos = df.loc[mask_invalidos, 'Adquirente'].unique()
        erros.append(
            f"⚠ VALIDAÇÃO FALHOU: {total_invalidos} registro(s) com adquirente inválida"
        )
        erros.append(f"   → Valores encontrados: {list(valores_invalidos)}")
        erros.append(f"   → Valores esperados: {adquirentes_validos}")

    if not erros:
        distribuicao = df['Adquirente'].value_counts().to_dict()
        print(f"✓ VALIDAÇÃO OK: Coluna 'Adquirente' preenchida corretamente")
        print(f"   → Distribuição: {distribuicao}")

    return df, erros


def exibir_relatorio_validacao(tipo_operacao, adquirente, erros, avisos=None):
    """
    Exibe relatório consolidado de validação

    Args:
        tipo_operacao: 'Vendas', 'Chargebacks', 'Consolidado'
        adquirente: Nome da adquirente
        erros: Lista de erros encontrados
        avisos: Lista de avisos (opcional)
    """
    print(f"\n{'='*60}")
    print(f"RELATÓRIO DE VALIDAÇÃO - {tipo_operacao} {adquirente}")
    print(f"{'='*60}")

    if erros:
        print("\n❌ ERROS ENCONTRADOS:")
        for erro in erros:
            print(f"  {erro}")

    if avisos:
        print("\n⚠ AVISOS:")
        for aviso in avisos:
            print(f"  {aviso}")

    if not erros and not avisos:
        print("\n✅ NENHUM PROBLEMA ENCONTRADO")

    print(f"{'='*60}\n")

    return len(erros) == 0
