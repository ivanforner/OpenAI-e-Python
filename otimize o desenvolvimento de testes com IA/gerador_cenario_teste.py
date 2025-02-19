from openai import OpenAI
from tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_cenario_teste(caso_uso, assistente, thread, modelo=MODELO_GPT_4):
    pergunta = f""""
    Você é um especialista em desenvolver cenários de teste para validar uma aplicação web, quanto sua navegação.
    Para isso, considere o caso de uso destacado em: {caso_uso}.
    
    Utilize os arquivos do vector store para gerar a resposta.

    Seu caso de teste deve fornecer dados suficientes para validar uma aplicação HTML, CSS e JS e para que
    possa ser implementado usando Python e Selenium.
    """

    cliente.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=pergunta
    )

    run = cliente.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistente.id,
        tools=[{"type": "file_search"}],
        model=modelo
    )

    ran = cliente.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    while ran.status != STATUS_COMPLETED:
        print("Gerando Cenario: ", ran.status)
        ran = cliente.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if ran.status == STATUS_FAILED:
            raise Exception("OpenAI Falhou!")

    mensagens = cliente.beta.threads.messages.list(
        thread_id=thread.id
    )

    return mensagens.data[0].content[0].text.value
