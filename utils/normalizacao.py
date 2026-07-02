# Funções de normalização de valores e datas
import pandas as pd


def normalizar_valor_moeda(df, colunas):
    """Remove símbolos monetários e converte para float"""
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = (df[coluna]
                .astype(str)
                .str.replace('R$', '', regex=False)
                .str.strip()
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.replace('-', '', regex=False))
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0.0)
    return df


def converter_centavos_para_reais(df, colunas):
    """Converte valores em centavos (Pagar.me) para reais"""
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce') / 100
    return df


def normalizar_data(df, coluna_origem, coluna_destino, formato='%d/%m/%Y %H:%M'):
    """Converte e formata coluna de data"""
    df[coluna_destino] = pd.to_datetime(
        df[coluna_origem], format=formato, errors='coerce'
    ).dt.strftime('%d/%m/%Y')
    return df


# ============================================================================
# FORMATAÇÃO PADRÃO BRASILEIRO (pt_BR)
# ============================================================================

def formatar_data_br(data):
    """
    Formata data para padrão brasileiro DD/MM/YYYY

    Args:
        data: String, datetime, ou Timestamp

    Returns:
        String no formato DD/MM/YYYY ou string vazia se inválido

    Exemplos:
        '2026-06-04' -> '04/06/2026'
        '04/06/2026' -> '04/06/2026'
    """
    if pd.isna(data) or data == '':
        return ''

    try:
        dt = pd.to_datetime(data, errors='coerce')
        if pd.isna(dt):
            return ''
        return dt.strftime('%d/%m/%Y')
    except:
        return ''


def formatar_moeda_br(valor):
    """
    Formata valor numérico para padrão monetário brasileiro

    Args:
        valor: Float ou int

    Returns:
        String no formato R$ 1.234,56

    Exemplos:
        1.0     -> 'R$ 1,00'
        10.0    -> 'R$ 10,00'
        100.0   -> 'R$ 100,00'
        1000.0  -> 'R$ 1.000,00'
        1234.56 -> 'R$ 1.234,56'
    """
    if pd.isna(valor):
        return 'R$ 0,00'

    try:
        valor_float = float(valor)

        # Formata com 2 casas decimais
        valor_formatado = f'{valor_float:,.2f}'

        # Substitui separadores (1,234.56 -> 1.234,56)
        valor_formatado = valor_formatado.replace(',', '_')  # temp
        valor_formatado = valor_formatado.replace('.', ',')  # decimal
        valor_formatado = valor_formatado.replace('_', '.')  # milhares

        return f'R$ {valor_formatado}'
    except:
        return 'R$ 0,00'


def formatar_colunas_data_br(df, colunas):
    """
    Formata múltiplas colunas de data para padrão brasileiro

    Args:
        df: DataFrame
        colunas: Lista de nomes de colunas

    Returns:
        DataFrame com colunas formatadas
    """
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(formatar_data_br)
    return df


def formatar_colunas_moeda_br(df, colunas):
    """
    Formata múltiplas colunas de valores para padrão monetário brasileiro

    Args:
        df: DataFrame
        colunas: Lista de nomes de colunas

    Returns:
        DataFrame com colunas formatadas
    """
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(formatar_moeda_br)
    return df
