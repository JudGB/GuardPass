from datetime import datetime, timedelta #para mexer nas datas
from getpass import getpass #para digitar as senhas sem mostrar
from cryptography.exceptions import InvalidTag #para tratar erros de senha incorreta
from cofre.cofre_definitivo import carregar_cofre, salvar_cofre #para acessar essas funções do cofre
from time import sleep #para dar uma pausa no programa

 
def add_nova_senha(credenciais):
    #inicio da verificação da senha mestra para abrir o cofre
    senha_mestre = getpass("\nDigite a senha mestra para cadastrar: ", echo_char="*")

    try:
        credenciais, chave, salt = carregar_cofre(senha_mestre)
    except InvalidTag:
        print("Senha mestra incorreta ou cofre alterado.")
        return
    except (OSError, ValueError) as erro:
        print(f"Não foi possível abrir o cofre: {erro}")
        return
    #fim da verificação da senha mestra para abrir o cofre

    #Sistema de cadastro de senha
    while True:
        print("\n================================\n")
        nome = input("Nome do app ou sistema: ").strip()

        if not nome:
            print("Digite um nome para identificar a conta.")
        elif nome in credenciais:
            print("App ou sistema já cadastrado. Escolha outro nome.")
        elif nome == "0":
            print("0 é reservado para a função de retornar")
            return
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

    gerador = input("Deseja gerar uma senha aleatória? (s/n): ").strip().lower()
    if gerador == 's':
        import secrets
        import string
        tamanho = 12  # Tamanho da senha aleatória
        caracteres = string.ascii_letters + string.digits + string.punctuation
        senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        print(f"Senha gerada: {senha}") 
    else:    
        senha = getpass("Digite a senha da conta: ", echo_char="*")
    data_n = datetime.today().strftime("%d/%m/%Y")

    confirmacao = input("Você confirma o cadastro? (s/n): ").strip().lower()
    if confirmacao != 's':  
        print("Cadastro cancelado.")
        return
        

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