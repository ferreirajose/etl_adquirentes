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
from utils.mappings import assign_bandeira_pagarme, STATUS_PAGARME
from utils.normalizacao import converter_centavos_para_reais


def consolidar_vendas_pagarme():
    """
    Consolida múltiplos arquivos de vendas Pagar.me em único CSV

    Entrada: PAGAR.ME_PRE_[1-3].xlsx, PAGAR.ME_ES.xlsx
    Saída: PAGAR.ME_CONSOLIDADO.csv
    """
    base_temp = PATHS['temp']

    files = [
        os.path.join(base_temp, 'PAGAR.ME_PRE_1.xlsx'),
        os.path.join(base_temp, 'PAGAR.ME_PRE_2.xlsx'),
        os.path.join(base_temp, 'PAGAR.ME_PRE_3.xlsx'),
        os.path.join(base_temp, 'PAGAR.ME_ES.xlsx')
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

    merged_df['forma_pagamento_agrupado'] = merged_df.apply(
        assign_forma_pagamento_pagarme, axis=1
    )

    merged_df['bandeira_pagamento'] = merged_df.apply(
        assign_bandeira_pagarme, axis=1
    )

    merged_df = converter_centavos_para_reais(
        merged_df,
        ['Paid_Amount_In_Cents']
    )

    merged_df['Valor Capturado (R$)'] = merged_df['Paid_Amount_In_Cents'].fillna(
        pd.to_numeric(merged_df['Amount_In_Cents'], errors='coerce') / 100
    )

    merged_df['Valor líquido da venda'] = 0.0
    merged_df['Valor descontado'] = 0.0

    merged_df['Status'] = (
        merged_df['Status'].astype(str).str.lower().map(STATUS_PAGARME)
    )
    merged_df['Status'].fillna('Aprovada', inplace=True)

    merged_df.rename(columns={
        'Card_Brand': 'Bandeira',
        'Payment_Method': 'Forma de Pagamento',
        'Installments': 'Número de Parcelas'
    }, inplace=True)

    selected_columns = [
        'Data', 'EC', 'Adquirente', 'Bandeira', 'bandeira_pagamento',
        'Forma de Pagamento', 'forma_pagamento_agrupado',
        'Número de Parcelas', 'Valor Capturado (R$)',
        'Valor líquido da venda', 'Valor descontado', 'Status'
    ]

    output_file = os.path.join(base_temp, 'PAGAR.ME_CONSOLIDADO.csv')
    merged_df[selected_columns].to_csv(output_file, index=False, decimal=',', sep=';')

    print(f"✓ Arquivo consolidado: {output_file}")


if __name__ == '__main__':
    print("=== Consolidação de Vendas Pagar.me ===")
    consolidar_vendas_pagarme()
    print("Concluído!\n")
