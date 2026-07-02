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
from utils.validacao import validar_quantidade_parcelas_chargebacks, exibir_relatorio_validacao


def transformar_chargebacks_cielo():
    """
    Transforma arquivos brutos de chargebacks Cielo

    Entrada: Chargeback-cielo-pre (.xls, .xlsx ou .csv), Chargeback-cielo-es (.xls, .xlsx ou .csv)
    Saída: CIELO_CBK_1.xlsx, CIELO_CBK_2.xlsx (normalizados)

    Suporta múltiplas extensões: .xlsx, .xls, .csv
    """
    input_path = PATHS['input']
    output_path = PATHS['temp']

    for input_name, output_name in CIELO_FILES['chargebacks']:
        # Remover extensão do nome de entrada para detectar automaticamente
        nome_base = os.path.splitext(input_name)[0]

        # Tentar ler com diferentes extensões
        df, extensao_encontrada = detectar_e_ler_arquivo(
            input_path,
            nome_base,
            extensoes_possiveis=['.xlsx', '.xls', '.csv'],
            skiprows=3
        )

        if df is None:
            print(f"⚠ Arquivo não encontrado: {nome_base} (.xlsx, .xls ou .csv)")
            continue

        output_excel = os.path.join(output_path, output_name)

        try:
            print(f"📄 Lendo: {nome_base}{extensao_encontrada}")

            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)

            df.rename(columns={
                'Nº do estabelecimento': 'Número do cliente',
                'Data Ação': 'Data da solicitação',
                'Valor Transação (R$)': 'Valor do cancelamento',
                'Produto': 'Forma de pagamento'
            }, inplace=True)

            df['Adquirente'] = 'Cielo'
            df['Status'] = 'Chargeback'

            # REGRA 1: Quantidade de parcelas é OPCIONAL para chargebacks
            df_validado, avisos = validar_quantidade_parcelas_chargebacks(df, 'Cielo')

            if avisos:
                exibir_relatorio_validacao('Chargebacks', 'Cielo', [], avisos)

            # Salvar sempre como .xlsx
            salvar_arquivo_excel_ou_csv(df_validado, output_excel, index=False)
            print(f"✓ {output_name} processado (origem: {extensao_encontrada})")

        except Exception as e:
            print(f"✗ Erro ao processar {nome_base}: {e}")


if __name__ == '__main__':
    print("=== Transformação de Chargebacks Cielo ===")
    transformar_chargebacks_cielo()
    print("Concluído!\n")
