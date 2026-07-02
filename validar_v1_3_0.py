#!/usr/bin/env python3
"""
Script de Validação v1.3.0
Verifica se todas as mudanças foram aplicadas corretamente
"""

import os
import sys

def validar_modulo_leitura():
    """Valida se o módulo leitura_arquivos existe e tem todas as funções"""
    print("\n" + "="*60)
    print("1. Validando módulo utils/leitura_arquivos.py")
    print("="*60)

    try:
        from utils.leitura_arquivos import (
            ler_arquivo_excel_ou_csv,
            detectar_e_ler_arquivo,
            listar_arquivos_por_extensao,
            salvar_arquivo_excel_ou_csv
        )
        print("✓ Módulo importado com sucesso")
        print("✓ Todas as 4 funções encontradas:")
        print("  - ler_arquivo_excel_ou_csv()")
        print("  - detectar_e_ler_arquivo()")
        print("  - listar_arquivos_por_extensao()")
        print("  - salvar_arquivo_excel_ou_csv()")
        return True
    except ImportError as e:
        print(f"✗ Erro ao importar módulo: {e}")
        return False


def validar_script(script_path, nome):
    """Valida se um script importa as funções de leitura"""
    print(f"\n  Validando {nome}...")

    if not os.path.exists(script_path):
        print(f"  ✗ Arquivo não encontrado: {script_path}")
        return False

    with open(script_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Verificar imports
    tem_import = 'from utils.leitura_arquivos import' in conteudo
    tem_detectar = 'detectar_e_ler_arquivo' in conteudo
    tem_salvar = 'salvar_arquivo_excel_ou_csv' in conteudo
    tem_splitext = 'os.path.splitext' in conteudo
    tem_log = 'extensao_encontrada' in conteudo or 'ext' in conteudo

    if tem_import and tem_detectar and tem_salvar and tem_splitext:
        print(f"  ✓ {nome}")
        if tem_log:
            print(f"    - Log de extensão implementado")
        return True
    else:
        print(f"  ✗ {nome} - Faltam elementos:")
        if not tem_import:
            print(f"    - Import de utils.leitura_arquivos")
        if not tem_detectar:
            print(f"    - Uso de detectar_e_ler_arquivo()")
        if not tem_salvar:
            print(f"    - Uso de salvar_arquivo_excel_ou_csv()")
        if not tem_splitext:
            print(f"    - Uso de os.path.splitext()")
        return False


def validar_scripts_transformacao():
    """Valida todos os 6 scripts de transformação"""
    print("\n" + "="*60)
    print("2. Validando Scripts de Transformação (6 scripts)")
    print("="*60)

    scripts = [
        ("scripts/cielo/01_transforma_vendas.py", "01_transforma_vendas.py (Cielo)"),
        ("scripts/cielo/04_transforma_estornos.py", "04_transforma_estornos.py (Cielo)"),
        ("scripts/cielo/07_transforma_chargebacks.py", "07_transforma_chargebacks.py (Cielo)"),
        ("scripts/pagarme/10_transforma_vendas.py", "10_transforma_vendas.py (Pagar.me)"),
        ("scripts/pagarme/13_transforma_estornos.py", "13_transforma_estornos.py (Pagar.me)"),
        ("scripts/pagarme/16_transforma_chargebacks.py", "16_transforma_chargebacks.py (Pagar.me)"),
    ]

    resultados = []
    for script_path, nome in scripts:
        resultado = validar_script(script_path, nome)
        resultados.append(resultado)

    total = len(scripts)
    sucesso = sum(resultados)

    print(f"\nResultado: {sucesso}/{total} scripts atualizados corretamente")
    return all(resultados)


def validar_notebook():
    """Valida se o notebook tem as células de configuração"""
    print("\n" + "="*60)
    print("3. Validando Notebook Colab")
    print("="*60)

    notebook_path = "ETL_Adquirentes_Colab.ipynb"

    if not os.path.exists(notebook_path):
        print(f"✗ Arquivo não encontrado: {notebook_path}")
        return False

    with open(notebook_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Verificar elementos chave
    tem_custom_paths = 'CUSTOM_PATHS' in conteudo
    tem_base_drive = 'BASE_DRIVE' in conteudo
    tem_validacao = 'os.path.exists(path)' in conteudo
    tem_listagem = 'listar_arquivos_por_extensao' in conteudo
    tem_teste_deteccao = 'detectar_e_ler_arquivo' in conteudo
    tem_versao = '1.3.0' in conteudo

    elementos = [
        (tem_custom_paths, "Configuração CUSTOM_PATHS"),
        (tem_base_drive, "Configuração BASE_DRIVE"),
        (tem_validacao, "Validação de paths"),
        (tem_listagem, "Listagem por extensão"),
        (tem_teste_deteccao, "Teste de detecção"),
        (tem_versao, "Versão 1.3.0")
    ]

    for presente, nome in elementos:
        status = "✓" if presente else "✗"
        print(f"  {status} {nome}")

    total = len(elementos)
    sucesso = sum(1 for presente, _ in elementos if presente)
    print(f"\nResultado: {sucesso}/{total} elementos encontrados")

    return all(presente for presente, _ in elementos)


def validar_documentacao():
    """Valida se a documentação foi criada/atualizada"""
    print("\n" + "="*60)
    print("4. Validando Documentação")
    print("="*60)

    arquivos_doc = [
        ("GUIA_PATHS_MULTIPLAS_EXTENSOES.md", "Guia completo"),
        ("STATUS_V1_3_0.md", "Status de implementação"),
        ("RESUMO_ATUALIZACAO_V1_3_0.md", "Resumo técnico"),
        ("CHANGELOG.md", "Changelog (deve ter v1.3.0)"),
        ("RESUMO_FINAL.md", "Resumo final (deve ter v1.3.0)"),
        ("README.md", "README (deve mencionar v1.3.0)")
    ]

    resultados = []
    for arquivo, descricao in arquivos_doc:
        existe = os.path.exists(arquivo)

        if existe:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            tem_v130 = '1.3.0' in conteudo

            if tem_v130:
                print(f"  ✓ {descricao}")
                resultados.append(True)
            else:
                print(f"  ⚠ {descricao} (existe mas não menciona v1.3.0)")
                resultados.append(False)
        else:
            print(f"  ✗ {descricao} (não encontrado)")
            resultados.append(False)

    total = len(arquivos_doc)
    sucesso = sum(resultados)
    print(f"\nResultado: {sucesso}/{total} documentos OK")

    return all(resultados)


def validar_estrutura():
    """Valida estrutura de diretórios"""
    print("\n" + "="*60)
    print("5. Validando Estrutura de Diretórios")
    print("="*60)

    diretorios = [
        "config",
        "utils",
        "scripts/cielo",
        "scripts/pagarme",
        "scripts/final"
    ]

    for diretorio in diretorios:
        existe = os.path.exists(diretorio) and os.path.isdir(diretorio)
        status = "✓" if existe else "✗"
        print(f"  {status} {diretorio}/")

    return all(os.path.exists(d) for d in diretorios)


def gerar_relatorio_final(resultados):
    """Gera relatório final da validação"""
    print("\n" + "="*60)
    print("RELATÓRIO FINAL DA VALIDAÇÃO v1.3.0")
    print("="*60)

    categorias = [
        ("Módulo de Leitura", resultados['modulo']),
        ("Scripts de Transformação", resultados['scripts']),
        ("Notebook Colab", resultados['notebook']),
        ("Documentação", resultados['documentacao']),
        ("Estrutura", resultados['estrutura'])
    ]

    for categoria, sucesso in categorias:
        status = "✅" if sucesso else "❌"
        print(f"{status} {categoria}")

    total_sucesso = sum(1 for _, sucesso in categorias if sucesso)
    total = len(categorias)

    print("\n" + "="*60)
    print(f"RESULTADO: {total_sucesso}/{total} categorias validadas")
    print("="*60)

    if total_sucesso == total:
        print("\n🎉 SUCESSO! Todas as validações passaram!")
        print("\n✅ v1.3.0 implementada corretamente")
        print("\nPróximos passos:")
        print("  1. Testar com arquivos reais")
        print("  2. Executar pipeline completo")
        print("  3. Validar outputs")
        return True
    else:
        print("\n⚠️ ATENÇÃO! Algumas validações falharam")
        print("\nRevisar:")
        for categoria, sucesso in categorias:
            if not sucesso:
                print(f"  - {categoria}")
        return False


def main():
    """Executa todas as validações"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   VALIDAÇÃO DE IMPLEMENTAÇÃO v1.3.0                   ║
    ║   Pipeline ETL Adquirentes                            ║
    ╚════════════════════════════════════════════════════════╝
    """)

    resultados = {
        'modulo': validar_modulo_leitura(),
        'scripts': validar_scripts_transformacao(),
        'notebook': validar_notebook(),
        'documentacao': validar_documentacao(),
        'estrutura': validar_estrutura()
    }

    sucesso = gerar_relatorio_final(resultados)

    sys.exit(0 if sucesso else 1)


if __name__ == '__main__':
    main()
