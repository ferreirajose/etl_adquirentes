import pandas as pd
import os
import sys


# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS, COLUNAS_AGRUPAMENTO
from utils.agregacao import preparar_valores_para_agregacao, agregar_transacoes


def agregar_vendas_cielo():
    """
    Agrega dados consolidados de vendas Cielo

    Entrada: CIELO_CONSOLIDADO.csv
    Saída: CIELO_AGREGADO.csv
    """
    caminho_arquivo = f"{PATHS['temp']}CIELO_CONSOLIDADO.csv"
    data = pd.read_csv(caminho_arquivo, decimal=',', sep=';')

    colunas_valores = ['Valor da venda', 'Valor descontado', 'Valor líquido da venda']
    data = preparar_valores_para_agregacao(data, colunas_valores)

    data_agregado = agregar_transacoes(
        df=data,
        coluna_data='Data da venda',
        colunas_agrupamento_extras=COLUNAS_AGRUPAMENTO,
        colunas_valores={
            'Valor da venda': 'sum',
            'Valor descontado': 'sum',
            'Valor líquido da venda': 'sum'
        }
    )

    data_agregado['Valor descontado'] = data_agregado['Valor descontado'].abs()

    data_agregado.rename(columns={
        'Valor da venda': 'Valor bruto',
        'Valor líquido da venda': 'Valor líquido',
        'forma_pagamento_agrupado': 'Forma de pagamento'
    }, inplace=True)

    output_path = f"{PATHS['temp']}CIELO_AGREGADO.csv"
    data_agregado.to_csv(output_path, index=False, decimal=',', sep=';')

    print(f"✓ Agregado salvo: {output_path}")


if __name__ == '__main__':
    print("=== Agregação de Vendas Cielo ===")
    agregar_vendas_cielo()
    print("Concluído!\n")
