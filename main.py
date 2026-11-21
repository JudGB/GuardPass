from datetime import datetime, timedelta #para mexer nas datas
from getpass import getpass #para digitar as senhas sem mostrar

credenciais ={}

nome   = input("Nome do app ou sistema: ")
login  = input("Digite seu login: ")
data_c = input("Digite a data de criação da senha: dd/mm/aaaa: ")
data_c = datetime.strptime(data_c, "%d/%m/%Y").date()
data_e = data_c + timedelta(days=30) #quando chegar nessa data você tem que trocar a senha
infos  = input("Digite informações adicionais: ") #opcional
senha  = getpass("Digite sua senha: ", echo_char='*')

credenciais[nome] = {
    "login": login,
    "data_c": data_c.strftime("%d/%m/%Y"),
    "data_e": data_e.strftime("%d/%m/%Y"),
    "infos": infos,
    "senha": senha
}

busca = input("Digite o nome do app ou sistema que deseja buscar: ")

while True:
    if busca in credenciais:
        #val_e = int(credenciais[busca]['data_c'][0:1])
        #pega a data de criação da senha e adiciona 30 dias para saber quando expira
        print(f"Login para {busca}: {credenciais[busca]['login']}")
        print(f"Data de criação: {credenciais[busca]['data_c']}")
        print(f"Data de expiração: {credenciais[busca]['data_e']}")
        print(f"Informações adicionais: {credenciais[busca]['infos']}")
        print(f"Senha: {credenciais[busca]['senha']}")

        break
        
    else:
        print("App ou sistema não encontrado.")
    busca = input("Digite o nome do app ou sistema que deseja buscar: ")