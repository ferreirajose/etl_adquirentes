# Funções de transformação e agrupamento de formas de pagamento


def assign_forma_pagamento_cielo(row):
    """Agrupa formas de pagamento Cielo baseado em tipo e parcelas"""
    forma = row['Forma de pagamento']
    parcelas = row['Quantidade de parcelas']

    if forma in ['Crédito à vista', 'Crédito pré-pago']:
        return 'Crédito à vista'
    elif forma in ['Débito à vista', 'Débito pré-pago']:
        return 'Débito à vista'
    elif forma in ['Crédito parcelado loja - Taxa de embarque', 'Crédito parcelado loja']:
        if 2 <= parcelas <= 6:
            return 'Crédito 2x a 6x'
        elif 7 <= parcelas <= 12:
            return 'Crédito 7x a 12x'
    return None


def assign_forma_pagamento_pagarme(row):
    """Agrupa formas de pagamento Pagar.me com suporte a boleto/pix"""
    forma = str(row.get('Payment_Method', '')).strip().lower()
    parcelas = row.get('Installments', 1)

    if 'credit_card' in forma:
        if parcelas == 1:
            return 'Crédito à vista'
        elif 2 <= parcelas <= 6:
            return 'Crédito 2x a 6x'
        elif 7 <= parcelas <= 12:
            return 'Crédito 7x a 12x'
    elif 'boleto' in forma:
        return 'Boleto'
    elif 'pix' in forma:
        return 'Pix'
    return 'Outro'


def assign_forma_pagamento_chargeback_cielo(forma_str):
    """Simplificada para chargebacks Cielo (sem análise de parcelas)"""
    forma = str(forma_str).upper()
    if 'CRÉDITO À VISTA' in forma:
        return 'Crédito à vista'
    elif 'CRÉDITO PARCELADO' in forma or 'PARCELADO LOJA' in forma:
        return 'Crédito parcelado loja'
    return forma.capitalize()
