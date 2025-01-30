from gerador_casos_uso import *
from gerador_cenario_teste import *
from gerador_script_teste import *
from tools import *


def main():
    pedido_usuario = input("Digite um caso de uso: ")

    casos_uso = gerar_caso_uso(pedido_usuario, MODELO_GPT)
    print(casos_uso)

    casos_uso_refinado = gerar_caso_uso(pedido_usuario, MODELO_REFINADO)
    print("CASO DE USO REFINADO:")
    print(casos_uso_refinado)
    # cenario_teste = gerar_cenario_teste(casos_uso)
    # script_teste = gerar_script_teste(casos_uso, cenario_teste)
    # salva('script_temp_ia.py', script_teste)


if __name__ == "__main__":
    main()
