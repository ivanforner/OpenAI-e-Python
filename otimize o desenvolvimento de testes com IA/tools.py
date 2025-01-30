MODELO_REFINADO = "ft:gpt-3.5-turbo-1106:yp::AvOXLBxZ"
MODELO_GPT = "gpt-3.5-turbo-1106"


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f'Erro no carregamento de arquivo: ({e})')


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f'Erro ao salvar arquivo: ({e})')
