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

    # groupby descarta silenciosamente linhas com chave vazia (ex.: Data NaN
    # quando o formato de data do export muda). Avisar para não perder valores.
    descartadas = df[colunas_agrupamento].isna().any(axis=1)
    if descartadas.any():
        total = len(df)
        print(f"   ⚠ {descartadas.sum()} de {total} linha(s) descartada(s) na agregação "
              f"por chave vazia:")
        for col in colunas_agrupamento:
            n = df[col].isna().sum()
            if n:
                nome = coluna_data if col == 'Data_temp' else col
                print(f"      - '{nome}' vazia em {n} linha(s)")
        if descartadas.all():
            print("   ✗ TODAS as linhas foram descartadas — verifique o formato das datas "
                  "do arquivo de origem")

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
