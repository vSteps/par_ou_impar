from PIL import Image, ImageDraw

def criar_x():
    tamanho = 200
    espessura_linha = 15
    cor_fundo = "white"
    cor_x = "red"

    img = Image.new("RGB", (tamanho, tamanho), cor_fundo)
    draw = ImageDraw.Draw(img)

    # Desenha um X
    draw.line([(0, 0), (tamanho, tamanho)], fill=cor_x, width=espessura_linha)
    draw.line([(0, tamanho), (tamanho, 0)], fill=cor_x, width=espessura_linha)

    img.save("X.png")
    print("X salvo como 'X.png'.")

def criar_o():
    tamanho = 200
    espessura_linha = 15
    cor_fundo = "white"
    cor_o = "blue"

    img = Image.new("RGB", (tamanho, tamanho), cor_fundo)
    draw = ImageDraw.Draw(img)

    # Desenha um O
    draw.ellipse([(15, 15), (tamanho-15, tamanho-15)], outline=cor_o, width=espessura_linha)

    img.save("O.png")
    print("O salvo como 'O.png'.")

criar_x()
criar_o()
