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

            if 'Canceled_Date' in df.columns:
                coluna_data = 'Canceled_Date'
                formato_data = '%d/%m/%Y %H:%M'
            elif 'Created_Date' in df.columns:
                coluna_data = 'Created_Date'
                formato_data = '%d/%m/%Y %H:%M'
            elif 'Data' in df.columns:
                print(f"   ℹ️  Colunas 'Canceled_Date' e 'Created_Date' não existem no arquivo {nome_base}")
                print(f"   Colunas disponíveis: {list(df.columns)}")
                print(f"   → Usando coluna 'Data' como origem")
                coluna_data = 'Data'
                formato_data = '%d/%m/%Y %H:%M:%S'
            else:
                print(f"   ℹ️  Colunas 'Canceled_Date' e 'Created_Date' não existem no arquivo {nome_base}")
                print(f"   Colunas disponíveis: {list(df.columns)}")
                continue

            df['Data'] = pd.to_datetime(
                df[coluna_data], format=formato_data, errors='coerce'
            ).dt.strftime('%d/%m/%Y')

            df['EC'] = ec_name
            df['Adquirente'] = 'Pagar.me'

            # Tratamento das colunas do arquivo .es (nomes em português)
            # O pipeline padrão espera Payment_Method, Card_Brand, Installments
            # e Refunded_Amount. No arquivo .es os nomes vêm em português.
            if 'Payment_Method' not in df.columns and 'Forma de Pagamento' in df.columns:
                print(f"   ℹ️  Coluna 'Payment_Method' não existe no arquivo {nome_base}")
                print(f"   → Usando coluna 'Forma de Pagamento' como origem")
                mapa_forma_pagamento = {
                    'pix': 'pix',
                    'boleto': 'boleto',
                    'cartão de crédito': 'credit_card',
                    'cartao de credito': 'credit_card',
                }
                df['Payment_Method'] = (
                    df['Forma de Pagamento'].astype(str).str.strip().str.lower()
                    .map(mapa_forma_pagamento)
                    .fillna(df['Forma de Pagamento'].astype(str).str.strip().str.lower())
                )

            if 'Card_Brand' not in df.columns:
                if 'Bandeira do Cartão' in df.columns:
                    print(f"   ℹ️  Coluna 'Card_Brand' não existe no arquivo {nome_base}")
                    print(f"   → Usando coluna 'Bandeira do Cartão' como origem")
                    df['Card_Brand'] = df['Bandeira do Cartão']
                elif 'Bandeira' in df.columns:
                    print(f"   ℹ️  Coluna 'Card_Brand' não existe no arquivo {nome_base}")
                    print(f"   → Usando coluna 'Bandeira' como origem")
                    df['Card_Brand'] = df['Bandeira']

            if 'Installments' not in df.columns and 'Número de Parcelas' in df.columns:
                print(f"   ℹ️  Coluna 'Installments' não existe no arquivo {nome_base}")
                print(f"   → Usando coluna 'Número de Parcelas' como origem")
                df['Installments'] = df['Número de Parcelas']

            if 'Refunded_Amount' in df.columns:
                df = converter_centavos_para_reais(df, ['Refunded_Amount'])
            elif 'Valor Estornado (R$)' in df.columns:
                print(f"   ℹ️  Coluna 'Refunded_Amount' não existe no arquivo {nome_base}")
                print(f"   → Usando coluna 'Valor Estornado (R$)' (já em reais) como origem")
                df['Refunded_Amount'] = pd.to_numeric(df['Valor Estornado (R$)'], errors='coerce')
            elif 'Valor (R$)' in df.columns:
                print(f"   ℹ️  Coluna 'Refunded_Amount' não existe no arquivo {nome_base}")
                print(f"   → Usando coluna 'Valor (R$)' (já em reais) como origem")
                df['Refunded_Amount'] = pd.to_numeric(df['Valor (R$)'], errors='coerce')

            # Salvar sempre como .xlsx
            salvar_arquivo_excel_ou_csv(df, output_path, index=False)
            print(f"✓ {out_file} exportado (origem: {extensao_encontrada})")

        except Exception as e:
            print(f"✗ Erro ao processar {nome_base}: {e}")


if __name__ == '__main__':
    print("=== Transformação de Estornos Pagar.me ===")
    transformar_estornos_pagarme()
    print("Concluído!\n")
