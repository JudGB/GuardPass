from datetime import datetime, timedelta #para mexer nas datas
from getpass import getpass #para digitar as senhas sem mostrar
from menu import exibir_menu #importando o menu
from time import sleep #para dar uma pausa no programa
from cryptography.exceptions import InvalidTag
from cofre import abrir_cofre #para abrir o cofre

credenciais ={}


while True:
    exibir_menu()
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
        nome   = input("Nome do app ou sistema: ")
        if nome in credenciais:
            print("App ou sistema já cadastrado.")
            sleep(2) #pausa de 2 segundos
            continue
        login  = input("Digite seu login: ")
        data_c = input("Digite a data de criação da senha: dd/mm/aaaa: ")
        data_c = datetime.strptime(data_c, "%d/%m/%Y").date()
        data_e = data_c + timedelta(days=30) #quando chegar nessa data você tem que trocar a senha
        infos  = input("Digite informações adicionais: ") #opcional
        senha  = getpass("Digite sua senha: ", echo_char='*')
        data_n = datetime.today().strftime("%d/%m/%Y") #data de cadastro da senha

        credenciais[nome] = {
            "login": login,
            "data_c": data_c.strftime("%d/%m/%Y"),
            "data_e": data_e.strftime("%d/%m/%Y"),
            "infos": infos,
            "senha": senha,
            "data_n": data_n
        }

        print(f"Senha cadastrada com sucesso para {nome}!")
        sleep(2) #pausa de 2 segundos

        continue

    elif opcao == "2":
        senha_mestra = getpass("Digite a senha mestra para abrir o cofre: ")

        try:
            contas_salvas = abrir_cofre(senha_mestra)

        except InvalidTag:
            print("Não foi possível abrir: senha incorreta ou arquivo alterado.")
            sleep(2) #pausa de 2 segundos
            continue

        except FileNotFoundError:
            print("Arquivo de credenciais não encontrado.")
            sleep(2) #pausa de 2 segundos
            continue

        for i in credenciais.keys():
            print(i)

        busca = input("Digite o nome do app ou sistema que deseja buscar: ")
        if busca in credenciais:
            #val_e = int(credenciais[busca]['data_c'][0:1])
            #pega a data de criação da senha e adiciona 30 dias para saber quando expira
            print(f"Login para {busca}: {credenciais[busca]['login']}")
            print(f"Data de criação: {credenciais[busca]['data_c']}")
            print(f"Data de expiração: {credenciais[busca]['data_e']}")
            print(f"Informações adicionais: {credenciais[busca]['infos']}")
            print(f"Senha: {credenciais[busca]['senha']}")
            print(f"Data de cadastro da senha: {credenciais[busca]['data_n']}")

            sair = input("enter para sair...")
            if sair == "":
                sleep(2) #pausa de 2 segundos
                continue

        else:
            print("App ou sistema não encontrado.")
            sleep(2) #pausa de 2 segundos
            continue

    elif opcao == "3":
        print("sistemas ou apps cadastrados: ")
        if not credenciais:
            print("Nenhum app ou sistema cadastrado.")
            sleep(2) #pausa de 2 segundos
            continue
        for i in credenciais.keys():
            print(i)

        remover = input("Digite o nome do app ou sistema que deseja remover: ")
        if remover in credenciais:
            del credenciais[remover]
            print(f"Senha removida com sucesso para {remover}!")
            sleep(2) #pausa de 2 segundos
            continue

        elif remover == "0":
            print("Voltando...")
            sleep(2) #pausa de 2 segundos
            continue

        else:
            print("App ou sistema não encontrado.")
            sleep(2) #pausa de 2 segundos
            continue

    elif opcao == "4":
        print("sistemas ou apps cadastrados: ")
        if not credenciais:
            print("Nenhum app ou sistema cadastrado.")
            sleep(2) #pausa de 2 segundos
            continue
        for i in credenciais.keys():
            print(i)

        modificar = input("Digite o nome do app ou sistema que deseja modificar: ")

        print("1 - Modificar login")
        print("2 - Modificar informações adicionais")
        print("3 - Modificar senha")
        print("4 - Modificar data de criação da senha")
        print("0 - Voltar")

        opcao_modificar = input("Escolha uma opção: ")

        if opcao_modificar == "0":
            print("Voltando...")
            sleep(2) #pausa de 2 segundos
            continue

        elif opcao_modificar == "1":
            if modificar in credenciais:
                novo_login = input("Digite o novo login: ")
                credenciais[modificar]['login'] = novo_login
                print(f"Login modificado com sucesso para {modificar}!")
                sleep(2) #pausa de 2 segundos
                continue

        elif opcao_modificar == "2":
            if modificar in credenciais:
                novas_infos = input("Digite as novas informações adicionais: ")
                credenciais[modificar]['infos'] = novas_infos
                print(f"Informações adicionais modificadas com sucesso para {modificar}!")
                sleep(2) #pausa de 2 segundos
                continue

        elif opcao_modificar == "3":
            if modificar in credenciais:
                nova_senha = getpass("Digite a nova senha: ", echo_char='*')
                credenciais[modificar]['senha'] = nova_senha
                print(f"Senha modificada com sucesso para {modificar}!")
                sleep(2) #pausa de 2 segundos
                continue

        elif opcao_modificar == "4":
            if modificar in credenciais:
                nova_data = input("Digite a nova data de criação da senha (DD/MM/AAAA): ")
                credenciais[modificar]['data'] = nova_data
                print(f"Data de criação da senha modificada com sucesso para {modificar}!")
                sleep(2) #pausa de 2 segundos
                continue

        else:
            print("App ou sistema não encontrado.")
            sleep(2) #pausa de 2 segundos
            continue

        print("credencial modificada com sucesso!")
        sleep(2) #pausa de 2 segundos

    elif opcao == "5":
                print("Saindo do programa...")
                sleep(2) #pausa de 2 segundos
                exit()
        
    