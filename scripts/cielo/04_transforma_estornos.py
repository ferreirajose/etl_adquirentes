import pandas as pd
import os
import sys


# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS, CIELO_FILES
from utils.leitura_arquivos import detectar_e_ler_arquivo, salvar_arquivo_excel_ou_csv


def transformar_estornos_cielo():
    """
    Transforma arquivos brutos de estornos Cielo

    Entrada: Estorno-cielo-pre (.xls, .xlsx ou .csv), Estorno-cielo-es (.xls, .xlsx ou .csv)
    Saída: CIELO_ESTORNOS_1.xlsx, CIELO_ESTORNOS_2.xlsx (normalizados)

    Suporta múltiplas extensões: .xlsx, .xls, .csv
    """
    input_path = PATHS['input']
    output_path = PATHS['temp']

    for input_name, output_name in CIELO_FILES['estornos']:
        # Remover extensão do nome de entrada para detectar automaticamente
        nome_base = os.path.splitext(input_name)[0]

        # Tentar ler com diferentes extensões
        df, extensao_encontrada = detectar_e_ler_arquivo(
            input_path,
            nome_base,
            extensoes_possiveis=['.xlsx', '.xls', '.csv'],
            skiprows=4,
            header=0
        )

        if df is None:
            print(f"⚠ Arquivo não encontrado: {nome_base} (.xlsx, .xls ou .csv)")
            continue

        output_excel = os.path.join(output_path, output_name)

        try:
            print(f"📄 Lendo: {nome_base}{extensao_encontrada}")

            df.rename(columns={
                'NSU': 'Adquirente',
                'Código de autorização': 'Quantidade de parcelas'
            }, inplace=True)

            df['Adquirente'] = 'Cielo'
            df['Quantidade de parcelas'] = '0'

            # Salvar sempre como .xlsx
            salvar_arquivo_excel_ou_csv(df, output_excel, index=False)
            print(f"✓ {output_name} processado (origem: {extensao_encontrada})")

        except Exception as e:
            print(f"✗ Erro ao processar {nome_base}: {e}")


if __name__ == '__main__':
    print("=== Transformação de Estornos Cielo ===")
    transformar_estornos_cielo()
    print("Concluído!\n")
