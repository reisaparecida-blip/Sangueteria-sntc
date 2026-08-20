# `main.py` — Sangueteria com arrastar e soltar
import pygame
import sys

pygame.init()

# ============================================================
# CONFIGURAÇÕES
# ============================================================

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sangueteria")

relogio = pygame.time.Clock()

# ============================================================
# CORES
# ============================================================

FUNDO = (35, 20, 45)
ROXO = (105, 55, 145)
ROXO_ESCURO = (65, 30, 85)
ROSA = (255, 105, 175)
ROSA_CLARO = (255, 175, 215)
BRANCO = (255, 255, 255)
AMARELO = (255, 220, 100)
VERDE = (100, 230, 150)
AZUL = (100, 190, 255)
VERMELHO = (240, 80, 100)

# ============================================================
# FONTES
# ============================================================

titulo = pygame.font.Font(None, 68)
fonte_grande = pygame.font.Font(None, 46)
fonte = pygame.font.Font(None, 32)
fonte_pequena = pygame.font.Font(None, 23)

# ============================================================
# RECEITAS
# ============================================================

receitas = [
    {
        "nome": "Radio-Glow Shake",
        "cientista": "Marie Curie",
        "ingredientes": [
            ("Isotopo de Radio-Glow", 1),
            ("Baga Eletrica de Pantano", 2),
            ("Essencia de Radiacao Fashion", 1)
        ],
        "etapas": [
            "Esmague as 2 bagas eletricas no almofariz.",
            "Despeje o suco no tubo de ensaio grande.",
            "Adicione a Essencia de Radiacao Fashion.",
            "Insira o Isotopo de Radio-Glow com uma pinca.",
            "Sirva no copo de laboratorio decorado."
        ]
    },

    {
        "nome": "Bio-Spooky",
        "cientista": "Rosalind Franklin",
        "ingredientes": [
            ("Extrato de Planta Trepadeira Mutante", 1),
            ("Soro de Raio-X Fotografico", 1),
            ("Essencia de Estilo Genetico", 2)
        ],
        "etapas": [
            "Extraia a seiva da planta trepadeira mutante.",
            "Adicione o soro de raio-X gota a gota.",
            "Use a lampada ultravioleta para revelar as cores.",
            "Misture as 2 essencias com o bastao de vidro.",
            "Decore o frasco com um pingente de esqueleto."
        ]
    },

    {
        "nome": "Cosmic Boo-cake",
        "cientista": "Katherine Johnson",
        "ingredientes": [
            ("Acucar Gravitacional Lunar", 1),
            ("Massa de Baunilha das Trevas", 1),
            ("Granulado Estrela Cadente", 3)
        ],
        "etapas": [
            "Bata a massa de baunilha ate ficar leve e aerada.",
            "Misture o Acucar Gravitacional Lunar.",
            "Coloque a massa nas forminhas.",
            "Asse usando o tempo calculado no cronometro.",
            "Decore com glace azul e roxo e os 3 granulados."
        ]
    },

    {
        "nome": "Steampunk Choco-Pie",
        "cientista": "Ada Lovelace",
        "ingredientes": [
            ("Massa de Baunilha Sombria", 1),
            ("Geleia de Frutas Vermelhas Ciberneticas", 1),
            ("Engrenagem de Chocolate Binario", 8)
        ],
        "etapas": [
            "Molde a massa preta na assadeira.",
            "Despeje a geleia de frutas vermelhas.",
            "Coloque as 8 engrenagens alternando 1 e 0.",
            "Asse no forno de fusao do laboratorio."
        ]
    }
]

# ============================================================
# CIENTISTAS
# ============================================================

cientistas = [
    ("Marie Curie", "Radio-Glow Shake"),
    ("Rosalind Franklin", "Bio-Spooky"),
    ("Katherine Johnson", "Cosmic Boo-cake"),
    ("Ada Lovelace", "Steampunk Choco-Pie")
]

# ============================================================
# ESTADO DO JOGO
# ============================================================

rodando = True
tela_atual = "menu"

receita_selecionada = None

pontuacao = 0
etapa_atual = 0

ingredientes = []
ingrediente_arrastando = None

# ============================================================
# FUNÇÕES
# ============================================================

def texto(msg, fonte_usada, cor, x, y):
    imagem = fonte_usada.render(msg, True, cor)
    tela.blit(imagem, (x, y))


def texto_centralizado(msg, fonte_usada, cor, y):
    imagem = fonte_usada.render(msg, True, cor)
    x = (LARGURA - imagem.get_width()) // 2
    tela.blit(imagem, (x, y))


def botao(nome, x, y, largura, altura):
    retangulo = pygame.Rect(x, y, largura, altura)

    pygame.draw.rect(
        tela,
        ROXO,
        retangulo,
        border_radius=15
    )

    pygame.draw.rect(
        tela,
        ROSA,
        retangulo,
        2,
        border_radius=15
    )

    imagem = fonte.render(nome, True, BRANCO)

    tela.blit(
        imagem,
        (
            x + (largura - imagem.get_width()) // 2,
            y + (altura - imagem.get_height()) // 2
        )
    )

    return retangulo


def voltar_botao():
    retangulo = pygame.Rect(25, 25, 85, 55)

    pygame.draw.rect(
        tela,
        ROXO,
        retangulo,
        border_radius=12
    )

    texto(
        "<",
        fonte_grande,
        ROSA,
        57,
        30
    )

    return retangulo


# ============================================================
# CRIA OS OBJETOS DOS INGREDIENTES
# ============================================================

def criar_ingredientes():
    global ingredientes
    ingredientes = []
    receita = receitas[receita_selecionada]

    # Grade para manter TODOS os ingredientes visiveis.
    colunas = [30, 285]
    y_inicial = 145
    espacamento_y = 70
    largura = 225
    altura = 58

    indice = 0
    for nome, quantidade in receita["ingredientes"]:
        for numero in range(quantidade):
            coluna = indice % 2
            linha = indice // 2
            x = colunas[coluna]
            y = y_inicial + linha * espacamento_y

            ingredientes.append({
                "nome": nome,
                "x": x,
                "y": y,
                "largura": largura,
                "altura": altura,
                "original_x": x,
                "original_y": y,
                "colocado": False,
                "arrastando": False,
                "numero": numero + 1,
                "indice": indice
            })
            indice += 1


# ============================================================
# COMEÇAR RECEITA
# ============================================================

def iniciar_receita():

    global pontuacao
    global etapa_atual
    global ingrediente_arrastando

    pontuacao = 0
    etapa_atual = 0
    ingrediente_arrastando = None

    criar_ingredientes()


# ============================================================
# MENU
# ============================================================

def desenhar_menu():

    tela.fill(FUNDO)

    texto_centralizado(
        "SANGUETERIA",
        titulo,
        ROSA,
        90
    )

    texto_centralizado(
        "LABORATORIO DE DOCES",
        fonte_grande,
        BRANCO,
        170
    )

    jogar = botao(
        "JOGAR",
        300,
        260,
        200,
        60
    )

    cientistas_btn = botao(
        "CIENTISTAS",
        270,
        340,
        260,
        60
    )

    sair = botao(
        "SAIR",
        300,
        420,
        200,
        60
    )

    return jogar, cientistas_btn, sair


# ============================================================
# RECEITAS
# ============================================================

def desenhar_receitas():

    tela.fill(FUNDO)

    voltar = voltar_botao()

    texto_centralizado(
        "LIVRO DE RECEITAS",
        titulo,
        ROSA,
        55
    )

    texto_centralizado(
        "Escolha uma receita",
        fonte,
        BRANCO,
        125
    )

    botoes = []

    posicoes = [
        (90, 190),
        (420, 190),
        (90, 330),
        (420, 330)
    ]

    for i, receita in enumerate(receitas):

        x, y = posicoes[i]

        caixa = pygame.Rect(
            x,
            y,
            290,
            105
        )

        pygame.draw.rect(
            tela,
            ROXO,
            caixa,
            border_radius=15
        )

        pygame.draw.rect(
            tela,
            ROSA,
            caixa,
            3,
            border_radius=15
        )

        texto(
            receita["nome"],
            fonte,
            BRANCO,
            x + 15,
            y + 18
        )

        texto(
            receita["cientista"],
            fonte_pequena,
            ROSA_CLARO,
            x + 15,
            y + 65
        )

        botoes.append(caixa)

    return voltar, botoes


# ============================================================
# APRESENTAÇÃO DA RECEITA
# ============================================================

def desenhar_preparo():

    tela.fill(FUNDO)

    voltar = voltar_botao()

    receita = receitas[receita_selecionada]

    texto_centralizado(
        receita["nome"],
        titulo,
        ROSA,
        50
    )

    texto_centralizado(
        "Cientista: " + receita["cientista"],
        fonte,
        BRANCO,
        120
    )

    texto(
        "INGREDIENTES",
        fonte_grande,
        ROSA,
        90,
        175
    )

    y = 225

    for nome, quantidade in receita["ingredientes"]:

        texto(
            f"• {quantidade}x {nome}",
            fonte_pequena,
            BRANCO,
            110,
            y
        )

        y += 35

    iniciar = botao(
        "COMEÇAR",
        300,
        490,
        200,
        55
    )

    return voltar, iniciar


# ============================================================
# DESENHA A BANCADA
# ============================================================

def desenhar_bancada():

    pygame.draw.rect(
        tela,
        ROXO_ESCURO,
        (0, 420, LARGURA, 180)
    )

    pygame.draw.rect(
        tela,
        ROXO,
        (0, 420, LARGURA, 8)
    )


# ============================================================
# DESENHA UM INGREDIENTE
# ============================================================

def desenhar_icone_ingrediente(nome, centro_x, centro_y):
    nome_l = nome.lower()

    if "baga" in nome_l or "frutas vermelhas" in nome_l:
        pygame.draw.circle(tela, VERMELHO, (centro_x - 7, centro_y + 2), 10)
        pygame.draw.circle(tela, ROSA, (centro_x + 8, centro_y + 2), 10)
        pygame.draw.circle(tela, VERMELHO, (centro_x, centro_y - 8), 10)
        pygame.draw.ellipse(tela, VERDE, (centro_x - 4, centro_y - 20, 9, 7))
    elif "planta" in nome_l:
        pygame.draw.line(tela, VERDE, (centro_x, centro_y + 16), (centro_x, centro_y - 12), 4)
        pygame.draw.ellipse(tela, VERDE, (centro_x - 18, centro_y - 7, 18, 10))
        pygame.draw.ellipse(tela, VERDE, (centro_x + 1, centro_y - 15, 18, 10))
    elif any(p in nome_l for p in ["soro", "essencia", "isotopo", "geleia"]):
        pygame.draw.rect(tela, BRANCO, (centro_x - 10, centro_y - 14, 20, 28), border_radius=4)
        pygame.draw.rect(tela, ROSA_CLARO, (centro_x - 7, centro_y - 7, 14, 17), border_radius=3)
        pygame.draw.rect(tela, ROSA, (centro_x - 7, centro_y - 18, 14, 5), border_radius=2)
    elif "engrenagem" in nome_l:
        import math
        pygame.draw.circle(tela, AMARELO, (centro_x, centro_y), 15)
        pygame.draw.circle(tela, ROXO_ESCURO, (centro_x, centro_y), 6)
        for ang in range(0, 360, 60):
            px = int(centro_x + math.cos(math.radians(ang)) * 19)
            py = int(centro_y + math.sin(math.radians(ang)) * 19)
            pygame.draw.circle(tela, AMARELO, (px, py), 4)
    elif "acucar" in nome_l or "granulado" in nome_l:
        pygame.draw.circle(tela, AMARELO, (centro_x, centro_y), 15)
        pygame.draw.circle(tela, BRANCO, (centro_x - 5, centro_y - 5), 3)
        pygame.draw.circle(tela, ROSA, (centro_x + 6, centro_y + 4), 3)
    elif "massa" in nome_l:
        pygame.draw.ellipse(tela, (245, 210, 180), (centro_x - 18, centro_y - 12, 36, 24))
        pygame.draw.ellipse(tela, (220, 175, 140), (centro_x - 10, centro_y - 7, 20, 12))
    else:
        pygame.draw.circle(tela, ROSA_CLARO, (centro_x, centro_y), 16)


def desenhar_ingrediente(ingrediente):
    if ingrediente["colocado"]:
        return

    x, y = ingrediente["x"], ingrediente["y"]
    largura, altura = ingrediente["largura"], ingrediente["altura"]
    caixa = pygame.Rect(x, y, largura, altura)

    if ingrediente["arrastando"]:
        pygame.draw.rect(tela, (20, 10, 30), caixa.move(4, 4), border_radius=14)

    pygame.draw.rect(tela, ROXO, caixa, border_radius=14)
    pygame.draw.rect(tela, ROSA, caixa, 2, border_radius=14)
    desenhar_icone_ingrediente(ingrediente["nome"], x + 30, y + altura // 2)

    nome = ingrediente["nome"]
    fonte_nome = fonte_pequena if fonte_pequena.size(nome)[0] <= largura - 65 else pygame.font.Font(None, 18)
    texto(nome, fonte_nome, BRANCO, x + 55, y + 8)
    if ingrediente["numero"] > 1:
        texto(f"unidade {ingrediente['numero']}", pygame.font.Font(None, 18), ROSA_CLARO, x + 55, y + 34)


# ============================================================
# TIGELA
# ============================================================

TIGELA_RECT = pygame.Rect(485, 250, 260, 145)

def desenhar_tigela():
    pygame.draw.ellipse(tela, (20, 10, 30), (492, 260, 260, 145))
    pygame.draw.ellipse(tela, AZUL, TIGELA_RECT)
    pygame.draw.ellipse(tela, ROXO_ESCURO, (505, 272, 220, 92))
    pygame.draw.ellipse(tela, (80, 145, 220), (505, 272, 220, 92), 4)
    texto_centralizado("TIGELA", fonte, BRANCO, 375)

    contador = 0
    for ingrediente in ingredientes:
        if ingrediente["colocado"]:
            x = 535 + (contador % 5) * 38
            y = 305 + (contador // 5) * 28
            desenhar_icone_ingrediente(ingrediente["nome"], x, y)
            contador += 1


# ============================================================
# TELA JOGAVEL
# ============================================================

def desenhar_jogo():
    tela.fill(FUNDO)
    receita = receitas[receita_selecionada]
    voltar = voltar_botao()

    texto(receita["nome"], fonte_grande, ROSA, 130, 25)
    texto("Cientista: " + receita["cientista"], fonte_pequena, BRANCO, 135, 75)
    texto("Pontos: " + str(pontuacao), fonte, AMARELO, 650, 25)

    pygame.draw.rect(tela, ROXO_ESCURO, (0, 435, LARGURA, 165))
    pygame.draw.rect(tela, ROXO, (0, 435, LARGURA, 7))

    if etapa_atual == 0:
        texto_centralizado("ARRASTE OS INGREDIENTES PARA A TIGELA!", fonte, ROSA_CLARO, 105)
        for ingrediente in ingredientes:
            desenhar_ingrediente(ingrediente)
        desenhar_tigela()

        total = len(ingredientes)
        colocados = sum(1 for ingrediente in ingredientes if ingrediente["colocado"])
        texto(f"INGREDIENTES: {colocados}/{total}", fonte, BRANCO, 545, 400)

        if colocados == total:
            texto_centralizado("TODOS OS INGREDIENTES!", fonte_grande, VERDE, 445)
            continuar = botao("CONTINUAR", 300, 505, 200, 55)
            return voltar, continuar
    else:
        etapa = receita["etapas"][etapa_atual - 1]
        texto_centralizado(f"ETAPA {etapa_atual}", fonte_grande, ROSA, 120)

        pygame.draw.rect(tela, ROXO, (100, 190, 600, 135), border_radius=18)
        pygame.draw.rect(tela, ROSA, (100, 190, 600, 135), 3, border_radius=18)

        palavras = etapa.split()
        linhas, linha = [], ""
        for palavra in palavras:
            teste = linha + palavra + " "
            if fonte_pequena.size(teste)[0] > 530:
                linhas.append(linha)
                linha = palavra + " "
            else:
                linha = teste
        if linha:
            linhas.append(linha)

        y = 220
        for linha in linhas:
            texto_centralizado(linha.strip(), fonte_pequena, BRANCO, y)
            y += 28

        continuar = botao("FAZER ETAPA", 300, 360, 200, 55)
        return voltar, continuar

    return voltar, None


# ============================================================
# RESULTADO
# ============================================================

def desenhar_resultado():

    tela.fill(FUNDO)

    receita = receitas[receita_selecionada]

    texto_centralizado(
        "RECEITA CONCLUIDA!",
        titulo,
        ROSA,
        100
    )

    texto_centralizado(
        "✨ PARABENS! ✨",
        fonte_grande,
        AMARELO,
        190
    )

    texto_centralizado(
        receita["nome"],
        fonte_grande,
        BRANCO,
        260
    )

    texto_centralizado(
        "Pontuacao: " + str(pontuacao),
        fonte,
        ROSA_CLARO,
        320
    )

    novamente = botao(
        "JOGAR NOVAMENTE",
        240,
        400,
        320,
        60
    )

    livro = botao(
        "VOLTAR AO LIVRO",
        240,
        480,
        320,
        60
    )

    return novamente, livro


# ============================================================
# CIENTISTAS
# ============================================================

def desenhar_cientistas():

    tela.fill(FUNDO)

    voltar = voltar_botao()

    texto_centralizado(
        "CIENTISTAS",
        titulo,
        ROSA,
        55
    )

    texto_centralizado(
        "As cientistas da Sangueteria",
        fonte,
        BRANCO,
        125
    )

    botoes = []

    posicoes = [
        (90, 190),
        (420, 190),
        (90, 350),
        (420, 350)
    ]

    for i, (nome, receita) in enumerate(cientistas):

        x, y = posicoes[i]

        caixa = pygame.Rect(
            x,
            y,
            290,
            125
        )

        pygame.draw.rect(
            tela,
            ROXO,
            caixa,
            border_radius=15
        )

        pygame.draw.rect(
            tela,
            ROSA,
            caixa,
            3,
            border_radius=15
        )

        texto(
            nome,
            fonte,
            BRANCO,
            x + 20,
            y + 25
        )

        texto(
            receita,
            fonte_pequena,
            ROSA_CLARO,
            x + 20,
            y + 75
        )

        botoes.append(caixa)

    return voltar, botoes


# ============================================================
# LOOP PRINCIPAL
# ============================================================

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # ====================================================
        # MOUSE PRESSIONADO
        # ====================================================

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if tela_atual == "menu":

                jogar, cientistas_btn, sair = desenhar_menu()

                if jogar.collidepoint(evento.pos):

                    tela_atual = "receitas"

                elif cientistas_btn.collidepoint(evento.pos):

                    tela_atual = "cientistas"

                elif sair.collidepoint(evento.pos):

                    rodando = False

            # =================================================
            # RECEITAS
            # =================================================

            elif tela_atual == "receitas":

                voltar, botoes = desenhar_receitas()

                if voltar.collidepoint(evento.pos):

                    tela_atual = "menu"

                else:

                    for i, caixa in enumerate(botoes):

                        if caixa.collidepoint(evento.pos):

                            receita_selecionada = i

                            tela_atual = "preparo"

            # =================================================
            # PREPARO
            # =================================================

            elif tela_atual == "preparo":

                voltar, iniciar = desenhar_preparo()

                if voltar.collidepoint(evento.pos):

                    tela_atual = "receitas"

                elif iniciar.collidepoint(evento.pos):

                    iniciar_receita()

                    tela_atual = "jogo"

            # =================================================
            # JOGO
            # =================================================

            elif tela_atual == "jogo":
                voltar, continuar = desenhar_jogo()

                if voltar.collidepoint(evento.pos):
                    tela_atual = "receitas"
                    ingrediente_arrastando = None

                # O botao CONTINUAR precisa ser testado antes do arrastar.
                elif continuar is not None and continuar.collidepoint(evento.pos):
                    etapa_atual += 1
                    pontuacao += 15
                    if etapa_atual > len(receitas[receita_selecionada]["etapas"]):
                        tela_atual = "resultado"

                elif etapa_atual == 0:
                    for ingrediente in ingredientes:
                        if ingrediente["colocado"]:
                            continue

                        caixa = pygame.Rect(
                            ingrediente["x"], ingrediente["y"],
                            ingrediente["largura"], ingrediente["altura"]
                        )

                        if caixa.collidepoint(evento.pos):
                            ingrediente_arrastando = ingrediente
                            ingrediente["arrastando"] = True
                            ingrediente["offset_x"] = evento.pos[0] - ingrediente["x"]
                            ingrediente["offset_y"] = evento.pos[1] - ingrediente["y"]
                            break

            # =================================================
            # RESULTADO
            # =================================================

            elif tela_atual == "resultado":

                novamente, livro = desenhar_resultado()

                if novamente.collidepoint(
                    evento.pos
                ):

                    iniciar_receita()

                    tela_atual = "jogo"

                elif livro.collidepoint(
                    evento.pos
                ):

                    tela_atual = "receitas"

            # =================================================
            # CIENTISTAS
            # =================================================

            elif tela_atual == "cientistas":

                voltar, botoes = desenhar_cientistas()

                if voltar.collidepoint(evento.pos):

                    tela_atual = "menu"

        # ====================================================
        # MOUSE MOVENDO
        # ====================================================

        if evento.type == pygame.MOUSEMOTION:

            if (
                tela_atual == "jogo"
                and ingrediente_arrastando is not None
                and ingrediente_arrastando["arrastando"]
            ):

                ingrediente_arrastando["x"] = (
                    evento.pos[0]
                    - ingrediente_arrastando["offset_x"]
                )

                ingrediente_arrastando["y"] = (
                    evento.pos[1]
                    - ingrediente_arrastando["offset_y"]
                )

        # ====================================================
        # MOUSE SOLTO
        # ====================================================

        if evento.type == pygame.MOUSEBUTTONUP:

            if (
                tela_atual == "jogo"
                and ingrediente_arrastando is not None
            ):

                ingrediente = ingrediente_arrastando

                ingrediente["arrastando"] = False

                # --------------------------------------------
                # ÁREA DA TIGELA
                # --------------------------------------------

                tigela = TIGELA_RECT

                caixa_ingrediente = pygame.Rect(
                    ingrediente["x"],
                    ingrediente["y"],
                    ingrediente["largura"],
                    ingrediente["altura"]
                )

                # --------------------------------------------
                # ACERTOU
                # --------------------------------------------

                if tigela.colliderect(
                    caixa_ingrediente
                ):

                    ingrediente["colocado"] = True

                    ingrediente["x"] = 0
                    ingrediente["y"] = 0

                    pontuacao += 10

                # --------------------------------------------
                # ERROU
                # --------------------------------------------

                else:

                    ingrediente["x"] = (
                        ingrediente["original_x"]
                    )

                    ingrediente["y"] = (
                        ingrediente["original_y"]
                    )

                ingrediente_arrastando = None

    # ========================================================
    # DESENHO
    # ========================================================

    if tela_atual == "menu":

        desenhar_menu()

    elif tela_atual == "receitas":

        desenhar_receitas()

    elif tela_atual == "preparo":

        desenhar_preparo()

    elif tela_atual == "jogo":

        desenhar_jogo()

    elif tela_atual == "resultado":

        desenhar_resultado()

    elif tela_atual == "cientistas":

        desenhar_cientistas()

    pygame.display.flip()

    relogio.tick(60)


pygame.quit()
sys.exit()
