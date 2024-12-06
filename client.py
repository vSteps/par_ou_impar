import socket

IP = "192.168.0.108"  # Altere para o IP do servidor
UDP_PORT = 5005
TCP_PORT = 5008

# Cria socket TCP para se conectar ao servidor e receber o resultado final
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.connect((IP, TCP_PORT))

# Cria socket UDP para enviar as jogadas ao servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Solicita ao jogador um número e a escolha de "par" ou "ímpar"
numero = input("Escolha um número entre 0 e 10: ")

escolha = input("Você escolhe par ou impar? ").strip().lower()

# Envia o número e a escolha para o servidor via UDP
sock.sendto(numero.encode(), (IP, UDP_PORT))
sock.sendto(escolha.encode(), (IP, UDP_PORT))

# Recebe o resultado via TCP
data = socket_tcp.recv(1024)
print("Resultado:", data.decode('utf-8'))

# Fecha os sockets
sock.close()
socket_tcp.close()
