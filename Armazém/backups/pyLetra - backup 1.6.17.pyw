from tkinter import *
from tkinter import messagebox
from functools import partial
from Requisicao import Requisicao

import os


def search(e):
    btn_search['state'] = 'normal'  # Armar botão
    
    # Mostrar e limpar campo da letra
    imagem.destroy()
    texto.pack()
    texto.delete(1.0, END)

    # Verificando se existe algum campo em branco
    if (music.get() != '') or (artist.get() != ''):

        # Baixar letra
        letra = Requisicao(artist, music)

        # Verificando se a letra foi encontrada
        if (letra['type'] != 'notfound') and (letra['type'] != 'song_notfound'):
            # Informações sobre a música
            scrollbar.pack(side=RIGHT, fill=Y)  # Mostrar barra de rolagem

            musica = letra['mus'][0]['name']
            artista = letra['art']['name']
            link = letra['mus'][0]['url']
            letra_music = letra['mus'][0]['text']

            texto.insert(INSERT, '-=' * 36 + '\nMúsica: ' + musica + '\n' +  # Música
                         'Artista: ' + artista + '\n' +  # Artista
                         'Disponível em: ' + link + '\n' + '-=' * 36 +  # Link
                         '\n\n' + musica + '\n\n' + letra_music)  # Letra

            # Criando botão de salvamento
            save = Button(janela, text='Salvar letra', activeforeground='white', activebackground='grey',
                          cursor='hand2')
            save.place(x=410, y=125)
            save['command'] = partial(salvar, musica, artista, link, letra_music)

            # Criando botão de abrir musica no YouTube
            yt = Button(janela, text='Abrir música no YouTube',
                        activeforeground='white', activebackground='grey', cursor='hand2')
            yt.place(x=10, y=125)
            yt['command'] = partial(youtube, musica, artista)
        else:
            messagebox.showerror('ERRO!', 'Letra não encontrada!')  # Mensagem de erro
            texto.insert(INSERT, 'ERRO!\nLetra não encontrada!')  # Mensagem de erro
            btn_search['state'] = 'disable'  # Desarmar botão
    else:
        messagebox.showerror("ERRO!", "Você deixou algum campo em branco!")  # Mensagem de erro
        texto.insert(INSERT, 'ERRO!\nVocê deixou algum campo em branco!')  # Mensagem de erro
        btn_search['state'] = 'disable'  # Desarmar botão


def salvar(musica, artista, link, letra_music):
    # Criando arquivo txt
    arquivo = open('letras/' + musica.replace(' ', '_') + '-' + artista.replace(' ', '_') + '.txt', 'w')

    # Salvando letra dentro do arquivo txt
    arquivo.write('-=' * 34 + '\nMúsica: ' + musica + '\n' +  # Música
                  'Artista: ' + artista + '\n' +  # Artista
                  'Disponível em: ' + link + '\n' + '-=' * 34 +  # Link
                  '\n\n' + musica + '\n\n' + letra_music)  # Letra
    arquivo.close()

    messagebox.showinfo("Salvo!", "Música salva com sucesso!")  # Mensagem arquivo salvo com sucesso!


def letras_salvas():
    
    def get_list(event):
        # Função para abrir musica selecionada
        
        index = lista.curselection()[0]
        seltext = lista.get(index)

        os.system('start letras/' + seltext + '.txt')
        
    # Criando janela secundária
    janela_segunda = Tk()

    # Procurando as letras salvas
    lista_letras = os.listdir('letras')

    # Criando Listbox onde os nomes serão exibido
    lista = Listbox(janela_segunda)
    lista.pack(side=LEFT, expand=TRUE, fill='both')
    lista.delete(END)
    lista.insert(END, 'Lista de músicas salvas:')
    lista['font'] = 'Calibri'
    lista.insert(END, '')

    # Criar barra de rolagem
    sb = Scrollbar(janela_segunda)
    sb.pack(side=RIGHT, fill=Y)
    sb.configure(command=lista.yview)
    lista.configure(yscrollcommand=sb.set)

    # Inserindo nomes dentro do campo
    for i in range(0, len(lista_letras)):
        lista.insert(END, lista_letras[i].replace('.txt', ''))

    lista.bind('<Double-Button-1>', get_list) # Abrindo musica selecionada

    # Configurando janela secundária
    janela_segunda.title('Músicas salvas')
    janela_segunda.geometry('350x500+500+120')
    janela_segunda.minsize(width=400, height=500)
    janela_segunda.maxsize(width=400, height=500)
    janela_segunda.iconbitmap('favicon.ico')
    janela_segunda.focus_force()
    janela_segunda.mainloop()


def youtube(musica, artista):
    # Abrir música no YoutTube
    musica = '-'.join(musica.split())
    artista = '-'.join(artista.split())
    os.system('''start https://www.youtube.com/results?search_query={}+-+{}'''.format(musica, artista))


def mostrar_pasta():
    # Abrir pasta de músicas
    os.system('start letras')


def sobre():
    # Criar janela sobre
    janela_sobre = Toplevel()
    # Carregar e exibir imagem contendo as informações
    img_sobre = PhotoImage(file='sobre.png')
    imagem_sobre = Label(janela_sobre, image=img_sobre)
    imagem_sobre.pack(fill='both', expand=True)

    # Fechar janela
    close = Button(janela_sobre, text='X', bg='white', bd=0, foreground='red', font='Arial 10 bold',
                   activebackground='red', cursor='hand2', command=janela_sobre.destroy)
    close.place(x=313, y=8)

    # Versão e atualização
    Label(janela_sobre, text='Versão: 1.5.11', bg='white').place(x=130, y=377)

    # Botão atualizar
    btn_atualizar = Button(janela_sobre, text='Atualizar', command=update, activebackground='grey', cursor='hand2')
    btn_atualizar.place(x=140, y=402)

    # Configurando janela sobre
    janela_sobre.title('Sobre')
    janela_sobre.geometry('340x480+540+120')
    janela_sobre.minsize(width=340, height=480)
    janela_sobre.maxsize(width=340, height=480)
    janela_sobre.overrideredirect(True)
    janela_sobre.iconbitmap('favicon.ico')
    janela_sobre.focus_force()
    janela_sobre.mainloop()


def update():
    os.system('start https://www.dropbox.com/s/27ffcbmi9v5b6zj/pyLetra.pyw?dl=0')


janela = Tk()

# Criando Frame
corpo = Frame(janela)
corpo.place(y=160)

# Menu toplevel
principal = Menu(janela)
arquivo = Menu(principal, tearoff=0)
arquivo.add_command(label='Músicas salvas', command=letras_salvas)
arquivo.add_command(label='Mostrar pasta de músicas', command=mostrar_pasta)
arquivo.add_command(label='Sair', command=janela.destroy)
principal.add_cascade(label="Arquivo", menu=arquivo)
principal.add_command(label='Sobre', command=sobre)
janela.configure(menu=principal)

# Mensagem boas vindas
Label(janela, text='Seja bem vindo ao pyLetra!\nAqui você encontra as letras das suas músicas favoritas').place(x=105)

# Campos
Label(janela, text='Música: ').place(x=100, y=65)
music = Entry(janela)
music.focus_force()
music['width'] = 40
music.place(x=150, y=65)
music.bind('<Return>', search)

Label(janela, text='Artista: ').place(x=104, y=90)
artist = Entry(janela)
artist['width'] = 40
artist.place(x=150, y=90)
artist.bind('<Return>', search)

# Botão procurar
btn_search = Button(janela, text='Procurar', activeforeground='white', activebackground='grey', cursor='hand2')
btn_search.place(x=230, y=120)
btn_search.bind('<Button-1>', search)

# Imagem
img = PhotoImage(file='logo.png')
imagem = Label(janela, image=img)
imagem.place(x=70, y=240)

# Criar barra de rolagem
scrollbar = Scrollbar(janela)

# Criar campo da letra
texto = Text(corpo, font='Calibri', yscrollcommand=scrollbar.set, exportselection=0)
texto['width'] = 60
texto['height'] = 25
scrollbar.config(command=texto.yview)

# Configurando janela principal
janela.title('pyLetra')
janela.geometry('500x640+450+15')
janela.minsize(width=500, height=640)
janela.maxsize(width=500, height=640)
janela.iconbitmap('favicon.ico')
janela.mainloop()
