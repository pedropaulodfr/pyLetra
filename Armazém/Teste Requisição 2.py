import requests
import json

def Result():
    letra = Requisicao(artist, music)
    print(letra)
    print(letra['mus'][0]['name'] + '\n' + letra['mus'][0]['url'])

def Requisicao(artist, music):
    requisicao = requests.get('https://api.vagalume.com.br/search.php?art=' + artist + '&mus=' + music +
                              '&apikey={9790636438dcf6fe0cb11ded844d9786}')   
    requisicao_text = requisicao.json()
    print(requisicao_text)

artist = input('Artista: ')
music = input('Música: ')

Requisicao(artist, music)
