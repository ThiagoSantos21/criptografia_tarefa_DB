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
client = MongoClient("mongodb+srv://thiago:1234qwer@cluster0.ez0960m.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
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

def gerar_json(user, mensagem):
    if user == 'Alice':
        user2 = 'Bob'
    else :
        user2 = 'Alice'    
    dados = {
        "from": user,
        "to": user2,
        "wasRead": False,
        "message": mensagem.decode('utf-8')
    }

    # Caminho e nome do arquivo JSON
    nome_arquivo = 'message.json'

    # Abrir o arquivo JSON em modo de escrita
    with open(nome_arquivo, 'w') as arquivo:
        # Escrever os dados no arquivo JSON
        json.dump(dados, arquivo)

    print("Arquivo JSON gerado com sucesso!")

def enviar_para_mongodb(nome_arquivo):
    # Selecionar o banco de dados
    db = client['ChatEncrypt']

    # Selecionar a coleção
    collection = db['Chat']

    # Ler o arquivo JSON
    with open(nome_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)

    # Inserir os dados na coleção
    collection.insert_one(dados)

    print("Arquivo JSON enviado para o MongoDB com sucesso!")

def ler_mensagens():
    os.system('cls')
    # Selecionar o banco de dados
    db = client['ChatEncrypt']

    # Selecionar a coleção
    collection = db['Chat']

    # Consultar as mensagens na coleção
    mensagens = collection.find({'wasRead' : False})
    if not mensagens:
        print('Não possui mensagens para ser lidas')    
        return
    
    for index, mensagem in enumerate(mensagens):
        print(f'{index+1}) {mensagem["message"]}')

    indexMensagem = -1

    while indexMensagem < 0 or indexMensagem > int(len(mensagem)) - 1:
        indexMensagem = int(input("\nQual das mensagens voce deseja decifrar? "))

    chave = input('\nDigite a chave da mensagem escolhida: ')

    fernet = Fernet(chave)

    # Exibir as mensagens
    mensagemCifrada = mensagens[indexMensagem]['message']
    mensagemDecifrada = fernet.decrypt(mensagemCifrada).decode('utf-8')
    print(mensagemDecifrada)

    """ 
    for mensagemBD in mensagens:
        print(f"Mensagem de: {mensagemBD['from']}")
        mensagem_cifrada = mensagemBD['message'].encode('utf-8')
        mensagem_decifrada = fernet.decrypt(mensagem_cifrada).decode('utf-8')
        print(f"Mensagem: {mensagem_decifrada}")
        print() """


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
            mensagem = enviar_mensagem()
            gerar_json(user, mensagem)
            enviar_para_mongodb("message.json")
        case 'B' :
            ler_mensagens()
        case _ :
            print('Opção inválida - Refaça a operação')
            menu()
            
menu()

# Gerar arquivo json

    
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
