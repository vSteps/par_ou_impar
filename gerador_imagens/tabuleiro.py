from PIL import Image, ImageDraw

def criar_tabuleiro():
    tamanho = 600
    espessura_linha = 10
    cor_fundo = "white"
    cor_linhas = "black"

    img = Image.new("RGB", (tamanho, tamanho), cor_fundo)
    draw = ImageDraw.Draw(img)

    # Linhas horizontais
    draw.line([(0, 200), (600, 200)], fill=cor_linhas, width=espessura_linha)
    draw.line([(0, 400), (600, 400)], fill=cor_linhas, width=espessura_linha)

    # Linhas verticais
    draw.line([(200, 0), (200, 600)], fill=cor_linhas, width=espessura_linha)
    draw.line([(400, 0), (400, 600)], fill=cor_linhas, width=espessura_linha)

    img.save("tabuleiro.png")
    print("Tabuleiro salvo como 'tabuleiro.png'.")

criar_tabuleiro()
