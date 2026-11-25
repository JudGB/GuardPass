from datetime import datetime, timedelta #para mexer nas datas
from getpass import getpass #para digitar as senhas sem mostrar
from Menus.menu import exibir_menu #importando o menu
from funções.criar_senha import * #importando opção 1
from time import sleep #para dar uma pausa no programa
from cryptography.exceptions import InvalidTag
from cofre.cofre_definitivo import * #para abrir o cofre
from funções.buscar_senhas import buscar_senhas
from secrets import token_bytes
import json
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from funções.portaria_cofre import *
from funções.remover_app import *
from funções.modificar_senha import *
from filelock import FileLock, Timeout

def executar_guardpass():

    try:
        credenciais = iniciar_guardpass()
    except InvalidTag:
        print("Não foi possível abrir o cofre: senha incorreta ou arquivo alterado.")
        raise SystemExit(1)
    except (OSError, ValueError) as erro:
        print(f"Não foi possível acessar o cofre: {erro}")
        raise SystemExit(1)

    # Seu while True com exibir_menu() continua aqui.
        

    while True:
        exibir_menu(credenciais)
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
        
            add_nova_senha(credenciais)

        elif opcao == "2":
            
            buscar_senhas(credenciais)

        elif opcao == "3":

            remover_apps(credenciais)

        elif opcao == "4":

            modificar_senhas(credenciais)

        elif opcao == "0":
                    print("Saindo do programa...")
                    sleep(2) #pausa de 2 segundos
                    exit()




if __name__ == "__main__":
    
    arquivo_lock = ARQUIVO_COFRE.with_suffix(".lock")

try:
    with FileLock(arquivo_lock, timeout=0):
        executar_guardpass()
except Timeout:
    print("Este cofre já está aberto em outra janela.")
