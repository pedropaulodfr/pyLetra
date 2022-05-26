from tkinter import *
from functools import partial

tamanhoText = 12

def janela_letra(musicSave, seltext, janela):
    global tamanhoText
    janela_musicSave = Tk()

    textoSave = Text(janela_musicSave, font='Calibri ' + str(tamanhoText), exportselection=0)
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

    # MENU POP-UP
    def menuPopup(opc):
        global tamanhoText

        if (opc == 'Aumentar'):
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

    janela_musicSave.title(seltext.replace('-', ' - ').replace('_', ' '))
    janela_musicSave.geometry('500x600' + '+' + str(janela.winfo_x()) + '+' + str(janela.winfo_y()))
    janela_musicSave.minsize(width='500', height='400')
    janela_musicSave.maxsize(width='500', height='700')
    janela_musicSave.iconbitmap('imagens/ico.ico')
    janela_musicSave.focus_force()
    janela_musicSave.mainloop()
    