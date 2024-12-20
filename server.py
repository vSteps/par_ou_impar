import socket

IP = "192.168.0.108"
UDP_PORT = 5005
TCP_PORT = 5008


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((IP, TCP_PORT))
serversocket.listen(2)
print("Servidor aguardando conexão...")
(clientsocket1, address1) = serversocket.accept()
print("Jogador 1 conectado:", address1)
(clientsocket2, address2) = serversocket.accept()
print("Jogador 2 conectado:", address2)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, UDP_PORT))


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


if escolha1 == escolha2:
    mensagem1 = "Erro: Ambos os jogadores escolheram a mesma opção! O jogo não pode continuar."
    mensagem2 = "Erro: Ambos os jogadores escolheram a mesma opção! O jogo não pode continuar."
else:

    escolhas_validas = ['par', 'impar']
    if escolha1 not in escolhas_validas or escolha2 not in escolhas_validas:
        mensagem1 = "Escolha inválida! Você deve escolher 'par' ou 'ímpar'."
        mensagem2 = "Escolha inválida! Você deve escolher 'par' ou 'ímpar'."
    else:

        soma = numero1 + numero2


        if soma == 0:
            mensagem1 = "Nenhum jogador ganhou, a soma foi 0!"
            mensagem2 = "Nenhum jogador ganhou, a soma foi 0!"
        else:

            resultado = "par" if soma % 2 == 0 else "impar"


            mensagem1 = "Você venceu!" if resultado == escolha1 else "Você perdeu!"
            mensagem2 = "Você venceu!" if resultado == escolha2 else "Você perdeu!"


clientsocket1.send(str.encode(mensagem1))
clientsocket2.send(str.encode(mensagem2))


sock.close()
clientsocket1.close()
clientsocket2.close()
serversocket.close()
