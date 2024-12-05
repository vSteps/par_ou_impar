import pygame
import socket
import threading
import json


HOST = '127.0.0.1'
TCP_PORT = 5000
UDP_PORT = 5001


pygame.init()


WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

X_IMG = pygame.image.load('gerador_imagens/X.png')
O_IMG = pygame.image.load('gerador_imagens/O.png')
BOARD_IMG = pygame.image.load('gerador_imagens/tabuleiro.png')

X_IMG = pygame.transform.scale(X_IMG, (200, 200))
O_IMG = pygame.transform.scale(O_IMG, (200, 200))

class ClienteJogo:
    def __init__(self):
        self.tabuleiro = [' '] * 9
        self.vez = 'X'
        self.jogador = None
        self.conexao_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexao_tcp.connect((HOST, TCP_PORT))
        dados = self.conexao_tcp.recv(1024).decode('utf-8')
        info = json.loads(dados)
        self.jogador = info['jogador']
        print(f"Você é o jogador {self.jogador}")
        self.conexao_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conexao_udp.sendto(b'Conectado', (HOST, UDP_PORT))
        self.thread_udp = threading.Thread(target=self.receber_atualizacoes, daemon=True)
        self.thread_udp.start()

        self.run_game()

    def receber_atualizacoes(self):
        while True:
            dados, _ = self.conexao_udp.recvfrom(1024)
            estado = json.loads(dados.decode('utf-8'))
            self.tabuleiro = estado['tabuleiro']
            self.vez = estado['vez']

    def enviar_jogada(self, posicao):
        comando = {'tipo': 'jogada', 'posicao': posicao, 'jogador': self.jogador}
        self.conexao_tcp.send(json.dumps(comando).encode('utf-8'))

    def run_game(self):
        running = True
        while running:
            WIN.fill(WHITE)
            WIN.blit(BOARD_IMG, (0, 0))
            for i in range(9):
                x = (i % 3) * 200
                y = (i // 3) * 200
                if self.tabuleiro[i] == 'X':
                    WIN.blit(X_IMG, (x, y))
                elif self.tabuleiro[i] == 'O':
                    WIN.blit(O_IMG, (x, y))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.vez == self.jogador:
                    x, y = pygame.mouse.get_pos()
                    col = x // 200
                    row = y // 200
                    posicao = row * 3 + col
                    if self.tabuleiro[posicao] == ' ':
                        self.enviar_jogada(posicao)

        pygame.quit()

if __name__ == "__main__":
    ClienteJogo()
