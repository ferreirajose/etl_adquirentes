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


def agregar_chargebacks_cielo():
    """
    Agrega dados consolidados de chargebacks Cielo

    Entrada: CIELO_CHARGEBACK_CONSOLIDADO.csv
    Saída: CIELO_CHARGEBACK_AGREGADO.csv
    """
    caminho_arquivo = f"{PATHS['temp']}CIELO_CHARGEBACK_CONSOLIDADO.csv"
    data = pd.read_csv(caminho_arquivo, decimal=',', sep=';')

    colunas_valores = ['Valor do cancelamento', 'Valor descontado', 'Valor líquido']
    data = preparar_valores_para_agregacao(data, colunas_valores)

    data_agregado = agregar_transacoes(
        df=data,
        coluna_data='Data de pagamento',
        colunas_agrupamento_extras=COLUNAS_AGRUPAMENTO,
        colunas_valores={
            'Valor do cancelamento': 'sum',
            'Valor descontado': 'sum',
            'Valor líquido': 'sum'
        }
    )

    data_agregado.rename(columns={
        'Valor do cancelamento': 'Valor bruto',
        'forma_pagamento_agrupado': 'Forma de pagamento'
    }, inplace=True)

    output_path = f"{PATHS['temp']}CIELO_CHARGEBACK_AGREGADO.csv"
    data_agregado.to_csv(output_path, index=False, decimal=',', sep=';')

    print(f"✓ Agregado salvo: {output_path}")


if __name__ == '__main__':
    print("=== Agregação de Chargebacks Cielo ===")
    agregar_chargebacks_cielo()
    print("Concluído!\n")
