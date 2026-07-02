# Mapeamentos de estabelecimentos, bandeiras e status

# Mapeamento de estabelecimentos para ECs
ESTABELECIMENTOS = {
    2884599708: "Gran Centro",
    1055389455: "Gran Tec",
    2888238742: "Gran Tec",
    1045440202: "Gran Tec",
    2800363180: "Gran Tec"
}

# Mapeamento de status Pagar.me
# Apenas 3 status são considerados: Aprovada, Estornada (refunded), Chargeback
# Outros status (canceled, pending, failed) são mapeados para "Aprovada" para não perder dados
STATUS_PAGARME = {
    "paid": "Aprovada",
    "canceled": "Aprovada",  # Desconsiderado como status separado
    "refunded": "Estornada",
    "pending": "Aprovada",   # Desconsiderado como status separado
    "failed": "Aprovada"     # Desconsiderado como status separado
}

# Mapeamento de bandeiras (padrão)
BANDEIRAS = {
    'master': 'Mastercard',
    'visa': 'Visa',
    'elo': 'Elo',
    'amex': 'American Express',
    'american': 'American Express',
    'hiper': 'Hipercard'
}


def assign_ec(estabelecimento):
    """Mapeia código de estabelecimento para nome EC"""
    return ESTABELECIMENTOS.get(estabelecimento, None)


def assign_bandeira_cielo(bandeira_str):
    """Normaliza bandeiras para padrão Cielo"""
    b = str(bandeira_str).upper()
    if 'MASTERCARD' in b:
        return 'Mastercard'
    elif 'VISA' in b:
        return 'Visa'
    elif 'ELO' in b:
        return 'Elo'
    elif 'AMEX' in b:
        return 'American Express'
    elif 'HIPERCARD' in b:
        return 'Hipercard'
    return 'Outro'


def assign_bandeira_pagarme(row, forma_pagamento_col='forma_pagamento_agrupado'):
    """Normaliza bandeiras para padrão Pagar.me"""
    forma = row.get(forma_pagamento_col, '')
    if forma in ['Boleto', 'Pix']:
        return 'Pix e Boleto'

    bandeira = str(row.get('Card_Brand', '')).lower()
    for key, value in BANDEIRAS.items():
        if key in bandeira:
            return value
    return 'Outro'
