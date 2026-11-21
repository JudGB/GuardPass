credenciais ={}

nome   = input("Nome do app ou sistema: ")
login  = input("Digite seu login: ")
data_c = input("Digite a data de criação da senha: ")
data_e = 0 #quando chegar nessa data você tem que trocar a senha
infos  = input("Digite informações adicionais: ") #opcional

credenciais[nome] = {
    "login": login,
    "data_c": data_c,
    "data_e": data_e,
    "infos": infos
}

busca = input("Digite o nome do app ou sistema que deseja buscar: ")

while True:
    if busca in credenciais:
        val_e = int(credenciais[busca]['data_c'][0:1])
        print(f"Login para {busca}: {credenciais[busca]['login']}")
        print(f"Data de criação: {credenciais[busca]['data_c']}")
        print(f"Data de expiração: {val_e + 10}")
        print(f"Informações adicionais: {credenciais[busca]['infos']}")
        exit()
    else:
        print("App ou sistema não encontrado.")
    busca = input("Digite o nome do app ou sistema que deseja buscar: ")