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
from utils.transformacoes import assign_forma_pagamento_pagarme
from utils.mappings import assign_bandeira_pagarme
from utils.normalizacao import converter_centavos_para_reais


def consolidar_chargebacks_pagarme():
    """
    Consolida múltiplos arquivos de chargebacks Pagar.me em único CSV

    Entrada: PAGAR.ME_CHARGEBACK_[1, ES].xlsx
    Saída: PAGAR.ME_CHARGEBACK_CONSOLIDADO.csv
    """
    base_temp = PATHS['temp']

    files = [
        os.path.join(base_temp, 'PAGAR.ME_CHARGEBACK_1.xlsx'),
        os.path.join(base_temp, 'PAGAR.ME_CHARGEBACK_ES.xlsx')
    ]

    dfs = []
    for f in files:
        try:
            df_temp = pd.read_excel(f, dtype={'Data': str})
            dfs.append(df_temp)
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

    merged_df['Adquirente'] = 'Pagar.me'
    merged_df['forma_pagamento_agrupado'] = merged_df.apply(
        assign_forma_pagamento_pagarme, axis=1
    )

    merged_df['bandeira_pagamento'] = merged_df.apply(
        assign_bandeira_pagarme, axis=1
    )

    merged_df = converter_centavos_para_reais(
        merged_df,
        ['Amount_In_Cents']
    )

    merged_df['Valor Chargeback'] = merged_df['Amount_In_Cents']

    merged_df['Status'] = 'Chargeback'

    merged_df.rename(columns={
        'Card_Brand': 'Bandeira',
        'Payment_Method': 'Forma de Pagamento',
        'Installments': 'Número de Parcelas'
    }, inplace=True)

    selected_columns = [
        'Data', 'EC', 'Adquirente', 'Bandeira', 'bandeira_pagamento',
        'Forma de Pagamento', 'forma_pagamento_agrupado',
        'Número de Parcelas', 'Valor Chargeback', 'Status'
    ]

    output_file = os.path.join(base_temp, 'PAGAR.ME_CHARGEBACK_CONSOLIDADO.csv')
    merged_df[selected_columns].to_csv(output_file, index=False, decimal=',', sep=';')

    print(f"✓ Arquivo consolidado: {output_file}")


if __name__ == '__main__':
    print("=== Consolidação de Chargebacks Pagar.me ===")
    consolidar_chargebacks_pagarme()
    print("Concluído!\n")
