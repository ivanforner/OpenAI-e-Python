from openai import OpenAI
from tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_caso_uso(prompt, assistente, thread, modelo=MODELO_GPT_4):
    pergunta = f"""Gere um caso de uso para: {prompt}. 
        
        Utilize o arquivo "exemplos_casos_uso.txt" do vector store associado.
    
        Adote o formato de saída abaixo.
    
        # Formato de Saída
    
        *Nome da Persona*, em *contexto do app*, precisa realizar *tarefa no app* no aplicativo. Logo, *Beneficio Esperado*, para isso ela *descrição detalhada da tarefa realizada*.
    """

    cliente.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=pergunta
    )

    run = cliente.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistente.id,
        tools=[{"type": "file_search"}],
        model=modelo
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

    return mensagens.data[0].content[0].text.value
