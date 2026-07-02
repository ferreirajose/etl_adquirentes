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
from utils.normalizacao import formatar_colunas_data_br, formatar_colunas_moeda_br


def formatar_consolidado_brasileiro():
    """
    Aplica formatação brasileira ao arquivo consolidado

    Entrada: AGREGADO_CONSOLIDADO.csv
    Saída: AGREGADO_CONSOLIDADO_BR.csv

    Formatações:
    - Datas: DD/MM/YYYY (ex: 04/06/2026)
    - Moedas: R$ 1.234,56
    """
    input_path = f"{PATHS['output']}AGREGADO_CONSOLIDADO.csv"
    output_path = f"{PATHS['output']}AGREGADO_CONSOLIDADO_BR.csv"

    try:
        # Ler arquivo consolidado
        df = pd.read_csv(input_path, sep=";", decimal=",", dtype={"Data": str})

        print(f"Lido: {len(df)} registros")

        # Identificar colunas de data e valores
        colunas_data = ['Data']
        colunas_moeda = [
            'Valor bruto',
            'Valor descontado',
            'Valor líquido'
        ]

        # Aplicar formatação brasileira
        print("Aplicando formatação de datas (DD/MM/YYYY)...")
        df = formatar_colunas_data_br(df, colunas_data)

        print("Aplicando formatação de moeda (R$ 1.234,56)...")
        df = formatar_colunas_moeda_br(df, colunas_moeda)

        # Salvar com formatação brasileira
        df.to_csv(output_path, index=False, sep=";", encoding='utf-8-sig')

        print(f"✓ Arquivo formatado salvo: {output_path}")
        print(f"  - Datas no formato: DD/MM/YYYY")
        print(f"  - Valores no formato: R$ 1.234,56")

    except FileNotFoundError:
        print(f"✗ Arquivo não encontrado: {input_path}")
        print("  Execute o script 19_consolida_final.py primeiro")
    except Exception as e:
        print(f"✗ Erro ao formatar: {e}")


if __name__ == '__main__':
    print("=== Formatação Brasileira do Consolidado ===")
    formatar_consolidado_brasileiro()
    print("Concluído!\n")
