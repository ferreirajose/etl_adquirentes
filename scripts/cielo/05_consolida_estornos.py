import pandas as pd
import os
import sys
from zipfile import BadZipFile


# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS
from utils.mappings import assign_ec, assign_bandeira_cielo
from utils.normalizacao import normalizar_valor_moeda


def consolidar_estornos_cielo():
    """
    Consolida múltiplos arquivos de estornos Cielo em único CSV

    Entrada: CIELO_ESTORNOS_1.xlsx, CIELO_ESTORNOS_2.xlsx
    Saída: CIELO_ESTORNO_CONSOLIDADO.csv
    """
    base_temp = PATHS['temp']

    files = [
        os.path.join(base_temp, "CIELO_ESTORNOS_1.xlsx"),
        os.path.join(base_temp, "CIELO_ESTORNOS_2.xlsx")
    ]

    dfs = []
    for f in files:
        try:
            dfs.append(pd.read_excel(f))
        except FileNotFoundError:
            print(f"⚠ Arquivo não encontrado: {f}")
        except BadZipFile:
            print(f"⚠ Arquivo corrompido: {f}")
        except Exception as e:
            print(f"⚠ Erro ao ler {f}: {e}")

    if not dfs:
        print("✗ Nenhum arquivo carregado")
        return

    merged_df = pd.concat(dfs, ignore_index=True)

    merged_df['EC'] = merged_df['Número do cliente'].apply(assign_ec)
    merged_df['Adquirente'] = 'Cielo'
    merged_df['forma_pagamento_agrupado'] = merged_df['Forma de pagamento']
    merged_df['Bandeira'] = merged_df.apply(assign_bandeira_cielo, axis=1)
    merged_df['Status'] = 'Estornada'

    merged_df['Valor líquido'] = ''
    merged_df['Valor descontado'] = ''

    # REGRA 1: Quantidade de parcelas é OPCIONAL para estornos
    if 'Quantidade de parcelas' not in merged_df.columns:
        print("ℹ️ Coluna 'Quantidade de parcelas' não encontrada. Criando com valor padrão (1)")
        merged_df['Quantidade de parcelas'] = 1

    columns_to_clean = ['Valor do cancelamento']
    merged_df = normalizar_valor_moeda(merged_df, columns_to_clean)

    selected_columns = [
        'Data da solicitação', 'Número do cliente', 'EC', 'Bandeira',
        'Forma de pagamento', 'forma_pagamento_agrupado',
        'Quantidade de parcelas', 'Valor do cancelamento',
        'Valor descontado', 'Valor líquido', 'Status', 'Adquirente'
    ]

    output_file = os.path.join(base_temp, "CIELO_ESTORNO_CONSOLIDADO.csv")
    merged_df[selected_columns].to_csv(output_file, index=False, decimal=',', sep=';')

    print(f"✓ Arquivo consolidado: {output_file}")


if __name__ == '__main__':
    print("=== Consolidação de Estornos Cielo ===")
    consolidar_estornos_cielo()
    print("Concluído!\n")
