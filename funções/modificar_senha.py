from time import sleep #para dar uma pausa no programa
from datetime import datetime, timedelta
from getpass import getpass #para digitar as senhas sem mostrar
from cofre.cofre_definitivo import carregar_cofre, salvar_cofre #para abrir e salvar o cofre
from cryptography.exceptions import InvalidTag #para tratar erros de senha incorreta
import json
from datetime import date

def modificar_senhas(credenciais):

    senha_mestre = getpass("Digite a senha mestra para modificar: ", echo_char="*")
    
    try:
        credenciais, chave, salt = carregar_cofre(senha_mestre)
    except InvalidTag:
        print("Senha mestra incorreta ou cofre alterado.")
        return
    except (OSError, ValueError) as erro:
        print(f"Não foi possível abrir o cofre: {erro}")
        return

    while True:
        print("sistemas ou apps cadastrados: ")
        if not credenciais:
            print("Nenhum app ou sistema cadastrado.")
            sleep(2) #pausa de 2 segundos
            break

        for i in credenciais.keys():
            print(i)

        modificar = input("Digite o nome do app ou sistema que deseja modificar: ")

        if not modificar:
            print("Digite um nome para identificar a conta.")
            sleep(2) #pausa de 2 segundos
            return
        elif modificar not in credenciais:
            print("App ou sistema não cadastrado.")
            sleep(2) #pausa de 2 segundos
            return
        

        print("1 - Modificar login")
        print("2 - Modificar informações adicionais")
        print("3 - Modificar senha")
        print("4 - Modificar data de criação da senha")
        print("0 - Voltar")

        opcao_modificar = input("Escolha uma opção: ")

        if opcao_modificar == "0":
            print("Voltando...")
            sleep(2) #pausa de 2 segundos
            break

        elif opcao_modificar == "1":

            print(f"Login antigo: {credenciais[modificar]['login']}")
            if modificar in credenciais:
                novo_login = input("Digite o novo login: ")
                credenciais[modificar]['login'] = novo_login
                try:
                    salvar_cofre(credenciais, chave, salt)
                except OSError as erro:
                    print(f"Não foi possível salvar o cadastro: {erro}")
                    return
                print(f"Login modificado com sucesso para {modificar}!")
                sleep(2) #pausa de 2 segundos
                break

        elif opcao_modificar == "2":
            print(f"Informações adicionais antigas: {credenciais[modificar]['infos']}")
            if modificar in credenciais:
                novas_infos = input("Digite as novas informações adicionais: ")
                credenciais[modificar]['infos'] = novas_infos

                try:
                    salvar_cofre(credenciais, chave, salt)
                except OSError as erro:
                    print(f"Não foi possível salvar o cadastro: {erro}")
                    return
                
                print(f"Informações adicionais modificadas com sucesso para {modificar}!")
                sleep(2) #pausa de 2 segundos
                break

        elif opcao_modificar == "3":
            senha_atual = getpass("Digite a senha atual: ", echo_char='*')
            if senha_atual != credenciais[modificar]['senha']:
                print("senha incorreta!")
                sleep(2)
                continue

            else:
                mostrar_senha = input("Deseja mostrar a senha atual? (s/n): ").lower()

                if mostrar_senha == "s":
                    print(f"Senha antiga: {credenciais[modificar]['senha']}")
                
                if modificar in credenciais:
                    nova_senha = getpass("Digite a nova senha: ", echo_char='*')
                    credenciais[modificar]['senha'] = nova_senha
                    try:
                        salvar_cofre(credenciais, chave, salt)
                    except OSError as erro:
                        print(f"Não foi possível salvar o cadastro: {erro}")
                        return

                    print(f"Senha modificada com sucesso para {modificar}!")
                    sleep(2) #pausa de 2 segundos
                    break

        elif opcao_modificar == "4":
            print(f"Data de criação antiga: {credenciais[modificar]['data_c']}")
            print(f"Data de expedição antiga: {credenciais[modificar]['data_e']}")
            if modificar in credenciais:
                nova_data_c = input("Digite a nova data de criação da senha (DD/MM/AAAA): ")

                try:
                    nova_data_c = datetime.strptime(nova_data_c, "%d/%m/%Y").date()
                    nova_data_e = nova_data_c + timedelta(days=30)
                except (ValueError, OverflowError):
                    print("Digite uma data válida que permita calcular a expiração.")
                    return

                credenciais[modificar]['data_c'] = nova_data_c.strftime("%d/%m/%Y")
                credenciais[modificar]['data_e'] = nova_data_e .strftime("%d/%m/%Y")

                try:
                    salvar_cofre(credenciais, chave, salt)
                except OSError as erro:
                    print(f"Não foi possível salvar o cadastro: {erro}")
                    return
                

                print(f"Data de criação da senha modificada com sucesso para {modificar}!")
                sleep(2) #pausa de 2 segundos
                break

        else:
            print("App ou sistema não encontrado.")
            sleep(2) #pausa de 2 segundos
            break

        print("credencial modificada com sucesso!")
        sleep(2) #pausa de 2 segundos
        break