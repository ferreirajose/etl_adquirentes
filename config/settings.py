# Configurações centralizadas do pipeline ETL Adquirentes

# Caminhos base
PATHS = {
    'input': "/content/drive/MyDrive/GRAN/Revenue Assurance/Dash/Backend Adq/",
    'temp': "/content/drive/MyDrive/GRAN/Revenue Assurance/Dash/Temp Adq/",
    'output': "/content/drive/MyDrive/GRAN/Revenue Assurance/Dash/AGREGADO CONSOLIDADO/"
}

# Google Sheets
GOOGLE_SHEETS = {
    'spreadsheet_id': "17TZuQKuZvB2onQgqKtliwIk9tGOLW4olrzk--wCM25Y",
    'sheet_name': "Adquirentes"
}

# Arquivos Cielo por tipo de transação
CIELO_FILES = {
    'vendas': [(f"Historico-de-vendas-pre_{i}.xlsx", f"CIELO_PRE_{i}.xlsx")
               for i in range(1, 10)] + [("Historico-de-vendas-es.xlsx", "CIELO_ES.xlsx")],
    'estornos': [("Estorno-cielo-pre.xls", "CIELO_ESTORNOS_1.xlsx"),
                 ("Estorno-cielo-es.xls", "CIELO_ESTORNOS_2.xlsx")],
    'chargebacks': [("Chargeback-cielo-pre.xls", "CIELO_CBK_1.xlsx"),
                    ("Chargeback-cielo-es.xls", "CIELO_CBK_2.xlsx")]
}

# Arquivos Pagar.me por tipo de transação (incluem EC nas tuplas)
PAGARME_FILES = {
    'vendas': [
        ("Historico-de-vendas-pagarme-pre_1.csv", "PAGAR.ME_PRE_1.xlsx", "Gran Tec"),
        ("Historico-de-vendas-pagarme-pre_2.csv", "PAGAR.ME_PRE_2.xlsx", "Gran Tec"),
        ("Historico-de-vendas-pagarme-pre_3.csv", "PAGAR.ME_PRE_3.xlsx", "Gran Tec"),
        ("Historico-de-vendas-pagarme-es.csv", "PAGAR.ME_ES.xlsx", "Gran Centro")
    ],
    'estornos': [
        ("Estorno-pagarme-pre_1.csv", "PAGAR.ME_ESTORNOS_1.xlsx", "Gran Tec"),
        ("Estorno-pagarme-es.csv", "PAGAR.ME_ESTORNOS_2.xlsx", "Gran Centro")
    ],
    'chargebacks': [
        ("Chargeback-pagarme-pre_1.csv", "PAGAR.ME_CHARGEBACK_1.xlsx", "Gran Tec"),
        ("Chargeback-pagarme-es.csv", "PAGAR.ME_CHARGEBACK_ES.xlsx", "Gran Centro")
    ]
}

# Colunas de agrupamento padrão para agregações
COLUNAS_AGRUPAMENTO = [
    'EC', 'Adquirente', 'Bandeira', 'forma_pagamento_agrupado',
    'Quantidade de parcelas', 'Status'
]
