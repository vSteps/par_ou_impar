import socket
import threading

# Configurações de rede
TCP_PORT = 12345
UDP_PORT = 12346
BUFFER_SIZE = 1024

# Tabuleiro do jogo da velha
tabuleiro = [' ' for _ in range(9)]  # Lista com 9 espaços vazios

# Função para verificar se alguém venceu
def verificar_vencedor():
    # Linhas
    for i in range(0, 9, 3):
        if tabuleiro[i] == tabuleiro[i+1] == tabuleiro[i+2] != ' ':
            return tabuleiro[i]
    # Colunas
    for i in range(3):
        if tabuleiro[i] == tabuleiro[i+3] == tabuleiro[i+6] != ' ':
            return tabuleiro[i]
    # Diagonais
    if tabuleiro[0] == tabuleiro[4] == tabuleiro[8] != ' ':
        return tabuleiro[0]
    if tabuleiro[2] == tabuleiro[4] == tabuleiro[6] != ' ':
        return tabuleiro[2]
    return None

# Função para gerenciar a comunicação TCP com o jogador
def handle_tcp_connection(client_socket, client_address):
    print(f"Nova conexão TCP com {client_address}")
    try:
        while True:
            # Receber movimento do cliente
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            move = int(data.decode())  # Recebe a posição do movimento
            if tabuleiro[move] == ' ':
                tabuleiro[move] = 'X'  # Ou 'O' dependendo do jogador
                client_socket.send(f"Movimento feito em {move}".encode())
                vencedor = verificar_vencedor()
                if vencedor:
                    client_socket.send(f"{vencedor} venceu!".encode())
                    break
                else:
                    # Alterna entre os jogadores
                    pass
            else:
                client_socket.send("Posição já ocupada!".encode())
    finally:
        client_socket.close()

# Função para comunicação UDP (sinal rápido)
def handle_udp_communication():
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind(('localhost', UDP_PORT))
    while True:
        data, addr = udp_server.recvfrom(BUFFER_SIZE)
        print(f"Recebido do cliente UDP {addr}: {data.decode()}")
        udp_server.sendto(f"Servidor UDP: {data.decode()}".encode(), addr)

# Função principal do servidor
def start_server():
    # Configuração do servidor TCP
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind(('localhost', TCP_PORT))
    tcp_server.listen(2)  # Até dois jogadores

    print(f"Servidor TCP escutando na porta {TCP_PORT}")

    # Criação da thread para UDP
    udp_thread = threading.Thread(target=handle_udp_communication)
    udp_thread.start()

    while True:
        # Aguardar conexão dos jogadores via TCP
        client_socket, client_address = tcp_server.accept()
        tcp_thread = threading.Thread(target=handle_tcp_connection, args=(client_socket, client_address))
        tcp_thread.start()

if __name__ == "__main__":
    start_server()
