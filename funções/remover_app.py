from time import sleep
from getpass import getpass

from cryptography.exceptions import InvalidTag
from cofre.cofre_definitivo import carregar_cofre, salvar_cofre




def remover_apps(credenciais):

    senha_mestre = getpass("\nDigite a senha mestra para remover: ", echo_char="*")

    try:
        credenciais, chave, salt = carregar_cofre(senha_mestre)
    except InvalidTag:
        print("Senha mestra incorreta ou cofre alterado.")
        return
    except (OSError, ValueError) as erro:
        print(f"Não foi possível abrir o cofre: {erro}")
        return

    while True:
        print("\nsistemas ou apps cadastrados: ")
        if not credenciais:
            print("Nenhum app ou sistema cadastrado.")
            sleep(2) #pausa de 2 segundos
            break

        for i in credenciais.keys():
            print(f"- {i}")

        remover = input("\nDigite o nome do app ou sistema que deseja remover: ")
        if remover in credenciais:
            credenciais.pop(remover, None)
            try:
                salvar_cofre(credenciais, chave, salt)
            except OSError as erro:
                print(f"Não foi possível salvar o cadastro: {erro}")
                return

            print(f"Senha removida com sucesso para {remover}!")
            sleep(2) #pausa de 2 segundos
            break

        elif remover == "0":
            print("Voltando...")
            sleep(2) #pausa de 2 segundos
            break

        else:
            print("App ou sistema não encontrado.")
            sleep(2) #pausa de 2 segundos
            break