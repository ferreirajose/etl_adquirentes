import pandas as pd
import sys
import os


# Adiciona o caminho do projeto ao sys.path para importações relativas.
# '/content/etl_adquirentes' é o diretório raiz do projeto após o cd.
# A verificação 'if path not in sys.path' evita duplicações.
project_root_path = '/content/etl_adquirentes'
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)
from config.settings import PATHS, GOOGLE_SHEETS
from utils.normalizacao import formatar_colunas_data_br, formatar_colunas_moeda_br

try:
    from google.auth import default
    from google.colab import auth
    from googleapiclient.discovery import build
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


def enviar_para_sheets():
    """
    Envia dados consolidados para Google Sheets

    Entrada: AGREGADO_CONSOLIDADO.csv
    Saída: Google Sheets (ID configurado)
    """
    if not GOOGLE_AVAILABLE:
        print("✗ Google Colab não disponível. Execute em ambiente Google Colab.")
        return

    auth.authenticate_user()
    creds, _ = default()
    service = build("sheets", "v4", credentials=creds)

    spreadsheet_id = GOOGLE_SHEETS['spreadsheet_id']
    sheet_name = GOOGLE_SHEETS['sheet_name']
    csv_path = f"{PATHS['output']}AGREGADO_CONSOLIDADO.csv"

    try:
        df = pd.read_csv(csv_path, sep=";", decimal=",", dtype={"Data": str})
        df = df.fillna("")

        # Aplicar formatação brasileira apenas para datas
        print("Aplicando formatação brasileira...")
        colunas_data = ['Data']

        df = formatar_colunas_data_br(df, colunas_data)
        print("  ✓ Datas: DD/MM/YYYY")

        # IMPORTANTE: NÃO formatar valores monetários para strings
        # Google Sheets precisa receber números para permitir operações aritméticas
        # A formatação visual (R$, vírgulas) será aplicada no próprio Sheets
        colunas_moeda = ['Valor bruto', 'Valor descontado', 'Valor líquido']
        for col in colunas_moeda:
            if col in df.columns:
                # Garantir que valores são numéricos
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

        print("  ✓ Valores monetários: mantidos como números (para permitir operações)")

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A1:Z"
        ).execute()
        values = result.get("values", [])

        if not values:
            values_to_append = [list(df.columns)] + df.values.tolist()
            target_range = f"{sheet_name}!A1"
        else:
            values_to_append = df.values.tolist()
            target_range = f"{sheet_name}!A{len(values) + 1}"

        body = {"values": values_to_append}
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=target_range,
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()

        print("✓ Dados enviados para Google Sheets com sucesso")

    except Exception as e:
        print(f"✗ Erro ao enviar para Sheets: {e}")


if __name__ == '__main__':
    print("=== Envio para Google Sheets ===")
    enviar_para_sheets()
    print("Concluído!\n")