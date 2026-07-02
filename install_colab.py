#!/usr/bin/env python3
"""
Script de instalação rápida para Google Colab
Execute este script no Colab para configurar tudo automaticamente
"""

def install_on_colab():
    """Instala e configura o projeto no Google Colab"""

    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   INSTALAÇÃO AUTOMÁTICA - ETL ADQUIRENTES v1.1.0      ║
    ║   Google Colab Setup                                   ║
    ╚════════════════════════════════════════════════════════╝
    """)

    import subprocess
    import sys
    import os

    # 1. Verificar se está no Colab
    try:
        from google.colab import drive
        is_colab = True
    except ImportError:
        is_colab = False
        print("⚠️  AVISO: Este script é otimizado para Google Colab")
        print("   Pode funcionar em outros ambientes, mas não é garantido.\n")

    # 2. Montar Google Drive
    if is_colab:
        print("📂 Montando Google Drive...")
        drive.mount('/content/drive')
        print("✓ Drive montado\n")

    # 3. Instalar dependências
    print("📦 Instalando dependências...")
    packages = ['pandas', 'openpyxl']

    for package in packages:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', package],
                      check=False)

    import pandas as pd
    print(f"✓ Pandas {pd.__version__} instalado")
    print("✓ Openpyxl instalado\n")

    # 4. Verificar estrutura do projeto
    print("🔍 Verificando estrutura do projeto...")

    required_dirs = [
        'config',
        'utils',
        'scripts/cielo',
        'scripts/pagarme',
        'scripts/final'
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)

    if missing_dirs:
        print("⚠️  Diretórios faltando:")
        for d in missing_dirs:
            print(f"   - {d}")
        print("\n   Execute este script do diretório raiz do projeto!")
        return False

    print("✓ Estrutura OK\n")

    # 5. Verificar arquivos de entrada
    print("📁 Verificando arquivos de entrada...")

    input_path = "/content/drive/Shared drives/Revenue Assurance/Dash/Backend Adq/"

    if os.path.exists(input_path):
        files = os.listdir(input_path)
        print(f"✓ Pasta de entrada encontrada: {len(files)} arquivos")
    else:
        print("⚠️  Pasta de entrada não encontrada:")
        print(f"   {input_path}")
        print("   Verifique se o Drive está montado e o caminho está correto\n")

    # 6. Adicionar ao PYTHONPATH
    print("🔧 Configurando PYTHONPATH...")
    project_root = os.getcwd()
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    print(f"✓ Adicionado: {project_root}\n")

    # 7. Testar importações
    print("🧪 Testando importações...")

    try:
        from config.settings import PATHS
        print("✓ config.settings")
    except ImportError as e:
        print(f"✗ config.settings: {e}")
        return False

    try:
        from utils.mappings import assign_ec
        print("✓ utils.mappings")
    except ImportError as e:
        print(f"✗ utils.mappings: {e}")
        return False

    try:
        from utils.normalizacao import formatar_data_br, formatar_moeda_br
        print("✓ utils.normalizacao")
    except ImportError as e:
        print(f"✗ utils.normalizacao: {e}")
        return False

    # 8. Testar formatações
    print("\n🎨 Testando formatações brasileiras...")

    data_teste = formatar_data_br('2026-06-04')
    if data_teste == '04/06/2026':
        print(f"✓ Data: '2026-06-04' → '{data_teste}'")
    else:
        print(f"✗ Data: esperado '04/06/2026', obtido '{data_teste}'")

    moeda_teste = formatar_moeda_br(1234.56)
    if moeda_teste == 'R$ 1.234,56':
        print(f"✓ Moeda: 1234.56 → '{moeda_teste}'")
    else:
        print(f"✗ Moeda: esperado 'R$ 1.234,56', obtido '{moeda_teste}'")

    # 9. Resumo
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO                  ║
    ╚════════════════════════════════════════════════════════╝

    📋 Próximos passos:

    1. Executar pipeline completo:
       !python orchestrator.py

    2. Ou executar parcialmente:
       !python run_cielo.py       # Apenas Cielo
       !python run_pagarme.py     # Apenas Pagar.me

    3. Ou scripts individuais:
       !python scripts/final/19_consolida_final.py
       !python scripts/final/21_formatar_brasileiro.py
       !python scripts/final/20_envia_sheets.py

    📚 Documentação:
       - README.md
       - GUIA_GOOGLE_COLAB.md
       - FORMATACAO_BRASILEIRA.md

    🆘 Suporte:
       - Execute: !python testar_formatacao_br.py
       - Consulte: TROUBLESHOOTING.md
    """)

    return True


if __name__ == '__main__':
    import sys
    success = install_on_colab()
    sys.exit(0 if success else 1)
