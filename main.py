# print('Login: ', end='')
# user = input()
# print('Olá {user}, o que deseja fazer ?')
# print('A) Enviar uma mensagem')
# print('B) Ler mensagens do banco')

# Neste exemplo utilizamos o Fernet com o uma lib encapsulada que já contem
# todos os pacotes necessários para usar o modo CBC.
# Não precisamos informar uma chave criptografada, neste caso a chave é gerada
# (podemos exibí-la).

import base64
import hashlib
import os
from cryptography.fernet import Fernet
import json

# Conexão com o MongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# para gerar uma chave no fernet precisamos
# garantir que essa "string" depois de transformada em bytes
# gere uma chave em bytes que possa ser "codada" em base64 (apenas uma exigência do modo Fernet CBC)
def gerar_chave_fernet(chave: bytes) -> bytes:
    assert isinstance(chave, bytes)
    hlib = hashlib.md5()
    hlib.update(chave)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def enviar_mensagem():
    os.system('cls')
    print('Digite a mensagem: ', end='')
    mensagem = input()
    print('Digite a chave: ', end='')
    mensagem_chave = input()
    chave = gerar_chave_fernet(mensagem_chave.encode('utf-8'))
    fernet = Fernet(chave)
    return fernet.encrypt(mensagem.encode('utf-8'))
    # print(f"string para gerar a chave: {mensagem_chave}")
    # print(f"chave gerada: {chave}")
    # print(f"string para gerar a mensagem: {mensagem}")
    # print(f"mensagem criptografada: {texto_cifrado}")    

def menu():
    print('Login: ', end='')
    user = input()
    print(f'Olá {user}, o que deseja fazer ?')
    print('A) Enviar uma mensagem')
    print('B) Ler mensagens do banco')
    op = input()
    op = str.upper(op)
    match op:
        case 'A':
            print('sexo')
            mensagem = enviar_mensagem()
        case 'B' :
            print('oxes')
        case _ :
            print('Opção inválida - Refaça a operação')
            menu()
            

menu()

# Gerar arquivo json

def gerar_json(user, mensagem):
    dados = {
        "from": user,
        "to": "Thiago",
        "wasRead": False,
        "message": mensagem
    }

    # Caminho e nome do arquivo JSON
    nome_arquivo = 'message.json'

    # Abrir o arquivo JSON em modo de escrita
    with open(nome_arquivo, 'w') as arquivo:
        # Escrever os dados no arquivo JSON
        json.dump(dados, arquivo)

    print("Arquivo JSON gerado com sucesso!")

    
# texto_chave_secreta = "Vasco da Gama"

# derivando a chave a partir do texto secreto.
# key = gerar_chave_fernet(texto_chave_secreta.encode('utf-8'))
# fernet = Fernet(key)
# texto_cifrado = fernet.encrypt(mensagem_em_claro.encode('utf-8'))
# texto_decifrado = fernet.decrypt(texto_cifrado).decode('utf-8')

# fazendo os prints para ver o resultado
# print(f"string para gerar a chave: {texto_chave_secreta}")
# print(f"mensagem_em_claro: {mensagem_em_claro}")
# print(f"chave gerada em bytes: {key}")
# print(f"chave gerada em impressão de string: {key.decode()}")
# print(f"texto_cifrado: {texto_cifrado}")
# print(f"texto_decifrado: {texto_decifrado}")
