#!/usr/bin/env python3
"""
Orquestrador do Pipeline ETL Completo
Executa todos os 20 scripts em ordem
"""
import subprocess
import sys

SCRIPTS_ORDEM = [
    # Cielo
    "scripts/cielo/01_transforma_vendas.py",
    "scripts/cielo/02_consolida_vendas.py",
    "scripts/cielo/03_agrega_vendas.py",
    "scripts/cielo/04_transforma_estornos.py",
    "scripts/cielo/05_consolida_estornos.py",
    "scripts/cielo/06_agrega_estornos.py",
    "scripts/cielo/07_transforma_chargebacks.py",
    "scripts/cielo/08_consolida_chargebacks.py",
    "scripts/cielo/09_agrega_chargebacks.py",

    # Pagar.me
    "scripts/pagarme/10_transforma_vendas.py",
    "scripts/pagarme/11_consolida_vendas.py",
    "scripts/pagarme/12_agrega_vendas.py",
    "scripts/pagarme/13_transforma_estornos.py",
    "scripts/pagarme/14_consolida_estornos.py",
    "scripts/pagarme/15_agrega_estornos.py",
    "scripts/pagarme/16_transforma_chargebacks.py",
    "scripts/pagarme/17_consolida_chargebacks.py",
    "scripts/pagarme/18_agrega_chargebacks.py",

    # Final
    "scripts/final/19_consolida_final.py",
    "scripts/final/21_formatar_brasileiro.py",  # Formatação BR (opcional)
    "scripts/final/20_envia_sheets.py"          # Já formata automaticamente
]


def executar_script(script_path):
    """Executa um script Python e retorna status"""
    try:
        print(f"\n{'='*60}")
        print(f"Executando: {script_path}")
        print('='*60)

        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False,
            text=True
        )

        print(f"✓ Concluído: {script_path}\n")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ ERRO em {script_path}: {e}\n")
        return False


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   PIPELINE ETL ADQUIRENTES - EXECUÇÃO COMPLETA        ║
    ║   21 scripts serão executados em sequência            ║
    ║   Inclui formatação brasileira (DD/MM/YYYY, R$)       ║
    ╚════════════════════════════════════════════════════════╝
    """)

    executados = 0
    com_erro = 0

    for script in SCRIPTS_ORDEM:
        if executar_script(script):
            executados += 1
        else:
            com_erro += 1
            resposta = input(f"\nContinuar mesmo com erro? (s/N): ")
            if resposta.lower() != 's':
                print("\nPipeline interrompido pelo usuário.")
                break

    print("\n" + "="*60)
    print("RESUMO DA EXECUÇÃO")
    print("="*60)
    print(f"Scripts executados com sucesso: {executados}/{len(SCRIPTS_ORDEM)}")
    print(f"Scripts com erro: {com_erro}")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
