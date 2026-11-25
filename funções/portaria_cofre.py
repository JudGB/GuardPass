from datetime import datetime, timedelta #para mexer nas datas
from getpass import getpass #para digitar as senhas sem mostrar
from time import sleep #para dar uma pausa no programa
from cryptography.exceptions import InvalidTag
from cofre.cofre_definitivo import * #para abrir o cofre
from secrets import token_bytes
import json
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def iniciar_guardpass():
    if ARQUIVO_COFRE.exists():
        senha_mestre = getpass("\nDigite a senha mestra para entrar: ", echo_char="*")
        return abrir_cofre(senha_mestre)

    print("Primeiro acesso ao GuardPass.")

    while True:
        senha_mestre = getpass("Crie sua senha mestra: ")

        if not senha_mestre:
            print("A senha mestra não pode ficar vazia.")
            continue

        confirmacao = getpass("Digite a senha mestra novamente: ")

        if senha_mestre != confirmacao:
            print("As senhas ficaram diferentes. Tente novamente.")
            continue

        criar_cofre(senha_mestre)
        print("Cofre criado com sucesso!")
        return {}

