#!/usr/bin/env python3
"""Executa apenas o pipeline Cielo (scripts 01-09)"""
import subprocess
import sys

SCRIPTS_CIELO = [
    "scripts/cielo/01_transforma_vendas.py",
    "scripts/cielo/02_consolida_vendas.py",
    "scripts/cielo/03_agrega_vendas.py",
    "scripts/cielo/04_transforma_estornos.py",
    "scripts/cielo/05_consolida_estornos.py",
    "scripts/cielo/06_agrega_estornos.py",
    "scripts/cielo/07_transforma_chargebacks.py",
    "scripts/cielo/08_consolida_chargebacks.py",
    "scripts/cielo/09_agrega_chargebacks.py",
]

if __name__ == '__main__':
    print("\n=== PIPELINE CIELO ===\n")
    for script in SCRIPTS_CIELO:
        subprocess.run([sys.executable, script], check=True)
    print("\n✓ Pipeline Cielo concluído!\n")
