from datetime import datetime, timedelta
from getpass import getpass

from cryptography.exceptions import InvalidTag
from cofre.cofre_definitivo import carregar_cofre, salvar_cofre


def add_nova_senha(credenciais):
    senha_mestre = getpass("Digite a senha mestra para cadastrar: ", echo_char="*")

    try:
        credenciais, chave, salt = carregar_cofre(senha_mestre)
    except InvalidTag:
        print("Senha mestra incorreta ou cofre alterado.")
        return
    except (OSError, ValueError) as erro:
        print(f"Não foi possível abrir o cofre: {erro}")
        return

    while True:
        nome = input("Nome do app ou sistema: ").strip()

        if not nome:
            print("Digite um nome para identificar a conta.")
        elif nome in credenciais:
            print("App ou sistema já cadastrado. Escolha outro nome.")
        else:
            break

    login = input("Digite seu login: ")

    while True:
        try:
            data_c = input("Data de criação da senha (dd/mm/aaaa): ")
            data_c = datetime.strptime(data_c, "%d/%m/%Y").date()
            data_e = data_c + timedelta(days=30)
            break
        except (ValueError, OverflowError):
            print("Digite uma data válida que permita calcular a expiração.")

    infos = input("Digite informações adicionais: ")
    senha = getpass("Digite a senha da conta: ", echo_char="*")
    data_n = datetime.today().strftime("%d/%m/%Y")

    credenciais[nome] = {
        "login": login,
        "data_c": data_c.strftime("%d/%m/%Y"),
        "data_e": data_e.strftime("%d/%m/%Y"),
        "infos": infos,
        "senha": senha,
        "data_n": data_n,
    }

    try:
        salvar_cofre(credenciais, chave, salt)
    except OSError as erro:
        print(f"Não foi possível salvar o cadastro: {erro}")
        return

    print(f"Senha cadastrada com sucesso para {nome}!")