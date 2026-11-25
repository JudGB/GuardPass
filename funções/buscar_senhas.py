import threading
from time import sleep, time #para dar uma pausa no programa
from datetime import datetime, timedelta #para mexer nas datas
from getpass import getpass #para digitar as senhas sem mostrar
from cofre.cofre_definitivo import abrir_cofre #para abrir o cofre
from cryptography.exceptions import InvalidTag
from pyperclip import copy #para copiar a senha para a área de transferência
from threading import * #para criar uma thread que vai limpar a área de transferência depois de 40 segundos

def buscar_senhas(credenciais):
    while True:
        senha_mestra = getpass("\nDigite a senha mestra para abrir o cofre: ", echo_char='*')

        try:
            credenciais = abrir_cofre(senha_mestra)

        except InvalidTag:
            print("Não foi possível abrir: senha incorreta ou arquivo alterado.")
            sleep(2) #pausa de 2 segundos
            break

        except FileNotFoundError:
            print("Arquivo de credenciais não encontrado.")
            sleep(2) #pausa de 2 segundos
            break
        
        except (OSError, ValueError) as erro:
            print(f"Não foi possível ler o cofre: {erro}")
            return

        if not credenciais:
            print("Nenhum app ou sistema cadastrado.")
            sleep(2) #pausa de 2 segundos
            break

        print("\nsistemas ou apps cadastrados: ")
                
        for i in credenciais.keys():
            print(f"- {i}")

        busca = input("\nDigite o nome do app ou sistema que deseja buscar: ")
        if busca in credenciais:
            #val_e = int(credenciais[busca]['data_c'][0:1])
            #pega a data de criação da senha e adiciona 30 dias para saber quando expira
            print(f"\nLogin para {busca}: {credenciais[busca]['login']}")
            print(f"Data de criação: {credenciais[busca]['data_c']}")
            print(f"Data de expiração: {credenciais[busca]['data_e']}")
            print(f"Informações adicionais: {credenciais[busca]['infos']}")
            print(f"Data de cadastro da senha: {credenciais[busca]['data_n']}\n")

            print("Deseja mostrar a senha? (s/n)")
            mostrar_senha = input().lower()
            if mostrar_senha == "s":
                print(f"Senha: {credenciais[busca]['senha']}\n")

            copiar_senha = input("Deseja copiar a senha para a área de transferência? (s/n): ").lower()
            if copiar_senha == "s": 
                copy(credenciais[busca]['senha'])
                print("Senha copiada para a área de transferência\n")

            sair = input("enter para sair...")
            if sair == "":
                sleep(2) #pausa de 2 segundos
                break
        elif busca == "0":
            print("Voltando...")
            sleep(2) #pausa de 2 segundos
            break

        else:
            print("App ou sistema não encontrado.")
            sleep(2) #pausa de 2 segundos
            break