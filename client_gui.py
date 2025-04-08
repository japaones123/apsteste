import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog

# Função para receber mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            mostrar_mensagem(mensagem)
        except:
            mostrar_mensagem("Conexão encerrada.")
            cliente.close()
            break
# Mostrar mensagem na janela
def mostrar_mensagem(mensagem):
    area_texto.config(state='normal')
    area_texto.insert('end', mensagem + '\n')
    area_texto.config(state='disabled')
    area_texto.see('end')

# Enviar mensagem ao servidor
def enviar_mensagem():
    mensagem = entrada_mensagem.get()
    entrada_mensagem.delete(0, 'end')
    if mensagem:
        mensagem_formatada = f"{nome}: {mensagem}"
        mostrar_mensagem(mensagem_formatada)
        cliente.send(mensagem_formatada.encode('utf-8'))

# Criar interface
janela = tk.Tk()
janela.title("Chat TCP/IP")
janela.configure(bg='#2c2f33')  # Fundo escuro

area_texto = scrolledtext.ScrolledText(
    janela, 
    state='disabled', 
    fg='#f1f1f1', 
    bg='#23272a',
    font=('Consolas', 12),
    wrap='word'
)
area_texto.pack(padx=10, pady=10)

entrada_mensagem = tk.Entry(
    janela, 
    width=50, 
    fg='#f1f1f1', 
    bg='#23272a',
    insertbackground='white',  # cor do cursor
    font=('Consolas', 11)
)
entrada_mensagem.pack(padx=10, pady=5, side='left')
entrada_mensagem.bind("<Return>", lambda event: enviar_mensagem())

botao_enviar = tk.Button(
    janela, 
    text="Enviar", 
    command=enviar_mensagem, 
    fg='white', 
    bg='#7289da',
    activebackground='#5b6eae',
    font=('Verdana', 10, 'bold')
)
botao_enviar.pack(padx=5, pady=5, side='left')

# Perguntar o nome do usuário
nome = simpledialog.askstring("Nome", "Digite seu nome:")

# Conectar ao servidor
HOST = '127.0.0.1'
PORT = 12345

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

# Enviar nome ao entrar
cliente.send(f"{nome} entrou no chat.".encode('utf-8'))

# Thread para receber mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.daemon = True
thread_receber.start()

# Iniciar a interface
janela.mainloop()