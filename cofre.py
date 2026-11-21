import json
from pathlib import Path
from argon2.low_level import Type, hash_secret_raw #para usar a função de hash do Argon2
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


#aqui vou pegar minha senha e transformar ela em unica e deixar no jeitinho que o AES
#pode usar e assim virar de fato a chave de tudo
def gerar_chave(senha_mestre, salt):
    chave = hash_secret_raw(
        secret=senha_mestre.encode('utf-8'), #transforma a senha mestre em bytes
        salt=salt, #transforma o salt em bytes
        #salt é uma sequencia de numeros aleatoria que possibilita
        #que a mesma senha mestre gere senhas diferentes para cada app ou sistema
        #pois a senha + salt é que gera um hash unico para cada app ou sistema
        time_cost=2, #tempo de execução do algoritmo, vai passar 2 vezes pelo algoritmo
        memory_cost = 65536, #espaço que vai usar na memoria, 65536 bytes = 64kb
        parallelism = 2, #total de partes que é dividido todo o processo e memoria
        hash_len = 32, #32 bytes = 256 bits, tamanho do hash que vai ser gerado
        type = Type.ID 
    )

    return chave

def abrir_cofre(senha_mestre):
    arquivo = Path(__file__).with_name("credenciais_teste.bin")

    with arquivo.open("rb") as f:
        salt = f.read(16)
        nonce = f.read(12)
        cifrado = f.read()

    chave = gerar_chave(senha_mestre, salt)
    dados = AESGCM(chave).decrypt(nonce, cifrado, None)
    credenciais = json.loads(dados.decode("utf-8"))

    return credenciais

if __name__ == "__main__":
    from getpass import getpass
    from pathlib import Path
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    arquivo = Path(__file__).with_name("credenciais_teste.bin")

    with arquivo.open("rb") as f:
        salt = f.read(16)
        nonce = f.read(12)
        cifrado = f.read()

    senha_mestre = getpass("Digite a senha mestra para abrir o cofre: ")
    chave = gerar_chave(senha_mestre, salt)

    try:
        dados = AESGCM(chave).decrypt(nonce, cifrado, None)
        # Bytes → texto JSON → dicionário
        credenciais = json.loads(dados.decode("utf-8"))
        print("Login recuperado:", credenciais["GitHub"]["login"])
    except InvalidTag:
        print("Não foi possível abrir: senha incorreta ou arquivo alterado.")