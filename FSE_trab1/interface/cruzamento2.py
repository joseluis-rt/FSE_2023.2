import socket

def main():
    # Configurações do servidor
    HOST = '127.0.0.1'  # Escuta em todas as interfaces de rede
    PORT = 10731  # Porta do servidor (10731-10740)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Envia uma mensagem ao se conectar
    client_socket.send("Cruzamento 2 conectado".encode())

    # Não é necessário o loop contínuo para envio de mensagens
    # Aqui, o cliente está apenas conectando ao servidor

    client_socket.close()

if __name__ == "__main__":
    main()
