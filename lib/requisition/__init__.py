import requests, json

def get_request(artist, music): # Função para procurar as músicas
    requisição =  requests.get('https://api.vagalume.com.br/search.php?art=' + artist.get() + '&mus=' + music.get() +
                              '&apikey={9790636438dcf6fe0cb11ded844d9786}')
    requisição_texto = json.loads(requisição.text)
    return requisição_texto
    