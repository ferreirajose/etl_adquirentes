"""
Módulo de utilidades para o pipeline ETL Adquirentes

Exporta todas as funções dos submódulos para facilitar imports
"""

from .mappings import (
    assign_ec,
    assign_bandeira_cielo,
    assign_bandeira_pagarme,
    STATUS_PAGARME,
    ESTABELECIMENTOS,
    BANDEIRAS
)

from .transformacoes import (
    assign_forma_pagamento_cielo,
    assign_forma_pagamento_pagarme,
    assign_forma_pagamento_chargeback_cielo
)

from .normalizacao import (
    normalizar_valor_moeda,
    converter_centavos_para_reais,
    normalizar_data,
    formatar_data_br,
    formatar_moeda_br,
    formatar_colunas_data_br,
    formatar_colunas_moeda_br
)

from .agregacao import (
    agregar_transacoes,
    preparar_valores_para_agregacao
)

from .leitura_arquivos import (
    ler_arquivo_excel_ou_csv,
    detectar_e_ler_arquivo,
    listar_arquivos_por_extensao,
    salvar_arquivo_excel_ou_csv
)

__all__ = [
    # Mappings
    'assign_ec',
    'assign_bandeira_cielo',
    'assign_bandeira_pagarme',
    'STATUS_PAGARME',
    'ESTABELECIMENTOS',
    'BANDEIRAS',
    # Transformações
    'assign_forma_pagamento_cielo',
    'assign_forma_pagamento_pagarme',
    'assign_forma_pagamento_chargeback_cielo',
    # Normalização
    'normalizar_valor_moeda',
    'converter_centavos_para_reais',
    'normalizar_data',
    'formatar_data_br',
    'formatar_moeda_br',
    'formatar_colunas_data_br',
    'formatar_colunas_moeda_br',
    # Agregação
    'agregar_transacoes',
    'preparar_valores_para_agregacao',
    # Leitura de arquivos
    'ler_arquivo_excel_ou_csv',
    'detectar_e_ler_arquivo',
    'listar_arquivos_por_extensao',
    'salvar_arquivo_excel_ou_csv',
]
