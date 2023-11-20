import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import io
from editor import editor_pdf_iniciar

def Verificação():
    try:
        banco = sqlite3.connect('configue.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM configuração")
        banco.close()
    except:
        banco = sqlite3.connect('configue.db')
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE configuração (link text, marca BLOB, primeiro text, ultimo text, id integer)")
        comando = "INSERT INTO configuração (id) VALUES (?)"
        cursor.execute(comando, (1,))
        banco.commit()
        banco.close()


Verificação()


def Read(coluna):

    banco = sqlite3.connect('configue.db')
    cursor = banco.cursor()

    cursor.execute(f"SELECT {coluna} FROM configuração WHERE id = ?", (1,))

    resultado = cursor.fetchone()

    banco.close()

    try:
        bytes_ = memoryview(resultado[0]).tobytes()
        return bytes_

    except:

        return resultado[0]


def Delet(coluna):

    banco = sqlite3.connect('configue.db')
    cursor = banco.cursor()

    cursor.execute(f"UPDATE configuração SET {coluna} = NULL WHERE id = {1}")

    banco.commit()
    banco.close()

def salvar_link():
    link = entrada_link.get()
    banco = sqlite3.connect('configue.db')
    cursor = banco.cursor()
    cursor.execute("UPDATE configuração SET link = ? WHERE id = ?", (link, 1))
    banco.commit()
    banco.close()


root = tk.Tk()
root.title("Editor de PDF")
root.geometry("190x220")
root.configure(bg='orange')

button = tk.Button(root, text="Processar PDF", command=editor_pdf_iniciar)
button.grid(pady=20, padx=10, row=0, column=0)
button.config(bg='dark orange')

botão_link = tk.Button(root, text="Salvar link referência", command=salvar_link)
botão_link.grid(pady=10, padx=10, row=1, column=0)
botão_link.config(bg='dark orange')

entrada_link = tk.Entry(root)
entrada_link.grid(padx=10, row=2, column=0)

Delet_link = lambda: Delet('link')
botão_limpar_link = tk.Button(root, text="Resetar link", command=Delet_link)
botão_limpar_link.grid(pady=20, padx=10, row=3, column=0)
botão_limpar_link.config(bg='dark orange')

root.mainloop()