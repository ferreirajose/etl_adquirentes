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
from utils.mappings import assign_ec
from utils.transformacoes import assign_forma_pagamento_cielo


def consolidar_vendas_cielo():
    """
    Consolida múltiplos arquivos de vendas Cielo em único CSV

    Entrada: CIELO_PRE_[1-9].xlsx, CIELO_ES.xlsx
    Saída: CIELO_CONSOLIDADO.csv
    """
    base_temp = PATHS['temp']

    files = [os.path.join(base_temp, f"CIELO_PRE_{i}.xlsx") for i in range(1, 10)]
    files.append(os.path.join(base_temp, "CIELO_ES.xlsx"))

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

    merged_df['EC'] = merged_df['Estabelecimento'].apply(assign_ec)
    merged_df['forma_pagamento_agrupado'] = merged_df.apply(
        assign_forma_pagamento_cielo, axis=1
    )
    merged_df['forma_pagamento_agrupado'] = merged_df['forma_pagamento_agrupado'].fillna('Outro')
    merged_df['Status'] = 'Aprovada'

    selected_columns = [
        'Data da venda', 'Estabelecimento', 'EC', 'Bandeira',
        'Forma de pagamento', 'forma_pagamento_agrupado',
        'Quantidade de parcelas', 'Valor da venda', 'Valor descontado',
        'Valor líquido da venda', 'Status', 'Adquirente'
    ]

    output_file = os.path.join(base_temp, "CIELO_CONSOLIDADO.csv")
    merged_df[selected_columns].to_csv(output_file, index=False, decimal=',', sep=';')

    print(f"✓ Arquivo consolidado: {output_file}")


if __name__ == '__main__':
    print("=== Consolidação de Vendas Cielo ===")
    consolidar_vendas_cielo()
    print("Concluído!\n")
