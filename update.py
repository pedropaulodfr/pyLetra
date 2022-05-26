import pyrebase
from os import system

def Initialize():
    config = {
      "apiKey": "AIzaSyAz6Of30xKdkDYgtplXqAljmALdNAMc-nI",
      "authDomain": "fir-8fbbf.firebaseapp.com",
      "databaseURL": "https://fir-8fbbf.firebaseio.com",
      "storageBucket": "fir-8fbbf.appspot.com"
    }

    firebase = pyrebase.initialize_app(config) # Iniciar Firebase
    storage = firebase.storage() # Abrir Armazenamento

    return firebase, storage

def Authentication():
    firebase, storage = Initialize()
    
    credenciais_arq = open('login.log', 'r')  # Abrindo arquivo com as credenciais
    credenciais_elements = credenciais_arq.readlines()

    # Colocando elementos do arquivo dentro de uma lista
    credenciais_list = []

    for i in range(0, len(credenciais_elements)):
        credenciais_list.append(credenciais_elements[i].replace('\n', ''))

    # Colocando elementos da lista dentro de um dicionário
    credenciais = {'email': credenciais_list[0], 'password': credenciais_list[1]}

    auth = firebase.auth()
    email = credenciais['email']
    password = credenciais['password']

    user = auth.sign_in_with_email_and_password(email, password)  # Pegar nome de usuário

    url = storage.child('pyLetra/Update/pyLetra.rar').get_url(user['idToken'])  # Pegar URL
    system('start ' + url)

    return user

Authentication()
