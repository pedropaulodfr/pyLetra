from tkinter import *
from tkinter import messagebox
from functools import partial
from Requisicao import Requisicao
from playsound import playsound

import os

janela_musicSave = None
janela_segunda = None
janela_sobre = None
tamanhoText = 12
letra = None

def search_off(a):
    def get_list(event):
        # Função para abrir musica selecionada
        index = lista_salvas.curselection()[0]
        seltext = lista_salvas.get(index)

        os.system('start letras/' + seltext + '.txt')
        
    btn_search['state'] = 'normal'  # Armar botão
    
    # Ocultar imagem e campo texto
    imagem.destroy()
    texto.pack_forget()

    # Verificando se existe algum campo em branco
    if (music.get() != '') or (artist.get() != ''):

        musicas_salvas = str(os.listdir('letras'))

        # Criando lista
        lista_salvas.pack(side=LEFT, expand=TRUE, fill='both')

        # Limpar lista
        for i in range(0, len(musicas_salvas)):
            lista_salvas.delete(END)
        
        lista_salvas.insert(END, 'Músicas encontradas:')
        lista_salvas['font'] = 'Calibri'
        lista_salvas.insert(END, '')

        # Criar barra de rolagem
        sb = Scrollbar(corpo)
        sb.pack(side=RIGHT, fill=Y)
        sb.configure(command=lista_salvas.yview)
        lista_salvas.configure(yscrollcommand=sb.set)

        musicas_salvas = str(musicas_salvas).lower().split()

        # Inserindo nomes dentro do campo
        for i in range(0, len(musicas_salvas)):
            if music.get().lower().replace(' ', '_') in musicas_salvas[i]:
                linha = musicas_salvas[i].replace('.txt', '').replace("," ,'')
                lista_salvas.insert(END, linha.replace("'", '').replace("[" , '').replace("]",''))
        
        lista_salvas.bind('<Double-Button-1>', get_list) # Abrindo musica selecionada
        lista_salvas.bind('<Button-1>', sons)

    else:
        messagebox.showerror("ERRO!", "Você deixou algum campo em branco!")  # Mensagem de erro
        texto.insert(INSERT, 'ERRO!\nVocê deixou algum campo em branco!')  # Mensagem de erro
        btn_search['state'] = 'active'  # Armar botão

def offline(arg):
    if(off.get() == 1 or arg == 1):
        artist['state'] = 'disabled'
        artist_lb['foreground'] = 'gray'
        off_lb['text'] = (25 * ' ') + 'Você está no modo offline!'
        off_lb['foreground'] = 'red'
        off_lb.place(x=105, y=35)
        btn_search['command'] = partial(search_off, '')
        music.bind('<Return>', search_off)
        artist.bind('<Return>', search_off)
    else:
        offline_btn.deselect()
        artist['state'] = 'normal'
        artist_lb['foreground'] = 'black'
        off_lb.place_forget()
        btn_search['command'] = partial(search, '')
        music.bind('<Return>', search)
        artist.bind('<Return>', search)

def search(e):
    def translate():
        texto.delete(1.0, END)
        texto.insert(INSERT, '-=' * 36 + '\nMúsica: ' + musica + '\n' +  # Música
                     'Artista: ' + artista + '\n' +  # Artista
                     'Disponível em: ' + link + '\n' + '-=' * 36 +  # Link
                     '\n\n' + musica + '\n\n' + letra['mus'][0]['translate'][0]['text'])  # Letra

    btn_search['state'] = 'normal'  # Armar botão procurar
    lista_salvas.pack_forget() # Ocultando lista com musicas salvas
    offline_btn.place(x=410, y=60) # Alterando posição do botão offline
    
    # Mostrar e limpar campo da letra
    imagem.destroy()
    texto.pack()
    texto.delete(1.0, END)

    # Verificando se existe algum campo em branco
    if (music.get() != '') or (artist.get() != ''):

        # Baixar letra
        try:
            global letra
            letra = Requisicao(artist, music)
        except:
            messagebox.showerror("ERRO!", "Verifique sua conexão!")  # Mensagem de erro
            texto.insert(INSERT, 'ERRO!\nVerifique sua conexão!')  # Mensagem de erro
            btn_search['state'] = 'active'  # Armar botão
            offline_btn.select()
            offline(1)

        # Verificando se a letra foi encontrada
        if (letra['type'] != 'notfound') and (letra['type'] != 'song_notfound'):

            # Verificando se há tradução
            try:
                letra['mus'][0]['translate'][0]['text']
                traducao = True
            except:
                traducao = False

            # Criando botão de tradução
            traduzir = Button(janela, text='Traduzir', activeforeground='white', activebackground='grey',
                               cursor='hand2')
            traduzir.place(x=340, y=125)
            traduzir['command'] = translate

            # Ativando/Desativando botão de tradução
            if (traducao == True):
                traduzir['state'] = 'normal'
            else:
                traduzir['state'] = 'disabled'

            scrollbar.pack(side=RIGHT, fill=Y)  # Mostrar barra de rolagem

            # Informações sobre a música
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
            btn_search['state'] = 'active'  # Armar botão
    else:
        messagebox.showerror("ERRO!", "Você deixou algum campo em branco!")  # Mensagem de erro
        texto.insert(INSERT, 'ERRO!\nVocê deixou algum campo em branco!')  # Mensagem de erro
        btn_search['state'] = 'active'  # Armar botão


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
        seltext = lista.get(index).replace(' - ', '-').replace(' ', '_')

        # Fechar janela com lista de músicas
        global janela_segunda
        janela_segunda.destroy()

        # Criar janela contendo a letra da música
        global janela_musicSave
        janela_musicSave = Tk()

        musicOpen = open('letras/' + seltext + '.txt', 'r')
        musicSave = musicOpen.read()

        global tamanhoText
        textoSave = Text(janela_musicSave, font='Calibri ' + str(tamanhoText), yscrollcommand=scrollbar.set, exportselection=0)
        textoSave['width'] = 60
        textoSave['height'] = 40
        
        # Criar barra de rolagem
        scroll = Scrollbar(janela_musicSave)
        scroll.pack(side=RIGHT, fill=Y)
        scroll.configure(command=textoSave.yview)
        textoSave.configure(yscrollcommand=scroll.set)

        # Inserir letra dentro do campo
        textoSave.insert(INSERT, musicSave)
        textoSave.pack()
        
        # MENU POPUP
        def menuPopup(opc):
            global tamanhoText
            
            if(opc == 'Aumentar'):
                tamanhoText = tamanhoText + 1
                textoSave.config(font='Calibri ' + str(tamanhoText))
            else:
                tamanhoText = tamanhoText - 1
                textoSave.config(font='Calibri ' + str(tamanhoText))
                
        def popup(position):
            menu.post(position.x_root, position.y_root)
            
        # Opções do popup
        menu = Menu(janela_musicSave, tearoff=0)
        menu.add_command(label='Aumentar letra', command=partial(menuPopup, 'Aumentar'))
        menu.add_command(label='Diminuir letra', command=partial(menuPopup, 'Diminuir'))
        textoSave.bind('<Button-3>', popup)

        # Configurando janela musicSave
        janela_musicSave.title(seltext.replace('-', ' - ').replace('_', ' '))
        janela_musicSave.geometry('500x600+30+40')
        janela_musicSave.minsize(width='500', height='400')
        janela_musicSave.maxsize(width='500', height='700')
        janela_musicSave.iconbitmap('ico.ico')
        janela_musicSave.focus_force()
        janela_musicSave.mainloop()
        
        
    # Criando janela secundária
    global janela_segunda
    janela_segunda = Tk()

    # Procurando as letras salvas
    lista_letras = os.listdir('letras')

    # Criando Listbox onde os nomes serão exibido
    lista = Listbox(janela_segunda, cursor='hand2')
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
        lista.insert(END, lista_letras[i].replace('.txt', '').replace('_', ' ').replace('-', ' - '))

    lista.bind('<Double-Button-1>', get_list) # Abrindo musica selecionada
    lista.bind('<Button-1>', sons)

    # Configurando janela secundária
    janela_segunda.title('Músicas salvas')
    janela_segunda.geometry('200x250+' + str(janela.winfo_x()+50) + '+' +  str(janela.winfo_y()+80))
    janela_segunda.minsize(width=400, height=500)
    janela_segunda.maxsize(width=400, height=500)
    janela_segunda.iconbitmap('ico.ico')
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
    global janela_sobre
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
    Label(janela_sobre, text='Versão: 1.9.13', bg='white').place(x=130, y=377)

    # Botão atualizar
    btn_atualizar = Button(janela_sobre, text='Atualizar', command=update, activebackground='grey', cursor='hand2')
    btn_atualizar.place(x=140, y=402)

    # Configurando janela sobre
    janela_sobre.title('Sobre')
    janela_sobre.geometry('340x480+' + str(janela.winfo_x()+85) + '+' +  str(janela.winfo_y()+120))
    janela_sobre.minsize(width=340, height=480)
    janela_sobre.maxsize(width=340, height=480)
    janela_sobre.overrideredirect(True)
    janela_sobre.iconbitmap('ico.ico')
    janela_sobre.focus_force()
    janela_sobre.mainloop()

def update():
    os.system('start https://www.dropbox.com/s/27ffcbmi9v5b6zj/pyLetra.pyw?dl=0')

def sons(e):
    playsound('sons/clique.mp3')

def sair():
    janela.destroy()
    janela_segunda.destroy()

janela = Tk()

# Criando Frame
corpo = Frame(janela)
corpo.place(y=160)

# Menu toplevel
principal = Menu(janela)
arquivo = Menu(principal, tearoff=0)
arquivo.add_command(label='Músicas salvas', command=letras_salvas)
arquivo.add_command(label='Mostrar pasta de músicas', command=mostrar_pasta)
arquivo.add_command(label='Sair', command=sair)
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

artist_lb = Label(janela, text='Artista: ')
artist_lb.place(x=104, y=90)
artist = Entry(janela)
artist['width'] = 40
artist.place(x=150, y=90)
artist.bind('<Return>', search)

# Botão procurar
btn_search = Button(janela, text='Procurar', cursor='hand2')
btn_search.place(x=230, y=120)
#btn_search.bind('<Button-1>', search)
btn_search['command'] = partial(search, '')

# Botão Offline
off = IntVar(janela)
offline_btn = Checkbutton(text='Offline', var=off, command=partial(offline, ''))
offline_btn.place(x=300, y=120)
offline_btn.bind('<Button-1>', sons)

# Notificação offline
off_lb = Label(janela)

# Criar campo lista de musicas offline
lista_salvas = Listbox(corpo, width=60, height=24, cursor='hand2')

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
janela.iconbitmap('ico.ico')
janela.mainloop()
