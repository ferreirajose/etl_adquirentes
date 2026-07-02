import pandas as pd
import os
import sys


# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS
from utils.agregacao import preparar_valores_para_agregacao, agregar_transacoes


def agregar_estornos_pagarme():
    """
    Agrega dados consolidados de estornos Pagar.me

    Entrada: PAGAR.ME_ESTORNO_CONSOLIDADO.csv
    Saída: PAGAR.ME_ESTORNADO_AGREGADO.csv
    """
    caminho_arquivo = f"{PATHS['temp']}PAGAR.ME_ESTORNO_CONSOLIDADO.csv"

    try:
        data = pd.read_csv(caminho_arquivo, sep=';', decimal=',')
    except FileNotFoundError:
        print(f"✗ Arquivo não encontrado: {caminho_arquivo}")
        return
    except Exception as e:
        print(f"✗ Erro ao ler arquivo: {e}")
        return

    colunas_valores = ['Valor Estornado']
    data = preparar_valores_para_agregacao(data, colunas_valores)

    data['Número de Parcelas'] = (
        pd.to_numeric(data['Número de Parcelas'], errors='coerce')
        .fillna(1)
        .astype(int)
    )

    colunas_agrupamento = [
        'EC',
        'Adquirente',
        'bandeira_pagamento',
        'forma_pagamento_agrupado',
        'Número de Parcelas',
        'Status'
    ]

    data_agregado = agregar_transacoes(
        df=data,
        coluna_data='Data',
        colunas_agrupamento_extras=colunas_agrupamento,
        colunas_valores={
            'Valor Estornado': 'sum'
        }
    )

    data_agregado.rename(columns={
        'forma_pagamento_agrupado': 'Forma de pagamento',
        'bandeira_pagamento': 'Bandeira',
        'Número de Parcelas': 'Quantidade de parcelas',
        'Valor Estornado': 'Valor bruto'
    }, inplace=True)

    # Adicionar colunas de valores faltantes
    data_agregado['Valor descontado'] = 0.0
    data_agregado['Valor líquido'] = data_agregado['Valor bruto']

    output_path = f"{PATHS['temp']}PAGAR.ME_ESTORNADO_AGREGADO.csv"
    data_agregado.to_csv(output_path, index=False, decimal=',', sep=';')

    print(f"✓ Agregado salvo: {output_path}")


if __name__ == '__main__':
    print("=== Agregação de Estornos Pagar.me ===")
    agregar_estornos_pagarme()
    print("Concluído!\n")
