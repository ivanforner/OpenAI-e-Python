import openai

from gerador_casos_uso import *
from gerador_cenario_teste import *
from gerador_script_teste import *
from tools import *
from assistente_projeto import *
from criador_usuarios_de_teste import *


def main():
    pedido_usuario = input("Digite um caso de uso: ")
    pagina_considerada = 'index'

    try:
        # vector_store = criar_vector_store()
        # subir_arquivos(vector_store_id=vector_store.id)

        assistente = criar_assistente()
        assistente = atualiza_assistente(assistente, "vs_ZOLsR0CK276Jp5IEC7e0hY94")

        thread = criar_thread()

        caso_uso = gerar_caso_uso(pedido_usuario, assistente, thread)
        print("\nCaso de Uso:\n", caso_uso)

        cenario_teste = gerar_cenario_teste(caso_uso, assistente, thread)
        print("\nCenário de teste\n", cenario_teste)

        script_teste = gerar_script_teste(cenario_teste, assistente, thread)
        print("\nScript de Teste\n", cenario_teste)

        salva(f"scripts_gerados/script_{pagina_considerada}.py", script_teste)

        apagar_thread(thread.id)
        apagar_assistente(assistente.id)
        # apagar_vector_store("vs_ZOLsR0CK276Jp5IEC7e0hY94")

    except openai.APIError as error:
        print(error)


if __name__ == "__main__":
    main()
