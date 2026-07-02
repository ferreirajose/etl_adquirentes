#!/usr/bin/env python3
"""Executa apenas o pipeline Pagar.me (scripts 10-18)"""
import subprocess
import sys

SCRIPTS_PAGARME = [
    "scripts/pagarme/10_transforma_vendas.py",
    "scripts/pagarme/11_consolida_vendas.py",
    "scripts/pagarme/12_agrega_vendas.py",
    "scripts/pagarme/13_transforma_estornos.py",
    "scripts/pagarme/14_consolida_estornos.py",
    "scripts/pagarme/15_agrega_estornos.py",
    "scripts/pagarme/16_transforma_chargebacks.py",
    "scripts/pagarme/17_consolida_chargebacks.py",
    "scripts/pagarme/18_agrega_chargebacks.py",
]

if __name__ == '__main__':
    print("\n=== PIPELINE PAGAR.ME ===\n")
    for script in SCRIPTS_PAGARME:
        subprocess.run([sys.executable, script], check=True)
    print("\n✓ Pipeline Pagar.me concluído!\n")
