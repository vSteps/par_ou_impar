import socket
import threading
import json

# Configurações de rede
TCP_HOST = '0.0.0.0'  # Escutando em todas as interfaces
TCP_PORT = 5000
UDP_HOST = '0.0.0.0'
UDP_PORT = 5001

# Variáveis do jogo
estado_jogo = 'JOGANDO'
vez = 'JOGADOR1'
tabuleiro = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Índices do tabuleiro

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_udp_address = None

def enviar_udp(mensagem):
    # Envia o estado do jogo para os jogadores via UDP
    if client_udp_address:
        udp_sock.sendto(mensagem, client_udp_address)
    udp_sock.sendto(mensagem, (client_udp_address))

def gerenciar_jogo():
    global estado_jogo, vez, tabuleiro
    
    while True:
        if estado_jogo == 'JOGANDO':
            # Aqui você pode colocar a lógica para alternar as jogadas e verificar vitórias
            pass
        
        # Envia o estado atual do jogo para os clientes
        enviar_udp({'estado': estado_jogo, 'vez': vez, 'tabuleiro': tabuleiro})

def handle_client_tcp(client_sock, client_address):
    global vez, tabuleiro, estado_jogo
    
    while True:
        try:
            data = client_sock.recv(1024)
            if not data:
                break
            
            jogada = int(data.decode('utf-8'))
            tabuleiro[jogada] = vez
            
            if vez == 'JOGADOR1':
                vez = 'JOGADOR2'
            else:
                vez = 'JOGADOR1'
            
            # Verificar vitória e outros estados do jogo...
            # Se jogo acabou, mude o estado para RESET

            enviar_udp({'estado': estado_jogo, 'vez': vez, 'tabuleiro': tabuleiro})
        except:
            break

    client_sock.close()
    global client_udp_address, udp_sock
def start_server():
    global client_udp_address

    # Criação do socket TCP
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((TCP_HOST, TCP_PORT))
    tcp_sock.listen(2)  # Aceita até 2 conexões
    print(f"Servidor TCP iniciado em {TCP_HOST}:{TCP_PORT}")

    # Criação do socket UDP
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((UDP_HOST, UDP_PORT))
    print(f"Servidor UDP iniciado em {UDP_HOST}:{UDP_PORT}")
    
    # Esperando por conexões de clientes
    while True:
        client_sock, client_address = tcp_sock.accept()
        print(f"Cliente {client_address} conectado via TCP")

        # Definir o endereço do UDP para envio de atualizações
        client_udp_address = client_address  # Usado para enviar updates

        # Iniciar thread para gerenciar esse cliente
        threading.Thread(target=handle_client_tcp, args=(client_sock, client_address)).start()

# Rodando o servidor
if __name__ == "__main__":
    threading.Thread(target=gerenciar_jogo).start()  # Thread para gerenciar o jogo
    start_server()
