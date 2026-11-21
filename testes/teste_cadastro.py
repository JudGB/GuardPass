import json
from pathlib import Path
from getpass import getpass
from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cofre import gerar_chave

credenciais = {
    "GitHub": {
        "login": "judson_teste",
        "senha": "senha-ficticia",
        "data_c": "01/11/2026",
        "data_e": "01/12/2026",
        "infos": "Conta de demonstração",
        "data_n": "21/11/2026"
    }
}

senha_mestre = getpass("Crie a senha mestra deste teste: ")
salt = token_bytes(16)
nonce = token_bytes(12)
chave = gerar_chave(senha_mestre, salt)

# Dicionário → texto JSON → bytes
dados = json.dumps(credenciais, ensure_ascii=False).encode("utf-8")
cifrado = AESGCM(chave).encrypt(nonce, dados, None)

arquivo = Path(__file__).with_name("credenciais_teste.bin")

with arquivo.open("xb") as f:
    f.write(salt)
    f.write(nonce)
    f.write(cifrado)

print("Credencial salva em:", arquivo)