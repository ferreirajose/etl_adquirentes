# Funções para leitura de arquivos em múltiplos formatos
import pandas as pd
import os


def ler_arquivo_excel_ou_csv(caminho_arquivo, **kwargs):
    """
    Lê arquivo Excel (.xlsx, .xls) ou CSV (.csv) automaticamente
    baseado na extensão do arquivo

    Args:
        caminho_arquivo: Path completo do arquivo
        **kwargs: Argumentos adicionais para pd.read_excel ou pd.read_csv
                  (skiprows, sep, decimal, etc.)

    Returns:
        DataFrame do pandas

    Raises:
        FileNotFoundError: Se arquivo não existir
        ValueError: Se extensão não for suportada

    Exemplos:
        df = ler_arquivo_excel_ou_csv('dados.xlsx', skiprows=9)
        df = ler_arquivo_excel_ou_csv('dados.csv', sep=';', decimal=',')
        df = ler_arquivo_excel_ou_csv('dados.xls', skiprows=4)
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    # Detectar extensão
    _, extensao = os.path.splitext(caminho_arquivo)
    extensao = extensao.lower()

    # Ler conforme extensão
    if extensao in ['.xlsx', '.xls']:
        # Excel - filtrar argumentos que não são aceitos por read_excel
        excel_kwargs = {k: v for k, v in kwargs.items()
                       if k not in ['sep', 'decimal', 'low_memory']}
        return pd.read_excel(caminho_arquivo, **excel_kwargs)
    elif extensao == '.csv':
        # CSV - usar defaults comuns se não especificados
        if 'sep' not in kwargs:
            kwargs['sep'] = ';'  # Padrão brasileiro
        if 'decimal' not in kwargs:
            kwargs['decimal'] = ','  # Padrão brasileiro
        return pd.read_csv(caminho_arquivo, **kwargs)
    else:
        raise ValueError(f"Extensão não suportada: {extensao}. Use .xlsx, .xls ou .csv")


def detectar_e_ler_arquivo(base_path, nome_base, extensoes_possiveis=['.xlsx', '.xls', '.csv'], **kwargs):
    """
    Tenta ler arquivo com diferentes extensões até encontrar um que existe

    Args:
        base_path: Diretório base
        nome_base: Nome do arquivo sem extensão (ex: 'Historico-de-vendas-pre_1')
        extensoes_possiveis: Lista de extensões para tentar (ordem de prioridade)
        **kwargs: Argumentos para leitura

    Returns:
        Tupla (DataFrame, extensao_encontrada) ou (None, None) se não encontrar

    Exemplo:
        df, ext = detectar_e_ler_arquivo(
            '/path/to/files',
            'Historico-de-vendas-pre_1',
            ['.xlsx', '.xls', '.csv'],
            skiprows=9
        )
        if df is not None:
            print(f"Arquivo encontrado com extensão: {ext}")
    """
    for extensao in extensoes_possiveis:
        caminho = os.path.join(base_path, nome_base + extensao)
        if os.path.exists(caminho):
            try:
                df = ler_arquivo_excel_ou_csv(caminho, **kwargs)
                return df, extensao
            except Exception as e:
                print(f"⚠ Erro ao ler {caminho}: {e}")
                continue

    return None, None


def listar_arquivos_por_extensao(diretorio, extensoes=['.xlsx', '.xls', '.csv']):
    """
    Lista todos os arquivos de um diretório com extensões específicas

    Args:
        diretorio: Path do diretório
        extensoes: Lista de extensões para filtrar

    Returns:
        Dict {extensao: [lista_de_arquivos]}

    Exemplo:
        arquivos = listar_arquivos_por_extensao('/path/to/dir')
        print(f"XLS: {len(arquivos['.xls'])} arquivos")
        print(f"XLSX: {len(arquivos['.xlsx'])} arquivos")
        print(f"CSV: {len(arquivos['.csv'])} arquivos")
    """
    resultado = {ext: [] for ext in extensoes}

    if not os.path.exists(diretorio):
        return resultado

    for arquivo in os.listdir(diretorio):
        _, ext = os.path.splitext(arquivo)
        ext = ext.lower()
        if ext in extensoes:
            resultado[ext].append(arquivo)

    return resultado


def salvar_arquivo_excel_ou_csv(df, caminho_arquivo, **kwargs):
    """
    Salva DataFrame em Excel ou CSV baseado na extensão

    Args:
        df: DataFrame do pandas
        caminho_arquivo: Path completo do arquivo
        **kwargs: Argumentos para to_excel ou to_csv

    Exemplo:
        salvar_arquivo_excel_ou_csv(df, 'saida.xlsx', index=False)
        salvar_arquivo_excel_ou_csv(df, 'saida.csv', sep=';', decimal=',', index=False)
    """
    _, extensao = os.path.splitext(caminho_arquivo)
    extensao = extensao.lower()

    # Criar diretório se não existir
    diretorio = os.path.dirname(caminho_arquivo)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)

    if extensao in ['.xlsx', '.xls']:
        df.to_excel(caminho_arquivo, **kwargs)
    elif extensao == '.csv':
        # Defaults para CSV brasileiro
        if 'sep' not in kwargs:
            kwargs['sep'] = ';'
        if 'decimal' not in kwargs:
            kwargs['decimal'] = ','
        df.to_csv(caminho_arquivo, **kwargs)
    else:
        raise ValueError(f"Extensão não suportada: {extensao}")
