import json
from pathlib import Path
from argon2.low_level import Type, hash_secret_raw #para usar a função de hash do Argon2
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from secrets import token_bytes

ARQUIVO_COFRE = Path(__file__).with_name("guardpass.bin")


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

def criar_cofre(senha_mestre):
    salt = token_bytes(16)
    nonce = token_bytes(12)
    chave = gerar_chave(senha_mestre, salt)

    credenciais = {}
    dados = json.dumps(credenciais).encode("utf-8")
    cifrado = AESGCM(chave).encrypt(nonce, dados, None)

    with ARQUIVO_COFRE.open("xb") as f:
        f.write(salt)
        f.write(nonce)
        f.write(cifrado)

def carregar_cofre(senha_mestre):
    with ARQUIVO_COFRE.open("rb") as f:
        salt = f.read(16)
        nonce = f.read(12)
        cifrado = f.read()

    if len(salt) != 16 or len(nonce) != 12 or len(cifrado) < 16:
        raise ValueError("O arquivo do cofre está incompleto.")

    chave = gerar_chave(senha_mestre, salt)
    dados = AESGCM(chave).decrypt(nonce, cifrado, None)

    credenciais = json.loads(dados.decode("utf-8"))
    return credenciais, chave, salt

    
def abrir_cofre(senha_mestre):
    credenciais, _, _ = carregar_cofre(senha_mestre)
    return credenciais

def salvar_cofre(credenciais, chave, salt):
    nonce = token_bytes(12)
    dados = json.dumps(credenciais, ensure_ascii=False).encode("utf-8")
    cifrado = AESGCM(chave).encrypt(nonce, dados, None)

    temporario = ARQUIVO_COFRE.with_suffix(".tmp")

    with temporario.open("wb") as f:
        f.write(salt)
        f.write(nonce)
        f.write(cifrado)

    temporario.replace(ARQUIVO_COFRE)


