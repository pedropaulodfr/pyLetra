import requests, json

def Requisicao(artist, music):
    requisicao = requests.get('https://api.vagalume.com.br/search.php?art=' + artist.get() + '&mus=' + music.get() +
                              '&apikey={9790636438dcf6fe0cb11ded844d9786}')
    requisicao_text = json.loads(requisicao.text)

    return requisicao_text