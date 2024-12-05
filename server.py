import socket

IP = "127.0.0.1"  # Altere para o IP da máquina do servidor
UDP_PORT = 5005
TCP_PORT = 5008

# Cria socket TCP para enviar o resultado final para os clientes
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((IP, TCP_PORT))
serversocket.listen(2)
print("Servidor aguardando conexão...")
(clientsocket1, address1) = serversocket.accept()
print("Jogador 1 conectado:", address1)
(clientsocket2, address2) = serversocket.accept()
print("Jogador 2 conectado:", address2)

# Cria socket UDP para receber as jogadas de ambos os jogadores
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, UDP_PORT))

# Recebe as jogadas de Jogador 1 e Jogador 2
def recebe_jogada():
    data, addr = sock.recvfrom(1024)
    numero = int(data.decode())
    data, addr = sock.recvfrom(1024)
    escolha = data.decode().lower()
    return numero, escolha, addr

print("Aguardando as jogadas...")
numero1, escolha1, addr1 = recebe_jogada()
print(f"Jogador 1 escolheu: {numero1} e {escolha1}")
numero2, escolha2, addr2 = recebe_jogada()
print(f"Jogador 2 escolheu: {numero2} e {escolha2}")

# Soma dos números dos jogadores
soma = numero1 + numero2
resultado = "par" if soma % 2 == 0 else "ímpar"

# Verifica se cada jogador acertou
mensagem1 = "Você venceu!" if resultado == escolha1 else "Você perdeu!"
mensagem2 = "Você venceu!" if resultado == escolha2 else "Você perdeu!"

# Envia o resultado para ambos os jogadores via TCP
clientsocket1.send(str.encode(mensagem1))
clientsocket2.send(str.encode(mensagem2))

# Fecha os sockets
sock.close()
clientsocket1.close()
clientsocket2.close()
serversocket.close()
