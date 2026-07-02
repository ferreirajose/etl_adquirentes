import os
import pandas as pd
import locale
import sys


# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS
from utils.validacao import validar_adquirente_consolidado, exibir_relatorio_validacao


def consolidar_final():
    """
    Consolida todos os arquivos agregados em arquivo único

    Entrada: CIELO_AGREGADO.csv, CIELO_ESTORNADO_AGREGADO.csv, etc.
    Saída: AGREGADO_CONSOLIDADO.csv
    """
    base_dir = PATHS['temp']
    file_paths = [
        f"{base_dir}CIELO_AGREGADO.csv",
        f"{base_dir}CIELO_CHARGEBACK_AGREGADO.csv",
        f"{base_dir}CIELO_ESTORNADO_AGREGADO.csv",
        f"{base_dir}PAGAR.ME_CHARGEBACK_AGREGADO.csv",
        f"{base_dir}PAGAR.ME_ESTORNADO_AGREGADO.csv",
        f"{base_dir}PAGAR.ME_AGREGADO.csv",
    ]

    dfs = []
    for path in file_paths:
        if os.path.exists(path):
            try:
                df_temp = pd.read_csv(path, sep=";", decimal=",", dtype={"Data": str})
                dfs.append(df_temp)
            except Exception as e:
                print(f"⚠ Erro ao ler {path}: {e}")
        else:
            print(f"⚠ Arquivo não encontrado: {path}")

    if not dfs:
        print("✗ Nenhum arquivo para consolidar")
        return

    merged_df = pd.concat(dfs, ignore_index=True)

    merged_df['Data'] = pd.to_datetime(merged_df['Data'], format='%d/%m/%Y', errors='coerce')
    merged_df['Ano'] = merged_df['Data'].dt.year.astype(str)

    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        print("⚠ Locale pt_BR.UTF-8 indisponível")

    merged_df['Mês'] = merged_df['Data'].dt.strftime('%m.%B').str.capitalize()
    merged_df['Ano'] = merged_df['Ano'].fillna('')
    merged_df['Mês'] = merged_df['Mês'].fillna('')

    final_columns = [
        'Data', 'EC', 'Adquirente', 'Bandeira', 'Forma de pagamento',
        'Quantidade de parcelas', 'Status', 'Valor bruto', 'Valor descontado',
        'Valor líquido', 'Quantidade de linhas', 'Ano', 'Mês'
    ]

    for col in final_columns:
        if col not in merged_df.columns:
            merged_df[col] = ''

    merged_df = merged_df[final_columns]

    # REGRA 3: Validar coluna Adquirente (deve exibir Cielo ou Pagar.me)
    df_validado, erros = validar_adquirente_consolidado(merged_df)

    if erros:
        exibir_relatorio_validacao('Consolidado Final', 'Todas', erros)
        print("⚠ ATENÇÃO: Consolidação possui registros com problemas na coluna Adquirente")

    output_path = f"{PATHS['output']}AGREGADO_CONSOLIDADO.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_validado.to_csv(output_path, index=False, decimal=",", sep=";")

    print(f"✓ Consolidação final salva: {output_path}")


if __name__ == '__main__':
    print("=== Consolidação Final ===")
    consolidar_final()
    print("Concluído!\n")
