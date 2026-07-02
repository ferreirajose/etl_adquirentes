# Funções de agregação reutilizáveis
import pandas as pd


def agregar_transacoes(df, coluna_data, colunas_agrupamento_extras, colunas_valores):
    """
    Padrão universal de agregação de transações

    Args:
        df: DataFrame a agregar
        coluna_data: Nome da coluna de data
        colunas_agrupamento_extras: Lista de colunas adicionais para groupby
        colunas_valores: Dict {coluna: operação} para agregação (ex: {'Valor bruto': 'sum'})

    Returns:
        DataFrame agregado com contagem de linhas
    """
    df.rename(columns={coluna_data: 'Data_temp'}, inplace=True)

    colunas_agrupamento = ['Data_temp'] + colunas_agrupamento_extras

    agg_dict = {**colunas_valores, 'Data_temp': 'count'}

    resultado = (df.groupby(colunas_agrupamento)
                   .agg(agg_dict)
                   .rename(columns={'Data_temp': 'Quantidade de linhas'})
                   .reset_index())

    resultado.rename(columns={'Data_temp': 'Data'}, inplace=True)

    return resultado


def preparar_valores_para_agregacao(df, colunas_valores, decimal=','):
    """Converte valores string para float antes da agregação"""
    for coluna in colunas_valores:
        if coluna in df.columns and df[coluna].dtype == object:
            df[coluna] = (df[coluna]
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False))
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0.0)
    return df
