import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # localhost
PORT = 12345

# Lista que armazena os clientes conectados
clientes = []

# Função para processar cada cliente
def lidar_com_cliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            if mensagem:
                print(f"Mensagem recebida: {mensagem}")
                # Repassar mensagem para todos os outros clientes
                for c in clientes:
                    if c != cliente:
                        c.send(mensagem.encode('utf-8'))
        except:
            clientes.remove(cliente)
            cliente.close()
            break

# Criar socket do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print(f"Servidor ouvindo em {HOST}:{PORT}")

# Aceitar conexões de clientes
while True:
    cliente, endereco = servidor.accept()
    print(f"Conexão aceita de {endereco}")
    clientes.append(cliente)

    # Criar uma thread para lidar com o cliente
    thread = threading.Thread(target=lidar_com_cliente, args=(cliente,))
    thread.start()