from openai import OpenAI
from tools import *
from dotenv import load_dotenv
import os
from assistente_projeto import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def criar_usuarios_teste(cenario_teste, assistente, modelo=MODELO_GPT_4):
    prompt_sistema = f"""
        Você é um assistente útil projetado para gerar saídas em JSON.
        
        Você deve gerar um conjunto de dados de teste em formato JSON que serão utilizados com Selenium e Python para simular e aprovar a navegabilidade de uma aplicação.
        Faça isso com base no cenário de teste: {cenario_teste}
        
        Consulte o Vector Store para verificar os dados corretos de autenticação. 
        
        Gere quatro casos distintos de teste, com apenas um deles resultando em 'Aprovado'.
        Lembre-se de que os dados gerados devem ser em formato JSON válido.
    
        Inclua explicitamente na sua resposta o formato JSON esperado para os casos de teste.
    """

    thread = criar_thread()

    cliente.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=prompt_sistema
    )

    run = cliente.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistente.id,
        tools=[{"type": "file_search"}],
        model=modelo,
        response_format={ "type": "json_object" }
    )

    run = cliente.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    while run.status != STATUS_COMPLETED:
        run = cliente.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if run.status == STATUS_FAILED:
            raise Exception('OpenAI falhou!')

    mensagens = cliente.beta.threads.messages.list(
        thread_id=thread.id
    )

    apagar_thread(thread.id)

    return mensagens.data[0].content[0].text.value
