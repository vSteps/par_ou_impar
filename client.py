import socket

IP = "192.168.0.108" 
UDP_PORT = 5005
TCP_PORT = 5008


socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.connect((IP, TCP_PORT))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


numero = input("Escolha um número entre 0 e 10: ")

escolha = input("Você escolhe par ou impar? ").strip().lower()


sock.sendto(numero.encode(), (IP, UDP_PORT))
sock.sendto(escolha.encode(), (IP, UDP_PORT))


data = socket_tcp.recv(1024)
print("Resultado:", data.decode('utf-8'))


sock.close()
socket_tcp.close()
