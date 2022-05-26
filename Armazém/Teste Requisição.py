from Requisicao import Requisicao
from tkinter import *
from functools import partial

def Result():
    letra = Requisicao(artist, music)
    print(letra)
    print(letra['mus'][0]['name'] + '\n' + letra['mus'][0]['url'])

root = Tk()

artist = Entry(root)
artist.pack()
music = Entry(root)
music.pack()

btn = Button(root, text='Ir')
btn['command'] = Result
btn.pack()



root.mainloop()