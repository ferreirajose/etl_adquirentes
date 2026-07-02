#!/usr/bin/env python3
"""
Script de teste para validar imports do módulo utils
"""

import sys
import os

# Adicionar raiz do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

print("="*60)
print("TESTE DE IMPORTS - Pipeline ETL Adquirentes")
print("="*60)

# Teste 1: Import do módulo utils
print("\n1. Testando import do módulo utils...")
try:
    import utils
    print("   ✓ import utils")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 2: Imports de mappings
print("\n2. Testando utils.mappings...")
try:
    from utils.mappings import (
        assign_ec,
        assign_bandeira_cielo,
        assign_bandeira_pagarme,
        STATUS_PAGARME,
        ESTABELECIMENTOS,
        BANDEIRAS
    )
    print("   ✓ assign_ec")
    print("   ✓ assign_bandeira_cielo")
    print("   ✓ assign_bandeira_pagarme")
    print("   ✓ STATUS_PAGARME")
    print("   ✓ ESTABELECIMENTOS")
    print("   ✓ BANDEIRAS")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 3: Imports de transformacoes
print("\n3. Testando utils.transformacoes...")
try:
    from utils.transformacoes import (
        assign_forma_pagamento_cielo,
        assign_forma_pagamento_pagarme,
        assign_forma_pagamento_chargeback_cielo
    )
    print("   ✓ assign_forma_pagamento_cielo")
    print("   ✓ assign_forma_pagamento_pagarme")
    print("   ✓ assign_forma_pagamento_chargeback_cielo")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 4: Imports de normalizacao
print("\n4. Testando utils.normalizacao...")
try:
    from utils.normalizacao import (
        normalizar_valor_moeda,
        converter_centavos_para_reais,
        normalizar_data,
        formatar_data_br,
        formatar_moeda_br,
        formatar_colunas_data_br,
        formatar_colunas_moeda_br
    )
    print("   ✓ normalizar_valor_moeda")
    print("   ✓ converter_centavos_para_reais")
    print("   ✓ normalizar_data")
    print("   ✓ formatar_data_br")
    print("   ✓ formatar_moeda_br")
    print("   ✓ formatar_colunas_data_br")
    print("   ✓ formatar_colunas_moeda_br")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 5: Imports de agregacao
print("\n5. Testando utils.agregacao...")
try:
    from utils.agregacao import (
        agregar_transacoes,
        preparar_valores_para_agregacao
    )
    print("   ✓ agregar_transacoes")
    print("   ✓ preparar_valores_para_agregacao")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 6: Imports de leitura_arquivos
print("\n6. Testando utils.leitura_arquivos...")
try:
    from utils.leitura_arquivos import (
        ler_arquivo_excel_ou_csv,
        detectar_e_ler_arquivo,
        listar_arquivos_por_extensao,
        salvar_arquivo_excel_ou_csv
    )
    print("   ✓ ler_arquivo_excel_ou_csv")
    print("   ✓ detectar_e_ler_arquivo")
    print("   ✓ listar_arquivos_por_extensao")
    print("   ✓ salvar_arquivo_excel_ou_csv")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 7: Import via utils.__init__
print("\n7. Testando import via utils.__init__...")
try:
    from utils import (
        assign_ec,
        formatar_data_br,
        detectar_e_ler_arquivo,
        agregar_transacoes
    )
    print("   ✓ Import via utils.__init__ funciona")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 8: Import de config
print("\n8. Testando import de config...")
try:
    from config.settings import PATHS, CIELO_FILES, PAGARME_FILES
    print("   ✓ PATHS")
    print("   ✓ CIELO_FILES")
    print("   ✓ PAGARME_FILES")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 9: Verificar __all__
print("\n9. Testando __all__ do módulo utils...")
try:
    from utils import __all__
    print(f"   ✓ __all__ definido com {len(__all__)} itens")
    print(f"   Funções exportadas: {', '.join(__all__[:5])}...")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Resumo
print("\n" + "="*60)
print("RESULTADO")
print("="*60)
print("✅ Todos os imports funcionam corretamente!")
print("\nItens testados:")
print("  ✓ 6 funções de mappings")
print("  ✓ 3 funções de transformacoes")
print("  ✓ 7 funções de normalizacao")
print("  ✓ 2 funções de agregacao")
print("  ✓ 4 funções de leitura_arquivos")
print("  ✓ Import via utils.__init__")
print("  ✓ Import de config.settings")
print("  ✓ __all__ definido corretamente")
print("\nTotal: 31 imports testados com sucesso")
print("="*60)

sys.exit(0)
