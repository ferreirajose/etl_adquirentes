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
from utils.normalizacao import normalizar_data
from utils.leitura_arquivos import detectar_e_ler_arquivo, salvar_arquivo_excel_ou_csv
from utils.validacao import validar_quantidade_parcelas_vendas, exibir_relatorio_validacao


def transformar_vendas_pagarme():
    """
    Transforma arquivos brutos de vendas Pagar.me em formato padronizado

    Entrada: Historico-de-vendas-pagarme-* (.csv, .xlsx ou .xls)
    Saída: PAGAR.ME_PRE_[1-3].xlsx, PAGAR.ME_ES.xlsx

    Suporta múltiplas extensões: .csv, .xlsx, .xls
    """
    input_base = PATHS['input']
    output_base = PATHS['temp']

    processamento = PAGARME_FILES['vendas']

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

            df = normalizar_data(
                df,
                coluna_origem='Paid_Date',
                coluna_destino='Data',
                formato='%d/%m/%Y %H:%M'
            )

            df['EC'] = ec_name
            df['Adquirente'] = 'Pagar.me'

            # REGRA 2: Validar quantidade de parcelas (obrigatório para vendas)
            # A coluna 'Installments' deve existir nos dados do Pagar.me
            # Identificar a coluna de parcelas (pode ser 'Installments' ou 'Número de Parcelas')
            coluna_parcelas = None
            for col in ['Installments', 'Número de Parcelas', 'Quantidade de parcelas']:
                if col in df.columns:
                    coluna_parcelas = col
                    break

            if coluna_parcelas:
                # Contar registros sem quantidade de parcelas ANTES de corrigir
                registros_sem_parcelas = df[coluna_parcelas].isna().sum()

                # Regra: Se não tem parcelas, assumir 1 (à vista / débito)
                # Vendas sempre têm pelo menos 1 parcela
                df[coluna_parcelas] = df[coluna_parcelas].fillna(1)

                # Alertar usuário sobre correção aplicada
                if registros_sem_parcelas > 0:
                    print(f"   ℹ️  {registros_sem_parcelas} venda(s) sem quantidade de parcelas")
                    print(f"   → Valor padrão aplicado: 1 parcela (à vista/débito)")

            df_validado, erros = validar_quantidade_parcelas_vendas(df, 'Pagar.me')

            if erros:
                exibir_relatorio_validacao('Vendas', 'Pagar.me', erros)
                print(f"⚠ {out_file} exportado COM ALERTAS (origem: {extensao_encontrada})")
            else:
                print(f"✓ {out_file} exportado e validado (origem: {extensao_encontrada})")

            # Salvar sempre como .xlsx
            salvar_arquivo_excel_ou_csv(df_validado, output_path, index=False)

        except Exception as e:
            print(f"✗ Erro ao processar {nome_base}: {e}")


if __name__ == '__main__':
    print("=== Transformação de Vendas Pagar.me ===")
    transformar_vendas_pagarme()
    print("Concluído!\n")
