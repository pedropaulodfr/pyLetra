import requests
from bs4 import BeautifulSoup

def encontrar(url):

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    soup = str(soup.find_all('title')[0].get_text())
    info = soup.split()
    info = {'musica': info[0].replace('-', ' '), 'artista': info[2].replace('-', ' ')}

    return info

    #print('\nMúsica: {} \nArtista: {}'.format(formata['musica'], formata['artista']))

#print(import_YouTube('https://www.youtube.com/watch?v=ys0OHnK1p5M')['artista'])
