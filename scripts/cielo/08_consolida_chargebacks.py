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
from utils.transformacoes import assign_forma_pagamento_chargeback_cielo
from utils.normalizacao import normalizar_valor_moeda


def consolidar_chargebacks_cielo():
    """
    Consolida múltiplos arquivos de chargebacks Cielo em único CSV

    Entrada: CIELO_CBK_1.xlsx, CIELO_CBK_2.xlsx
    Saída: CIELO_CHARGEBACK_CONSOLIDADO.csv
    """
    base_temp = PATHS['temp']

    files = [
        os.path.join(base_temp, "CIELO_CBK_1.xlsx"),
        os.path.join(base_temp, "CIELO_CBK_2.xlsx")
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
    merged_df['forma_pagamento_agrupado'] = merged_df['Forma de pagamento'].apply(
        assign_forma_pagamento_chargeback_cielo
    )
    merged_df['bandeira_pagamento'] = merged_df.apply(assign_bandeira_cielo, axis=1)
    merged_df['Status'] = 'Chargeback'

    merged_df['Valor líquido'] = 0.0
    merged_df['Valor descontado'] = 0.0

    if 'Data de pagamento' not in merged_df.columns:
        merged_df['Data de pagamento'] = merged_df['Data da solicitação']

    # REGRA 1: Quantidade de parcelas é OPCIONAL para chargebacks
    if 'Quantidade de parcelas' not in merged_df.columns:
        print("ℹ️ Coluna 'Quantidade de parcelas' não encontrada. Criando com valor padrão (1)")
        merged_df['Quantidade de parcelas'] = 1

    # columns_to_clean = ['Valor do cancelamento']
    # for column in columns_to_clean:
    #     merged_df[column] = normalizar_valor_moeda(merged_df[column])
    
    columns_to_clean = ['Valor do cancelamento']
    merged_df = normalizar_valor_moeda(merged_df, columns_to_clean)

    selected_columns = [
        'Status', 'Número do cliente', 'EC', 'Adquirente',
        'Data de pagamento', 'Bandeira', 'bandeira_pagamento',
        'Forma de pagamento', 'forma_pagamento_agrupado',
        'Quantidade de parcelas', 'Valor do cancelamento',
        'Valor descontado', 'Valor líquido'
    ]

    output_file = os.path.join(base_temp, "CIELO_CHARGEBACK_CONSOLIDADO.csv")
    merged_df[selected_columns].to_csv(output_file, index=False, decimal=',', sep=';')

    print(f"✓ Arquivo consolidado: {output_file}")


if __name__ == '__main__':
    print("=== Consolidação de Chargebacks Cielo ===")
    consolidar_chargebacks_cielo()
    print("Concluído!\n")
