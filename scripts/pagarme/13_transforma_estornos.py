import pandas as pd
import os
import sys


# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS, PAGARME_FILES
from utils.normalizacao import converter_centavos_para_reais
from utils.leitura_arquivos import detectar_e_ler_arquivo, salvar_arquivo_excel_ou_csv


def transformar_estornos_pagarme():
    """
    Transforma arquivos brutos de estornos Pagar.me em formato padronizado

    Entrada: Estorno-pagarme-* (.csv, .xlsx ou .xls)
    Saída: PAGAR.ME_ESTORNOS_[1-2].xlsx

    Suporta múltiplas extensões: .csv, .xlsx, .xls
    """
    input_base = PATHS['input']
    output_base = PATHS['temp']

    processamento = PAGARME_FILES['estornos']

    for in_file, out_file, ec_name in processamento:
        # Remover extensão do nome de entrada para detectar automaticamente
        nome_base = os.path.splitext(in_file)[0]

        # Tentar ler com diferentes extensões
        df, extensao_encontrada = detectar_e_ler_arquivo(
            input_base,
            nome_base,
            extensoes_possiveis=['.csv', '.xlsx', '.xls'],
            sep=';',
            header=0,
            low_memory=False
        )

        if df is None:
            print(f"⚠ Arquivo não encontrado: {nome_base} (.csv, .xlsx ou .xls)")
            continue

        output_path = os.path.join(output_base, out_file)

        try:
            print(f"📄 Lendo: {nome_base}{extensao_encontrada}")

            coluna_data = 'Canceled_Date' if 'Canceled_Date' in df.columns else 'Created_Date'

            df['Data'] = pd.to_datetime(
                df[coluna_data], format='%d/%m/%Y %H:%M', errors='coerce'
            ).dt.strftime('%d/%m/%Y')

            df['EC'] = ec_name
            df['Adquirente'] = 'Pagar.me'

            if 'Refunded_Amount' in df.columns:
                df = converter_centavos_para_reais(df, ['Refunded_Amount'])

            # Salvar sempre como .xlsx
            salvar_arquivo_excel_ou_csv(df, output_path, index=False)
            print(f"✓ {out_file} exportado (origem: {extensao_encontrada})")

        except Exception as e:
            print(f"✗ Erro ao processar {nome_base}: {e}")


if __name__ == '__main__':
    print("=== Transformação de Estornos Pagar.me ===")
    transformar_estornos_pagarme()
    print("Concluído!\n")
