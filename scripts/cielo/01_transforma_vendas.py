import pandas as pd
import os
import sys

# Adicionar path do projeto ao PYTHONPATH

# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS, CIELO_FILES
from utils.leitura_arquivos import detectar_e_ler_arquivo, salvar_arquivo_excel_ou_csv
from utils.validacao import validar_quantidade_parcelas_vendas, exibir_relatorio_validacao


def transformar_vendas_cielo():
    """
    Transforma arquivos brutos de vendas Cielo

    Entrada: Historico-de-vendas-pre_[1-9] (.xlsx, .xls ou .csv)
    Saída: CIELO_PRE_[1-9].xlsx, CIELO_ES.xlsx (normalizados)

    Suporta múltiplas extensões: .xlsx, .xls, .csv
    """
    input_path = PATHS['input']
    output_path = PATHS['temp']

    for input_name, output_name in CIELO_FILES['vendas']:
        # Remover extensão do nome de entrada para detectar automaticamente
        nome_base = os.path.splitext(input_name)[0]

        # Tentar ler com diferentes extensões
        df, extensao_encontrada = detectar_e_ler_arquivo(
            input_path,
            nome_base,
            extensoes_possiveis=['.xlsx', '.xls', '.csv'],
            skiprows=9,
            header=0
        )

        if df is None:
            print(f"⚠ Arquivo não encontrado: {nome_base} (.xlsx, .xls ou .csv)")
            continue

        output_excel = os.path.join(output_path, output_name)

        try:
            print(f"📄 Lendo: {nome_base}{extensao_encontrada}")

            df.rename(columns={
                'Motivo': 'Adquirente',
                'Quantidade total de parcelas': 'Quantidade de parcelas',
                'Valor bruto': 'Valor da venda',
                'Taxa/tarifa': 'Valor descontado',
                'Valor líquido': 'Valor líquido da venda',
                'Status da venda': 'Status'
            }, inplace=True)

            df['Adquirente'] = 'Cielo'

            # REGRA 2: Quantidade de parcelas é OBRIGATÓRIA para vendas
            # Contar registros sem quantidade de parcelas ANTES de corrigir
            registros_sem_parcelas = df['Quantidade de parcelas'].isna().sum()

            # Regra: Se não tem parcelas, assumir 1 (à vista / débito)
            # Vendas sempre têm pelo menos 1 parcela
            df['Quantidade de parcelas'] = df['Quantidade de parcelas'].fillna(1)

            # Alertar usuário sobre correção aplicada
            if registros_sem_parcelas > 0:
                print(f"   ℹ️  {registros_sem_parcelas} venda(s) sem quantidade de parcelas")
                print(f"   → Valor padrão aplicado: 1 parcela (à vista/débito)")

            # Validar quantidade de parcelas (obrigatório para vendas)
            df_validado, erros = validar_quantidade_parcelas_vendas(df, 'Cielo')

            if erros:
                exibir_relatorio_validacao('Vendas', 'Cielo', erros)
                print(f"⚠ {output_name} processado COM ALERTAS (origem: {extensao_encontrada})")
            else:
                print(f"✓ {output_name} processado e validado (origem: {extensao_encontrada})")

            # Salvar sempre como .xlsx
            salvar_arquivo_excel_ou_csv(df_validado, output_excel, index=False)

        except Exception as e:
            print(f"✗ Erro ao processar {nome_base}: {e}")


if __name__ == '__main__':
    print("=== Transformação de Vendas Cielo ===")
    transformar_vendas_cielo()
    print("Concluído!\n")
