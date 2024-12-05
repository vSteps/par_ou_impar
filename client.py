import socket
import pygame

# Configurações de rede
TCP_PORT = 12345
UDP_PORT = 12346
BUFFER_SIZE = 1024

# Inicialização do Pygame
pygame.init()
LARGURA_TELA = 300
ALTURA_TELA = 300
TAMANHO_QUADRADO = 100
COR_FUNDO = (255, 255, 255)
COR_LINHA = (0, 0, 0)
COR_X = (255, 0, 0)
COR_O = (0, 0, 255)

# Função para desenhar o tabuleiro
def desenhar_tabuleiro(tela, tabuleiro):
    for i in range(1, 3):
        pygame.draw.line(tela, COR_LINHA, (i * TAMANHO_QUADRADO, 0), (i * TAMANHO_QUADRADO, ALTURA_TELA), 5)
        pygame.draw.line(tela, COR_LINHA, (0, i * TAMANHO_QUADRADO), (LARGURA_TELA, i * TAMANHO_QUADRADO), 5)
    
    for i, valor in enumerate(tabuleiro):
        x = (i % 3) * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
        y = (i // 3) * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
        if valor == 'X':
            pygame.draw.line(tela, COR_X, (x - 30, y - 30), (x + 30, y + 30), 5)
            pygame.draw.line(tela, COR_X, (x + 30, y - 30), (x - 30, y + 30), 5)
        elif valor == 'O':
            pygame.draw.circle(tela, COR_O, (x, y), 30, 5)

# Função para enviar movimento ao servidor
def enviar_movimento(cliente_tcp, movimento):
    cliente_tcp.send(str(movimento).encode())
    resposta = cliente_tcp.recv(BUFFER_SIZE).decode()
    print(f"Resposta do servidor: {resposta}")
    return resposta

# Função para comunicação UDP
def enviar_udp_signal(cliente_udp, sinal):
    cliente_udp.sendto(sinal.encode(), ('localhost', UDP_PORT))
    resposta, addr = cliente_udp.recvfrom(BUFFER_SIZE)
    print(f"Resposta do servidor UDP: {resposta.decode()}")

# Função principal do cliente
def iniciar_cliente():
    cliente_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_tcp.connect(('localhost', TCP_PORT))
    
    cliente_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    tabuleiro = [' ' for _ in range(9)]
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Jogo da Velha")

    rodando = True
    turno = 'X'

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                linha = x // TAMANHO_QUADRADO
                coluna = y // TAMANHO_QUADRADO
                movimento = linha + coluna * 3
                if tabuleiro[movimento] == ' ':
                    tabuleiro[movimento] = turno
                    desenhar_tabuleiro(tela, tabuleiro)
                    resposta = enviar_movimento(cliente_tcp, movimento)
                    if 'venceu' in resposta:
                        print(f"Jogador {turno} venceu!")
                        rodando = False
                    turno = 'O' if turno == 'X' else 'X'
                    pygame.display.update()
                    enviar_udp_signal(cliente_udp, "Pronto para jogar")

    pygame.quit()

if __name__ == "__main__":
    iniciar_cliente()
