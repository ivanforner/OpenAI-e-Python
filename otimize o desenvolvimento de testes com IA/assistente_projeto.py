from openai import OpenAI
from tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def criar_vector_store():
    return cliente.beta.vector_stores.create(name="AcordLab Vector Store")


def criar_thread():
    return cliente.beta.threads.create()


def criar_assistente(modelo=MODELO_GPT_4):
    instrucoes = f"""
        Assuma que você é um assistente virtual especializado em orientar desenvolvedores e QA testers na criação de testes automatizados para aplicações web usando Python e Selenium. 
            
        Você deve oferecer suporte abrangente, desde o setup inicial do ambiente de desenvolvimento até a implementação 
        de testes complexos, adotando e consultando principalmente os documentos de sua
        base (para identificar padrões e formas de estruturar os scripts solicitados).

        Consulte sempre os arquivos html, css e js para elaborar um teste.
        
        Adicionalmente, você deve ser capaz de explicar conceitos chave de 
        testes automatizados e Selenium, fornecer templates de código personalizáveis, e oferecer feedback sobre scripts de teste escritos pelo usuário. 

        O objetivo é facilitar o aprendizado e a aplicação de testes automatizados, 
        melhorando a qualidade e a confiabilidade das aplicações web desenvolvidas.

        Caso solicitado a gerar um script, apenas gere ele sem outros comentários adicionais.

        Você também é um especialista em casos de uso, seguindo os templates indicados.
        E também é um especialista em gerar cenários de teste.
    """

    assistente = cliente.beta.assistants.create(
        name="Assistente Eng. Software",
        instructions=instrucoes,
        tools=[{"type": "file_search"}],
        model=modelo,
    )

    return assistente


def atualiza_assistente(assistente, vector_store_id):
    return cliente.beta.assistants.update(
        assistant_id=assistente.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
    )


def subir_arquivos(vector_store_id, diretorio="AcordeLab"):
    for caminho_diretorio, nomes_diretorios, nomes_arquivos in os.walk(diretorio):
        arquivos_web = [f for f in nomes_arquivos if f.endswith(('.html', '.css', '.js'))]

        for arquivo in arquivos_web:
            caminho_completo = os.path.join(caminho_diretorio, arquivo)
            with open(caminho_completo, 'rb') as arquivo_aberto:
                web_file = cliente.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store_id, files=[arquivo_aberto]
                )
                print(web_file.status)

    caminho_arquivo = "documentos/exemplo_caso_uso.txt"
    arquivo_exemplo_caso = cliente.beta.vector_stores.file_batches.upload_and_poll(
        files=[open(caminho_arquivo, "rb")],
        vector_store_id=vector_store_id
    )
    print(arquivo_exemplo_caso.status)


def apagar_thread(thread_id):
    cliente.beta.threads.delete(thread_id)


def apagar_vector_store(vector_id):
    cliente.beta.vector_stores.delete(vector_id)


def apagar_assistente(assistente_id):
    cliente.beta.assistants.delete(assistente_id)
